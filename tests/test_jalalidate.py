import os
import pickle
from datetime import date, timedelta
from time import struct_time, time
from unittest import TestCase

import pytest

from persiantools.jdatetime import JalaliDate


class TestJalaliDate(TestCase):
    def test_shamsi_to_gregorian(self):
        self.assertEqual(JalaliDate(1367, 2, 14).to_gregorian(), date(1988, 5, 4))
        self.assertEqual(JalaliDate(1395, 3, 21).to_gregorian(), date(2016, 6, 10))
        self.assertEqual(JalaliDate(1395, 12, 9).to_gregorian(), date(2017, 2, 27))
        self.assertEqual(JalaliDate(1395, 12, 30).to_gregorian(), date(2017, 3, 20))
        self.assertEqual(JalaliDate(1396, 1, 1).to_gregorian(), date(2017, 3, 21))
        self.assertEqual(JalaliDate(1400, 6, 31).to_gregorian(), date(2021, 9, 22))
        self.assertEqual(JalaliDate(1396, 7, 27).to_gregorian(), date(2017, 10, 19))
        self.assertEqual(JalaliDate(1397, 11, 29).to_gregorian(), date(2019, 2, 18))
        self.assertEqual(JalaliDate(1399, 11, 23).to_gregorian(), date(2021, 2, 11))
        self.assertEqual(JalaliDate(1400, 4, 25).to_gregorian(), date(2021, 7, 16))
        self.assertEqual(JalaliDate(1400, 12, 20).to_gregorian(), date(2022, 3, 11))
        self.assertEqual(JalaliDate(1403, 1, 5).to_gregorian(), date(2024, 3, 24))
        self.assertEqual(JalaliDate(1390, 10, 11).to_gregorian(), date(2012, 1, 1))
        self.assertEqual(JalaliDate(1398, 10, 11).to_gregorian(), date(2020, 1, 1))
        self.assertEqual(JalaliDate(1402, 10, 11).to_gregorian(), date(2024, 1, 1))
        self.assertEqual(JalaliDate(1402, 10, 10).to_gregorian(), date(2023, 12, 31))
        self.assertEqual(JalaliDate(1403, 10, 11).to_gregorian(), date(2024, 12, 31))
        self.assertEqual(JalaliDate(1403, 2, 23).to_gregorian(), date(2024, 5, 12))

        self.assertEqual(JalaliDate.today().to_gregorian(), date.today())

    def test_gregorian_to_shamsi(self):
        self.assertEqual(JalaliDate(date(1988, 5, 4)), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate(date(2122, 1, 31)), JalaliDate(1500, 11, 11))
        self.assertEqual(JalaliDate(date(2017, 3, 20)), JalaliDate(1395, 12, 30))
        self.assertEqual(JalaliDate(date(2000, 1, 1)), JalaliDate(1378, 10, 11))
        self.assertEqual(JalaliDate(date(2017, 10, 19)), JalaliDate(1396, 7, 27))
        self.assertEqual(JalaliDate(date(2019, 2, 18)), JalaliDate(1397, 11, 29))
        self.assertEqual(JalaliDate.to_jalali(1990, 9, 23), JalaliDate(1369, 7, 1))
        self.assertEqual(JalaliDate.to_jalali(1990, 9, 23), JalaliDate(1369, 7, 1))
        self.assertEqual(JalaliDate.to_jalali(2013, 9, 16), JalaliDate(1392, 6, 25))
        self.assertEqual(JalaliDate.to_jalali(2018, 3, 20), JalaliDate(1396, 12, 29))
        self.assertEqual(JalaliDate.to_jalali(2021, 2, 11), JalaliDate(1399, 11, 23))
        self.assertEqual(JalaliDate.to_jalali(2021, 7, 16), JalaliDate(1400, 4, 25))
        self.assertEqual(JalaliDate.to_jalali(2024, 3, 24), JalaliDate(1403, 1, 5))
        self.assertEqual(JalaliDate.to_jalali(2012, 1, 1), JalaliDate(1390, 10, 11))
        self.assertEqual(JalaliDate.to_jalali(2020, 1, 1), JalaliDate(1398, 10, 11))
        self.assertEqual(JalaliDate.to_jalali(2024, 1, 1), JalaliDate(1402, 10, 11))
        self.assertEqual(JalaliDate.to_jalali(2024, 1, 1), JalaliDate(1402, 10, 11))
        self.assertEqual(JalaliDate.to_jalali(2023, 12, 31), JalaliDate(1402, 10, 10))
        self.assertEqual(JalaliDate.to_jalali(2024, 12, 31), JalaliDate(1403, 10, 11))
        self.assertEqual(JalaliDate.to_jalali(2024, 5, 12), JalaliDate(1403, 2, 23))

        self.assertEqual(JalaliDate(date.today()), JalaliDate.today())

    def test_checkdate(self):
        self.assertEqual(JalaliDate.check_date(1367, 2, 14), True)
        self.assertEqual(JalaliDate.check_date(1395, 12, 30), True)
        self.assertEqual(JalaliDate.check_date(1394, 12, 30), False)
        self.assertEqual(JalaliDate.check_date(13, 13, 30), False)
        self.assertEqual(JalaliDate.check_date(0, 0, 0), False)
        self.assertEqual(JalaliDate.check_date(9378, 0, 0), False)
        self.assertEqual(JalaliDate.check_date("1300", "1", "1"), False)
        self.assertEqual(JalaliDate.check_date(1396, 12, 30), False)
        self.assertEqual(JalaliDate.check_date(1397, 7, 1), True)
        self.assertEqual(JalaliDate.check_date(1396, 7, 27), True)
        self.assertEqual(JalaliDate.check_date(1397, 11, 29), True)
        self.assertEqual(JalaliDate.check_date(1399, 11, 31), False)
        self.assertEqual(JalaliDate.check_date(1400, 4, 25), True)
        self.assertEqual(JalaliDate.check_date(1400, 12, 30), False)
        self.assertEqual(JalaliDate.check_date(1403, 12, 30), True)

    def test_completeday(self):
        jdate = JalaliDate(1398, 3, 17)
        self.assertEqual(jdate.year, 1398)
        self.assertEqual(jdate.month, 3)
        self.assertEqual(jdate.day, 17)
        self.assertEqual(jdate.locale, "en")
        self.assertEqual(jdate.to_gregorian(), date(2019, 6, 7))
        self.assertEqual(jdate.isoformat(), "1398-03-17")
        self.assertEqual(jdate.weekday(), 6)
        self.assertEqual(jdate.isoweekday(), 7)
        self.assertEqual(jdate.week_of_year(), 12)
        self.assertEqual(jdate.isocalendar(), (1398, 12, 7))
        self.assertEqual(jdate.ctime(), "Jomeh 17 Khordad 1398")
        self.assertEqual(jdate - JalaliDate(1398, 1, 1), timedelta(days=78))
        self.assertEqual(jdate > JalaliDate(1398, 3, 16), True)
        self.assertEqual(JalaliDate(1398, 3, 16) + timedelta(days=1), jdate)
        self.assertEqual(jdate.timetuple(), struct_time((2019, 6, 7, 0, 0, 0, 4, 158, -1)))

        jdate = JalaliDate(1399, 11, 23)
        self.assertEqual(jdate.to_gregorian(), date(2021, 2, 11))
        self.assertEqual(jdate.isoformat(), "1399-11-23")
        self.assertEqual(jdate.weekday(), 5)
        self.assertEqual(jdate.week_of_year(), 48)

    def test_timetuple(self):
        self.assertEqual(
            JalaliDate(1398, 3, 17).timetuple(),
            struct_time((2019, 6, 7, 0, 0, 0, 4, 158, -1)),
        )
        self.assertEqual(
            JalaliDate(1367, 2, 14).timetuple(),
            struct_time((1988, 5, 4, 0, 0, 0, 2, 125, -1)),
        )

    def test_isocalendar(self):
        self.assertEqual(JalaliDate(1364, 1, 31).isocalendar(), (1364, 6, 1))
        self.assertEqual(JalaliDate(1398, 3, 17).isocalendar(), (1398, 12, 7))
        self.assertEqual(JalaliDate(1398, 1, 1).isocalendar(), (1398, 1, 6))
        self.assertEqual(JalaliDate(1399, 1, 2).isocalendar(), (1399, 2, 1))
        self.assertEqual(JalaliDate(1403, 1, 5).isocalendar(), (1403, 2, 2))

    def test_additions(self):
        self.assertEqual(JalaliDate(JalaliDate(1395, 3, 21)), JalaliDate(1395, 3, 21))

        self.assertEqual(JalaliDate.days_before_month(1), 0)
        self.assertEqual(JalaliDate.days_before_month(12), 336)

        self.assertEqual(JalaliDate(1395, 1, 1).replace(1367), JalaliDate(1367, 1, 1))
        self.assertEqual(JalaliDate(1395, 1, 1).replace(month=2), JalaliDate(1395, 2, 1))
        self.assertEqual(JalaliDate(1367, 1, 1).replace(year=1396, month=7), JalaliDate(1396, 7, 1))
        self.assertEqual(
            JalaliDate(1395, 1, 1, "en").replace(1367, 2, 14, "fa"),
            JalaliDate(1367, 2, 14, "en"),
        )

        self.assertEqual(JalaliDate.fromtimestamp(time()), JalaliDate.today())
        self.assertEqual(JalaliDate.fromtimestamp(578707200), JalaliDate(1367, 2, 14))
        self.assertEqual(JalaliDate.fromtimestamp(1508371200), JalaliDate(1396, 7, 27))

        with pytest.raises(ValueError):
            JalaliDate(1400, 1, 1, "us")

    def test_leap(self):
        self.assertEqual(JalaliDate.is_leap(1214), True)
        self.assertEqual(JalaliDate.is_leap(1216), False)
        self.assertEqual(JalaliDate.is_leap(1218), True)
        self.assertEqual(JalaliDate.is_leap(1309), True)
        self.assertEqual(JalaliDate.is_leap(1313), True)
        self.assertEqual(JalaliDate.is_leap(1321), True)
        self.assertEqual(JalaliDate.is_leap(1342), True)
        self.assertEqual(JalaliDate.is_leap(1346), True)
        self.assertEqual(JalaliDate.is_leap(1358), True)
        self.assertEqual(JalaliDate.is_leap(1366), True)
        self.assertEqual(JalaliDate.is_leap(1367), False)
        self.assertEqual(JalaliDate.is_leap(1370), True)
        self.assertEqual(JalaliDate.is_leap(1387), True)
        self.assertEqual(JalaliDate.is_leap(1395), True)
        self.assertEqual(JalaliDate.is_leap(1396), False)
        self.assertEqual(JalaliDate.is_leap(1397), False)
        self.assertEqual(JalaliDate.is_leap(1398), False)
        self.assertEqual(JalaliDate.is_leap(1399), True)
        self.assertEqual(JalaliDate.is_leap(1400), False)
        self.assertEqual(JalaliDate.is_leap(1402), False)
        self.assertEqual(JalaliDate.is_leap(1403), True)
        self.assertEqual(JalaliDate.is_leap(1407), False)
        self.assertEqual(JalaliDate.is_leap(1408), True)
        self.assertEqual(JalaliDate.is_leap(1424), True)
        self.assertEqual(JalaliDate.is_leap(1474), True)
        self.assertEqual(JalaliDate.is_leap(1498), True)

    def test_format(self):
        j = JalaliDate(date(1988, 5, 4))
        self.assertEqual(j.isoformat(), "1367-02-14")
        self.assertEqual(j.strftime("%a %A %w"), "Cha Chaharshanbeh 4")

        j.locale = "fa"

        self.assertEqual(j.isoformat(), "۱۳۶۷-۰۲-۱۴")
        self.assertEqual(j.strftime("%a %A %w"), "چ چهارشنبه ۴")

        j = JalaliDate(1395, 3, 1)

        self.assertEqual(j.strftime("%d %b %B"), "01 Kho Khordad")
        self.assertEqual(j.strftime("%m %m %y %Y"), "03 03 95 1395")
        self.assertEqual(j.strftime("%p %j %j %U %W %%"), "AM 063 063 10 10 %")
        self.assertEqual(j.strftime("%c"), j.ctime())
        self.assertEqual(j.strftime("%c"), "Shanbeh 01 Khordad 1395")
        self.assertEqual(j.strftime("%x"), "95/03/01")
        self.assertEqual(format(j, "%c"), j.ctime())
        self.assertEqual(format(j), "1395-03-01")
        self.assertEqual(j.__repr__(), "JalaliDate(1395, 3, 1, Shanbeh)")

        j.locale = "fa"

        self.assertEqual(j.strftime("%d %b %B"), "۰۱ خرد خرداد")
        self.assertEqual(j.strftime("%m %m %y %Y"), "۰۳ ۰۳ ۹۵ ۱۳۹۵")
        self.assertEqual(j.strftime("%p %j %j %U %W %%"), "ق.ظ ۰۶۳ ۰۶۳ ۱۰ ۱۰ %")
        self.assertEqual(j.strftime("%c"), j.ctime())
        self.assertEqual(j.strftime("%c"), "شنبه ۰۱ خرداد ۱۳۹۵")
        self.assertEqual(j.strftime("%x"), "۹۵/۰۳/۰۱")
        self.assertEqual(format(j, "%c"), j.ctime())
        self.assertEqual(j.__repr__(), "JalaliDate(1395, 3, 1, Shanbeh)")

        self.assertEqual(format(j), "۱۳۹۵-۰۳-۰۱")

        with pytest.raises(TypeError):
            format(j, 1)

        j = JalaliDate(1397, 11, 29)

        self.assertEqual(j.strftime("%c"), "Doshanbeh 29 Bahman 1397")
        self.assertEqual(format(j), "1397-11-29")

        j.locale = "fa"

        self.assertEqual(j.strftime("%c"), "دوشنبه ۲۹ بهمن ۱۳۹۷")
        self.assertEqual(format(j), "۱۳۹۷-۱۱-۲۹")

        j = JalaliDate(1400, 4, 25)
        self.assertEqual(j.strftime("%c", "fa"), "جمعه ۲۵ تیر ۱۴۰۰")

        self.assertEqual(JalaliDate(1367, 2, 14), JalaliDate.fromisoformat("1367-02-14"))
        self.assertEqual(JalaliDate(1397, 12, 9), JalaliDate.fromisoformat("۱۳۹۷-۱۲-۰۹"))

        with pytest.raises(TypeError):
            JalaliDate.fromisoformat(13670214)

        with pytest.raises(ValueError, match="Invalid date separator: /"):
            JalaliDate.fromisoformat("1367/02/14")

        with pytest.raises(ValueError):
            JalaliDate.fromisoformat("1367-02/14")

    def test_week(self):
        self.assertEqual(JalaliDate(1394, 3, 30).week_of_year(), 14)
        self.assertEqual(JalaliDate(1394, 7, 30).week_of_year(), 31)
        self.assertEqual(JalaliDate(1394, 10, 11).week_of_year(), 41)
        self.assertEqual(JalaliDate(1394, 12, 29).week_of_year(), 53)
        self.assertEqual(JalaliDate(1395, 1, 21).week_of_year(), 4)
        self.assertEqual(JalaliDate(1395, 3, 21).week_of_year(), 12)
        self.assertEqual(JalaliDate(1395, 7, 1).week_of_year(), 27)
        self.assertEqual(JalaliDate(1395, 12, 27).week_of_year(), 52)
        self.assertEqual(JalaliDate(1395, 12, 30).week_of_year(), 53)
        self.assertEqual(JalaliDate(1396, 1, 25).week_of_year(), 4)
        self.assertEqual(JalaliDate(1396, 7, 8).week_of_year(), 29)
        self.assertEqual(JalaliDate(1397, 11, 29).week_of_year(), 49)
        self.assertEqual(JalaliDate(1399, 1, 2).week_of_year(), 2)
        self.assertEqual(JalaliDate(1403, 1, 5).week_of_year(), 2)

        self.assertEqual(JalaliDate(1367, 2, 14).weekday(), 4)
        self.assertEqual(JalaliDate(1393, 1, 1).weekday(), 6)
        self.assertEqual(JalaliDate(1394, 1, 1).weekday(), 0)
        self.assertEqual(JalaliDate(1394, 1, 1).isoweekday(), 1)
        self.assertEqual(JalaliDate(1395, 1, 1).weekday(), 1)
        self.assertEqual(JalaliDate(1395, 3, 21).weekday(), 6)
        self.assertEqual(JalaliDate(1396, 1, 1).weekday(), 3)
        self.assertEqual(JalaliDate(1396, 7, 27).weekday(), 5)
        self.assertEqual(JalaliDate(1397, 1, 1).weekday(), 4)
        self.assertEqual(JalaliDate(1397, 11, 29).weekday(), 2)
        self.assertEqual(JalaliDate(1400, 1, 1).weekday(), 1)
        self.assertEqual(JalaliDate(1400, 1, 1).isoweekday(), 2)
        self.assertEqual(JalaliDate(1396, 7, 27).isoweekday(), 6)
        self.assertEqual(JalaliDate(1397, 11, 29).isoweekday(), 3)

    def test_operators(self):
        self.assertTrue(JalaliDate(1367, 2, 14) == JalaliDate(date(1988, 5, 4)))
        self.assertTrue(JalaliDate(1367, 2, 14) == date(1988, 5, 4), True)
        self.assertTrue(JalaliDate(1396, 7, 27) == JalaliDate(date(2017, 10, 19)))
        self.assertFalse(JalaliDate(1367, 2, 14) != JalaliDate(date(1988, 5, 4)))
        self.assertFalse(JalaliDate(1367, 2, 14) != date(1988, 5, 4))
        self.assertTrue(JalaliDate(1367, 2, 14) < JalaliDate(1369, 1, 1))
        self.assertFalse(JalaliDate(1367, 2, 14) < date(1988, 5, 4))
        self.assertTrue(JalaliDate(1395, 12, 30) > JalaliDate(1395, 12, 29))
        self.assertTrue(JalaliDate(1395, 12, 30) > date(2000, 11, 15))
        self.assertTrue(JalaliDate(1395, 12, 30) >= JalaliDate(1395, 12, 30))
        self.assertFalse(JalaliDate(1367, 2, 13) >= date(1988, 5, 4))
        self.assertTrue(JalaliDate(1367, 2, 14) <= JalaliDate(1369, 1, 1))
        self.assertTrue(JalaliDate(1367, 2, 14) <= date(1988, 5, 4))
        self.assertFalse(JalaliDate(1367, 2, 14) >= JalaliDate(1369, 1, 1))
        self.assertTrue(JalaliDate(1397, 11, 29) >= JalaliDate(1397, 11, 10))

        self.assertEqual(JalaliDate(1395, 3, 21) + timedelta(days=2), JalaliDate(1395, 3, 23))
        self.assertEqual(JalaliDate(1396, 7, 27) + timedelta(days=4), JalaliDate(1396, 8, 1))
        self.assertEqual(JalaliDate(1395, 3, 21) + timedelta(days=-38), JalaliDate(1395, 2, 14))
        self.assertEqual(JalaliDate(1395, 3, 21) - timedelta(days=38), JalaliDate(1395, 2, 14))
        self.assertEqual(JalaliDate(1397, 11, 29) + timedelta(days=2), JalaliDate(1397, 12, 1))
        self.assertEqual(JalaliDate(1395, 3, 21) - JalaliDate(1395, 2, 14), timedelta(days=38))
        self.assertEqual(JalaliDate(1397, 12, 1) - JalaliDate(1397, 11, 29), timedelta(hours=48))
        self.assertEqual(JalaliDate(1395, 3, 21) - date(2016, 5, 3), timedelta(days=38))
        self.assertEqual(JalaliDate(1395, 12, 30) - JalaliDate(1395, 1, 1), timedelta(days=365))
        self.assertEqual(JalaliDate(1403, 1, 1) - JalaliDate(1402, 12, 29), timedelta(days=1))

        self.assertFalse(JalaliDate(1367, 2, 14) == (1367, 2, 14))
        self.assertFalse(JalaliDate(1367, 2, 14) == "")
        self.assertTrue(JalaliDate(1367, 2, 14) != 5)

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) < "string"

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) <= 0.5

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) > True

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) >= [1367, 2, 14]

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) + b"A"

        with pytest.raises(NotImplementedError):
            assert JalaliDate(1367, 2, 14) - {1, 2}

    def test_pickle(self):
        file = open("save.p", "wb")
        pickle.dump(JalaliDate(1367, 2, 14), file, protocol=2)
        file.close()

        file2 = open("save.p", "rb")
        j = pickle.load(file2)
        file2.close()

        self.assertEqual(j, JalaliDate(1367, 2, 14))

        os.remove("save.p")

    def test_hash(self):
        j1 = JalaliDate.today()
        j2 = JalaliDate(1367, 2, 14)
        j3 = JalaliDate(date(1988, 5, 4))

        self.assertEqual(
            {j1: "today", j2: "majid1", j3: "majid2"},
            {JalaliDate.today(): "today", JalaliDate(1367, 2, 14): "majid2"},
        )
