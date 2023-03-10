"""
This module contains functions and utilities that involve more components of sciafeed.
"""

import logging
import operator
from os import listdir
from os.path import isfile, join, splitext

from sciafeed import LOG_NAME
from sciafeed import checks
from sciafeed import compute
from sciafeed import db_utils
from sciafeed import dma
from sciafeed import export
from sciafeed import parsing
from sciafeed import querying
from sciafeed import utils
from sciafeed import upsert


def make_report(in_filepath, outdata_filepath=None, parameters_filepath=None, logger=None,
                do_checks=True, limiting_params=None):
    """
    Read a file located at `in_filepath` and generate a report on the parsing.
    If the path `outdata_filepath` is defined, a file with the data parsed is created at the path.
    Return the data parsed.

    :param in_filepath: input file
    :param outdata_filepath: path of the output file containing data
    :param parameters_filepath: path to the CSV file containing info about stored parameters
    :param logger: logging object where to report actions
    :param limiting_params: dictionary of limiting parameters for each parameter code
    :param do_checks: True if must do checks, False otherwise
    :return: data parsed
    """
    if logger is None:
        logger = logging.getLogger(LOG_NAME)
    format_label, format_module = parsing.guess_format(in_filepath)
    data = None
    if not format_module:
        logger.warning("file %r has unknown format" % in_filepath)
        return data
    if not parameters_filepath:
        parameters_filepath = getattr(format_module, 'PARAMETERS_FILEPATH')
    if limiting_params is None:
        limiting_params = getattr(format_module, 'LIMITING_PARAMETERS')

    logger.info("START OF ANALYSIS OF %s FILE %r" % (format_label, in_filepath))
    parse_f = getattr(format_module, 'parse')
    load_parameter_thresholds_f = getattr(format_module, 'load_parameter_thresholds')
    par_thresholds = load_parameter_thresholds_f(parameters_filepath)
    # 1. parsing
    data, err_msgs = parse_f(in_filepath, parameters_filepath)
    if do_checks:
        # 2. weak climatologic check
        wcc_err_msgs, data = checks.data_weak_climatologic_check(data, par_thresholds)
        # 3. internal consistence check
        icc_err_msgs, data = checks.data_internal_consistence_check(data, limiting_params)
        err_msgs += wcc_err_msgs + icc_err_msgs

    if not err_msgs:
        logger.info("No errors found")
    else:
        for row_index, err_msg in err_msgs:
            logger.info("Row %s: %s" % (row_index, err_msg))

    if outdata_filepath:
        export.export2csv(data, outdata_filepath)
        logger.info("Data saved on file %r" % outdata_filepath)

    logger.info("END OF ANALYSIS OF %s FILE" % format_label)
    return data


def compute_daily_indicators(conn, data_folder, indicators_folder=None, logger=None):
    """
    Read each file located inside `data_folder` and generate indicators
    and a report of the processing.
    If the path `indicators_folder` is defined, a file with the indicators
    is created at the path.
    Return the the report strings (list) and the computed indicators (dictionary).

    :param conn: db connection object
    :param data_folder: folder path containing input data
    :param indicators_folder: path of the output data
    :param logger: logging object where to report actions
    :return: computed_indicators
    """
    if logger is None:
        logger = logging.getLogger(LOG_NAME)
    computed_indicators = dict()
    writers = utils.open_csv_writers(indicators_folder, compute.INDICATORS_TABLES)
    block_data = []
    for i, file_name in enumerate(listdir(data_folder), 1):
        csv_path = join(data_folder, file_name)
        if not isfile(csv_path) or splitext(file_name.lower())[1] != '.csv':
            continue
        logger.info("reading data from %r" % csv_path)
        try:
            data = export.csv2data(csv_path)
        except:
            logger.error('CSV file %r not parsable' % csv_path)
            continue
        block_data.extend(data)
    logger.info("computing daily indicators...")
    if block_data:
        computed_indicators = compute.compute_and_store(
            conn, block_data, writers, compute.INDICATORS_TABLES, logger)
    utils.close_csv_writers(writers)
    return computed_indicators


def process_checks_preci(conn, stations_ids, schema, logger, temp_records=None):
    logger.info('== initial process chain for PRECI ==')

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    sql_reset = "UPDATE %s.ds__preci SET prec24.flag.wht = 1 WHERE %s AND (" \
                "((prec24).flag).wht <= -10 OR ((prec24).flag).wht IS NULL )" \
                % (schema, stations_where)
    conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, (prec24).val_tot, ((prec24).flag).wht"
    prec_records = querying.select_prec_records(
        conn, sql_fields=sql_fields, stations_ids=stations_ids, schema=schema,
        exclude_flag_interval=(-9, 0), exclude_null=True)

    if temp_records is None:
        logger.info('* get records of temperature...')
        sql_fields = "cod_staz, data_i, " \
                     "(tmxgg).val_md, ((tmxgg).flag).wht, " \
                     "(tmngg).val_md, ((tmngg).flag).wht, " \
                     "(tmdgg).val_md, ((tmdgg).flag).wht"
        temp_records = querying.select_temp_records(
            conn, fields=['tmxgg', 'tmngg', 'tmdgg'], sql_fields=sql_fields,
            stations_ids=stations_ids, schema=schema, exclude_null=False)
        temp_records = list(temp_records)

    logger.info("* 'controllo valori ripetuti = 0'")
    prec_records = checks.check1(prec_records, logger=logger)
    logger.info("* 'controllo valori ripetuti'")
    prec_records = checks.check2(prec_records, exclude_values=(0, None), logger=logger)
    logger.info("* 'controllo mesi duplicati (stesso anno)'")
    prec_records = checks.check3(prec_records, min_not_zero=5, logger=logger)
    logger.info("* 'controllo mesi duplicati (anni differenti)'")
    prec_records = checks.check4(prec_records, min_not_zero=5, logger=logger)
    logger.info("* 'controllo world excedence'")
    prec_records = checks.check7(prec_records, min_threshold=-0.001, max_threshold=800,
                                 logger=logger)
    logger.info('* controllo gap checks')
    prec_records = checks.check8(prec_records, threshold=300, exclude_zero=True, logger=logger)
    logger.info("* 'controllo z-score checks'")
    prec_records = checks.check10(prec_records, temp_records, logger=logger)
    logger.info("* 'controllo z-score checks ghiaccio'")
    prec_records = checks.check10(prec_records, temp_records, ice=True, times_perc=5, flag=-26,
                                  logger=logger)

    logger.info('* final set of flags on database...')
    flag_records = [r for r in prec_records if r[3] and r[3] <= -10]
    upsert.update_prec_flags(conn, flag_records, schema=schema)
    logger.info('== end process chain for PRECI ==')
    return prec_records


def process_checks_t200(conn, stations_ids, schema, logger):
    logger.info('== initial process chain for T200 ==')

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    for field in ['tmxgg', 'tmngg', 'tmdgg']:
        sql_reset = "UPDATE %s.ds__t200 SET %s.flag.wht = 1 WHERE %s AND (" \
                    "((%s).flag).wht <= -10 OR ((%s).flag).wht IS NULL )" \
                    % (schema, field, stations_where, field, field)
        conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, " \
                 "(tmxgg).val_md, ((tmxgg).flag).wht, " \
                 "(tmngg).val_md, ((tmngg).flag).wht, " \
                 "(tmdgg).val_md, ((tmdgg).flag).wht"
    temp_records = querying.select_temp_records(
        conn, fields=['tmxgg', 'tmngg', 'tmdgg'], sql_fields=sql_fields, stations_ids=stations_ids,
        schema=schema, exclude_null=False)
    temp_records = list(temp_records)

    logger.info("* 'controllo valori ripetuti' (Tmax)")
    temp_records = checks.check2(temp_records, exclude_values=(None,), logger=logger)
    logger.info("* 'controllo valori ripetuti'  (Tmin)")
    temp_records = checks.check2(temp_records, exclude_values=(None,), val_index=4, logger=logger)
    logger.info("* 'controllo mesi duplicati (stesso anno)' (Tmax)")
    temp_records = checks.check3(temp_records, min_same=2, logger=logger)
    logger.info("* 'controllo mesi duplicati (stesso anno)' (Tmin)")
    temp_records = checks.check3(temp_records, min_same=2, val_index=4, logger=logger)
    logger.info("* 'controllo mesi duplicati (anni differenti)' for variable Tmax")
    temp_records = checks.check4(temp_records, min_same=2, logger=logger)
    logger.info("* 'controllo mesi duplicati (anni differenti)' (Tmin)")
    temp_records = checks.check4(temp_records, min_same=2, val_index=4, logger=logger)
    logger.info("* controllo TMAX=TMIN")
    temp_records = checks.check5(temp_records, logger=logger)
    logger.info("* controllo TMAX=TMIN=0")
    temp_records = checks.check6(temp_records, logger=logger)
    logger.info("* 'controllo world excedence' for Tmax")
    temp_records = checks.check7(temp_records, min_threshold=-30, max_threshold=50, logger=logger)
    logger.info("* 'controllo world excedence' for Tmin")
    temp_records = checks.check7(temp_records, min_threshold=-40, max_threshold=40,
                                 val_index=4, logger=logger)
    logger.info("* 'controllo gap checks temperatura' for Tmax")
    temp_records = checks.check8(temp_records, threshold=10, split=True, logger=logger)
    logger.info("* 'controllo gap checks temperatura' Tmin")
    temp_records = checks.check8(temp_records, threshold=10, split=True, val_index=4,
                                 logger=logger)
    logger.info("* 'controllo z-score checks temperatura' for Tmax")
    temp_records = checks.check9(temp_records, logger=logger)
    logger.info("* 'controllo z-score checks temperatura' (Tmin)")
    temp_records = checks.check9(temp_records, val_index=4, logger=logger)
    logger.info("* 'controllo jump checks' for Tmax")
    temp_records = checks.check11(temp_records, logger=logger)
    logger.info("* 'controllo jump checks' (Tmin)")
    temp_records = checks.check11(temp_records, val_index=4, logger=logger)
    logger.info("* 'controllo Tmax < Tmin'")
    temp_records = checks.check12(temp_records, logger=logger)
    logger.info("* 'controllo dtr (diurnal temperature range)' (Tmax)")
    operators = max, operator.ge
    temp_records = checks.check13(temp_records, operators, logger=logger)
    logger.info("* 'controllo dtr (diurnal temperature range)' (Tmin)")
    operators = min, operator.le
    temp_records = checks.check13(temp_records, operators, logger=logger, jump=-35,
                                  val_indexes=(4,2))
    logger.info("* 'controllo world excedence' (tmdgg)")
    temp_records = checks.check7(
        temp_records, min_threshold=-36, max_threshold=46, val_index=6, logger=logger)

    logger.info('* final set of flags on database...')
    flag_records = [r for r in temp_records if r[3] and r[3] <= -10]
    upsert.update_flags(conn, flag_records, 'ds__t200', schema=schema, db_field='tmxgg')
    flag_records = [r for r in temp_records if r[5] and r[5] <= -10]
    upsert.update_flags(conn, flag_records, 'ds__t200', schema=schema, db_field='tmngg',
                        flag_index=5)
    flag_records = [r for r in temp_records if r[7] and r[7] <= -10]
    upsert.update_flags(conn, flag_records, 'ds__t200', schema=schema, db_field='tmdgg',
                        flag_index=7)
    logger.info('== end process chain for T200 ==')
    return temp_records


def process_checks_bagna(conn, stations_ids, schema, logger):
    logger.info('== initial process chain for BAGNA ==')
    table, main_field, sub_field, min_threshold, max_threshold = \
        ('ds__bagna', 'bagna', 'val_md', -1, 25)

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    sql_reset = "UPDATE %s.%s SET %s.flag.wht = 1 WHERE %s AND (" \
                "((%s).flag).wht <= -10 OR ((%s).flag).wht IS NULL )" \
                % (schema, table, main_field, stations_where, main_field, main_field)
    conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, (%s).%s, ((%s).flag).wht" % (main_field, sub_field, main_field)
    where_sql = '(%s).%s IS NOT NULL' % (main_field, sub_field)
    table_records = querying.select_records(
        conn, table, fields=[main_field], sql_fields=sql_fields, stations_ids=stations_ids,
        schema=schema, exclude_flag_interval=(-9, 0), where_sql=where_sql)

    logger.info("* 'controllo world excedence' (%s.%s)" % (main_field, sub_field))
    table_records = checks.check7(
        table_records, min_threshold, max_threshold, logger=logger)

    logger.info('* final set of flags on database...')
    flag_records = [r for r in table_records if r[3] and r[3] <= -10]
    upsert.update_flags(conn, flag_records, table, schema=schema, db_field=main_field)

    logger.info('== end process chain for BAGNA ==')
    return table_records


def process_checks_elio(conn, stations_ids, schema, logger):
    logger.info('== initial process chain for ELIOFANIA ==')
    table, main_field, sub_field, min_threshold, max_threshold = \
        ('ds__elio', 'elio', 'val_md', -1, 19)

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    sql_reset = "UPDATE %s.%s SET %s.flag.wht = 1 WHERE %s AND (" \
                "((%s).flag).wht <= -10 OR ((%s).flag).wht IS NULL )" \
                % (schema, table, main_field, stations_where, main_field, main_field)
    conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, (%s).%s, case when ((%s).flag).wht=5 then 5 else 1 end" \
                 % (main_field, sub_field, main_field)
    where_sql = '(%s).%s IS NOT NULL' % (main_field, sub_field)
    table_records = querying.select_records(
        conn, table, fields=[main_field], sql_fields=sql_fields, stations_ids=stations_ids,
        schema=schema, exclude_flag_interval=(-9, 0), where_sql=where_sql)

    logger.info("* 'controllo world excedence' (%s.%s)" % (main_field, sub_field))
    table_records = checks.check7(
        table_records, min_threshold, max_threshold, logger=logger)

    logger.info('* final set of flags on database...')
    flag_records = [r for r in table_records if r[3] and r[3] <= -10]
    upsert.update_flags(conn, flag_records, table, schema=schema, db_field=main_field)

    logger.info('== end process chain for ELIOFANIA ==')
    return table_records


def process_checks_radglob(conn, stations_ids, schema, logger):
    logger.info('== initial process chain for RADIAZIONE GLOBALE ==')
    table, main_field, sub_field, min_threshold, max_threshold = \
        ('ds__radglob', 'radglob', 'val_md', -1, 601)

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    sql_reset = "UPDATE %s.%s SET %s.flag.wht = 1 WHERE %s AND (" \
                "((%s).flag).wht <= -10 OR ((%s).flag).wht IS NULL )" \
                % (schema, table, main_field, stations_where, main_field, main_field)
    conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, (%s).%s, case when ((%s).flag).wht=5 then 5 else 1 end" \
                 % (main_field, sub_field, main_field)
    where_sql = '(%s).%s IS NOT NULL' % (main_field, sub_field)
    table_records = querying.select_records(
        conn, table, fields=[main_field], sql_fields=sql_fields, stations_ids=stations_ids,
        schema=schema, exclude_flag_interval=(-9, 0), where_sql=where_sql)

    logger.info("* 'controllo world excedence' (%s.%s)" % (main_field, sub_field))
    table_records = checks.check7(
        table_records, min_threshold, max_threshold, logger=logger)

    logger.info('* final set of flags on database...')
    flag_records = [r for r in table_records if r[3] and r[3] <= -10]
    upsert.update_flags(conn, flag_records, table, schema=schema, db_field=main_field)

    logger.info('== end process chain for RADIAZIONE GLOBALE ==')
    return table_records


def process_checks_press(conn, stations_ids, schema, logger):
    logger.info('== initial process chain for PRESS ==')

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    sql_reset = "UPDATE %s.ds__press SET press.flag.wht = 1 WHERE %s AND (" \
                "((press).flag).wht <= -10 OR ((press).flag).wht IS NULL )" \
                % (schema, stations_where)
    conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, " \
                 "(press).val_md, ((press).flag).wht, " \
                 "(press).val_mx, ((press).flag).wht, " \
                 "(press).val_mn, ((press).flag).wht"
    table_records = querying.select_records(
        conn, 'ds__press', fields=['press'], sql_fields=sql_fields, stations_ids=stations_ids,
        schema=schema)
    table_records = list(table_records)

    for main_field, sub_field, min_threshold, max_threshold, val_index in [
            ('press', 'val_md', 959, 1061, 2),
            ('press', 'val_mx', 959, 1061, 4),
            ('press', 'val_mn', 959, 1061, 6),
    ]:
        logger.info("* 'controllo world excedence' (%s.%s)" % (main_field, sub_field))
        table_records = checks.check7(
            table_records, min_threshold, max_threshold, val_index=val_index, logger=logger,
            flag_index=3)
    logger.info("* 'controllo valori ripetuti' Pmedia")
    table_records = checks.check2(
        table_records, len_threshold=10, exclude_values=(None, ), val_index=2, logger=logger)
    logger.info("* 'controllo consistenza'")
    table_records = checks.check_consistency(table_records, (6, 2, 4), 3, flag=-10, logger=logger)

    logger.info('* final set of flags on database...')
    flag_records = [r for r in table_records if r[3] and r[3] <= -10]
    upsert.update_flags(conn, flag_records, 'ds__press', schema=schema, db_field='press')

    logger.info('== end process chain for PRESS ==')
    return table_records


def process_checks_urel(conn, stations_ids, schema, logger):
    logger.info('== initial process chain for UREL ==')

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    sql_reset = "UPDATE %s.ds__urel SET ur.flag.wht = 1 WHERE %s AND (" \
                "((ur).flag).wht <= -10 OR ((ur).flag).wht IS NULL )" % (schema, stations_where)
    conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, " \
                 "(ur).val_md, ((ur).flag).wht, " \
                 "(ur).val_mx, ((ur).flag).wht, " \
                 "(ur).val_mn, ((ur).flag).wht"
    table_records = querying.select_records(
        conn, 'ds__urel', fields=['ur'], sql_fields=sql_fields, stations_ids=stations_ids,
        schema=schema)
    table_records = list(table_records)

    for main_field, sub_field, min_threshold, max_threshold, val_index in [
        ('ur', 'val_md', -1, 101, 2),
        ('ur', 'val_mx', -1, 101, 4),
        ('ur', 'val_mn', -1, 101, 6),
    ]:
        logger.info("* 'controllo world excedence' (%s.%s)" % (main_field, sub_field))
        table_records = checks.check7(
            table_records, min_threshold, max_threshold, logger=logger, flag_index=3)
    logger.info("* 'controllo consistenza UR'")
    table_records = checks.check_consistency(table_records, (6, 2, 4), 3, flag=-10, logger=logger)

    logger.info('* final set of flags on database...')
    flag_records = [r for r in table_records if r[3] and r[3] <= -10]
    upsert.update_flags(conn, flag_records, 'ds__urel', schema=schema, db_field='ur')

    logger.info('== end process chain for UREL ==')
    return table_records


def process_checks_wind(conn, stations_ids, schema, logger):
    logger.info('== initial process chain for vnt10 ==')

    # initial reset of flags to 1 of records invalidated by previous check chains (flags <= -10)
    logger.info('* initial reset to 1 of flags <= -10 or null')
    if stations_ids is None:
        stations_where = '1=1'
    elif len(stations_ids) == 0:
        stations_where = 'cod_staz IN (NULL)'
    else:
        stations_where = 'cod_staz IN (%s)' % repr(list(stations_ids))[1:-1]
    for field in ['vntmd', 'vntmxgg']:
        sql_reset = "UPDATE %s.ds__vnt10 SET %s.flag.wht = 1 WHERE %s AND (" \
                    "((%s).flag).wht <= -10 OR ((%s).flag).wht IS NULL )" \
                    % (schema, field, stations_where, field, field)
        conn.execute(sql_reset)

    logger.info('* query to get records...')
    sql_fields = "cod_staz, data_i, " \
                 "(vntmd).ff, ((vntmd).flag).wht, " \
                 "(vntmxgg).dd, ((vntmxgg).flag).wht, " \
                 "(vntmxgg).ff, ((vntmxgg).flag).wht"
    table_records = querying.select_records(
        conn, 'ds__vnt10', fields=[], sql_fields=sql_fields, stations_ids=stations_ids,
        schema=schema)
    table_records = list(table_records)

    for main_field, sub_field, min_threshold, max_threshold, val_index in [
        ('vntmd', 'ff', -1, 103, 2),
        ('vntmxgg', 'dd', -1, 361, 4),
        ('vntmxgg', 'ff', -1, 103, 6),
    ]:
        logger.info("* 'controllo world excedence' (%s.%s)" % (main_field, sub_field))
        table_records = checks.check7(
            table_records, min_threshold, max_threshold, logger=logger, val_index=val_index)

    # some additional checks for series wind: valori ripetuti + consistence
    logger.info("* check 'valori ripetuti' for vntmd.ff...")
    filter_funct = lambda r: r[2] is not None and r[2] > 2
    table_records = checks.check2(
        table_records, len_threshold=10, exclude_values=(None, ), filter_funct=filter_funct,
        logger=logger)
    # logger.info('* final set of flags on database for FFmedia valori ripetuti')
    # upsert.update_vntmd_flags(conn, vntmd_series, schema=schema)

    logger.info("* check 'valori ripetuti' for vntmxgg.ff...")
    filter_funct = lambda r: r[2] is not None and r[2] > 2
    table_records = checks.check2(
        table_records, len_threshold=10, exclude_values=(None, ), filter_funct=filter_funct,
        logger=logger, val_index=6)

    logger.info("* check 'valori ripetuti' for vntmxgg.dd...")
    filter_funct = lambda r: r[2] is not None and r[2] > 0.5
    table_records = checks.check2(
        table_records, len_threshold=10, exclude_values=(None, ), filter_funct=filter_funct,
        logger=logger, val_index=4)

    logger.info("* 'controllo consistenza WIND'")
    table_records = checks.check12(table_records, min_diff=0, logger=logger, val_indexes=(6, 2))
    logger.info('* final set of flags on database...')

    # vntmd.flag setta anche quello di vnt.flag, per questo uso update_vntmd_flags
    flag_records = [r for r in table_records if r[3] and r[3] <= -10]
    upsert.update_vntmd_flags(conn, flag_records, schema=schema, logger=logger)
    flag_records = [r for r in table_records if r[5] and r[5] <= -10]
    upsert.update_flags(
        conn, flag_records, 'ds__vnt10', schema=schema, db_field='vntmxgg', flag_index=5)
    return table_records


def process_checks_chain(dburi, stations_ids=None, schema='dailypdbanpacarica', logger=None,
                         omit_flagsync=False):
    """
    Start a chain of checks on records of the database from a set of monitoring stations selected.

    :param dburi: db connection URI
    :param stations_ids: primary keys of the stations (if None: no filtering by stations)
    :param schema: database schema to use
    :param omit_flagsync: if False (default), omits the synchronization for flags -9, +5
    :param logger: logging object where to report actions
    """
    if logger is None:
        logger = logging.getLogger(LOG_NAME)
    logger.info('== Start process ==')
    conn = db_utils.ensure_connection(dburi)

    if not omit_flagsync:
        logger.info(
            '* synchronization of flags +5 and -9 loading from schema dailypdbanpaclima...')
        upsert.sync_flags(conn, flags=(-9, 5), sourceschema='dailypdbanpaclima',
                          targetschema=schema, logger=logger)
        logger.info('* end of synchronization of flags +5 and -9')

    temp_records = process_checks_t200(conn, stations_ids, schema, logger)
    process_checks_preci(conn, stations_ids, schema, logger, temp_records)
    process_checks_bagna(conn, stations_ids, schema, logger)
    process_checks_elio(conn, stations_ids, schema, logger)
    process_checks_radglob(conn, stations_ids, schema, logger)
    process_checks_press(conn, stations_ids, schema, logger)
    process_checks_urel(conn, stations_ids, schema, logger)
    process_checks_wind(conn, stations_ids, schema, logger)

    logger.info('== End process ==')


def compute_daily_indicators2(conn, schema, stations_ids, logger):
    """
    Compute secondary indicators.

    :param conn: db connection object
    :param schema: db schema to consider
    :param stations_ids: list of station ids to consider
    :param logger: logger object for reporting
    :return:
    """
    conn_r = db_utils.get_safe_memory_read_connection(conn)
    if logger is None:
        logger = logging.getLogger(LOG_NAME)
    station_ids_tuple = '(%s)' % repr(stations_ids)[1:-1]
    logger.info('* querying ds__t200 for compute temperature indicators...')
    sql = """
    SELECT cod_staz, data_i, lat,
    (tmxgg).val_md, ((tmxgg).flag).wht,
    (tmngg).val_md, ((tmngg).flag).wht,
    (tmdgg).val_md, ((tmdgg).flag).wht
    FROM %s.ds__t200 LEFT JOIN dailypdbadmclima.anag__stazioni ON cod_staz=id_staz
    WHERE cod_staz in %s""" % (schema, station_ids_tuple)
    temp_records = db_utils.results_list(conn_r.execute(sql))

    logger.info('* computing temperature indicators...')
    temp_items = []
    grgg_items = []
    etp_items = []

    for record in temp_records:
        cod_staz, data_i, lat = record[0:3]
        base_item = {'data_i': data_i, 'cod_staz': cod_staz,  'cod_aggr': 4}
        tmax, tmax_flag = record[3:5]
        tmin, tmin_flag = record[5:7]
        tmedia, tmedia_flag = record[7:9]
        allow_compute = tmax is not None and tmax_flag is not None and tmax_flag > 0 and \
            tmin is not None and tmin_flag is not None and tmin_flag > 0
        if allow_compute:
            # escursione termica e t.media
            deltagg = tmax - tmin
            tmdgg1 = (tmax + tmin) / 2
            temp_item = base_item.copy()
            temp_item.update({'tmdgg1.val_md': tmdgg1, 'tmdgg1.flag.wht': 1,
                              'deltagg.val_md': deltagg, 'deltagg.flag.wht': 1})
            temp_items.append(temp_item)
            # gradi giorno
            grgg_flag, grgg1, grgg2, grgg3, grgg4, grgg5 = compute.compute_grgg(tmdgg1)
            grgg_item = base_item.copy()
            grgg_item.update({
                'grgg.flag.wht': grgg_flag[1], 'grgg.tot00': grgg1, 'grgg.tot05': grgg2,
                'grgg.tot10': grgg3, 'grgg.tot15': grgg4, 'grgg.tot21': grgg5})
            grgg_items.append(grgg_item)
            # evapotraspirazione potenziale
            if lat is not None and deltagg >= 0:
                jd = int(data_i.strftime('%j'))
                etp = compute.compute_etp(tmax, tmin, lat, jd)
                etp_item = base_item.copy()
                etp_item.update({'etp.val_md': etp[1], 'etp.flag.wht': etp[0][1]})
                etp_items.append(etp_item)

    temp_fields = []
    if temp_items:
        temp_fields = list(temp_items[0].keys())
    etp_fields = []
    if etp_items:
        etp_fields = list(etp_items[0].keys())
    grgg_fields = []
    if grgg_items:
        grgg_fields = list(grgg_items[0].keys())
    for table_name, fields, data in [
        ('ds__t200', temp_fields, temp_items),
        ('ds__etp', etp_fields, etp_items),
        ('ds__grgg', grgg_fields, grgg_items),
    ]:
        logger.info('updating temperature indicators on table %s.%s' % (schema, table_name))
        for sub_data in utils.chunked_iterable(data, 10000):
            sql = upsert.create_upsert(table_name, schema, fields, sub_data, 'upsert')
            if sql:
                conn.execute(sql)

    logger.info('* computing bilancio idrico...')
    sql = """
    SELECT cod_staz, data_i, (prec24).val_tot, (etp).val_md 
    FROM %s.ds__etp a JOIN %s.ds__preci b USING (cod_staz,data_i) 
    WHERE ((prec24).flag).wht > 0 AND ((etp).flag).wht > 0 
    AND (prec24).val_tot IS NOT NULL AND (etp).val_md IS NOT NULL
    AND cod_staz in %s
    """ % (schema, schema, station_ids_tuple)
    idro_records = db_utils.results_list(conn_r.execute(sql))

    idro_items = []
    for idro_record in idro_records:
        cod_staz, data_i, lat = idro_record[0:3]
        base_item = {'data_i': data_i, 'cod_staz': cod_staz, 'cod_aggr': 4}
        prec24, etp = idro_record[2:4]
        deltaidro = compute.compute_deltaidro(prec24, etp)
        idro_item = base_item.copy()
        idro_item.update({'deltaidro.flag.wht': deltaidro[0][1], 'deltaidro.val_md': deltaidro[1]})
        idro_items.append(idro_item)

    logger.info('updating bilancio idrico on table %s.%s' % (schema, 'ds__delta_idro'))
    idro_fields = []
    if idro_items:
        idro_fields = list(idro_items[0].keys())
    for sub_data in utils.chunked_iterable(idro_items, 10000):
        sql = upsert.create_upsert('ds__delta_idro', schema, idro_fields, sub_data, 'upsert')
        if sql:
            conn.execute(sql)


def process_dma(conn, startschema, targetschema, policy, stations_ids, logger):
    """
    Compute DMA aggregations reading records from db schema `startschema` and writing results
    on db schema `targetschema`.

    :param conn: db connection object
    :param startschema: db schema to consider for input records
    :param targetschema: db schema to consider for output records
    :param policy: 'onlyinsert' or 'upsert'
    :param stations_ids: list of station ids to consider
    :param logger: logger object for reporting
    """
    if logger is None:
        logger = logging.getLogger(LOG_NAME)

    dma.process_dma_bagnatura(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_bilancio_idrico(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_eliofania(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_radiazione_globale(
        conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_evapotraspirazione(
        conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_gradi_giorno(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_pressione(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_umidita_relativa(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_bioclimatologia(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_precipitazione(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_vento(conn, startschema, targetschema, policy, stations_ids, logger)
    dma.process_dma_temperatura(conn, startschema, targetschema, policy, stations_ids, logger)
