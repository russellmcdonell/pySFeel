from sly.yacc import ERROR_COUNT
import datetime
import dateutil
import pySFeel

parser = pySFeel.SFeelParser()

class TestClass:
    def test_and1(self):
        SFeel = 'true and true'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_or1(self):
        SFeel = 'true or true'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_and2(self):
        SFeel = 'true and false'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_or2(self):
        SFeel = 'true or false'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_and3(self):
        SFeel = 'true and "otherwise"'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None
    
    def test_or3(self):
        SFeel = 'true or "otherwise"'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_and4(self):
        SFeel = 'false and true'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_or4(self):
        SFeel = 'false or true'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_and5(self):
        SFeel = 'false and false'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_or5(self):
        SFeel = 'false or false'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_and6(self):
        SFeel = 'false and 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_and7(self):
        SFeel = '1 and true'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None
    
    def test_or7(self):
        SFeel = '1 or true'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_and8(self):
        SFeel = '"otherwise" and false'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_or8(self):
        SFeel = '1 or false'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None
    
    def test_and9(self):
        SFeel = '1 and 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None
    
    def test_or9(self):
        SFeel = '1 or 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None
    
    def test_comparisonTest1a(self):
        SFeel = '1 = 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest1b(self):
        SFeel = '[1, 2, 3] = [1, 2, 3]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest1c(self):
        SFeel = '[1, 2, 3] = [1, 2]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest1d(self):
        SFeel = '{a:1, b:2, c:3} = {a:1, b:2, c:3}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest1e(self):
        SFeel = '{a:1, b:2, c:3} = {a:1, b:2, c:4}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest1f(self):
        SFeel = '{a:1, b:2, c:3} = {a:1, b:2, d:3}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest1g(self):
        SFeel = '{a:1, b:2, c:3} = {a:1, b:2}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest1h(self):
        SFeel = '[1..3] = [1..3]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest1i(self):
        SFeel = '[1..3] = (1..3]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest1j(self):
        SFeel = '[1..3] = [1..4]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest1k(self):
        SFeel = '[1..3] = ["a".."c"]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest2a(self):
        SFeel = '1 != 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest2b(self):
        SFeel = '[1, 2, 3] != [1, 2, 3]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest2c(self):
        SFeel = '[1, 2, 3] != [1, 2]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest2d(self):
        SFeel = '{a:1, b:2, c:3} != {a:1, b:2, c:3}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest2e(self):
        SFeel = '{a:1, b:2, c:3} != {a:1, b:2, c:4}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest2f(self):
        SFeel = '{a:1, b:2, c:3} != {a:1, b:2, d:3}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest2g(self):
        SFeel = '{a:1, b:2, c:3} != {a:1, b:2}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest2h(self):
        SFeel = '[1..3] != [1..3]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
    
    def test_comparisonTest2i(self):
        SFeel = '[1..3] != (1..3]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest2j(self):
        SFeel = '[1..3] != [1..4]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest2k(self):
        SFeel = '[1..3] != ["a".."c"]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
    
    def test_comparisonTest3(self):
        SFeel = '1 < 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_comparisonTest4(self):
        SFeel = '1 <= 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_comparisonTest5(self):
        SFeel = '1 > 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False
        
    def test_comparisonTest6(self):
        SFeel = '1 >= 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_in1(self):
        SFeel = '3 in [2,3,4]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_in2(self):
        SFeel = '3 in [(0..2),[3..4)]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_in3(self):
        SFeel = '3 in [3..4]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_in4(self):
        SFeel = '3 in(1,2,3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_in5(self):
        SFeel = '2 in(<1,!=2,>3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_in6(self):
        SFeel = '"c" in("abc")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_in7(self):
        SFeel = '"c" in("a","b","c")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_in8(self):
        SFeel = '"c" in(="a",="b",!="c")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_notin1(self):
        SFeel = 'not(4 in [3..5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_notin2(self):
        SFeel = 'not(2 in(<1,!=2,>3))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_notin3(self):
        SFeel = 'not("c" in(="a",="b",!="c"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_add1(self):
        SFeel = '[1, 2] + [3, 4]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2, 3, 4]
    
    def test_add2(self):
        SFeel = '1 + 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2
    
    def test_add2a(self):
        SFeel = '[1] + 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2
    
    def test_add2b(self):
        SFeel = '1 + [1]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2
    
    def test_add3(self):
        SFeel = '"a" + "b"'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'ab'
    
    def test_add4(self):
        SFeel = '["a", "b", "c"] + "d"'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ['a', 'b', 'c', 'd']
    
    def test_add5(self):
        SFeel = '2021-03-05T12:00:00 + PT3H10M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2021, month=3, day=5, hour=15, minute=10)
    
    def test_add6(self):
        SFeel = '2021-03-05T12:00:00 + P2Y2M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2023, month=5, day=5, hour=12, minute=0)
    
    def test_add7(self):
        SFeel = 'PT3H10M + 2021-03-05T12:00:00'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2021, month=3, day=5, hour=15, minute=10)
    
    def test_add8(self):
        SFeel = 'P2Y2M + 2021-03-05T12:00:00'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2023, month=5, day=5, hour=12, minute=0)
    
    def test_add9(self):
        SFeel = 'PT2H4M + PT3H10M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=(5*60+14)*60)
    
    def test_add10(self):
        SFeel = '2021-03-05T12:00:00 + P2Y2M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2023, month=5, day=5, hour=12, minute=0)
    
    def test_add11(self):
        SFeel = '12:00:00 + PT3H10M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time(hour=15,minute=10)
    
    def test_add12(self):
        SFeel = 'PT3H10M + 12:00:00'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time(hour=15, minute=10)
    
    def test_subtract1(self):
        SFeel = '1 - 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0
      
    def test_subtract1a(self):
        SFeel = '[1] - 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0
      
    def test_subtract1b(self):
        SFeel = '1 - [1]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0
      
    def test_subtract2(self):
        SFeel = '2021-03-03T00:00:00 - 2021-03-02T00:00:00'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(days=1)
      
    def test_subtract3(self):
        SFeel = '2021-03-07T14:45:00 - P1DT6H15M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2021, month=3, day=6, hour=8, minute=30)
      
    def test_subtract4(self):
        SFeel = '2021-03-07T14:45:00 - P1Y1M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2020, month=2, day=7, hour=14, minute=45)
      
    def test_subtract5(self):
        SFeel = '14:45:00 - 10:30:00'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=(4*60+15)*60)
      
    def test_subtract6(self):
        SFeel = '14:45:00 - PT10H30M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time(hour=4, minute=15)
      
    def test_subtract7(self):
        SFeel = 'PT14H15M - PT10H30M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=(3*60+45)*60)
      
    def test_multiply1(self):
        SFeel = '2 * 2'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 4
            
    def test_multiply2(self):
        SFeel = '2 * [2]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 4
            
    def test_divide(self):
        SFeel = '2 / 2'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1
         
    def test_exponentiation(self):
        SFeel = '2 ** 3'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 8

    def test_negation(self):
        SFeel = '- 1'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -1
    
    def test_interval1(self):
        SFeel = '(3 .. 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ('(', 3, 5, ')')

    def test_interval2(self):
        SFeel = ']3 .. 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ('(', 3, 5, ')')

    def test_interval3(self):
        SFeel = '[3 .. 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ('[', 3, 5, ')')

    def test_interval4(self):
        SFeel = '(3 .. 5['
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ('(', 3, 5, ')')

    def test_interval5(self):
        SFeel = ']3 .. 5]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ('(', 3, 5, ']')

    def test_time(self):
        SFeel = '13:15:17'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time(hour=13, minute=15, second=17)

    def test_datetime(self):
        SFeel = '2012-12-31T13:15:17'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2012, month=12, day=31, hour=13, minute=15, second=17)

    def test_date1(self):
        SFeel = '2012-12-31'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2012, month=12, day=31)

    def test_date2(self):
        SFeel = 'date("2012-12-31")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2012, month=12, day=31)

    def test_date3(self):
        SFeel = 'date(date and time("2012-12-31T11:00:00Z"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2012, month=12, day=31)

    def test_date4(self):
        SFeel = 'date(2012, 12,31)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2012, month=12, day=31)

    def test_dateandtime1(self):
        SFeel = 'date and time(date("2012-12-31"), time("11:00:00Z"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2012, month=12, day=31, hour=11, minute=0, second=0, tzinfo=datetime.timezone.utc)

    def test_dateandtime2(self):
        SFeel = 'date and time("2012-12-31T11:00:00Z")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2012, month=12, day=31, hour=11, minute=0, second=0, tzinfo=datetime.timezone.utc)

    def test_time1(self):
        SFeel = 'time("23:59:00Z") + duration("PT2M")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        tzinfo = dateutil.tz.UTC
        assert retval == datetime.time(hour=0, minute=1, second=0, tzinfo=tzinfo)

    def test_time2(self):
        SFeel = 'time(date and time("2012-12-31T11:00:00Z"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        tzinfo = dateutil.tz.UTC
        assert retval == datetime.time(hour=11, minute=0, second=0, tzinfo=tzinfo)

    def test_time3(self):
        SFeel = 'time("00:01:00@Etc/UTC")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        tzinfo = dateutil.tz.UTC
        assert retval == datetime.time(hour=0, minute=1, second=0, tzinfo=tzinfo)

    def test_number1(self):
        SFeel = 'number("1,000.0", ",", ".")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1000

    def test_number2(self):
        SFeel = 'number(null, ",", ".")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_range1(self):
        SFeel = '5 in ( <= 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_range2(self):
        SFeel = '5 in ( (5 ..10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_duration1(self):
        SFeel = 'P1DT1H1M5.5S'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(days=1, seconds=61*60 + 5, milliseconds=500)

    def test_duration2(self):
        SFeel = '-P1DT1H1M5.5S'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -datetime.timedelta(days=1, seconds=61*60 + 5, milliseconds=500)

    def test_duration3(self):
        SFeel = 'PT1H1M5.5S'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(days=0, seconds=61*60 + 5, milliseconds=500)

    def test_duration4(self):
        SFeel = '-PT1H1M5.5S'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -datetime.timedelta(days=0, seconds=61*60 + 5, milliseconds=500)

    def test_duration5(self):
        SFeel = '-P1Y1M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -13

    def test_duration6(self):
        SFeel = 'P0Y11M'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 11

    def test_null(self):
        SFeel = 'null'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_true(self):
        SFeel = 'true'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True
        
    def test_false(self):
        SFeel = 'false'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_between(self):
        SFeel = '5 between 3 and 7'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_not1(self):
        SFeel = 'not(true)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_not2(self):
        SFeel = 'not(false)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_not3(self):
        SFeel = 'not(1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_not4(self):
        SFeel = 'not(null)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_string1(self):
        SFeel = 'string(null)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'null'

    def test_string2(self):
        SFeel = 'string(true)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_string2(self):
        SFeel = 'string(false)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'false'

    def test_string3(self):
        SFeel = 'string(1.1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == '1.1'

    def test_string4(self):
        SFeel = 'string("Fred")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'Fred'

    def test_string5(self):
        SFeel = 'string(date and time("2012-12-31T11:00:00Z"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == '2012-12-31T11:00:00@UTC'

    def test_string6(self):
        SFeel = 'string(P2D)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'P2DT0H0M0S'

    def test_substring1(self):
        SFeel = 'substring("foobar", 3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'obar'

    def test_substring2(self):
        SFeel = 'substring("foobar", 3, 3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'oba'

    def test_substring3(self):
        SFeel = 'substring("foobar", -2, 1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'a'

    def test_uppercase(self):
        SFeel = 'upper case("aBc4")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'ABC4'

    def test_lowercase(self):
        SFeel = 'lower case("aBc4")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'abc4'

    def test_substringbefore1(self):
        SFeel = 'substring before("foobar", "bar")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'foo'

    def test_substringbefore2(self):
        SFeel = 'substring before("foobar", "xyz")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ''

    def test_substringafter1(self):
        SFeel = 'substring after("foobar", "ob")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'ar'

    def test_substringafter2(self):
        SFeel = 'substring after("", "a")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ''

    def test_replace(self):
        SFeel = 'replace("abcd", "(ab)|(a)", "[1=$1][2=$2]")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == '[1=ab][2=]cd'

    def test_contains1(self):
        SFeel = 'contains("foobar", "of")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_contains2(self):
        SFeel = 'contains("foobar", "ob")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startswith1(self):
        SFeel = 'starts with("foobar", "fo")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startswith2(self):
        SFeel = 'starts with("foobar", "of")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_endswith1(self):
        SFeel = 'ends with("foobar", "r")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_endswith2(self):
        SFeel = 'ends with("foobar", "or")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_matches1(self):
        SFeel = 'matches("foobar", "^fo*b")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_matches2(self):
        SFeel = 'matches("foobar", "fob")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_split1(self):
        SFeel = 'split("John Doe", "\\s")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ['John', 'Doe']

    def test_split2(self):
        SFeel = 'split("a;b;c;;", ";")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == ['a', 'b', 'c', '', '']

    def test_listcontains1(self):
        SFeel = 'list contains([1, 2, 3], 2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_listcontains2(self):
        SFeel = 'list contains([1, 2, 3], 4)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_count1(self):
        SFeel = 'count([1, 2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_count2(self):
        SFeel = 'count([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_count3(self):
        SFeel = 'count([1, [2, 3]])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_min1(self):
        SFeel = 'min([1, 2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_min2(self):
        SFeel = 'min(1, 2, 3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_min3(self):
        SFeel = 'min([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_max1(self):
        SFeel = 'max([1, 2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_max2(self):
        SFeel = 'max(1, 2, 3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_max3(self):
        SFeel = 'max([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_sum1(self):
        SFeel = 'sum([1, 2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 6

    def test_sum2(self):
        SFeel = 'sum(1, 2, 3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 6

    def test_sum3(self):
        SFeel = 'sum([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_mean1(self):
        SFeel = 'mean([1, 2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_mean2(self):
        SFeel = 'mean(1, 2, 3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_mean3(self):
        SFeel = 'mean([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_all1(self):
        SFeel = 'all([true, true])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_all2(self):
        SFeel = 'all([true, false])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_all3(self):
        SFeel = 'all(true, true)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_all4(self):
        SFeel = 'all(true, false)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_all5(self):
        SFeel = 'all(true, null, false)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_all6(self):
        SFeel = 'all(0)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_any1(self):
        SFeel = 'any([false, "otherwise", true])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_any2(self):
        SFeel = 'any([true])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_any3(self):
        SFeel = 'any(true)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_any4(self):
        SFeel = 'any([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_any5(self):
        SFeel = 'any(0)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_sublist(self):
        SFeel = 'sublist([4, 5, 6], 1, 2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [4, 5]

    def test_append(self):
        SFeel = 'append([1], 2, 3)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2, 3]

    def test_concatenate(self):
        SFeel = 'concatenate([1, 2], [3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2, 3]

    def test_insertbefore(self):
        SFeel = 'insert before([1, 3], 1, 2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [2, 1, 3]

    def test_remove(self):
        SFeel = 'remove([1, 2, 3], 2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 3]

    def test_reverse(self):
        SFeel = 'reverse([1, 2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [3, 2, 1]

    def test_indexof(self):
        SFeel = 'index of([1, 2, 3, 2], 2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [2, 4]

    def test_union(self):
        SFeel = 'union([1, 2], [2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2, 3]

    def test_distinctvalues(self):
        SFeel = 'distinct values([1, 2, 3, 2, 1])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2, 3]

    def test_flatten(self):
        SFeel = 'flatten([[1, 2], [[3]], 4])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2, 3, 4]

    def test_product1(self):
        SFeel = 'product([2, 3, 4])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 24

    def test_product2(self):
        SFeel = 'product(2, 3, 4)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 24

    def test_median1(self):
        SFeel = 'median(8, 2, 5, 3, 4)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 4

    def test_median2(self):
        SFeel = 'median([6, 1, 2, 3])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2.5

    def test_median3(self):
        SFeel = 'median([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_stddev1(self):
        SFeel = 'stddev(2, 4, 7, 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2.0816659994661326

    def test_stddev2(self):
        SFeel = 'stddev([47])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_stddev3(self):
        SFeel = 'stddev(47)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_stddev4(self):
        SFeel = 'stddev([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == None

    def test_mode1(self):
        SFeel = 'mode(6, 3, 9, 6, 6)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [6]

    def test_mode2(self):
        SFeel = 'mode([6, 1, 9, 6, 1])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 6]

    def test_mode3(self):
        SFeel = 'mode([])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == []

    def test_decimal1(self):
        SFeel = 'decimal(1/3, 2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == .33

    def test_decimal2(self):
        SFeel = 'decimal(1.5, 0)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_decimal3(self):
        SFeel = 'decimal(2.5, 0)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_floor1(self):
        SFeel = 'floor(1.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_floor2(self):
        SFeel = 'floor(-1.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -2

    def test_ceiling1(self):
        SFeel = 'ceiling(1.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_ceiling2(self):
        SFeel = 'ceiling(-1.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -1

    def test_abs1(self):
        SFeel = 'abs(10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 10

    def test_abs2(self):
        SFeel = 'abs(-10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 10

    def test_modulo1(self):
        SFeel = 'modulo(12, 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_modulo2(self):
        SFeel = 'modulo(-12, 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_modulo3(self):
        SFeel = 'modulo(12, -5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -3

    def test_modulo4(self):
        SFeel = 'modulo(-12, -5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == -2

    def test_modulo5(self):
        SFeel = 'modulo(10.1, 4.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert round(retval, 1) == 1.1

    def test_modulo6(self):
        SFeel = 'modulo(-10.1, 4.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert round(retval, 1) == 3.4

    def test_modulo7(self):
        SFeel = 'modulo(10.1, -4.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert round(retval, 1) == -3.4

    def test_modulo8(self):
        SFeel = 'modulo(-10.1, -4.5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert round(retval, 1) == -1.1

    def test_sqrt(self):
        SFeel = 'sqrt(16)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 4

    def test_log(self):
        SFeel = 'log(10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert round(retval, 11) == 2.30258509299

    def test_exp(self):
        SFeel = 'exp(5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert round(retval, 12) == 148.413159102577

    def test_odd1(self):
        SFeel = 'odd(5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_odd2(self):
        SFeel = 'odd(2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_even1(self):
        SFeel = 'even(5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_even2(self):
        SFeel = 'even(2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_list1(self):
        SFeel = '[1, 2, ["c"]]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2, ['c']]

    def test_list2(self):
        SFeel = '[[1, 2], [3, 4]]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [[1, 2], [3, 4]]

    def test_listitem1(self):
        SFeel = '[1, 2, 3, 4][item > 2]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [3, 4]

    def test_listitem2(self):
        SFeel = '[{x:1, y:2}, {x:2, y:3}][item.x=1]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'x':1, 'y':2}]

    def test_listitem3(self):
        SFeel = '[{x:1, y:2}, {x:null, y:3}][item.x<2]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'x':1, 'y':2}]

    def test_listitem4(self):
        SFeel = '[{x:1, y:2}, {x:null, y:3}].y'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [2, 3]

    def test_listitem5(self):
        SFeel = '[1, 2, 3, 4][item > 1]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [2, 3, 4]

    def test_listitem6(self):
        SFeel = '[1, 2, 3, 4][item = 1]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1]

    def test_context1(self):
        SFeel = '{a:1, b:2}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == {'a':1, 'b':2}

    def test_context2(self):
        SFeel = '{a:[1, 2], b:2, c:{d:3, e:"e"}}'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == {'a':[1, 2], 'b':2, 'c':{'d':3, 'e':'e'}}

    def test_getValue(self):
        SFeel = 'get value({a:[1, 2], b:2, c:{d:3, e:"e"}}, a)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1, 2]

    def test_entries1(self):
        SFeel = 'get entries({a:[1, 2], b:2, c:{d:3, e:"e"}})'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'key':'a', 'value':[1, 2]}, {'key':'b', 'value':2}, {'key':'c', 'value':{'d':3, 'e':'e'}}]

    def test_entries2a(self):
        SFeel = 'get entries({a:[1, 2], b:2, c:{d:3, e:"e"}})[item key="a"]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'key':'a', 'value':[1, 2]}]

    def test_entries2b(self):
        SFeel = '[{key:"a", value:[1, 2]}].value'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [[1, 2]]

    def test_entries3(self):
        SFeel = 'get entries({a:[1, 2], b:2, c:{d:3, e:"e"}})[item key="a"].value'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [[1, 2]]

    def test_is1(self):
        SFeel = 'is(date("2012-12-25"), time("23:00:50"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_is2(self):
        SFeel = 'is(date("2012-12-25"), date("2012-12-25"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_is3(self):
        SFeel = 'is(time("23:00:50z"), time("23:00:50"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_is4(self):
        SFeel = 'is("string1", "string2")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_is5(self):
        SFeel = 'is(7, 9.0)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_is6(self):
        SFeel = 'is(P2Y1M, P0Y2M)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_is7(self):
        SFeel = 'is(P1DT2H, P2DT3H5S)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_is8(self):
        SFeel = 'is(P2Y1M, 25)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_before1(self):
        SFeel = 'before(1, 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_before2(self):
        SFeel = 'before(10, 1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_before3(self):
        SFeel = 'before(1, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_before5(self):
        SFeel = 'before(1, (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_before6(self):
        SFeel = 'before(1, [5 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_before7(self):
        SFeel = 'before([1 .. 10], 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_before8(self):
        SFeel = 'before([1 .. 10), 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_before9(self):
        SFeel = 'before([1 .. 10], 15)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_before10(self):
        SFeel = 'before([1 .. 10], [15 .. 20])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_before11(self):
        SFeel = 'before([1 .. 10], [10 .. 20])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_before12(self):
        SFeel = 'before([1 .. 10), [10 .. 20])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_before13(self):
        SFeel = 'before([1 .. 10], (10 .. 20])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after1(self):
        SFeel = 'after(10, 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after2(self):
        SFeel = 'after(5, 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_after3(self):
        SFeel = 'after(12, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after5(self):
        SFeel = 'after(10, [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after6(self):
        SFeel = 'after(10, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_after7(self):
        SFeel = 'after([11 .. 20], 12)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_after8(self):
        SFeel = 'after([11 .. 20), 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after9(self):
        SFeel = 'after((11 .. 20], 11)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after10(self):
        SFeel = 'after([11 .. 0], 11)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_after11(self):
        SFeel = 'after([11 .. 20], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after12(self):
        SFeel = 'after([1 .. 10], [11 .. 20])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_after14(self):
        SFeel = 'after([11 .. 20], [1.. 11))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_after15(self):
        SFeel = 'after((11 .. 20], [1 .. 11])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_meets1(self):
        SFeel = 'meets([1 .. 5], [5 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_meets2(self):
        SFeel = 'meets([1 .. 5), [5 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_meets3(self):
        SFeel = 'meets([1 .. 5], (5 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_meets4(self):
        SFeel = 'meets([1 .. 5], [6 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_metby1(self):
        SFeel = 'met by([5 .. 10], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_metby2(self):
        SFeel = 'met by([5 .. 10], [1 .. 5))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_metby3(self):
        SFeel = 'met by((5 .. 10], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_metby4(self):
        SFeel = 'met by([6 .. 10], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlaps1(self):
        SFeel = 'overlaps([1 .. 5], [3 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlaps2(self):
        SFeel = 'overlaps([3 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlaps3(self):
        SFeel = 'overlaps([1 .. 8], [3 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlaps4(self):
        SFeel = 'overlaps([3 .. 5], [1 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlaps5(self):
        SFeel = 'overlaps([1 .. 5], [6 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlaps6(self):
        SFeel = 'overlaps([6 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlaps7(self):
        SFeel = 'overlaps([1 .. 5], [5 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlaps8(self):
        SFeel = 'overlaps([1 .. 5], (5 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlaps9(self):
        SFeel = 'overlaps([1 .. 5), [5 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlaps10(self):
        SFeel = 'overlaps([1 .. 5), (5 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlaps11(self):
        SFeel = 'overlaps([5 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlaps12(self):
        SFeel = 'overlaps((5 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlap13(self):
        SFeel = 'overlaps([5 .. 8], [1 .. 5))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlaps14(self):
        SFeel = 'overlaps((5 .. 8], [1 .. 5))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsbefore1(self):
        SFeel = 'overlaps before([1 .. 5], [3 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsbefore2(self):
        SFeel = 'overlaps before([1 .. 5], [6 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsbefore3(self):
        SFeel = 'overlaps before([1 .. 5], [5 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsbefore4(self):
        SFeel = 'overlaps before([1 .. 5], (5 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsbefore5(self):
        SFeel = 'overlaps before([1 .. 5), [5 .. 8])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsbefore6(self):
        SFeel = 'overlaps before([1 .. 5), (1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsbefore7(self):
        SFeel = 'overlaps before([1 .. 5], (1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsbefore8(self):
        SFeel = 'overlaps before([1 .. 5), [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsbefore9(self):
        SFeel = 'overlaps before([1 .. 5], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsafter1(self):
        SFeel = 'overlaps after([3 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsafter2(self):
        SFeel = 'overlaps after([6 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsafter3(self):
        SFeel = 'overlaps after([5 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsafter4(self):
        SFeel = 'overlaps after((5 .. 8], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsafter5(self):
        SFeel = 'overlaps after([5 .. 8], [1 .. 5))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsafter6(self):
        SFeel = 'overlaps after((1 .. 5], [1 .. 5))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsafter7(self):
        SFeel = 'overlaps after((1 .. 5], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_overlapsafter8(self):
        SFeel = 'overlaps after([1 .. 5], [1 .. 5))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_overlapsafter9(self):
        SFeel = 'overlaps after([1 .. 5], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_finishes1(self):
        SFeel = 'finishes(10, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishes2(self):
        SFeel = 'finishes(10, [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_finishes3(self):
        SFeel = 'finishes([5 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishes4(self):
        SFeel = 'finishes([5 .. 10), [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_finishes5(self):
        SFeel = 'finishes([5 .. 10), [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishes6(self):
        SFeel = 'finishes((1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishes7(self):
        SFeel = 'finishes((1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishedby1(self):
        SFeel = 'finished by([1 .. 10], 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishedby2(self):
        SFeel = 'finished by([1 .. 10), 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_finishedby3(self):
        SFeel = 'finished by([1 .. 10], [5 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishedby4(self):
        SFeel = 'finished by([1 .. 10], [5 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_finishedby5(self):
        SFeel = 'finished by([1 .. 10), [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishedby6(self):
        SFeel = 'finished by([1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_finishedby7(self):
        SFeel = 'finished by([1 .. 10], (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_includes1(self):
        SFeel = 'includes([1 .. 10], 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes2(self):
        SFeel = 'includes([1 .. 10], 12)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == False

    def test_includes3(self):
        SFeel = 'includes([1 .. 10], 1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes4(self):
        SFeel = 'includes([1 .. 10], 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes5(self):
        SFeel = 'includes((1 .. 10], 1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == False

    def test_includes6(self):
        SFeel = 'includes([1 .. 10), 10)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == False

    def test_includes7(self):
        SFeel = 'includes([1 .. 10], [4 .. 6])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes8(self):
        SFeel = 'includes([1 .. 10], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes9(self):
        SFeel = 'includes((1 .. 10], (1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes10(self):
        SFeel = 'includes([1 .. 10], (1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes11(self):
        SFeel = 'includes([1 .. 10), [5 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes12(self):
        SFeel = 'includes([1 .. 10], [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes13(self):
        SFeel = 'includes([1 .. 10], (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_includes14(self):
        SFeel = 'includes([1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during1(self):
        SFeel = 'during(5, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during2(self):
        SFeel = 'during(12, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == False

    def test_during3(self):
        SFeel = 'during(1, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during4(self):
        SFeel = 'during(10, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during5(self):
        SFeel = 'during(1, (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == False

    def test_during6(self):
        SFeel = 'during(10, [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == False

    def test_during7(self):
        SFeel = 'during([4 .. 6], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during8(self):
        SFeel = 'during([1 .. 5], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during9(self):
        SFeel = 'during((1 .. 5], (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during10(self):
        SFeel = 'during((1 .. 10), [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during11(self):
        SFeel = 'during([5 .. 10), [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during12(self):
        SFeel = 'during([1 .. 10), [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during13(self):
        SFeel = 'during((1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_during14(self):
        SFeel = 'during([1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errrors' not in status
        assert retval == True

    def test_starts1(self):
        SFeel = 'starts(1, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_starts2(self):
        SFeel = 'starts(1, (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_starts3(self):
        SFeel = 'starts(2, [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_starts4(self):
        SFeel = 'starts([1 .. 5], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_starts5(self):
        SFeel = 'starts((1 .. 5], (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_starts6(self):
        SFeel = 'starts((1 .. 5], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_starts7(self):
        SFeel = 'starts([1 .. 5], (1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_starts8(self):
        SFeel = 'starts([1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_starts9(self):
        SFeel = 'starts([1 .. 10), [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_starts10(self):
        SFeel = 'starts((1 .. 10), (1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startedby1(self):
        SFeel = 'started by([1 .. 10], 1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startedby2(self):
        SFeel = 'started by((1 .. 10], 1)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_startsedby3(self):
        SFeel = 'started by([1 .. 10], 2)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_startedby4(self):
        SFeel = 'started by([1 .. 10], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startedby5(self):
        SFeel = 'started by((1 .. 10], (1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startedby6(self):
        SFeel = 'started by([1 .. 10], (1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_startedby7(self):
        SFeel = 'started by((1 .. 10], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_startedby8(self):
        SFeel = 'started by([1 .. 10], [1 .. 10])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startedby9(self):
        SFeel = 'started by([1 .. 10], [1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_startedby10(self):
        SFeel = 'started by((1 .. 10), (1 .. 10))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_coincides1(self):
        SFeel = 'coincides(5, 5)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_coincides2(self):
        SFeel = 'coincides(3, 4)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_coincides3(self):
        SFeel = 'coincides([1 .. 5], [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_coincides4(self):
        SFeel = 'coincides((1 .. 5), [1 .. 5])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_coincides5(self):
        SFeel = 'coincides([1 .. 5], [2 .. 6])'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == False

    def test_dayofyear(self):
        SFeel = 'day of year(date(2019, 9, 17))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 260

    def test_dayofweek(self):
        SFeel = 'day of week(date(2019, 9, 17))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'Tuesday'
        
    def test_monthofyear(self):
        SFeel = 'month of year(date(2019, 9, 17))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'September'
        
    def test_weekofyear1(self):
        SFeel = 'week of year(date(2019, 9, 17))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 38
        
    def test_weekofyear2(self):
        SFeel = 'week of year(date(2003, 12, 29))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1
        
    def test_weekofyear3(self):
        SFeel = 'week of year(date(2004, 1, 4))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1
        
    def test_weekofyear4(self):
        SFeel = 'week of year(date(2005, 1, 1))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 53
        
    def test_weekofyear5(self):
        SFeel = 'week of year(date(2005, 1, 3))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1
        
    def test_weekofyear6(self):
        SFeel = 'week of year(date(2005, 1, 9))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotyear1(self):
        SFeel = 'date(2005, 1, 9).year'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2005

    def test_edotyear2(self):
        SFeel = 'thisDate <- date(2005, 1, 9)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2005, month=1, day=9)
        SFeel = 'thisDate.year'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2005

    def test_edotyear3(self):
        SFeel = '(2005-01-09).year'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2005

    def test_edotyear4(self):
        SFeel = 'date and time("2005-01-09T12:00:15").year'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2005

    def test_edotyear5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15)
        SFeel = 'thisDateTime.year'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2005

    def test_edotyear6(self):
        SFeel = '(2005-01-09T12:00:15).year'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2005

    def test_edotyear7(self):
        SFeel = '@"2005-01-09T12:00:15".year'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2005

    def test_edotmonth1(self):
        SFeel = 'date(2005, 1, 9).month'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotmonth2(self):
        SFeel = 'thisDate <- date(2005, 1, 9)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2005, month=1, day=9)
        SFeel = 'thisDate.month'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotmonth3(self):
        SFeel = '(2005-01-09).month'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotmonth4(self):
        SFeel = 'date and time("2005-01-09T12:00:15").month'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotmonth5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15)
        SFeel = 'thisDateTime.month'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotmonth6(self):
        SFeel = '(2005-01-09T12:00:15).month'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotmonth7(self):
        SFeel = '@"2005-01-09T12:00:15".month'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 1

    def test_edotyday1(self):
        SFeel = 'date(2005, 1, 9).day'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 9

    def test_edotday2(self):
        SFeel = 'thisDate <- date(2005, 1, 9)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2005, month=1, day=9)
        SFeel = 'thisDate.day'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 9

    def test_edotday3(self):
        SFeel = '(2005-01-09).day'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 9

    def test_edotday4(self):
        SFeel = 'date and time("2005-01-09T12:00:15").day'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 9

    def test_edotday5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15)
        SFeel = 'thisDateTime.day'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 9

    def test_edotday6(self):
        SFeel = '(2005-01-09T12:00:15).day'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 9

    def test_edotday7(self):
        SFeel = '@"2005-01-09T12:00:15".day'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 9

    def test_edotweekday1(self):
        SFeel = 'date(2005, 1, 9).weekday'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2005, month=1, day=9).isoweekday()

    def test_edotweekday2(self):
        SFeel = 'thisDate <- date(2005, 1, 9)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2005, month=1, day=9)
        SFeel = 'thisDate.weekday'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2005, month=1, day=9).isoweekday()

    def test_edotweekday3(self):
        SFeel = '(2005-01-09).weekday'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.date(year=2005, month=1, day=9).isoweekday()

    def test_edotweekday4(self):
        SFeel = 'date and time("2005-01-09T12:00:15").weekday'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15).isoweekday()

    def test_edotweekday5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15)
        SFeel = 'thisDateTime.weekday'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15).isoweekday()

    def test_edotweekday6(self):
        SFeel = '(2005-01-09T12:00:15).weekday'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15).isoweekday()

    def test_edotweekday7(self):
        SFeel = '@"2005-01-09T12:00:15".weekday'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15).isoweekday()

    def test_edothour1(self):
        SFeel = 'time(12, 0, 15).hour'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edothour2(self):
        SFeel = 'thisTime <- time(12, 0, 15)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time(hour=12, minute=0, second=15)
        SFeel = 'thisTime.hour'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edothour3(self):
        SFeel = '(12:00:15).hour'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edothour4(self):
        SFeel = 'date and time("2005-01-09T12:00:15").hour'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edothour5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15)
        SFeel = 'thisDateTime.hour'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edothour6(self):
        SFeel = '(2005-01-09T12:00:15).hour'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edothour7(self):
        SFeel = '@"2005-01-09T12:00:15".hour'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edotminute1(self):
        SFeel = 'time(12, 0, 15).minute'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotminute2(self):
        SFeel = 'thisTime <- time(12, 0, 15)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time(hour=12, minute=0, second=15)
        SFeel = 'thisTime.minute'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotminute3(self):
        SFeel = '(12:00:15).minute'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotminute4(self):
        SFeel = 'date and time("2005-01-09T12:00:15").minute'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotminute5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15)
        SFeel = 'thisDateTime.minute'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotminute6(self):
        SFeel = '(2005-01-09T12:00:15).minute'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotminute7(self):
        SFeel = '@"2005-01-09T12:00:15".minute'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotsecond1(self):
        SFeel = 'time(12, 0, 15).second'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotsecond2(self):
        SFeel = 'thisTime <- time(12, 0, 15)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time(hour=12, minute=0, second=15)
        SFeel = 'thisTime.second'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotsecond3(self):
        SFeel = '(12:00:15).second'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotsecond4(self):
        SFeel = 'date and time("2005-01-09T12:00:15").second'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotsecond5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime(year=2005, month=1, day=9, hour=12, minute=0, second=15)
        SFeel = 'thisDateTime.second'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotsecond6(self):
        SFeel = '(2005-01-09T12:00:15).second'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotsecond7(self):
        SFeel = '@"2005-01-09T12:00:15".second'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edottimezone1(self):
        SFeel = 'time(12, 0, 15, @"PT8H").timezone'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'UTC+08:00'

    def test_edottimezone2(self):
        SFeel = 'thisTime <- time(12, 0, 15, @"PT8H")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time.fromisoformat('12:00:15+08:00')
        SFeel = 'thisTime.timezone'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time.fromisoformat('12:00:15+08:00').tzname()

    def test_edottimezone3(self):
        SFeel = '(12:00:15@Australia/Perth).timezone'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'Australia/Perth'

    def test_edottimezone4(self):
        SFeel = 'date and time("2005-01-09T12:00:15@Australia/Perth").timezone'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'Australia/Perth'

    def test_edottimezone5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15, @"PT8H"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime.fromisoformat('2005-01-09T12:00:15+08:00')
        SFeel = 'thisDateTime.timezone'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time.fromisoformat('12:00:15+08:00').tzname()

    def test_edottimezone6(self):
        SFeel = '(2005-01-09T12:00:15@Australia/Perth).timezone'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'Australia/Perth'

    def test_edottimezone7(self):
        SFeel = '@"2005-01-09T12:00:15@Australia/Perth".timezone'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 'Australia/Perth'

    def test_edottimeoffset1(self):
        SFeel = 'time(12, 0, 15, @"PT8H").time offset'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=8*60*60)

    def test_edottimeoffset2(self):
        SFeel = 'thisTime <- time(12, 0, 15, @"PT8H")'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.time.fromisoformat('12:00:15+08:00')
        SFeel = 'thisTime.time_offset'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=8*60*60)

    def test_edottimeoffset3(self):
        SFeel = '(12:00:15@Australia/Perth).time offset'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=8*60*60)

    def test_edottimeoffset4(self):
        SFeel = 'date and time("2005-01-09T12:00:15@Australia/Perth").time offset'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=8*60*60)

    def test_edottimeoffset5(self):
        SFeel = 'thisDateTime <- date and time(date(2005, 1, 9), time(12, 0, 15, @"PT8H"))'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.datetime.fromisoformat('2005-01-09T12:00:15+08:00')
        SFeel = 'thisDateTime.time_offset'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=8*60*60)

    def test_edottimeoffset6(self):
        SFeel = '(2005-01-09T12:00:15@Australia/Perth).time offset'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=8*60*60)

    def test_edottimeoffset7(self):
        SFeel = '@"2005-01-09T12:00:15@Australia/Perth".time offset'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == datetime.timedelta(seconds=8*60*60)

    def test_edotyears1(self):
        SFeel = '(P2Y3M).years'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_edotyears2(self):
        SFeel = '@"P2Y3M".years'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_edotmonths1(self):
        SFeel = '(P2Y3M).months'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_edotymonth2(self):
        SFeel = '@"P2Y3M".months'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_edotdays1(self):
        SFeel = '(P2DT3H15M12S).days'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_edotdays2(self):
        SFeel = '@"P2DT3H15M12S".days'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 2

    def test_edothours1(self):
        SFeel = '(P2DT3H15M12S).hours'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_edothours2(self):
        SFeel = '@"P2DT3H15M12S".hours'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 3

    def test_edotminutes1(self):
        SFeel = '(P2DT3H15M12S).minutes'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotminutes2(self):
        SFeel = '@"P2DT3H15M12S".minutes'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 15

    def test_edotseconds1(self):
        SFeel = '(P2DT3H15M12S).seconds'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edotseconds2(self):
        SFeel = '@"P2DT3H15M12S".seconds'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 12

    def test_edotstart1(self):
        SFeel = '[0 .. 10].start'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 0

    def test_edotend1(self):
        SFeel = '[0 .. 10].end'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == 10

    def test_edotstartincluded1(self):
        SFeel = '[0 .. 10].start included'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_edotendincluded1(self):
        SFeel = '[0 .. 10].end included'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == True

    def test_sort1(self):
        SFeel =  'nums <- [1, 3, 5, 7, 9, 2, 4, 6, 8]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        SFeel = 'sort(nums, function(x,y) x<y)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        SFeel = 'sort(nums, function(x,y) y>x)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        SFeel = 'sort(nums, function(x,y) y<x)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]
        SFeel = 'sort(nums, function(x,y) x>y)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]

    def test_sort2(self):
        SFeel =  'dicts <- [{a:1, b:3}, {a:5, b:7}, {a:9, b:2}, {a:4, b:6}]'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        SFeel = 'sort(dicts, function(x,y) x.a<y.a)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'a': 1.0, 'b': 3.0}, {'a': 4.0, 'b': 6.0}, {'a': 5.0, 'b': 7.0}, {'a': 9.0, 'b': 2.0}]
        SFeel = 'sort(dicts, function(x,y) y.a>x.a)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'a': 1.0, 'b': 3.0}, {'a': 4.0, 'b': 6.0}, {'a': 5.0, 'b': 7.0}, {'a': 9.0, 'b': 2.0}]
        SFeel = 'sort(dicts, function(x,y) y.a<x.a)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'a': 9.0, 'b': 2.0}, {'a': 5.0, 'b': 7.0}, {'a': 4.0, 'b': 6.0}, {'a': 1.0, 'b': 3.0}]
        SFeel = 'sort(dicts, function(x,y) x.a>y.a)'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert retval == [{'a': 9.0, 'b': 2.0}, {'a': 5.0, 'b': 7.0}, {'a': 4.0, 'b': 6.0}, {'a': 1.0, 'b': 3.0}]

    def test_now(self):
        SFeel =  'now()'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert isinstance(retval, datetime.datetime)
        now = datetime.datetime.now()
        diff = retval - now
        assert diff.microseconds < 5

    def test_today(self):
        SFeel =  'today()'
        (status, retval) = parser.sFeelParse(SFeel)
        assert 'errors' not in status
        assert isinstance(retval, datetime.date)
        today = datetime.date.today()
        assert retval == today

        


