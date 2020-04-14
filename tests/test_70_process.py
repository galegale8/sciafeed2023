
from datetime import datetime, date
from os.path import exists, join

from sciafeed import process, arpa19, arpaer, hiscentral

from . import TEST_DATA_PATH


def test_parse_and_check(tmpdir):
    # --- arpa19 format ---
    filepath = join(TEST_DATA_PATH, 'arpa19', 'wrong_70002_201301010000_201401010100.dat')
    parameters_filepath = join(TEST_DATA_PATH, 'arpa19', 'arpa19_params.csv')
    limiting_params = {'Tmedia': ('FF', 'DD')}
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [
        (1, "The value of 'FF' is out of range [0.0, 102.0]"),
        (2, "The value of 'DD' is out of range [0.0, 360.0]"),
        (3, "The value of 'Tmedia' is out of range [-35.0, 45.0]"),
        (5, "The values of 'Tmedia' and 'DD' are not consistent"),
        (6, "The values of 'Tmedia' and 'DD' are not consistent"),
        (7, "The values of 'Tmedia' and 'DD' are not consistent"),
        (20, "The values of 'Tmedia' and 'DD' are not consistent")
    ]
    metadata = {'cod_utente': '70002', 'start_date': datetime(2013, 1, 1, 0, 0),
                'end_date': datetime(2014, 1, 1, 1, 0), 'lat': 43.876999,
                'source': 'arpa19/wrong_70002_201301010000_201401010100.dat',
                'format': 'ARPA-19'
                }
    expected_data_parsed = [
        (metadata, datetime(2012, 12, 31, 23, 0), 'FF', 200.0, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'DD', 355.0, True),
        (metadata, datetime(2012, 12, 31, 23, 0), 'Tmedia', 6.8, True),
        (metadata, datetime(2012, 12, 31, 23, 0), 'Tmin', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'Tmax', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), '6', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), '7', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), '8', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'UR media', 83.0, True),
        (metadata, datetime(2012, 12, 31, 23, 0), 'UR min', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'UR max', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), '12', 1020.5, True),
        (metadata, datetime(2012, 12, 31, 23, 0), 'P', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'INSOL', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'PREC', None, False),
        (metadata, datetime(2012, 12, 31, 23, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'FF', 0.6, True),
        (metadata, datetime(2013, 1, 1, 0, 0), 'DD', 361.0, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'Tmedia', 6.5, True),
        (metadata, datetime(2013, 1, 1, 0, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'UR media', 86.0, True),
        (metadata, datetime(2013, 1, 1, 0, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), '12', 1019.8, True),
        (metadata, datetime(2013, 1, 1, 0, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 0, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'FF', 0.3, True),
        (metadata, datetime(2013, 1, 1, 1, 0), 'DD', 288.0, True),
        (metadata, datetime(2013, 1, 1, 1, 0), 'Tmedia', -35.1, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'UR media', 86.0, True),
        (metadata, datetime(2013, 1, 1, 1, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), '12', 1019.6, True),
        (metadata, datetime(2013, 1, 1, 1, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 1, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'FF', 1.1, True),
        (metadata, datetime(2013, 1, 1, 2, 0), 'DD', 357.0, True),
        (metadata, datetime(2013, 1, 1, 2, 0), 'Tmedia', 6.3, True),
        (metadata, datetime(2013, 1, 1, 2, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'UR media', 87.0, True),
        (metadata, datetime(2013, 1, 1, 2, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), '12', 1018.9, True),
        (metadata, datetime(2013, 1, 1, 2, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 2, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'FF', 0.9, True),
        (metadata, datetime(2013, 1, 1, 3, 0), 'DD', 1.0, True),
        (metadata, datetime(2013, 1, 1, 3, 0), 'Tmedia', 6.4, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'UR media', 88.0, True),
        (metadata, datetime(2013, 1, 1, 3, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), '12', 1018.4, True),
        (metadata, datetime(2013, 1, 1, 3, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 3, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'FF', 3.0, True),
        (metadata, datetime(2013, 1, 1, 4, 0), 'DD', 6.0, True),
        (metadata, datetime(2013, 1, 1, 4, 0), 'Tmedia', 6.7, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'UR media', 89.0, True),
        (metadata, datetime(2013, 1, 1, 4, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), '12', 1018.1, True),
        (metadata, datetime(2013, 1, 1, 4, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 4, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'FF', 3.1, True),
        (metadata, datetime(2013, 1, 1, 5, 0), 'DD', 6.0, True),
        (metadata, datetime(2013, 1, 1, 5, 0), 'Tmedia', 6.5, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'UR media', 93.0, True),
        (metadata, datetime(2013, 1, 1, 5, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), '12', 1018.1, True),
        (metadata, datetime(2013, 1, 1, 5, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 5, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'FF', 2.0, True),
        (metadata, datetime(2013, 1, 1, 6, 0), 'DD', 358.0, True),
        (metadata, datetime(2013, 1, 1, 6, 0), 'Tmedia', 6.5, True),
        (metadata, datetime(2013, 1, 1, 6, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'UR media', 93.0, True),
        (metadata, datetime(2013, 1, 1, 6, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), '12', 1018.2, True),
        (metadata, datetime(2013, 1, 1, 6, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 6, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'FF', 0.5, True),
        (metadata, datetime(2013, 1, 1, 7, 0), 'DD', 342.0, True),
        (metadata, datetime(2013, 1, 1, 7, 0), 'Tmedia', 6.6, True),
        (metadata, datetime(2013, 1, 1, 7, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'UR media', 95.0, True),
        (metadata, datetime(2013, 1, 1, 7, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), '12', 1018.2, True),
        (metadata, datetime(2013, 1, 1, 7, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 7, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'FF', 3.5, True),
        (metadata, datetime(2013, 1, 1, 8, 0), 'DD', 12.0, True),
        (metadata, datetime(2013, 1, 1, 8, 0), 'Tmedia', 10.6, True),
        (metadata, datetime(2013, 1, 1, 8, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'UR media', 88.0, True),
        (metadata, datetime(2013, 1, 1, 8, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), '12', 1017.9, True),
        (metadata, datetime(2013, 1, 1, 8, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 8, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'FF', 1.3, True),
        (metadata, datetime(2013, 1, 1, 9, 0), 'DD', 154.0, True),
        (metadata, datetime(2013, 1, 1, 9, 0), 'Tmedia', 12.1, True),
        (metadata, datetime(2013, 1, 1, 9, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'UR media', 72.0, True),
        (metadata, datetime(2013, 1, 1, 9, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), '12', 1018.2, True),
        (metadata, datetime(2013, 1, 1, 9, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 9, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'FF', 5.4, True),
        (metadata, datetime(2013, 1, 1, 10, 0), 'DD', 218.0, True),
        (metadata, datetime(2013, 1, 1, 10, 0), 'Tmedia', 12.3, True),
        (metadata, datetime(2013, 1, 1, 10, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'UR media', 69.0, True),
        (metadata, datetime(2013, 1, 1, 10, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), '12', 1017.7, True),
        (metadata, datetime(2013, 1, 1, 10, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 10, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'FF', 6.1, True),
        (metadata, datetime(2013, 1, 1, 11, 0), 'DD', 225.0, True),
        (metadata, datetime(2013, 1, 1, 11, 0), 'Tmedia', 12.5, True),
        (metadata, datetime(2013, 1, 1, 11, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'UR media', 73.0, True),
        (metadata, datetime(2013, 1, 1, 11, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), '12', 1016.7, True),
        (metadata, datetime(2013, 1, 1, 11, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 11, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'FF', 6.5, True),
        (metadata, datetime(2013, 1, 1, 12, 0), 'DD', 226.0, True),
        (metadata, datetime(2013, 1, 1, 12, 0), 'Tmedia', 12.2, True),
        (metadata, datetime(2013, 1, 1, 12, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'UR media', 74.0, True),
        (metadata, datetime(2013, 1, 1, 12, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), '12', 1016.2, True),
        (metadata, datetime(2013, 1, 1, 12, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 12, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'FF', 4.6, True),
        (metadata, datetime(2013, 1, 1, 13, 0), 'DD', 221.0, True),
        (metadata, datetime(2013, 1, 1, 13, 0), 'Tmedia', 11.7, True),
        (metadata, datetime(2013, 1, 1, 13, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'UR media', 78.0, True),
        (metadata, datetime(2013, 1, 1, 13, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), '12', 1016.1, True),
        (metadata, datetime(2013, 1, 1, 13, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 13, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'FF', 1.9, True),
        (metadata, datetime(2013, 1, 1, 14, 0), 'DD', 233.0, True),
        (metadata, datetime(2013, 1, 1, 14, 0), 'Tmedia', 11.0, True),
        (metadata, datetime(2013, 1, 1, 14, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'UR media', 82.0, True),
        (metadata, datetime(2013, 1, 1, 14, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), '12', 1016.1, True),
        (metadata, datetime(2013, 1, 1, 14, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 14, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'FF', 2.8, True),
        (metadata, datetime(2013, 1, 1, 15, 0), 'DD', 355.0, True),
        (metadata, datetime(2013, 1, 1, 15, 0), 'Tmedia', 10.0, True),
        (metadata, datetime(2013, 1, 1, 15, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'UR media', 96.0, True),
        (metadata, datetime(2013, 1, 1, 15, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), '12', 1015.8, True),
        (metadata, datetime(2013, 1, 1, 15, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 15, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'FF', 2.4, True),
        (metadata, datetime(2013, 1, 1, 16, 0), 'DD', 345.0, True),
        (metadata, datetime(2013, 1, 1, 16, 0), 'Tmedia', 9.9, True),
        (metadata, datetime(2013, 1, 1, 16, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'UR media', 96.0, True),
        (metadata, datetime(2013, 1, 1, 16, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), '12', 1015.6, True),
        (metadata, datetime(2013, 1, 1, 16, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 16, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'FF', 2.6, True),
        (metadata, datetime(2013, 1, 1, 17, 0), 'DD', 357.0, True),
        (metadata, datetime(2013, 1, 1, 17, 0), 'Tmedia', 10.1, True),
        (metadata, datetime(2013, 1, 1, 17, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'UR media', 97.0, True),
        (metadata, datetime(2013, 1, 1, 17, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), '12', 1015.5, True),
        (metadata, datetime(2013, 1, 1, 17, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 17, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'FF', 2.6, True),
        (metadata, datetime(2013, 1, 1, 18, 0), 'DD', 2.0, True),
        (metadata, datetime(2013, 1, 1, 18, 0), 'Tmedia', 9.9, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'Tmin', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'Tmax', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), '6', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), '7', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), '8', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'UR media', 100.0, True),
        (metadata, datetime(2013, 1, 1, 18, 0), 'UR min', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'UR max', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), '12', 1015.4, True),
        (metadata, datetime(2013, 1, 1, 18, 0), 'P', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'Pmin', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'Pmax', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'RADSOL', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'INSOL', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'PREC', None, False),
        (metadata, datetime(2013, 1, 1, 18, 0), 'Bagnatura_f', None, False),
    ]
    for i, record in enumerate(data_parsed):
        assert data_parsed[i][1:] == expected_data_parsed[i][1:]
        expected_md = expected_data_parsed[i][0]
        expected_md['row'] = i // 19 + 1
        assert data_parsed[i][0] == expected_md
    # global error
    filepath = str(tmpdir.join('report.txt'))
    err_msgs, _ = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [(0, 'the file has unknown format')]

    # --- arpa21 format ---
    filepath = join(TEST_DATA_PATH, 'arpa21', 'wrong_00202_201201010000_201301010100.dat')
    parameters_filepath = join(TEST_DATA_PATH, 'arpa21', 'arpa21_params.csv')
    limiting_params = {'UR media': ('UR min', 'Tmin')}
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [
        (1, "The value of 'Tmedia' is out of range [-35.0, 45.0]"),
        (1, "The values of 'UR media' and 'Tmin' are not consistent"),
        (2, "The value of 'Tmin' is out of range [-40.0, 40.0]"),
        (3, "The value of 'Tmax' is out of range [-30.0, 50.0]"),
        (3, "The values of 'UR media' and 'Tmin' are not consistent"),
        (4, "The values of 'UR media' and 'Tmin' are not consistent"),
        (5, "The values of 'UR media' and 'Tmin' are not consistent"),
        (6, "The values of 'UR media' and 'Tmin' are not consistent"),
        (7, "The values of 'UR media' and 'Tmin' are not consistent"),
        (8, "The values of 'UR media' and 'Tmin' are not consistent"),
        (9, "The values of 'UR media' and 'Tmin' are not consistent"),
        (10, "The values of 'UR media' and 'Tmin' are not consistent"),
        (11, "The values of 'UR media' and 'Tmin' are not consistent"),
        (12, "The values of 'UR media' and 'Tmin' are not consistent"),
        (13, "The values of 'UR media' and 'Tmin' are not consistent"),
        (14, "The values of 'UR media' and 'Tmin' are not consistent"),
        (15, "The values of 'UR media' and 'Tmin' are not consistent"),
        (16, "The values of 'UR media' and 'Tmin' are not consistent"),
        (17, "The values of 'UR media' and 'Tmin' are not consistent"),
        (18, "The values of 'UR media' and 'Tmin' are not consistent"),
        (19, "The values of 'UR media' and 'Tmin' are not consistent"),
        (20, "The values of 'UR media' and 'Tmin' are not consistent")
    ]
    metadata = {'cod_utente': '00202', 'start_date': datetime(2012, 1, 1, 0, 0),
                'end_date': datetime(2013, 1, 1, 1, 0), 'lat': 37.33913, 'format': 'ARPA-21',
                'source': 'arpa21/wrong_00202_201201010000_201301010100.dat'}
    expected_data_parsed = [
        (metadata, datetime(2011, 12, 31, 23, 0), 'FF', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'DD', 242.0, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'Tmedia', -57.0, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'Tmin', 5.5, True),
        (metadata, datetime(2011, 12, 31, 23, 0), 'Tmax', 6.0, True),
        (metadata, datetime(2011, 12, 31, 23, 0), '6', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), '7', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), '8', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'UR media', 83.0, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'UR min', 80.0, True),
        (metadata, datetime(2011, 12, 31, 23, 0), 'UR max', 85.0, True),
        (metadata, datetime(2011, 12, 31, 23, 0), '12', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'P', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'Pmin', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'Pmax', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'RADSOL', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), '17', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), '18', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'INSOL_00', None, False),
        (metadata, datetime(2011, 12, 31, 23, 0), 'PREC', 0.0, True),
        (metadata, datetime(2011, 12, 31, 23, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'DD', 354.0, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'Tmedia', 5.6, True),
        (metadata, datetime(2012, 1, 1, 0, 0), 'Tmin', 52.0, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'Tmax', 5.9, True),
        (metadata, datetime(2012, 1, 1, 0, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'UR media', 81.0, True),
        (metadata, datetime(2012, 1, 1, 0, 0), 'UR min', 79.0, True),
        (metadata, datetime(2012, 1, 1, 0, 0), 'UR max', 83.0, True),
        (metadata, datetime(2012, 1, 1, 0, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 0, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 0, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'DD', 184.0, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'Tmedia', 5.6, True),
        (metadata, datetime(2012, 1, 1, 1, 0), 'Tmin', 5.3, True),
        (metadata, datetime(2012, 1, 1, 1, 0), 'Tmax', 58.0, False),
        (metadata, datetime(2012, 1, 1, 1, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'UR media', 79.0, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'UR min', 79.0, True),
        (metadata, datetime(2012, 1, 1, 1, 0), 'UR max', 81.0, True),
        (metadata, datetime(2012, 1, 1, 1, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 1, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 1, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'DD', 244.0, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'Tmedia', 5.0, True),
        (metadata, datetime(2012, 1, 1, 2, 0), 'Tmin', 4.6, True),
        (metadata, datetime(2012, 1, 1, 2, 0), 'Tmax', 5.7, True),
        (metadata, datetime(2012, 1, 1, 2, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'UR media', 82.0, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'UR min', 79.0, True),
        (metadata, datetime(2012, 1, 1, 2, 0), 'UR max', 85.0, True),
        (metadata, datetime(2012, 1, 1, 2, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 2, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 2, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'DD', 198.0, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'Tmedia', 4.4, True),
        (metadata, datetime(2012, 1, 1, 3, 0), 'Tmin', 3.9, True),
        (metadata, datetime(2012, 1, 1, 3, 0), 'Tmax', 5.0, True),
        (metadata, datetime(2012, 1, 1, 3, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'UR media', 84.0, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'UR min', 82.0, True),
        (metadata, datetime(2012, 1, 1, 3, 0), 'UR max', 87.0, True),
        (metadata, datetime(2012, 1, 1, 3, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 3, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 3, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'DD', 198.0, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'Tmedia', 4.6, True),
        (metadata, datetime(2012, 1, 1, 4, 0), 'Tmin', 3.9, True),
        (metadata, datetime(2012, 1, 1, 4, 0), 'Tmax', 4.9, True),
        (metadata, datetime(2012, 1, 1, 4, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'UR media', 84.0, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'UR min', 83.0, True),
        (metadata, datetime(2012, 1, 1, 4, 0), 'UR max', 88.0, True),
        (metadata, datetime(2012, 1, 1, 4, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 4, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 4, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'DD', 276.0, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'Tmedia', 5.0, True),
        (metadata, datetime(2012, 1, 1, 5, 0), 'Tmin', 4.4, True),
        (metadata, datetime(2012, 1, 1, 5, 0), 'Tmax', 5.9, True),
        (metadata, datetime(2012, 1, 1, 5, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'UR media', 84.0, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'UR min', 82.0, True),
        (metadata, datetime(2012, 1, 1, 5, 0), 'UR max', 86.0, True),
        (metadata, datetime(2012, 1, 1, 5, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 5, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 5, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'DD', 133.0, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'Tmedia', 5.9, True),
        (metadata, datetime(2012, 1, 1, 6, 0), 'Tmin', 5.8, True),
        (metadata, datetime(2012, 1, 1, 6, 0), 'Tmax', 6.2, True),
        (metadata, datetime(2012, 1, 1, 6, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'UR media', 83.0, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'UR min', 83.0, True),
        (metadata, datetime(2012, 1, 1, 6, 0), 'UR max', 85.0, True),
        (metadata, datetime(2012, 1, 1, 6, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 6, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 6, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'DD', 200.0, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'Tmedia', 7.2, True),
        (metadata, datetime(2012, 1, 1, 7, 0), 'Tmin', 6.2, True),
        (metadata, datetime(2012, 1, 1, 7, 0), 'Tmax', 8.5, True),
        (metadata, datetime(2012, 1, 1, 7, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'UR media', 82.0, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'UR min', 80.0, True),
        (metadata, datetime(2012, 1, 1, 7, 0), 'UR max', 85.0, True),
        (metadata, datetime(2012, 1, 1, 7, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 7, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 7, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'DD', 160.0, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'Tmedia', 9.3, True),
        (metadata, datetime(2012, 1, 1, 8, 0), 'Tmin', 8.3, True),
        (metadata, datetime(2012, 1, 1, 8, 0), 'Tmax', 11.1, True),
        (metadata, datetime(2012, 1, 1, 8, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'UR media', 80.0, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'UR min', 73.0, True),
        (metadata, datetime(2012, 1, 1, 8, 0), 'UR max', 86.0, True),
        (metadata, datetime(2012, 1, 1, 8, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 8, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 8, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'DD', 92.0, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'Tmedia', 12.2, True),
        (metadata, datetime(2012, 1, 1, 9, 0), 'Tmin', 11.1, True),
        (metadata, datetime(2012, 1, 1, 9, 0), 'Tmax', 14.0, True),
        (metadata, datetime(2012, 1, 1, 9, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'UR media', 73.0, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'UR min', 67.0, True),
        (metadata, datetime(2012, 1, 1, 9, 0), 'UR max', 77.0, True),
        (metadata, datetime(2012, 1, 1, 9, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 9, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 9, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'DD', 143.0, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'Tmedia', 13.5, True),
        (metadata, datetime(2012, 1, 1, 10, 0), 'Tmin', 13.4, True),
        (metadata, datetime(2012, 1, 1, 10, 0), 'Tmax', 14.0, True),
        (metadata, datetime(2012, 1, 1, 10, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'UR media', 74.0, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'UR min', 68.0, True),
        (metadata, datetime(2012, 1, 1, 10, 0), 'UR max', 78.0, True),
        (metadata, datetime(2012, 1, 1, 10, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 10, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 10, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'DD', 300.0, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'Tmedia', 13.9, True),
        (metadata, datetime(2012, 1, 1, 11, 0), 'Tmin', 13.6, True),
        (metadata, datetime(2012, 1, 1, 11, 0), 'Tmax', 14.4, True),
        (metadata, datetime(2012, 1, 1, 11, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'UR media', 78.0, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'UR min', 76.0, True),
        (metadata, datetime(2012, 1, 1, 11, 0), 'UR max', 82.0, True),
        (metadata, datetime(2012, 1, 1, 11, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 11, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 11, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'DD', 260.0, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'Tmedia', 14.0, True),
        (metadata, datetime(2012, 1, 1, 12, 0), 'Tmin', 13.7, True),
        (metadata, datetime(2012, 1, 1, 12, 0), 'Tmax', 14.5, True),
        (metadata, datetime(2012, 1, 1, 12, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'UR media', 82.0, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'UR min', 80.0, True),
        (metadata, datetime(2012, 1, 1, 12, 0), 'UR max', 85.0, True),
        (metadata, datetime(2012, 1, 1, 12, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 12, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 12, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'DD', 236.0, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'Tmedia', 14.3, True),
        (metadata, datetime(2012, 1, 1, 13, 0), 'Tmin', 13.9, True),
        (metadata, datetime(2012, 1, 1, 13, 0), 'Tmax', 14.7, True),
        (metadata, datetime(2012, 1, 1, 13, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'UR media', 85.0, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'UR min', 84.0, True),
        (metadata, datetime(2012, 1, 1, 13, 0), 'UR max', 87.0, True),
        (metadata, datetime(2012, 1, 1, 13, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 13, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 13, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'DD', 235.0, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'Tmedia', 14.1, True),
        (metadata, datetime(2012, 1, 1, 14, 0), 'Tmin', 13.4, True),
        (metadata, datetime(2012, 1, 1, 14, 0), 'Tmax', 14.6, True),
        (metadata, datetime(2012, 1, 1, 14, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'UR media', 86.0, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'UR min', 85.0, True),
        (metadata, datetime(2012, 1, 1, 14, 0), 'UR max', 90.0, True),
        (metadata, datetime(2012, 1, 1, 14, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 14, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 14, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'DD', 240.0, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'Tmedia', 12.8, True),
        (metadata, datetime(2012, 1, 1, 15, 0), 'Tmin', 12.3, True),
        (metadata, datetime(2012, 1, 1, 15, 0), 'Tmax', 13.3, True),
        (metadata, datetime(2012, 1, 1, 15, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'UR media', 95.0, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'UR min', 91.0, True),
        (metadata, datetime(2012, 1, 1, 15, 0), 'UR max', 98.0, True),
        (metadata, datetime(2012, 1, 1, 15, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 15, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 15, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'DD', 246.0, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'Tmedia', 11.9, True),
        (metadata, datetime(2012, 1, 1, 16, 0), 'Tmin', 11.2, True),
        (metadata, datetime(2012, 1, 1, 16, 0), 'Tmax', 12.3, True),
        (metadata, datetime(2012, 1, 1, 16, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'UR media', 98.0, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'UR min', 97.0, True),
        (metadata, datetime(2012, 1, 1, 16, 0), 'UR max', 100.0, True),
        (metadata, datetime(2012, 1, 1, 16, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 16, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 16, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'DD', 322.0, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'Tmedia', 11.0, True),
        (metadata, datetime(2012, 1, 1, 17, 0), 'Tmin', 10.6, True),
        (metadata, datetime(2012, 1, 1, 17, 0), 'Tmax', 11.3, True),
        (metadata, datetime(2012, 1, 1, 17, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'UR media', 100.0, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'UR min', 100.0, True),
        (metadata, datetime(2012, 1, 1, 17, 0), 'UR max', 100.0, True),
        (metadata, datetime(2012, 1, 1, 17, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 17, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 17, 0), 'Bagnatura_f', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'FF', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'DD', 65.0, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'Tmedia', 9.9, True),
        (metadata, datetime(2012, 1, 1, 18, 0), 'Tmin', 9.5, True),
        (metadata, datetime(2012, 1, 1, 18, 0), 'Tmax', 10.6, True),
        (metadata, datetime(2012, 1, 1, 18, 0), '6', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), '7', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), '8', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'UR media', 100.0, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'UR min', 100.0, True),
        (metadata, datetime(2012, 1, 1, 18, 0), 'UR max', 100.0, True),
        (metadata, datetime(2012, 1, 1, 18, 0), '12', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'P', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'Pmin', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'Pmax', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'RADSOL', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), '17', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), '18', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'INSOL_00', None, False),
        (metadata, datetime(2012, 1, 1, 18, 0), 'PREC', 0.0, True),
        (metadata, datetime(2012, 1, 1, 18, 0), 'Bagnatura_f', None, False),
    ]
    for i, record in enumerate(data_parsed):
        assert data_parsed[i][1:] == expected_data_parsed[i][1:]
        expected_md = expected_data_parsed[i][0]
        expected_md['row'] = i // 21 + 1
        assert data_parsed[i][0] == expected_md
    # global error
    filepath = str(tmpdir.join('report.txt'))
    err_msgs, _ = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [(0, 'the file has unknown format')]

    # --- arpafvg format ---
    filepath = join(TEST_DATA_PATH, 'arpafvg', 'wrong_00001_2018010101_2019010101.dat')
    parameters_filepath = join(TEST_DATA_PATH, 'arpafvg', 'arpafvg_params.csv')
    limiting_params = {'PREC': ('Bagnatura_f', 'DD')}
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    metadata = {'cod_utente': '00001', 'start_date': datetime(2018, 1, 1, 1, 0),
                'end_date': datetime(2019, 1, 1, 1, 0), 'lat': 46.077222, 'format': 'ARPA-FVG',
                'source': 'arpafvg/wrong_00001_2018010101_2019010101.dat', 'row': 2}
    assert err_msgs == [
        (1, 'The number of components in the row is wrong'),
        (3, 'duplication of rows with different data'),
        (4, 'the latitude changes'),
        (5, 'duplication of rows with different data'),
        (6, 'it is not strictly after the previous'),
        (7, 'the time is not coherent with the filename'),
        (2, "The values of 'PREC' and 'Bagnatura_f' are not consistent")]
    expected_data_parsed = [
        (metadata, datetime(2018, 1, 1, 1, 0), 'PREC', 0.0, False),
        (metadata, datetime(2018, 1, 1, 1, 0), 'Tmedia', 3.1, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'UR media', 85.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'Bagnatura_f', 59.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'DD', 317.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'FF', 1.6, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'Pstaz', 1001.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'RADSOL', 0.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'INSOL', 0.0, True),
    ]
    assert data_parsed == expected_data_parsed
    # global error
    filepath = str(tmpdir.join('report.txt'))
    err_msgs, _ = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [(0, 'the file has unknown format')]

    # --- bolzano format ---
    parameters_filepath = join(TEST_DATA_PATH, 'bolzano', 'bolzano_params.csv')
    filepath = join(TEST_DATA_PATH, 'bolzano', 'MonteMaria.xls')
    metadata = {'desc': 'Marienberg - Monte Maria', 'cod_utente': '02500MS',
                'utmx': '616288', 'utmy': '5173583', 'height': '1310',
                'source': 'bolzano/MonteMaria.xls', 'format': 'BOLZANO'}
    expected_data = [
        (metadata, date(1981, 1, 1), 'Tmin', 3.0, True),
        (metadata, date(1981, 1, 1), 'Tmax', 9.0, True),
        (metadata, date(1981, 1, 1), 'PREC', 0.0, True),
        (metadata, date(1981, 1, 2), 'Tmin', -4.0, True),
        (metadata, date(1981, 1, 2), 'Tmax', 5.0, True),
        (metadata, date(1981, 1, 2), 'PREC', 0.4, True),
        (metadata, date(1981, 1, 3), 'Tmin', -4.0, True),
        (metadata, date(1981, 1, 3), 'Tmax', 5.0, True),
        (metadata, date(1981, 1, 3), 'PREC', 0.0, True),
        (metadata, date(1981, 1, 4), 'Tmin', 1.0, True),
        (metadata, date(1981, 1, 4), 'Tmax', 9.0, True),
        (metadata, date(1981, 1, 4), 'PREC', 14.5, True),
        (metadata, date(1981, 1, 5), 'Tmin', -8.0, True),
        (metadata, date(1981, 1, 5), 'Tmax', 3.0, True),
        (metadata, date(1981, 1, 5), 'PREC', 5.1, True),
        (metadata, date(1981, 1, 6), 'Tmin', -8.0, True),
        (metadata, date(1981, 1, 6), 'Tmax', -5.0, True),
        (metadata, date(1981, 1, 6), 'PREC', 1.0, True),
        (metadata, date(1981, 1, 7), 'Tmin', -9.0, True),
        (metadata, date(1981, 1, 7), 'Tmax', -5.0, True),
        (metadata, date(1981, 1, 7), 'PREC', 6.1, True),
        (metadata, date(1981, 1, 8), 'Tmin', -13.0, True),
        (metadata, date(1981, 1, 8), 'Tmax', -7.0, True),
        (metadata, date(1981, 1, 8), 'PREC', 0.0, True),
    ]
    err_msgs, parsed_data = process.parse_and_check(filepath, parameters_filepath)
    assert not err_msgs
    for i, data_item in enumerate(parsed_data):
        expected_md = expected_data[i][0].copy()
        expected_md['row'] = i // 3 + 14
        assert data_item[0] == expected_md
        assert data_item[1:] == expected_data[i][1:]
    # with some errors
    limiting_params = {'Tmin': ('PREC', 'Tmax')}
    filepath = join(TEST_DATA_PATH, 'bolzano', 'wrong3.xls')
    err_msgs, parsed_data = process.parse_and_check(filepath, parameters_filepath,
                                                    limiting_params=limiting_params)
    metadata['source'] = 'bolzano/wrong3.xls'
    assert err_msgs == [
        (14, 'the date format is wrong'),
        (15, 'the row contains values not numeric'),
        (18, 'the row is not strictly after the previous'),
        (22, 'the row is duplicated with different values'),
        (16, "The values of 'Tmin' and 'PREC' are not consistent"),
        (17, "The value of 'Tmax' is out of range [-30.0, 50.0]"),
        (17, "The values of 'Tmin' and 'PREC' are not consistent"),
        (19, "The values of 'Tmin' and 'PREC' are not consistent"),
        (20, "The values of 'Tmin' and 'PREC' are not consistent"),
        (21, "The values of 'Tmin' and 'PREC' are not consistent"),
        (23, "The values of 'Tmin' and 'PREC' are not consistent"),
        (24, "The value of 'PREC' is out of range [0.0, 989.0]")
    ]
    expected_parsed_data = [
        (metadata, date(1981, 1, 3), 'Tmin', -4.0, False),
        (metadata, date(1981, 1, 3), 'Tmax', 5.0, True),
        (metadata, date(1981, 1, 3), 'PREC', 0.0, True),
        (metadata, date(1981, 1, 4), 'Tmin', 1.0, False),
        (metadata, date(1981, 1, 4), 'Tmax', 9999.0, False),
        (metadata, date(1981, 1, 4), 'PREC', 14.5, True),
        (metadata, date(1981, 1, 5), 'Tmin', -8.0, False),
        (metadata, date(1981, 1, 5), 'Tmax', 3.0, True),
        (metadata, date(1981, 1, 5), 'PREC', 5.1, True),
        (metadata, date(1981, 1, 5), 'Tmin', -8.0, False),
        (metadata, date(1981, 1, 5), 'Tmax', 3.0, True),
        (metadata, date(1981, 1, 5), 'PREC', 5.1, True),
        (metadata, date(1981, 1, 6), 'Tmin', -8.0, False),
        (metadata, date(1981, 1, 6), 'Tmax', -5.0, True),
        (metadata, date(1981, 1, 6), 'PREC', 1.0, True),
        (metadata, date(1981, 1, 7), 'Tmin', -9.0, False),
        (metadata, date(1981, 1, 7), 'Tmax', -5.0, True),
        (metadata, date(1981, 1, 7), 'PREC', 6.1, True),
        (metadata, date(1981, 1, 8), 'Tmin', -13.0, True),
        (metadata, date(1981, 1, 8), 'Tmax', -7.0, True),
        (metadata, date(1981, 1, 8), 'PREC', -3.0, False),
    ]
    rows_info = [16, 17, 19, 20, 21, 23, 24]
    for i, record in enumerate(parsed_data):
        assert parsed_data[i][1:] == expected_parsed_data[i][1:]
        expected_md = expected_parsed_data[i][0]
        expected_md['row'] = rows_info[i // 3]
        assert parsed_data[i][0] == expected_md
    # global error
    filepath = str(tmpdir.join('report.txt'))
    with open(filepath, 'w'):
        pass
    err_msgs, parsed_after_check = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [(0, 'the file has unknown format')]
    assert not parsed_after_check

    # --- NOAA format ---
    filepath = join(TEST_DATA_PATH, 'noaa', 'wrong2_160080-99999-2019.op')
    parameters_filepath = join(TEST_DATA_PATH, 'noaa', 'noaa_params.csv')
    limiting_params = {'Tmedia': ('Tmin', 'Tmax')}
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [
        (2, 'the length of the row is not standard'),
        (3, 'the reference time for the row is not parsable'),
        (4, 'the precipitation flag is not parsable'),
        (5, 'The number of components in the row is wrong'),
        (6, 'The row contains not numeric values'),
        (10, 'duplication of rows with different data'),
        (12, 'it is not strictly after the previous')
    ]
    metadata = {'source': 'noaa/wrong2_160080-99999-2019.op',
                'cod_utente': '160080', 'wban': '99999', 'format': 'NOAA'}
    expected_data_parsed = [
        (metadata, date(2019, 1, 6), 'Tmedia', -1.5, True),
        (metadata, date(2019, 1, 6), 'DEWP', -4.8333, True),
        (metadata, date(2019, 1, 6), 'P', None, True),
        (metadata, date(2019, 1, 6), 'STP', 857.8, True),
        (metadata, date(2019, 1, 6), 'VISIB', 12713.786, True),
        (metadata, date(2019, 1, 6), 'FF', 3.858, True),
        (metadata, date(2019, 1, 6), 'MXSPD', 4.5782, True),
        (metadata, date(2019, 1, 6), 'GUST', None, True),
        (metadata, date(2019, 1, 6), 'Tmax', 1.2222, True),
        (metadata, date(2019, 1, 6), 'Tmin', -2.7778, True),
        (metadata, date(2019, 1, 6), 'PREC', 0.0, True),
        (metadata, date(2019, 1, 6), 'SNDP', 119.38, True),
        (metadata, date(2019, 1, 6), 'UR media', 79.722, True),
        (metadata, date(2019, 1, 6), 'Tmedia', -1.5, True),
        (metadata, date(2019, 1, 6), 'DEWP', -4.8333, True),
        (metadata, date(2019, 1, 6), 'P', None, True),
        (metadata, date(2019, 1, 6), 'STP', 857.8, True),
        (metadata, date(2019, 1, 6), 'VISIB', 12713.786, True),
        (metadata, date(2019, 1, 6), 'FF', 3.858, True),
        (metadata, date(2019, 1, 6), 'MXSPD', 4.5782, True),
        (metadata, date(2019, 1, 6), 'GUST', None, True),
        (metadata, date(2019, 1, 6), 'Tmax', 1.2222, True),
        (metadata, date(2019, 1, 6), 'Tmin', -2.7778, True),
        (metadata, date(2019, 1, 6), 'PREC', 0.0, True),
        (metadata, date(2019, 1, 6), 'SNDP', 119.38, True),
        (metadata, date(2019, 1, 6), 'UR media', 79.722, True),
        (metadata, date(2019, 1, 7), 'Tmedia', -2.3333, True),
        (metadata, date(2019, 1, 7), 'DEWP', -5.7222, True),
        (metadata, date(2019, 1, 7), 'P', None, True),
        (metadata, date(2019, 1, 7), 'STP', 858.9, True),
        (metadata, date(2019, 1, 7), 'VISIB', 11909.116, True),
        (metadata, date(2019, 1, 7), 'FF', 3.6522, True),
        (metadata, date(2019, 1, 7), 'MXSPD', 4.5782, True),
        (metadata, date(2019, 1, 7), 'GUST', None, True),
        (metadata, date(2019, 1, 7), 'Tmax', 0.2222, True),
        (metadata, date(2019, 1, 7), 'Tmin', -5.0, True),
        (metadata, date(2019, 1, 7), 'PREC', 0.0, True),
        (metadata, date(2019, 1, 7), 'SNDP', 119.38, True),
        (metadata, date(2019, 1, 7), 'UR media', 83.334, True),
        (metadata, date(2019, 1, 9), 'Tmedia', -2.1667, True),
        (metadata, date(2019, 1, 9), 'DEWP', -4.4444, True),
        (metadata, date(2019, 1, 9), 'P', None, True),
        (metadata, date(2019, 1, 9), 'STP', 848.0, True),
        (metadata, date(2019, 1, 9), 'VISIB', 5632.69, True),
        (metadata, date(2019, 1, 9), 'FF', 2.9321, True),
        (metadata, date(2019, 1, 9), 'MXSPD', 4.1152, True),
        (metadata, date(2019, 1, 9), 'GUST', None, True),
        (metadata, date(2019, 1, 9), 'Tmax', 1.7778, True),
        (metadata, date(2019, 1, 9), 'Tmin', -5.7778, True),
        (metadata, date(2019, 1, 9), 'PREC', 3.048, True),
        (metadata, date(2019, 1, 9), 'SNDP', 149.86, True),
        (metadata, date(2019, 1, 9), 'UR media', 87.778, True),
    ]
    rows_info = [7, 8, 9, 11]
    for i, record in enumerate(data_parsed):
        assert record[1:] == expected_data_parsed[i][1:]
        expected_md = expected_data_parsed[i][0]
        expected_md['row'] = rows_info[i // 13]
        assert record[0] == expected_md
    # global error
    filepath = str(tmpdir.join('report.txt'))
    err_msgs, _ = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [(0, 'the file has unknown format')]

    # --- RMN format ---
    filepath = join(TEST_DATA_PATH, 'rmn', 'ancona_right.csv')
    parameters_filepath = join(TEST_DATA_PATH, 'rmn', 'rmn_params.csv')
    limiting_params = {'Tmedia': ('FF', 'UR media')}
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert not err_msgs
    metadata = {'cod_utente': 'ANCONA', 'format': 'RMN',
                'fieldnames': ['DATA', 'ORA', 'DD', 'FF', 'Tmedia', 'P', 'UR media']}
    rows_info = [7, 8, 9, 11]
    expected_data_parsed = [
        (metadata, datetime(2017, 12, 31, 23, 0), 'DD', 180.0, True),
        (metadata, datetime(2017, 12, 31, 23, 0), 'FF', 1.9, True),
        (metadata, datetime(2017, 12, 31, 23, 0), 'Tmedia', 7.2, True),
        (metadata, datetime(2017, 12, 31, 23, 0), 'P', 1018.1, True),
        (metadata, datetime(2017, 12, 31, 23, 0), 'UR media', 63.0, True),
        (metadata, datetime(2018, 1, 1, 0, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 0, 0), 'FF', 1.0, True),
        (metadata, datetime(2018, 1, 1, 0, 0), 'Tmedia', 8.0, True),
        (metadata, datetime(2018, 1, 1, 0, 0), 'P', 1017.6, True),
        (metadata, datetime(2018, 1, 1, 0, 0), 'UR media', 60.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'FF', 4.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'Tmedia', 9.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'P', 1016.9, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'UR media', 58.0, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'FF', 3.9, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'Tmedia', 8.7, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'P', 1016.2, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'UR media', 59.0, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'FF', 4.5, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'Tmedia', 10.1, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'P', 1015.2, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'UR media', 59.0, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'FF', 5.8, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'Tmedia', 9.7, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'P', 1014.3, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'UR media', 62.0, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'FF', 4.6, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'Tmedia', 9.5, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'P', 1014.1, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'UR media', 64.0, True),
    ]
    for i, record in enumerate(expected_data_parsed):
        assert record[1:] == expected_data_parsed[i][1:]
        expected_md = expected_data_parsed[i][0]
        expected_md['row'] = rows_info[i // 13]
        assert record[0] == expected_md
    # global error
    filepath = str(tmpdir.join('report.txt'))
    with open(filepath, 'w'):
        pass
    err_msgs, _ = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [(0, 'the file has unknown format')]
    # various errors
    limiting_params = {'Tmedia': ('UR media', 'DD')}
    filepath = join(TEST_DATA_PATH, 'rmn', 'ancona_wrong5.csv')
    parameters_filepath = join(TEST_DATA_PATH, 'rmn', 'rmn_params.csv')
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [
        (10, 'the row is duplicated with different values'),
        (4, "The value of 'DD' is out of range [0.0, 360.0]"),
        (4, "The values of 'Tmedia' and 'UR media' are not consistent"),
        (16, "The values of 'Tmedia' and 'UR media' are not consistent"),
        (22, "The values of 'Tmedia' and 'UR media' are not consistent"),
        (28, "The values of 'Tmedia' and 'UR media' are not consistent"),
        (34, "The values of 'Tmedia' and 'UR media' are not consistent"),
        (40, "The values of 'Tmedia' and 'UR media' are not consistent")
    ]
    expected_data_parsed = [
        (metadata, datetime(2017, 12, 31, 23, 0), 'DD', 361.0, False),
        (metadata, datetime(2017, 12, 31, 23, 0), 'FF', 1.9, True),
        (metadata, datetime(2017, 12, 31, 23, 0), 'Tmedia', 7.2, False),
        (metadata, datetime(2017, 12, 31, 23, 0), 'P', 1018.1, True),
        (metadata, datetime(2017, 12, 31, 23, 0), 'UR media', 63.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'FF', 4.0, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'Tmedia', 9.0, False),
        (metadata, datetime(2018, 1, 1, 1, 0), 'P', 1016.9, True),
        (metadata, datetime(2018, 1, 1, 1, 0), 'UR media', 58.0, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'FF', 3.9, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'Tmedia', 8.7, False),
        (metadata, datetime(2018, 1, 1, 2, 0), 'P', 1016.2, True),
        (metadata, datetime(2018, 1, 1, 2, 0), 'UR media', 59.0, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'FF', 4.5, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'Tmedia', 10.1, False),
        (metadata, datetime(2018, 1, 1, 3, 0), 'P', 1015.2, True),
        (metadata, datetime(2018, 1, 1, 3, 0), 'UR media', 59.0, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'FF', 5.8, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'Tmedia', 9.7, False),
        (metadata, datetime(2018, 1, 1, 4, 0), 'P', 1014.3, True),
        (metadata, datetime(2018, 1, 1, 4, 0), 'UR media', 62.0, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'DD', 180.0, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'FF', 4.6, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'Tmedia', 9.5, False),
        (metadata, datetime(2018, 1, 1, 5, 0), 'P', 1014.1, True),
        (metadata, datetime(2018, 1, 1, 5, 0), 'UR media', 64.0, True),
    ]
    rows_info = [4, 16, 22, 28, 34, 40]
    for i, record in enumerate(data_parsed):
        assert record[1:] == expected_data_parsed[i][1:]
        expected_md = expected_data_parsed[i][0]
        expected_md['row'] = rows_info[i // 5]
        assert record[0] == expected_md

    # --- trentino format ---
    parameters_filepath = join(TEST_DATA_PATH, 'trentino', 'trentino_params.csv')
    filepath = join(TEST_DATA_PATH, 'trentino', 'T0001.csv')
    metadata = {'cod_utente': '0001', 'desc': 'Pergine Valsugana (Convento)',
                'height': 475.0, 'lat': 46.06227631, 'lon': 11.23670156, 'format': 'TRENTINO',
                'source': 'trentino/T0001.csv', 'fieldnames': ['date', 'Tmin', 'quality']}
    expected_data = [
        (metadata, date(1930, 5, 1), 'Tmin', 10.0, True),
        (metadata, date(1930, 5, 2), 'Tmin', 11.0, True),
        (metadata, date(1930, 5, 3), 'Tmin', 10.0, True),
        (metadata, date(1930, 5, 4), 'Tmin', 8.0, True),
        (metadata, date(1930, 5, 5), 'Tmin', 12.0, True),
        (metadata, date(1930, 5, 6), 'Tmin', 8.0, True),
        (metadata, date(1930, 5, 7), 'Tmin', 10.0, True),
        (metadata, date(1930, 5, 8), 'Tmin', 7.0, True),
        (metadata, date(1930, 5, 9), 'Tmin', 8.0, True),
        (metadata, date(1930, 5, 10), 'Tmin', 7.0, True),
        (metadata, date(1930, 5, 11), 'Tmin', 5.0, True),
        (metadata, date(1930, 5, 12), 'Tmin', 7.0, True),
        (metadata, date(1930, 5, 13), 'Tmin', None, True),
        (metadata, date(1930, 5, 14), 'Tmin', 9.0, True),
    ]
    err_msgs, parsed_data = process.parse_and_check(filepath, parameters_filepath)
    assert not err_msgs
    for i, record in enumerate(parsed_data):
        assert record[1:] == expected_data[i][1:]
        expected_md = expected_data[i][0]
        expected_md['row'] = i + 5
        assert record[0] == expected_md
    # with some errors
    filepath = join(TEST_DATA_PATH, 'trentino', 'wrong3.csv')
    err_msgs, parsed_data = process.parse_and_check(filepath, parameters_filepath)
    metadata['source'] = 'trentino/wrong3.csv'
    assert err_msgs == [
        (5, 'the date format is wrong'),
        (6, 'the value for Tmin is not numeric'),
        (8, 'the row is not strictly after the previous'),
        (12, 'the row is duplicated with different values'),
        (13, 'the value for quality is missing'),
        (17, "The value of 'Tmin' is out of range [-40.0, 40.0]")]
    expected_data = [
        (metadata, date(1930, 5, 3), 'Tmin', 10.0, True),
        (metadata, date(1930, 5, 5), 'Tmin', 12.0, True),
        (metadata, date(1930, 5, 5), 'Tmin', 12.0, True),
        (metadata, date(1930, 5, 6), 'Tmin', 8.0, True),
        (metadata, date(1930, 5, 8), 'Tmin', 7.0, True),
        (metadata, date(1930, 5, 9), 'Tmin', 8.0, True),
        (metadata, date(1930, 5, 10), 'Tmin', 7.0, True),
        (metadata, date(1930, 5, 11), 'Tmin', 500.0, False),
        (metadata, date(1930, 5, 12), 'Tmin', 7.0, True),
        (metadata, date(1930, 5, 13), 'Tmin', None, True),
        (metadata, date(1930, 5, 14), 'Tmin', 9.0, True),
    ]
    rows_info = [7, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20]
    for i, record in enumerate(parsed_data):
        assert record[1:] == expected_data[i][1:]
        expected_md = expected_data[i][0]
        expected_md['row'] = rows_info[i]
        assert record[0] == expected_md

    # --- arpaer format ---
    filepath = join(TEST_DATA_PATH, 'arpaer', 'wrong_results1.json')
    parameters_filepath = join(TEST_DATA_PATH, 'arpaer', 'arpaer_params.csv')
    limiting_params = {'Tmedia': ('Tmin', 'Tmax')}
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [
        (2, 'information of the station is not parsable'),
        (3, 'information of the date is wrong')
    ]
    assert data_parsed == arpaer.parse(filepath, parameters_filepath)[0]

    # --- hiscentral format ---
    filepath = join(TEST_DATA_PATH, 'hiscentral', 'serie_wrong2-reg.abruzzoTmax.csv')
    parameters_filepath = join(TEST_DATA_PATH, 'hiscentral', 'hiscentral_params.csv')
    limiting_params = dict()
    err_msgs, data_parsed = process.parse_and_check(
        filepath, parameters_filepath, limiting_params)
    assert err_msgs == [
        (4, 'the reference time for the row is not parsable'),
        (8, 'the row is duplicated with different values'),
        (9, 'the row is not strictly after the previous'),
        (11, "the value '3A8' is not numeric")
    ]
    assert data_parsed == hiscentral.parse(filepath, parameters_filepath)[0]


def test_make_report(tmpdir):
    parameters_filepath = join(TEST_DATA_PATH, 'arpa19', 'arpa19_params.csv')
    # no errors
    in_filepath = join(TEST_DATA_PATH, 'arpa19', 'loc01_70001_201301010000_201401010100.dat')
    limiting_params = {'3': ('4', '5')}
    out_filepath = str(tmpdir.join('report.txt'))
    outdata_filepath = str(tmpdir.join('data.csv'))
    assert not exists(out_filepath)
    assert not exists(outdata_filepath)
    msgs, data_parsed = process.make_report(
        in_filepath, out_filepath, outdata_filepath, parameters_filepath=parameters_filepath,
        limiting_params=limiting_params)
    assert exists(out_filepath)
    assert exists(outdata_filepath)
    assert "No errors found" in msgs
    assert data_parsed == arpa19.parse(in_filepath, parameters_filepath)[0]

    # some formatting errors
    in_filepath = join(TEST_DATA_PATH, 'arpa19', 'wrong_70001_201301010000_201401010100.dat')
    limiting_params = {'3': ('4', '5')}
    out_filepath = str(tmpdir.join('report2.txt'))
    outdata_filepath = str(tmpdir.join('data2.csv'))
    assert not exists(out_filepath)
    assert not exists(outdata_filepath)
    msgs, data_parsed = process.make_report(
        in_filepath, out_filepath, outdata_filepath, parameters_filepath=parameters_filepath,
        limiting_params=limiting_params)
    assert exists(out_filepath)
    assert exists(outdata_filepath)
    err_msgs = [
        "Row 2: The spacing in the row is wrong",
        'Row 3: the latitude changes',
        'Row 5: it is not strictly after the previous',
        'Row 21: duplication of rows with different data',
        'Row 22: the time is not coherent with the filename',
    ]
    for err_msg in err_msgs:
        assert err_msg in msgs
    assert data_parsed == process.parse_and_check(
        in_filepath, parameters_filepath, limiting_params)[1]

    # some errors
    in_filepath = join(TEST_DATA_PATH, 'arpa19', 'wrong_70002_201301010000_201401010100.dat')
    limiting_params = {'Tmedia': ('FF', 'DD')}
    out_filepath = str(tmpdir.join('report3.txt'))
    outdata_filepath = str(tmpdir.join('data3.csv'))
    assert not exists(out_filepath)
    assert not exists(outdata_filepath)
    msgs, data_parsed = process.make_report(
        in_filepath, out_filepath, outdata_filepath, parameters_filepath=parameters_filepath,
        limiting_params=limiting_params)
    assert exists(out_filepath)
    assert exists(outdata_filepath)
    err_msgs = [
        "Row 1: The value of 'FF' is out of range [0.0, 102.0]",
        "Row 2: The value of 'DD' is out of range [0.0, 360.0]",
        "Row 3: The value of 'Tmedia' is out of range [-35.0, 45.0]",
        "Row 5: The values of 'Tmedia' and 'DD' are not consistent",
        "Row 6: The values of 'Tmedia' and 'DD' are not consistent",
        "Row 7: The values of 'Tmedia' and 'DD' are not consistent",
        "Row 20: The values of 'Tmedia' and 'DD' are not consistent"
    ]
    for err_msg in err_msgs:
        assert err_msg in msgs
    assert data_parsed == process.parse_and_check(
        in_filepath, parameters_filepath, limiting_params)[1]
