"""
This module contains functions and utilities that compute when seasons starts/ends
"""
from datetime import date, datetime

SOLSTICE_MONTH_DEFAULT = 6
SOLSTICE_DAY_DEFAULT = 21
MIN_YEAR = 1600
MAX_YEAR = 2149

# solstice_days = dict(
#     [(year,ephem.next_solstice(str(year)).datetime().date().day)
#      for year in range(MIN_YEAR, MAX_YEAR+1)
#      if ephem.next_solstice(str(year)).datetime().date().day!=21]
# )
# equinox_days = dict(
#     [(year,ephem.next_equinox(str(year)).datetime().date().day)
#      for year in range(MIN_YEAR, MAX_YEAR+1)
#      if ephem.next_equinox(str(year)).datetime().date().day!=20]
# )
equinox1_days = {
    1603: 21, 1607: 21, 1611: 21, 1615: 21, 1652: 19, 1656: 19, 1660: 19, 1664: 19, 1668: 19,
    1672: 19, 1676: 19, 1680: 19, 1684: 19, 1685: 19, 1688: 19, 1689: 19, 1692: 19, 1693: 19,
    1696: 19, 1697: 19, 1702: 21, 1703: 21, 1706: 21, 1707: 21, 1710: 21, 1711: 21, 1715: 21,
    1719: 21, 1723: 21, 1727: 21, 1731: 21, 1735: 21, 1739: 21, 1743: 21, 1780: 19, 1784: 19,
    1788: 19, 1792: 19, 1796: 19, 1801: 21, 1802: 21, 1803: 21, 1805: 21, 1806: 21, 1807: 21,
    1809: 21, 1810: 21, 1811: 21, 1814: 21, 1815: 21, 1818: 21, 1819: 21, 1822: 21, 1823: 21,
    1826: 21, 1827: 21, 1830: 21, 1831: 21, 1834: 21, 1835: 21, 1838: 21, 1839: 21, 1842: 21,
    1843: 21, 1847: 21, 1851: 21, 1855: 21, 1859: 21, 1863: 21, 1867: 21, 1871: 21, 1875: 21,
    1900: 21, 1901: 21, 1902: 21, 1903: 21, 1904: 21, 1905: 21, 1906: 21, 1907: 21, 1908: 21,
    1909: 21, 1910: 21, 1911: 21, 1913: 21, 1914: 21, 1915: 21, 1917: 21, 1918: 21, 1919: 21,
    1921: 21, 1922: 21, 1923: 21, 1925: 21, 1926: 21, 1927: 21, 1929: 21, 1930: 21, 1931: 21,
    1933: 21, 1934: 21, 1935: 21, 1937: 21, 1938: 21, 1939: 21, 1941: 21, 1942: 21, 1943: 21,
    1946: 21, 1947: 21, 1950: 21, 1951: 21, 1954: 21, 1955: 21, 1958: 21, 1959: 21, 1962: 21,
    1963: 21, 1966: 21, 1967: 21, 1970: 21, 1971: 21, 1974: 21, 1975: 21, 1979: 21, 1983: 21,
    1987: 21, 1991: 21, 1995: 21, 1999: 21, 2003: 21, 2007: 21, 2044: 19, 2048: 19, 2052: 19,
    2056: 19, 2060: 19, 2064: 19, 2068: 19, 2072: 19, 2076: 19, 2077: 19, 2080: 19, 2081: 19,
    2084: 19, 2085: 19, 2088: 19, 2089: 19, 2092: 19, 2093: 19, 2096: 19, 2097: 19, 2102: 21,
    2103: 21, 2106: 21, 2107: 21, 2111: 21, 2115: 21, 2119: 21, 2123: 21, 2127: 21, 2131: 21,
    2135: 21
}
solstice1_days = {  # day of June
    1603: 22, 1607: 22, 1611: 22, 1615: 22, 1652: 20, 1656: 20, 1660: 20, 1664: 20, 1668: 20,
    1672: 20, 1676: 20, 1680: 20, 1681: 20, 1684: 20, 1685: 20, 1688: 20, 1689: 20, 1692: 20,
    1693: 20, 1696: 20, 1697: 20, 1702: 22, 1703: 22, 1706: 22, 1707: 22, 1711: 22, 1715: 22,
    1719: 22, 1723: 22, 1727: 22, 1731: 22, 1735: 22, 1739: 22, 1772: 20, 1776: 20, 1780: 20,
    1784: 20, 1788: 20, 1792: 20, 1796: 20, 1802: 22, 1803: 22, 1806: 22, 1807: 22, 1810: 22,
    1811: 22, 1814: 22, 1815: 22, 1818: 22, 1819: 22, 1822: 22, 1823: 22, 1826: 22, 1827: 22,
    1831: 22, 1835: 22, 1839: 22, 1843: 22, 1847: 22, 1851: 22, 1855: 22, 1892: 20, 1896: 20,
    1901: 22, 1902: 22, 1903: 22, 1905: 22, 1906: 22, 1907: 22, 1909: 22, 1910: 22, 1911: 22,
    1913: 22, 1914: 22, 1915: 22, 1917: 22, 1918: 22, 1919: 22, 1922: 22, 1923: 22, 1926: 22,
    1927: 22, 1930: 22, 1931: 22, 1934: 22, 1935: 22, 1938: 22, 1939: 22, 1942: 22, 1943: 22,
    1946: 22, 1947: 22, 1951: 22, 1955: 22, 1959: 22, 1963: 22, 1967: 22, 1971: 22, 1975: 22,
    2008: 20, 2012: 20, 2016: 20, 2020: 20, 2024: 20, 2028: 20, 2032: 20, 2036: 20, 2040: 20,
    2041: 20, 2044: 20, 2045: 20, 2048: 20, 2049: 20, 2052: 20, 2053: 20, 2056: 20, 2057: 20,
    2060: 20, 2061: 20, 2064: 20, 2065: 20, 2068: 20, 2069: 20, 2070: 20, 2072: 20, 2073: 20,
    2074: 20, 2076: 20, 2077: 20, 2078: 20, 2080: 20, 2081: 20, 2082: 20, 2084: 20, 2085: 20,
    2086: 20, 2088: 20, 2089: 20, 2090: 20, 2092: 20, 2093: 20, 2094: 20, 2096: 20, 2097: 20,
    2098: 20, 2099: 20, 2128: 20, 2132: 20, 2136: 20, 2140: 20, 2144: 20, 2148: 20
}
solstice2_days = {
    1603: 22, 1607: 22, 1611: 22, 1615: 22, 1619: 22, 1623: 22, 1627: 22, 1664: 20, 1668: 20,
    1672: 20, 1676: 20, 1680: 20, 1684: 20, 1688: 20, 1692: 20, 1696: 20, 1697: 20, 1702: 22,
    1703: 22, 1706: 22, 1707: 22, 1710: 22, 1711: 22, 1714: 22, 1715: 22, 1718: 22, 1719: 22,
    1722: 22, 1723: 22, 1726: 22, 1727: 22, 1730: 22, 1731: 22, 1735: 22, 1739: 22, 1743: 22,
    1747: 22, 1751: 22, 1755: 22, 1759: 22, 1763: 22, 1800: 22, 1801: 22, 1802: 22, 1803: 22,
    1805: 22, 1806: 22, 1807: 22, 1809: 22, 1810: 22, 1811: 22, 1813: 22, 1814: 22, 1815: 22,
    1817: 22, 1818: 22, 1819: 22, 1821: 22, 1822: 22, 1823: 22, 1825: 22, 1826: 22, 1827: 22,
    1829: 22, 1830: 22, 1831: 22, 1833: 22, 1834: 22, 1835: 22, 1838: 22, 1839: 22, 1842: 22,
    1843: 22, 1846: 22, 1847: 22, 1850: 22, 1851: 22, 1854: 22, 1855: 22, 1858: 22, 1859: 22,
    1862: 22, 1863: 22, 1866: 22, 1867: 22, 1870: 22, 1871: 22, 1875: 22, 1879: 22, 1883: 22,
    1887: 22, 1891: 22, 1895: 22, 1899: 22, 1900: 22, 1901: 22, 1902: 22, 1903: 23, 1904: 22,
    1905: 22, 1906: 22, 1907: 22, 1908: 22, 1909: 22, 1910: 22, 1911: 22, 1912: 22, 1913: 22,
    1914: 22, 1915: 22, 1916: 22, 1917: 22, 1918: 22, 1919: 22, 1920: 22, 1921: 22, 1922: 22,
    1923: 22, 1924: 22, 1925: 22, 1926: 22, 1927: 22, 1928: 22, 1929: 22, 1930: 22, 1931: 22,
    1932: 22, 1933: 22, 1934: 22, 1935: 22, 1936: 22, 1937: 22, 1938: 22, 1939: 22, 1941: 22,
    1942: 22, 1943: 22, 1945: 22, 1946: 22, 1947: 22, 1949: 22, 1950: 22, 1951: 22, 1953: 22,
    1954: 22, 1955: 22, 1957: 22, 1958: 22, 1959: 22, 1961: 22, 1962: 22, 1963: 22, 1965: 22,
    1966: 22, 1967: 22, 1969: 22, 1970: 22, 1971: 22, 1973: 22, 1974: 22, 1975: 22, 1978: 22,
    1979: 22, 1982: 22, 1983: 22, 1986: 22, 1987: 22, 1990: 22, 1991: 22, 1994: 22, 1995: 22,
    1998: 22, 1999: 22, 2002: 22, 2003: 22, 2006: 22, 2007: 22, 2011: 22, 2015: 22, 2019: 22,
    2023: 22, 2027: 22, 2031: 22, 2035: 22, 2039: 22, 2043: 22, 2080: 20, 2084: 20, 2088: 20,
    2092: 20, 2096: 20, 2101: 22, 2102: 22, 2103: 22, 2105: 22, 2106: 22, 2107: 22, 2109: 22,
    2110: 22, 2111: 22, 2114: 22, 2115: 22, 2118: 22, 2119: 22, 2122: 22, 2123: 22, 2126: 22,
    2127: 22, 2130: 22, 2131: 22, 2134: 22, 2135: 22, 2138: 22, 2139: 22, 2142: 22, 2143: 22,
    2147: 22
}
equinox2_days = {
    1600: 22, 1604: 22, 1608: 22, 1612: 22, 1616: 22, 1620: 22, 1621: 22, 1624: 22, 1625: 22,
    1628: 22, 1629: 22, 1632: 22, 1633: 22, 1636: 22, 1637: 22, 1640: 22, 1641: 22, 1644: 22,
    1645: 22, 1648: 22, 1649: 22, 1652: 22, 1653: 22, 1654: 22, 1656: 22, 1657: 22, 1658: 22,
    1660: 22, 1661: 22, 1662: 22, 1664: 22, 1665: 22, 1666: 22, 1668: 22, 1669: 22, 1670: 22,
    1672: 22, 1673: 22, 1674: 22, 1676: 22, 1677: 22, 1678: 22, 1680: 22, 1681: 22, 1682: 22,
    1683: 22, 1684: 22, 1685: 22, 1686: 22, 1687: 22, 1688: 22, 1689: 22, 1690: 22, 1691: 22,
    1692: 22, 1693: 22, 1694: 22, 1695: 22, 1696: 22, 1697: 22, 1698: 22, 1699: 22, 1716: 22,
    1720: 22, 1724: 22, 1728: 22, 1732: 22, 1736: 22, 1740: 22, 1744: 22, 1745: 22, 1748: 22,
    1749: 22, 1752: 22, 1753: 22, 1756: 22, 1757: 22, 1760: 22, 1761: 22, 1764: 22, 1765: 22,
    1768: 22, 1769: 22, 1772: 22, 1773: 22, 1776: 22, 1777: 22, 1778: 22, 1780: 22, 1781: 22,
    1782: 22, 1784: 22, 1785: 22, 1786: 22, 1788: 22, 1789: 22, 1790: 22, 1792: 22, 1793: 22,
    1794: 22, 1796: 22, 1797: 22, 1798: 22, 1803: 24, 1807: 24, 1840: 22, 1844: 22, 1848: 22,
    1852: 22, 1856: 22, 1860: 22, 1864: 22, 1868: 22, 1872: 22, 1873: 22, 1876: 22, 1877: 22,
    1880: 22, 1881: 22, 1884: 22, 1885: 22, 1888: 22, 1889: 22, 1892: 22, 1893: 22, 1896: 22,
    1897: 22, 1903: 24, 1907: 24, 1911: 24, 1915: 24, 1919: 24, 1923: 24, 1927: 24, 1931: 24,
    1968: 22, 1972: 22, 1976: 22, 1980: 22, 1984: 22, 1988: 22, 1992: 22, 1996: 22, 1997: 22,
    2000: 22, 2001: 22, 2004: 22, 2005: 22, 2008: 22, 2009: 22, 2012: 22, 2013: 22, 2016: 22,
    2017: 22, 2020: 22, 2021: 22, 2024: 22, 2025: 22, 2028: 22, 2029: 22, 2030: 22, 2032: 22,
    2033: 22, 2034: 22, 2036: 22, 2037: 22, 2038: 22, 2040: 22, 2041: 22, 2042: 22, 2044: 22,
    2045: 22, 2046: 22, 2048: 22, 2049: 22, 2050: 22, 2052: 22, 2053: 22, 2054: 22, 2056: 22,
    2057: 22, 2058: 22, 2060: 22, 2061: 22, 2062: 22, 2063: 22, 2064: 22, 2065: 22, 2066: 22,
    2067: 22, 2068: 22, 2069: 22, 2070: 22, 2071: 22, 2072: 22, 2073: 22, 2074: 22, 2075: 22,
    2076: 22, 2077: 22, 2078: 22, 2079: 22, 2080: 22, 2081: 22, 2082: 22, 2083: 22, 2084: 22,
    2085: 22, 2086: 22, 2087: 22, 2088: 22, 2089: 22, 2090: 22, 2091: 22, 2092: 21, 2093: 22,
    2094: 22, 2095: 22, 2096: 21, 2097: 22, 2098: 22, 2099: 22, 2100: 22, 2104: 22, 2108: 22,
    2112: 22, 2116: 22, 2120: 22, 2121: 22, 2124: 22, 2125: 22, 2128: 22, 2129: 22, 2132: 22,
    2133: 22, 2136: 22, 2137: 22, 2140: 22, 2141: 22, 2144: 22, 2145: 22, 2148: 22, 2149: 22
}


def get_solstice(year, of_june=True):
    """
    Compute the date of the june solstice for the input `year`

    :param year: year
    :param of_june: if False, compute the winter solstice
    :return: the datetime of the solstice
    """
    if year > MAX_YEAR or year < MIN_YEAR:
        raise ValueError('cannot compute solstice for %r: year out of range')
    if of_june:
        month = 6
        day = solstice1_days.get(year, 21)
    else:
        month = 12
        day = solstice2_days.get(year, 21)
    ret_value = date(year, month, day)
    return ret_value


def get_equinox(year, of_september=True):
    """
    Compute the date of the autumn equinox for the input `year`

    :param year: year
    :param of_september: if False, compute the spring solstice
    :return: the datetime of the equinox
    """
    if year > MAX_YEAR or year < MIN_YEAR:
        raise ValueError('cannot compute equinox for %r: year out of range')
    if of_september:
        month = 9
        day = equinox2_days.get(year, 23)
    else:
        month = 3
        day = equinox1_days.get(year, 20)
    ret_value = date(year, month, day)
    return ret_value


def is_day_in_summer(day):
    """
    Return if the input datetime `day` is in summer season or not.

    :param day: input datetime object
    :return: True or False
    """
    if isinstance(day, datetime):
        day = day.date()
    year = day.year
    start_summer = get_solstice(year)
    end_summer = get_equinox(year)
    return start_summer <= day <= end_summer


def is_day_in_winter(day):
    """
    Return if the input datetime `day` is in winter season or not.

    :param day: input datetime object
    :return: True or False
    """
    if isinstance(day, datetime):
        day = day.date()
    year = day.year
    start_winter = get_solstice(year, of_june=False)
    end_winter = get_equinox(year, of_september=False)
    return day <= end_winter or day >= start_winter
