
from datetime import datetime

from sciafeed import checks


def test_data_internal_consistence_check():
    # right data
    metadata = {'cod_utente': '70001', 'lat': 43.876999, 'cod_rete': '15'}
    input_data = [
        [metadata, datetime(2013, 1, 1, 0, 0), '1', 9.0, True],
        [metadata, datetime(2013, 1, 1, 0, 0), '2', 355.0, True],
        [metadata, datetime(2013, 1, 1, 0, 0), '3', 68.0, True],
        [metadata, datetime(2013, 1, 1, 0, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '9', 83.0, True],
        [metadata, datetime(2013, 1, 1, 0, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '12', 10205.0, True],
        [metadata, datetime(2013, 1, 1, 0, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 0, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '1', 6.0, True],
        [metadata, datetime(2013, 1, 1, 1, 0), '2', 310.0, True],
        [metadata, datetime(2013, 1, 1, 1, 0), '3', 65.0, True],
        [metadata, datetime(2013, 1, 1, 1, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '9', 86.0, True],
        [metadata, datetime(2013, 1, 1, 1, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '12', 10198.0, True],
        [metadata, datetime(2013, 1, 1, 1, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 1, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '1', 3.0, True],
        [metadata, datetime(2013, 1, 1, 2, 0), '2', 288.0, True],
        [metadata, datetime(2013, 1, 1, 2, 0), '3', 63.0, True],
        [metadata, datetime(2013, 1, 1, 2, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '9', 86.0, True],
        [metadata, datetime(2013, 1, 1, 2, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '12', 10196.0, True],
        [metadata, datetime(2013, 1, 1, 2, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 2, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '1', 11.0, True],
        [metadata, datetime(2013, 1, 1, 3, 0), '2', 357.0, True],
        [metadata, datetime(2013, 1, 1, 3, 0), '3', 63.0, True],
        [metadata, datetime(2013, 1, 1, 3, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '9', 87.0, True],
        [metadata, datetime(2013, 1, 1, 3, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '12', 10189.0, True],
        [metadata, datetime(2013, 1, 1, 3, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 3, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '1', 9.0, True],
        [metadata, datetime(2013, 1, 1, 4, 0), '2', 1.0, True],
        [metadata, datetime(2013, 1, 1, 4, 0), '3', 64.0, True],
        [metadata, datetime(2013, 1, 1, 4, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '9', 88.0, True],
        [metadata, datetime(2013, 1, 1, 4, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '12', 10184.0, True],
        [metadata, datetime(2013, 1, 1, 4, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 4, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '1', 30.0, True],
        [metadata, datetime(2013, 1, 1, 5, 0), '2', 6.0, True],
        [metadata, datetime(2013, 1, 1, 5, 0), '3', 67.0, True],
        [metadata, datetime(2013, 1, 1, 5, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '9', 89.0, True],
        [metadata, datetime(2013, 1, 1, 5, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '12', 10181.0, True],
        [metadata, datetime(2013, 1, 1, 5, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 5, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '1', 31.0, True],
        [metadata, datetime(2013, 1, 1, 6, 0), '2', 6.0, True],
        [metadata, datetime(2013, 1, 1, 6, 0), '3', 65.0, True],
        [metadata, datetime(2013, 1, 1, 6, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '9', 93.0, True],
        [metadata, datetime(2013, 1, 1, 6, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '12', 10181.0, True],
        [metadata, datetime(2013, 1, 1, 6, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 6, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '1', 20.0, True],
        [metadata, datetime(2013, 1, 1, 7, 0), '2', 358.0, True],
        [metadata, datetime(2013, 1, 1, 7, 0), '3', 65.0, True],
        [metadata, datetime(2013, 1, 1, 7, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '9', 93.0, True],
        [metadata, datetime(2013, 1, 1, 7, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '12', 10182.0, True],
        [metadata, datetime(2013, 1, 1, 7, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 7, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '1', 5.0, True],
        [metadata, datetime(2013, 1, 1, 8, 0), '2', 342.0, True],
        [metadata, datetime(2013, 1, 1, 8, 0), '3', 66.0, True],
        [metadata, datetime(2013, 1, 1, 8, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '9', 95.0, True],
        [metadata, datetime(2013, 1, 1, 8, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '12', 10182.0, True],
        [metadata, datetime(2013, 1, 1, 8, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 8, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '1', 35.0, True],
        [metadata, datetime(2013, 1, 1, 9, 0), '2', 12.0, True],
        [metadata, datetime(2013, 1, 1, 9, 0), '3', 106.0, True],
        [metadata, datetime(2013, 1, 1, 9, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '9', 88.0, True],
        [metadata, datetime(2013, 1, 1, 9, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '12', 10179.0, True],
        [metadata, datetime(2013, 1, 1, 9, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 9, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '1', 13.0, True],
        [metadata, datetime(2013, 1, 1, 10, 0), '2', 154.0, True],
        [metadata, datetime(2013, 1, 1, 10, 0), '3', 121.0, True],
        [metadata, datetime(2013, 1, 1, 10, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '9', 72.0, True],
        [metadata, datetime(2013, 1, 1, 10, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '12', 10182.0, True],
        [metadata, datetime(2013, 1, 1, 10, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 10, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '1', 54.0, True],
        [metadata, datetime(2013, 1, 1, 11, 0), '2', 218.0, True],
        [metadata, datetime(2013, 1, 1, 11, 0), '3', 123.0, True],
        [metadata, datetime(2013, 1, 1, 11, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '9', 69.0, True],
        [metadata, datetime(2013, 1, 1, 11, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '12', 10177.0, True],
        [metadata, datetime(2013, 1, 1, 11, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 11, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '1', 61.0, True],
        [metadata, datetime(2013, 1, 1, 12, 0), '2', 225.0, True],
        [metadata, datetime(2013, 1, 1, 12, 0), '3', 125.0, True],
        [metadata, datetime(2013, 1, 1, 12, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '9', 73.0, True],
        [metadata, datetime(2013, 1, 1, 12, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '12', 10167.0, True],
        [metadata, datetime(2013, 1, 1, 12, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 12, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '1', 65.0, True],
        [metadata, datetime(2013, 1, 1, 13, 0), '2', 226.0, True],
        [metadata, datetime(2013, 1, 1, 13, 0), '3', 122.0, True],
        [metadata, datetime(2013, 1, 1, 13, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '9', 74.0, True],
        [metadata, datetime(2013, 1, 1, 13, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '12', 10162.0, True],
        [metadata, datetime(2013, 1, 1, 13, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 13, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '1', 46.0, True],
        [metadata, datetime(2013, 1, 1, 14, 0), '2', 221.0, True],
        [metadata, datetime(2013, 1, 1, 14, 0), '3', 117.0, True],
        [metadata, datetime(2013, 1, 1, 14, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '9', 78.0, True],
        [metadata, datetime(2013, 1, 1, 14, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '12', 10161.0, True],
        [metadata, datetime(2013, 1, 1, 14, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 14, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '1', 19.0, True],
        [metadata, datetime(2013, 1, 1, 15, 0), '2', 233.0, True],
        [metadata, datetime(2013, 1, 1, 15, 0), '3', 110.0, True],
        [metadata, datetime(2013, 1, 1, 15, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '9', 82.0, True],
        [metadata, datetime(2013, 1, 1, 15, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '12', 10161.0, True],
        [metadata, datetime(2013, 1, 1, 15, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 15, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '1', 28.0, True],
        [metadata, datetime(2013, 1, 1, 16, 0), '2', 355.0, True],
        [metadata, datetime(2013, 1, 1, 16, 0), '3', 100.0, True],
        [metadata, datetime(2013, 1, 1, 16, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '9', 96.0, True],
        [metadata, datetime(2013, 1, 1, 16, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '12', 10158.0, True],
        [metadata, datetime(2013, 1, 1, 16, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 16, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '1', 24.0, True],
        [metadata, datetime(2013, 1, 1, 17, 0), '2', 345.0, True],
        [metadata, datetime(2013, 1, 1, 17, 0), '3', 99.0, True],
        [metadata, datetime(2013, 1, 1, 17, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '9', 96.0, True],
        [metadata, datetime(2013, 1, 1, 17, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '12', 10156.0, True],
        [metadata, datetime(2013, 1, 1, 17, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 17, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '1', 26.0, True],
        [metadata, datetime(2013, 1, 1, 18, 0), '2', 357.0, True],
        [metadata, datetime(2013, 1, 1, 18, 0), '3', 101.0, True],
        [metadata, datetime(2013, 1, 1, 18, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '9', 97.0, True],
        [metadata, datetime(2013, 1, 1, 18, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '12', 10155.0, True],
        [metadata, datetime(2013, 1, 1, 18, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 18, 0), '19', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '1', 26.0, True],
        [metadata, datetime(2013, 1, 1, 19, 0), '2', 2.0, True],
        [metadata, datetime(2013, 1, 1, 19, 0), '3', 99.0, True],
        [metadata, datetime(2013, 1, 1, 19, 0), '4', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '5', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '6', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '7', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '8', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '9', 100.0, True],
        [metadata, datetime(2013, 1, 1, 19, 0), '10', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '11', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '12', 10154.0, True],
        [metadata, datetime(2013, 1, 1, 19, 0), '13', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '14', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '15', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '16', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '17', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '18', None, False],
        [metadata, datetime(2013, 1, 1, 19, 0), '19', None, False]
    ]
    limiting_params = {'3': ('4', '5')}
    err_msgs, out_data = checks.data_internal_consistence_check(input_data, limiting_params)
    assert not err_msgs
    assert input_data == out_data

    # with errors
    limiting_params = {'3': ('1', '2')}
    err_msgs, out_data = checks.data_internal_consistence_check(input_data, limiting_params)
    assert err_msgs == [
        "The values of '3' and '2' are not consistent",
        "The values of '3' and '2' are not consistent",
        "The values of '3' and '2' are not consistent",
        "The values of '3' and '2' are not consistent",
        "The values of '3' and '2' are not consistent"
    ]

    assert out_data[78] == [
        metadata, datetime(2013, 1, 1, 4, 0), '3', 64.0, False]
    out_data[78][-1] = True
    assert out_data[97] == [
        metadata, datetime(2013, 1, 1, 5, 0), '3', 67.0, False]
    out_data[97][-1] = True
    assert out_data[116] == [
        metadata, datetime(2013, 1, 1, 6, 0), '3', 65.0, False]
    out_data[116][-1] = True
    assert out_data[173] == [
        metadata, datetime(2013, 1, 1, 9, 0), '3', 106.0, False]
    out_data[173][-1] = True
    assert out_data[363] == [
        metadata, datetime(2013, 1, 1, 19, 0), '3', 99.0, False]
    out_data[363][-1] = True
    assert out_data == input_data

    # no limiting parameters: no check
    err_msgs, out_data = checks.data_internal_consistence_check(input_data)
    assert not err_msgs
    assert out_data == input_data


def test_data_weak_climatologic_check():
    parameters_thresholds = {
        '1': [0.0, 1020.0],
        '10': [20.0, 100.0],
        '11': [20.0, 100.0],
        '13': [9600.0, 10600.0],
        '16': [0.0, 100.0],
        '17': [0.0, 60.0],
        '18': [0.0, 9890.0],
        '19': [0.0, 60.0],
        '2': [0.0, 360.0],
        '3': [-350.0, 450.0],
        '4': [-400.0, 400.0],
        '5': [-300.0, 500.0],
        '9': [20.0, 100.0]
    }

    # right data
    input_data = [
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '1', 20.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '2', 358.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '3', 65.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '4', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '5', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '6', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '7', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '8', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '9', 93.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '10', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '11', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '12', 10182.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '13', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '14', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '15', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '16', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '17', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '18', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '19', None, False]
    ]
    err_msgs, out_data = checks.data_weak_climatologic_check(input_data, parameters_thresholds)
    assert not err_msgs
    assert out_data == input_data

    # two errors
    assert parameters_thresholds['1'] == [0, 1020]
    assert parameters_thresholds['9'] == [20, 100]
    input_data = [
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '1', 1021.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '2', 358.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '3', 65.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '4', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '5', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '6', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '7', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '8', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '9', 101.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '10', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '11', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '12', 10182.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '13', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '14', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '15', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '16', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '17', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '18', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '19', None, False]
    ]
    err_msgs, out_data = checks.data_weak_climatologic_check(
        input_data, parameters_thresholds)
    assert err_msgs == ["The value of '1' is out of range [0.0, 1020.0]",
                        "The value of '9' is out of range [20.0, 100.0]"]
    assert out_data[0] == [
        {'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '1', 1021.0, False]
    assert out_data[8] == [
        {'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '9', 101.0, False]
    out_data[0][-1] = True
    out_data[8][-1] = True
    assert out_data == input_data

    # no check if no parameters_thresholds
    err_msgs, out_data = checks.data_weak_climatologic_check(input_data)
    assert not err_msgs
    assert out_data == input_data

    # no check if the value is already invalid
    input_data = [
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '1', 1021.0, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '2', 358.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '3', 65.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '4', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '5', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '6', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '7', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '8', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '9', 93.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '10', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '11', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '12', 10182.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '13', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '14', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '15', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '16', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '17', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '18', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '19', None, False]
    ]
    err_msgs, out_data = checks.data_weak_climatologic_check(input_data, parameters_thresholds)
    assert not err_msgs
    assert out_data == out_data

    # no check if thresholds are not defined
    assert '12' not in parameters_thresholds
    input_data = [
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '1', 1021.0, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '2', 358.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '3', 65.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '4', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '5', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '6', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '7', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '8', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '9', 93.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '10', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '11', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '12', 99999.0, True],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '13', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '14', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '15', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '16', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '17', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '18', None, False],
        [{'lat': 43.876999}, datetime(2013, 1, 1, 7, 0), '19', None, False]
    ]
    err_msgs, out_data = checks.data_weak_climatologic_check(input_data, parameters_thresholds)
    assert not err_msgs
    assert out_data == input_data
