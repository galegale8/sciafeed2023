from datetime import datetime
from os.path import join

from sciafeed import noaa
from . import TEST_DATA_PATH


def test_load_parameter_file():
    test_filepath = join(TEST_DATA_PATH, 'noaa', 'noaa_params.csv')
    parameter_map = noaa.load_parameter_file(test_filepath)
    for key, value in parameter_map.items():
        assert 'NOAA_CODE' in value
        assert 'par_code' in value
        assert 'description' in value
        assert 'min' in value
        assert 'max' in value


def test_load_parameter_thresholds():
    test_filepath = join(TEST_DATA_PATH, 'noaa', 'noaa_params.csv')
    expected_thresholds = {
        'FF': [0.0, 102.0],
        'P': [960.0, 1060.0],
        'PREC': [0.0, 989.0],
        'Tmax': [-30.0, 50.0],
        'Tmedia': [-35.0, 45.0],
        'Tmin': [-40.0, 40.0]
    }
    parameter_thresholds = noaa.load_parameter_thresholds(test_filepath)
    assert parameter_thresholds == expected_thresholds


def test_extract_metadata():
    filepath = join(TEST_DATA_PATH, 'noaa', '160080-99999-2019.op')
    parameters_filepath = join(TEST_DATA_PATH, 'noaa', 'noaa_params.csv')
    metadata = noaa.extract_metadata(filepath, parameters_filepath)
    assert metadata == {'source': 'noaa/160080-99999-2019.op'}


def test_parse_row():
    row = "160080 99999  20190101    33.9 24    23.7 24  9999.9  0   859.6 24   11.0 24    " \
          "7.9 24   11.1  999.9    41.0    28.4   0.00F   1.6  000000"
    parameters_filepath = join(TEST_DATA_PATH, 'noaa', 'noaa_params.csv')
    parameters_map = noaa.load_parameter_file(parameters_filepath=parameters_filepath)

    # full parsing
    metadata = {'cod_utente': '160080', 'wban': '99999'}
    expected = [
        [metadata, datetime(2019, 1, 1, 0, 0), 'Tmedia', 1.0556, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'DEWP', -4.6111, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'STP', 859.6, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'VISIB', 17702.74, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'FF', 4.0638, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'MXSPD', 5.7098, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'Tmax', 5.0, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'Tmin', -2.0, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'PREC', 0.0, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'SNDP', 40.64, True]
    ]
    effective = noaa.parse_row(row, parameters_map)
    assert effective == expected


def test_validate_row_format():
    # right row
    row = "160080 99999  20190101    33.9 24    23.7 24  9999.9  0   859.6 24   11.0 24    " \
          "7.9 24   11.1  999.9    41.0    28.4   0.00F   1.6  000000"
    assert not noaa.validate_row_format(row)

    # empty row no raises errors
    row = '\n'
    assert not noaa.validate_row_format(row)

    # too less values
    row = "160080 99999  20190101    33.9 24    23.7 24  9999.9  0   859.6 24   11.0 24    " \
          "7.9 24   11.1  999.9    41.0    28.4   0.00F   1.6"
    assert noaa.validate_row_format(row) == "the length of the row is not standard"

    # wrong date
    row = "160080 99999  20190231    33.9 24    23.7 24  9999.9  0   859.6 24   11.0 24    " \
          "7.9 24   11.1  999.9    41.0    28.4   0.00F   1.6  000000"
    assert noaa.validate_row_format(row) == "the reference time for the row is not parsable"

    # wrong values
    row = "160080 99999  20190101    3A.9 24    23.7 24  9999.9  0   859.6 24   11.0 24    " \
          "7.9 24   11.1  999.9    41.0    28.4   0.00F   1.6  000000"
    assert noaa.validate_row_format(row) == 'The row contains not numeric values'


def test_validate_format():
    # right file
    filepath = join(TEST_DATA_PATH, 'noaa', '160080-99999-2019.op')
    parameters_filepath = join(TEST_DATA_PATH, 'noaa', 'noaa_params.csv')
    assert not noaa.validate_format(filepath, parameters_filepath=parameters_filepath)

    # wrong file name
    filepath = join(TEST_DATA_PATH, 'noaa', '160080-99999-2019.csv')
    err_msgs = noaa.validate_format(filepath, parameters_filepath=parameters_filepath)
    assert err_msgs and err_msgs == [(0, 'file extension must be .op')]

    # missing right header
    filepath = join(TEST_DATA_PATH, 'noaa', 'wrong1_160080-99999-2019.op')
    err_msgs = noaa.validate_format(filepath, parameters_filepath=parameters_filepath)
    assert err_msgs and err_msgs == [(0, "file doesn't include a correct header")]

    # compilation of errors on rows
    filepath = join(TEST_DATA_PATH, 'noaa', 'wrong2_160080-99999-2019.op')
    err_msgs = noaa.validate_format(filepath, parameters_filepath=parameters_filepath)
    assert err_msgs == [
        (2, 'the length of the row is not standard'),
        (3, 'the reference time for the row is not parsable'),
        (4, 'the precipitation flag is not parsable'),
        (5, 'The number of components in the row is wrong'),
        (6, 'The row contains not numeric values'),
        (10, 'duplication of rows with different data'),
        (12, 'it is not strictly after the previous')
    ]


def test_parse():
    filepath = join(TEST_DATA_PATH, 'noaa', '160080-99999-2019.op')
    parameters_filepath = join(TEST_DATA_PATH, 'noaa', 'noaa_params.csv')
    metadata = {'cod_utente': '160080', 'wban': '99999', 'source': 'noaa/160080-99999-2019.op'}
    expected_data = [
        [metadata, datetime(2019, 1, 1, 0, 0), 'Tmedia', 1.0556, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'DEWP', -4.6111, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'STP', 859.6, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'VISIB', 17702.74, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'FF', 4.0638, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'MXSPD', 5.7098, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'Tmax', 5.0, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'Tmin', -2.0, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'PREC', 0.0, True],
        [metadata, datetime(2019, 1, 1, 0, 0), 'SNDP', 40.64, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'Tmedia', -3.6111, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'DEWP', -9.1667, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'STP', 855.1, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'VISIB', 7724.832, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'FF', 4.0638, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'MXSPD', 5.7098, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'Tmax', 0.2222, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'Tmin', -7.0, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'PREC', 0.0, True],
        [metadata, datetime(2019, 1, 2, 0, 0), 'SNDP', 40.64, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'Tmedia', -7.0556, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'DEWP', -15.3889, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'STP', 860.1, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'VISIB', 11426.314, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'FF', 4.0638, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'MXSPD', 5.0926, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'Tmax', -3.2222, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'Tmin', -8.2222, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'PREC', 0.0, True],
        [metadata, datetime(2019, 1, 3, 0, 0), 'SNDP', 40.64, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'Tmedia', -5.0, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'DEWP', -11.7222, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'STP', 859.6, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'VISIB', 20277.684, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'FF', 5.967, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'MXSPD', 8.7962, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'Tmax', -1.3889, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'Tmin', -8.2222, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'PREC', 0.0, True],
        [metadata, datetime(2019, 1, 4, 0, 0), 'SNDP', 40.64, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'Tmedia', -3.0556, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'DEWP', -4.6111, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'STP', 857.4, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'VISIB', 7724.832, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'FF', 3.7037, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'MXSPD', 5.7098, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'Tmax', 4.0, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'Tmin', -5.6111, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'PREC', 2.032, True],
        [metadata, datetime(2019, 1, 5, 0, 0), 'SNDP', 88.9, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'Tmedia', -1.5, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'DEWP', -4.8333, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'STP', 857.8, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'VISIB', 12713.786, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'FF', 3.858, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'MXSPD', 4.5782, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'Tmax', 1.2222, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'Tmin', -2.7778, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'PREC', 0.0, True],
        [metadata, datetime(2019, 1, 6, 0, 0), 'SNDP', 119.38, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'Tmedia', -2.3333, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'DEWP', -5.7222, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'STP', 858.9, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'VISIB', 11909.116, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'FF', 3.6522, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'MXSPD', 4.5782, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'Tmax', 0.2222, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'Tmin', -5.0, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'PREC', 0.0, True],
        [metadata, datetime(2019, 1, 7, 0, 0), 'SNDP', 119.38, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'Tmedia', -2.1667, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'DEWP', -4.4444, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'P', None, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'STP', 848.0, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'VISIB', 5632.69, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'FF', 2.9321, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'MXSPD', 4.1152, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'GUST', None, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'Tmax', 1.7778, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'Tmin', -5.7778, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'PREC', 3.048, True],
        [metadata, datetime(2019, 1, 8, 0, 0), 'SNDP', 149.86, True]
    ]
    effective = noaa.parse(filepath, parameters_filepath=parameters_filepath)
    assert effective == expected_data


def test_is_format_compliant():
    filepath = join(TEST_DATA_PATH, 'noaa', '160080-99999-2019.op')
    assert noaa.is_format_compliant(filepath)
    filepath = join(TEST_DATA_PATH, 'noaa', 'wrong1_160080-99999-2019.op')
    assert not noaa.is_format_compliant(filepath)
    filepath = join(TEST_DATA_PATH, 'rmn', 'ancona_right.csv')
    assert not noaa.is_format_compliant(filepath)
