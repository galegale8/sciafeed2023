
from os.path import join

from sciafeed import arpa19, arpa21, arpaer, arpafvg, rmn, trentino
from sciafeed import formats

from . import TEST_DATA_PATH


def test_guess_format(tmpdir):
    # arpa19
    test_filepath = join(TEST_DATA_PATH, 'arpa19', 'loc01_70001_201301010000_201401010100.dat')
    label, module = formats.guess_format(test_filepath)
    assert label, module == ('ARPA-19', arpa19)
    # arpa21
    test_filepath = join(TEST_DATA_PATH, 'arpa21', 'loc01_00201_201201010000_201301010100.dat')
    label, module = formats.guess_format(test_filepath)
    assert label, module == ('ARPA-21', arpa21)
    # arpaer
    test_filepath = join(TEST_DATA_PATH, 'arpaer', 'results.json')
    label, module = formats.guess_format(test_filepath)
    assert label, module == ('ARPA-ER', arpaer)
    # arpafvg
    test_filepath = join(TEST_DATA_PATH, 'arpafvg', 'loc01_00001_2018010101_2019010101.dat')
    label, module = formats.guess_format(test_filepath)
    assert label, module == ('ARPA-FVG', arpafvg)
    # rmn
    test_filepath = join(TEST_DATA_PATH, 'rmn', 'ancona_right.csv')
    label, module = formats.guess_format(test_filepath)
    assert label, module == ('RMN', rmn)
    # unknown
    test_filepath = str(tmpdir.join('loc01_00001_2018010101_2019010101.dat'))
    with open(test_filepath, 'w') as fp:
        fp.write("Hello, I'm an unknown format")
    label, module = formats.guess_format(test_filepath)
    assert label, module == ('Unknown', None)


def test_validate_format():
    tests_paths = {
        'ARPA-19': [
            ('arpa19', 'loc01_70001_201301010000_201401010100.dat'),
            ('arpa19', 'wrong_70002_201301010000_201401010100.dat')],
        'ARPA-21': [
            ('arpa21', 'loc01_00201_201201010000_201301010100.dat'),
            ('arpa21', 'wrong_00202_201201010000_201301010100.dat')],
        'ARPA-ER': [
            ('arpaer', 'results.json'),
            ('arpaer', 'wrong_results1.json')],
        'ARPA-FVG': [
            ('arpafvg', 'loc01_00001_2018010101_2019010101.dat'),
            ('arpafvg', 'wrong_00002_2018010101_2019010101.dat')],
        'BOLZANO': [
            ('bolzano', 'MonteMaria.xls'),
            ('bolzano', 'wrong3.xls')],
        'NOAA': [
            ('noaa', '160080-99999-2019.op'),
            ('noaa', 'wrong3_160080-99999-2019.op')],
        'RMN': [
            ('rmn', 'ancona_right.csv'),
            ('rmn', 'ancona_wrong5.csv')],
        'TRENTINO': [
            ('trentino', 'T0001.csv'),
            ('trentino', 'wrong3.csv')],
    }
    for format_label, format_module in formats.FORMATS:
        validator = getattr(format_module, 'validate_format')
        for format_folder, filename in tests_paths[format_label]:
            filepath = join(TEST_DATA_PATH, format_folder, filename)
            parameters_filepath = join(TEST_DATA_PATH, format_folder,
                                       "%s_params.csv" % format_folder)
            expected_result = validator(filepath, parameters_filepath)
            result = formats.validate_format(filepath, parameters_filepath,
                                             format_label=format_label)
            assert result == expected_result
    # guessing ok
    filepath = join(TEST_DATA_PATH, 'trentino', 'T0001.csv')
    parameters_filepath = join(TEST_DATA_PATH, 'trentino', "trentino_params.csv")
    expected_result = trentino.validate_format(filepath, parameters_filepath)
    result = formats.validate_format(filepath, parameters_filepath)
    assert result == expected_result
    # guessing impossible
    result = formats.validate_format(filepath=parameters_filepath,
                                     parameters_filepath=parameters_filepath)
    assert result == ([(0, "file %r has unknown format" % parameters_filepath)], None)
