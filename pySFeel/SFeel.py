# -----------------------------------------------------------------------------
# SFeel.py
# -----------------------------------------------------------------------------

from enum import IntFlag
from os import truncate
from typing import KeysView, ValuesView
from sly import Lexer, Parser
import re
import datetime
import dateutil.parser, dateutil.tz
import math
import statistics

class SFeelLexer(Lexer):
    tokens = {BOOLEAN, DATEFUNC, TIMEFUNC, DATEANDTIMEFUNC,
              NUMBERFUNC, STRINGFUNC, NOTFUNC, INFUNC,
              SUBSTRINGFUNC, STRINGLENFUNC,UPPERCASEFUNC, LOWERCASEFUNC,
              SUBSTRINGBEFOREFUNC, SUBSTRINGAFTERFUNC,
              REPLACEFUNC, CONTAINSFUNC, STARTSWITHFUNC, ENDSWITHFUNC, MATCHESFUNC, SPLITFUNC,
              LISTCONTAINSFUNC, COUNTFUNC, MINFUNC, MAXFUNC, SUMFUNC, MEANFUNC,
              ALLFUNC, ANYFUNC, SUBLISTFUNC, APPENDFUNC, CONCATENATEFUNC, INSERTBEFOREFUNC,
              REMOVEFUNC, REVERSEFUNC, INDEXOFFUNC, UNIONFUNC, DISTINCTVALUESFUNC, FLATTENFUNC, PRODUCTFUNC,
              MEDIANFUNC, STDDEVFUNC, MODEFUNC,
              DECIMALFUNC, FLOORFUNC, CEILINGFUNC, ABSFUNC, MODULOFUNC,SQRTFUNC,
              LOGFUNC, EXPFUNC, ODDFUNC, EVENFUNC,
              VALUETFUNC, VALUET1FUNC, VALUEDTFUNC, VALUEDT1FUNC, VALUEDTDFUNC, VALUEDTD1FUNC,
              VALUEYMDFUNC, VALUEYMD1FUNC,
              DURATIONFUNC, YEARSANDMONTHSDURATIONFUNC, GETVALUEFUNC, GETENTRIESFUNC,
              ISFUNC,
              BEFOREFUNC, AFTERFUNC, MEETSFUNC, METBYFUNC, OVERLAPSFUNC, OVERLAPSBEFOREFUNC, OVERLAPSAFTERFUNC,
              FINISHESFUNC, FINISHEDBYFUNC, INCLUDESFUNC, DURINGFUNC, STARTSFUNC, STARTEDBYFUNC, COINCIDESFUNC,
              DAYOFYEARFUNC, DAYOFWEEKFUNC, MONTHOFYEARFUNC, WEEKOFYEARFUNC,
              STARTINCLUDED, ENDINCLUDED, TIMEOFFSET,
              NAME, ATSTRING, STRING, NULL,
              LBRACKET, RBRACKET,
              EQUALS, NOTEQUALS, LTTHANEQUAL, GTTHANEQUAL, LTTHAN, GTTHAN,
              AND, OR, NOT, BETWEEN,
              PLUS, MINUS, MULTIPY, DIVIDE, EXPONENT,
              ELLIPSE, COMMA, DATETIME, DATE, TIME, DTDURATION, YMDURATION,
              NUMBER,
              LPAREN, RPAREN,
              LCURLY, RCURLY, COLON, PERIOD,
              IN, ITEM, ASSIGN
            }
    ignore = '\u000A\u000B\u000C\u000D\u0009\u0020\u0085\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u2028\u2029\u202F\u205F\u3000\uFEFF'

    # Tokens
    BOOLEAN = r'true|false'
    DATEFUNC = r'date\('
    TIMEFUNC = r'time\('
    DATEANDTIMEFUNC = r'date and time\('
    NUMBERFUNC = r'number\('
    STRINGFUNC = r'string\('
    NOTFUNC = r'not\('
    INFUNC = r'in\s*\('
    SUBSTRINGFUNC = r'substring\('
    STRINGLENFUNC = r'string length\('
    UPPERCASEFUNC = r'upper case\('
    LOWERCASEFUNC = r'lower case\('
    SUBSTRINGBEFOREFUNC = r'substring before\('
    SUBSTRINGAFTERFUNC = r'substring after\('
    REPLACEFUNC = r'replace\('
    CONTAINSFUNC = r'contains\('
    STARTSWITHFUNC = r'starts with\('
    ENDSWITHFUNC = r'ends with\('
    MATCHESFUNC = r'matches\('
    SPLITFUNC = r'split\('
    LISTCONTAINSFUNC = r'list contains\('
    COUNTFUNC = r'count\('
    MINFUNC = r'min\('
    MAXFUNC = r'max\('
    SUMFUNC = r'sum\('
    MEANFUNC = r'mean\('
    ALLFUNC = r'all\('
    ANYFUNC = r'any\('
    SUBLISTFUNC = r'sublist\('
    APPENDFUNC = r'append\('
    CONCATENATEFUNC = r'concatenate\('
    INSERTBEFOREFUNC = r'insert before\('
    REMOVEFUNC = r'remove\('
    REVERSEFUNC = r'reverse\('
    INDEXOFFUNC = r'index of\('
    UNIONFUNC = r'union\('
    DISTINCTVALUESFUNC = r'distinct values\('
    FLATTENFUNC = r'flatten\('
    PRODUCTFUNC = r'product\('
    MEDIANFUNC = r'median\('
    STDDEVFUNC = r'stddev\('
    MODEFUNC = r'mode\('
    DECIMALFUNC = r'decimal\('
    FLOORFUNC = r'floor\('
    CEILINGFUNC = r'ceiling\('
    ABSFUNC = r'abs\('
    MODULOFUNC = r'modulo\('
    SQRTFUNC = r'sqrt\('
    LOGFUNC = r'log\('
    EXPFUNC = r'exp\('
    ODDFUNC = r'odd\('
    EVENFUNC = r'even\('
    VALUETFUNC = r'valuet\('
    VALUET1FUNC = r'valuet-1\('
    VALUEDTFUNC = r'valuedt\('
    VALUEDT1FUNC = r'valuedt-1\('
    VALUEDTDFUNC = r'valuedtd\('
    VALUEDTD1FUNC = r'valuedtd-1\('
    VALUEYMDFUNC = r'valueymd\('
    VALUEYMD1FUNC = r'valueymd-1\('
    DURATIONFUNC = r'duration\('
    YEARSANDMONTHSDURATIONFUNC = r'years and months duration\('
    GETVALUEFUNC = r'get\s+value\('
    GETENTRIESFUNC = r'get\s+entries\('
    ISFUNC = r'is\('
    BEFOREFUNC = r'before\('
    AFTERFUNC = r'after\('
    MEETSFUNC = r'meets\('
    METBYFUNC = r'met by\('
    OVERLAPSFUNC = r'overlaps\('
    OVERLAPSBEFOREFUNC = r'overlaps before\('
    OVERLAPSAFTERFUNC = r'overlaps after\('
    FINISHESFUNC = r'finishes\('
    FINISHEDBYFUNC = r'finished by\('
    INCLUDESFUNC = r'includes\('
    DURINGFUNC = r'during\('
    STARTSFUNC = r'starts\('
    STARTEDBYFUNC = r'started by\('
    COINCIDESFUNC = r'coincides\('
    DAYOFYEARFUNC = r'day of year\('
    DAYOFWEEKFUNC = r'day of week\('
    MONTHOFYEARFUNC = r'month of year\('
    WEEKOFYEARFUNC = r'week of year\('
    DTDURATION = r'-?P((([0-9]+D)(T(([0-9]+H)([0-9]+M)?([0-9]+(\.[0-9]+)?S)?|([0-9]+M)([0-9]+(\.[0-9]+)?S)?|([0-9]+(\.[0-9]+)?S)))?)|(T(([0-9]+H)([0-9]+M)?([0-9]+(\.[0-9]+)?S)?|([0-9]+M)([0-9]+(\.[0-9]+)?S)?|([0-9]+(\.[0-9]+)?S))))'
    YMDURATION = r'-?P[0-9]+Y[0-9]+M'
    STARTINCLUDED = r'\bstart included\b'
    ENDINCLUDED = r'\bend included\b'
    TIMEOFFSET = r'\btime offset\b'
    NAME = (u'[?A-Z_a-z' +
            u'\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF' +
            u'\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF' +
            u'\u3001-\uD7FF\uF900-\uFDCF\uFDF0\uFFFD' + 
            u'\U00010000-\U000EFFFF]' +
            u'[?A-Z_a-z' +
            u'\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF' +
            u'\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF' +
            u'\u3001-\uD7FF\uF900-\uFDCF\uFDF0\uFFFD' + 
            u'\U00010000-\U000EFFFF' +
            u"0-9\u00B7\u0300-\u036F\u203F-\u2040\\./\\-'+\\*]*")

    # Special cases of name
    NAME['in'] = IN
    NAME['and'] = AND
    NAME['or'] = OR
    NAME['not'] = NOT
    NAME['between'] = BETWEEN
    NAME['null'] = NULL
    NAME['item'] = ITEM

    ATSTRING = r'@"(' + r"\\'" + r'|\\"|\\\\|\\n|\\r|\\t|\\u[0-9]{4}|[^"])*"'
    STRING = r'"(' + r"\\'" + r'|\\"|\\\\|\\n|\\r|\\t|\\u[0-9]{4}|[^"])*"'
    DATETIME = r'-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)|@[A-Za-z0-9_-]+/[A-Za-z0-9_-]+)?'
    DATE = r'([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(Z|(\+|-)(0[0-9]|1[0-3]):[0-5][0-9]|14:00)?'
    TIME = r'(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))(Z|(\+|-)(0[0-9]|1[0-3]):[0-5][0-9]|14:00|@[A-Za-z0-9_-]+/[A-Za-z0-9_-]+)?'
    NUMBER = r'\d+(\.(\d+|\s)){0,1}'

    # Special symbols
    ASSIGN = r'<-'
    LTTHANEQUAL = r'<='
    LTTHAN = r'<'
    GTTHANEQUAL = r'>='
    GTTHAN = r'>'
    EQUALS = r'='
    NOTEQUALS = r'!='
    AND = r'and'
    OR = r'or'
    NOT = r'not'
    BETWEEN = r'between'
    PLUS = r'\+'
    MINUS = r'-'
    EXPONENT = r'\*\*'
    MULTIPY = r'\*'
    DIVIDE = r'/'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    COMMA = r','
    LPAREN = r'\('
    RPAREN = r'\)'
    LCURLY = r'{'
    RCURLY = r'}'
    ELLIPSE = r'\.\.'
    COLON = r':'
    PERIOD = r'\.'
    IN = r'in'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        t.value = "Illegal character '{!s}'".format(t.value[0])
        self.index += 1
        return t

class SFeelParser(Parser):
    # debugfile = 'parser.out'
    tokens = SFeelLexer.tokens

    precedence = (
        ('left', EQUALS, NOTEQUALS, LTTHANEQUAL, GTTHANEQUAL, LTTHAN, GTTHAN),
        ('left', PLUS, MINUS),
        ('left', MULTIPY, DIVIDE),
        ('left', EXPONENT),
        ('right', UMINUS),
        ('left', AND, OR, NOT, BETWEEN),
        ('left', LBRACKET, COMMA, RBRACKET),
        ('left', LPAREN, RPAREN),
        ('left', IN),
        ('left', NAME),
        )

    def __init__(self):
        self.names = { }
        self.errors = []
        self.lexer = SFeelLexer()

    def clearErrors(self):
        self.errors = []
        return

    def collectErrors(self):
        knownErrors = self.errors
        self.errors = []
        return knownErrors

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr
        return p.expr

    @_('expr')
    def statement(self, p):
        return p.expr

    @_(NULL)
    def expr(self, p):
        return None

    @_('expr IN expr')
    def expr(self, p):
        # This is 'in' as in 'in a list' or 'in a range' or simply 'in' as an alternative to '='
        # Grammer Rule 49.c
        if isinstance(p.expr1, tuple):      # in a range
            (end0, lowVal, highVal, end1) = p.expr1
            if isinstance(p.expr0, str):
                if not isinstance(lowVal, str) or not isinstance(highVal, str):
                    return False
            elif isinstance(p.expr0, int):              # Year, month durations
                if not isinstance(lowVal, int) or not isinstance(highVal, int):
                    return False
            elif isinstance(p.expr0, float):
                if not isinstance(lowVal, float) or not isinstance(highVal, float):
                    return False
            elif isinstance(p.expr0, datetime.date):                # True for both dates and datetimes
                if (not isinstance(lowVal, datetime.date)) and (not isinstance(highVal, datetime.date)):
                    return False
            elif isinstance(p.expr0, datetime.time):
                if (not isinstance(lowVal, datetime.time)) or (not isinstance(highVal, datetime.time)):
                    return False
            elif isinstance(p.expr0, datetime.timedelta):
                if (not isinstance(lowVal, datetime.timedelta)) or (not isinstance(highVal, datetime.timedelta)):
                    return False
            else:
                return False
            if lowVal > p.expr0:
                return False
            if highVal < p.expr0:
                return False
            if (end0 != '[') and (lowVal == p.expr0):
                return False
            if (end1 != ']') and (highVal == p.expr0):
                return False
            return True
        elif isinstance(p.expr1, list):     # in a list
            for i in range(len(p.expr1)):
                if isinstance(p.expr1[i], tuple):
                    (end0, lowVal, highVal, end1) = p.expr1[i]
                    if isinstance(p.expr0, str):
                        if not isinstance(lowVal, str) or not isinstance(highVal, str):
                            continue
                    elif isinstance(p.expr0, int):              # Year, month durations
                        if not isinstance(lowVal, int) or not isinstance(highVal, int):
                            continue
                    elif isinstance(p.expr0, float):
                        if not isinstance(lowVal, float) or not isinstance(highVal, float):
                            continue
                    elif isinstance(p.expr0, datetime.date):                # True for both dates and datetimes
                        if (not isinstance(lowVal, datetime.date)) or (not isinstance(highVal, datetime.datetime)):
                            continue
                    elif isinstance(p.expr0, datetime.time):
                        if (not isinstance(lowVal, datetime.time)) or (not isinstance(highVal, datetime.time)):
                            continue
                    elif isinstance(p.expr0, datetime.timedelta):
                        if (not isinstance(lowVal, datetime.timedelta)) or (not isinstance(highVal, datetime.timedelta)):
                            continue
                    else:
                        return False
                    if lowVal > p.expr0:
                        continue
                    if highVal < p.expr0:
                        continue
                    if (end0 != '[') and (lowVal == p.expr0):
                        continue
                    if (end1 != ']') and (highVal == p.expr0):
                        continue
                    return True
                elif p.expr0 == p.expr1[i]:
                    return True
            return False
        elif isinstance(p.expr0, str) and isinstance(p.expr1, str):
             return p.expr0 == p.expr1
        elif isinstance(p.expr0, int) and isinstance(p.expr1, int):             # Year, month durations
            return p.expr0 == p.expr1
        elif isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 == p.expr1
        elif isinstance(p.expr0, datetime.date) and isinstance(p.expr1, datetime.date):         # True for both dates and datetimes
            return p.expr0 == p.expr1
        elif isinstance(p.expr0, datetime.time) and isinstance(p.expr1, datetime.time):
            return p.expr0 == p.expr1
        elif isinstance(p.expr0, datetime.timedelta) and isinstance(p.expr1, datetime.timedelta):
            return p.expr0 == p.expr1
        else:
            return None

    @_('expr IN LTTHAN expr')
    def expr(self, p):
        # 'in <' as an alternative to '<'
        # Grammer Rule 49.c
        if isinstance(p.expr0, str) and isinstance(p.expr1, str):
            return p.expr0 < p.expr1
        elif isinstance(p.expr0, int) and isinstance(p.expr1, int):             # Year, month durations
            return p.expr0 < p.expr1
        elif isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 < p.expr1
        elif isinstance(p.expr0, datetime.date) and isinstance(p.expr1, datetime.date):         # True for both dates and datetimes
            return p.expr0 < p.expr1
        elif isinstance(p.expr0, datetime.time) and isinstance(p.expr1, datetime.time):
            return p.expr0 < p.expr1
        elif isinstance(p.expr0, datetime.timedelta) and isinstance(p.expr1, datetime.timedelta):
            return p.expr0 < p.expr1
        else:
            return None

    @_('expr IN GTTHAN expr')
    def expr(self, p):
        # 'in >' as an alternative to >'
        # Grammer Rule 49.c
        if isinstance(p.expr0, str) and isinstance(p.expr1, str):
            return p.expr0 > p.expr1
        elif isinstance(p.expr0, int) and isinstance(p.expr1, int):             # Year, month durations
            return p.expr0 > p.expr1
        elif isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 > p.expr1
        elif isinstance(p.expr0, datetime.date) and isinstance(p.expr1, datetime.date):         # True for both dates and datetimes
            return p.expr0 > p.expr1
        elif isinstance(p.expr0, datetime.time) and isinstance(p.expr1, datetime.time):
            return p.expr0 > p.expr1
        elif isinstance(p.expr0, datetime.timedelta) and isinstance(p.expr1, datetime.timedelta):
            return p.expr0 > p.expr1
        else:
            return None

    @_('expr IN LTTHANEQUAL expr')
    def expr(self, p):
        # 'in <=' as an alternative to <=
        # Grammer Rule 49.c
        if isinstance(p.expr0, str) and isinstance(p.expr1, str):
            return p.expr0 <= p.expr1
        elif isinstance(p.expr0, int) and isinstance(p.expr1, int):             # Year, month durations
            return p.expr0 <= p.expr1
        elif isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 <= p.expr1
        elif isinstance(p.expr0, datetime.date) and isinstance(p.expr1, datetime.date):         # True for both dates and datetimes
            return p.expr0 <= p.expr1
        elif isinstance(p.expr0, datetime.time) and isinstance(p.expr1, datetime.time):
            return p.expr0 <= p.expr1
        elif isinstance(p.expr0, datetime.timedelta) and isinstance(p.expr1, datetime.timedelta):
            return p.expr0 <= p.expr1
        else:
            return None

    @_('expr IN GTTHANEQUAL expr')
    def expr(self, p):
        # 'in >=' as an alternative to >=
        # Grammer Rule 49.c
        if isinstance(p.expr0, str) and isinstance(p.expr1, str):
            return p.expr0 >= p.expr1
        elif isinstance(p.expr0, int) and isinstance(p.expr1, int):             # Year, month durations
            return p.expr0 >= p.expr1
        elif isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 >= p.expr1
        elif isinstance(p.expr0, datetime.date) and isinstance(p.expr1, datetime.date):         # True for both dates and datetimes
            return p.expr0 >= p.expr1
        elif isinstance(p.expr0, datetime.time) and isinstance(p.expr1, datetime.time):
            return p.expr0 >= p.expr1
        elif isinstance(p.expr0, datetime.timedelta) and isinstance(p.expr1, datetime.timedelta):
            return p.expr0 >= p.expr1
        else:
            return None

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        '''
        Add two expressions
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if isinstance(p.expr0, list) and (len(p.expr0) == 1):
            var0 = p.expr0[0]
        else:
            var0 = p.expr0
        if isinstance(p.expr1, list) and (len(p.expr1) == 1):
            var1 = p.expr1[0]
        else:
            var1 = p.expr1
        if isinstance(var0, list) and isinstance(var1, list):       # Concatentation of two lists
            return var0 + var1
        if isinstance(var0, list):                                  # Append to a list
            return var0 + list(var1)
        if isinstance(var1, list):                                  # Prepend to a list
            return list(var0) + var1
        if isinstance(var0, int) and isinstance(var1, int):         #  Addition of two durations(yearMonth)
            return var0 + var1
        if isinstance(var0, float) and isinstance(var1, float):
            return var0 + var1
        if isinstance(var0, str) and isinstance(var1, str):         # Concatenation of strings
            return var0 + var1
        if isinstance(var0, datetime.date):                     # True for both dates and datetimes
            if isinstance(var1, datetime.timedelta):            # date/datetime plus days and time duration
                return var0 + var1
            elif isinstance(var1, int):                       # date/datetime plus year and month duration
                year = (var0).year
                month = (var0).month + var1
                while month < 1:                                # Allow for addition of a negative duration
                    year -= 1
                    month += 12
                while month > 12:                               # Bring month into range 1-12
                    year += 1
                    month -= 12
                return (var0).replace(year=int(year), month=int(month))
            else:
                return None
        if isinstance(var1, datetime.date):                 # True for both dates and datetimes
            if isinstance(var0, datetime.timedelta):         # day and time duration plus date/datetime
                return var0 + var1
            elif isinstance(var0, int):                    # year and month duration plus date/datetime
                year = (var1).year
                month = (var1).month + var0
                while month < 1:                            # Allow for the addtion of a negative duration
                    year -= 1
                    month += 12
                while month > 12:                           # Bring month into range 1-12
                    year += 1
                    month -= 12
                return (var1).replace(year=int(year), month=int(month))
            else:
                return None
        if isinstance(var0, datetime.time) and isinstance(var1, datetime.timedelta):        # date or datetime plus days and time duration
            return (datetime.datetime.combine(datetime.date.today(), var0) + var1).timetz()
        if isinstance(var1, datetime.time) and isinstance(var0, datetime.timedelta):        # days and time duration plus date or datetime
            return (datetime.datetime.combine(datetime.date.today(), var1) + var0).timetz()
        if isinstance(var0, datetime.timedelta) and isinstance(var1, datetime.timedelta):   # days and time duration plus days and time duration
            return var0 + var1
        return None

    @_('expr MINUS expr')
    def expr(self, p):
        '''
        Subtract two expressions
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if isinstance(p.expr0, list) and (len(p.expr0) == 1):
            var0 = p.expr0[0]
        else:
            var0 = p.expr0
        if isinstance(p.expr1, list) and (len(p.expr1) == 1):
            var1 = p.expr1[0]
        else:
            var1 = p.expr1
        if isinstance(var0, int) and isinstance(var1, int):         # Subtraction of two durations(yearMonth)
            return var0 - var1
        if isinstance(var0, float) and isinstance(var1, float):
            return var0 - var1
        if isinstance(var0, datetime.date):                         # True for both dates and datetimes
            if isinstance(var1, datetime.date):             # date or datetime minus date or datetime
                try:
                    return var0 - var1
                except:
                    return None
            if isinstance(var1, datetime.timedelta):         # date/datetime minus days and time duration
                return var0 - var1
            if isinstance(var1, int):                       # date/datetime minus years and months duration
                year = (var0).year
                month = (var0).month - p.expr1
                while month > 12:
                    year += 1
                    month -= 12
                while month < 1:
                    year -= 1
                    month += 12
                return (var0).replace(year=int(year), month=int(month))
            else:
                return None
        elif isinstance(var0, datetime.time):            # time minus time or days and time duration
            if isinstance(var1, datetime.time):               # time minus time
                return datetime.datetime.combine(datetime.date.today(), var0) - datetime.datetime.combine(datetime.date.today(), var1)
            elif isinstance(var1, datetime.timedelta):        # time minus days and time duration
                return (datetime.datetime.combine(datetime.date.today(), var0) - var1).timetz()
            else:
                return None
        elif isinstance(var0, datetime.timedelta) and isinstance(var1, datetime.timedelta):       # days and time duration minus days and time duration
            return var0 - var1
        else:
            return None

    @_('expr EXPONENT expr')
    def expr(self, p):
        '''
        expression power expression
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if isinstance(p.expr0, list) and (len(p.expr0) == 1):
            var0 = p.expr0[0]
        else:
            var0 = p.expr0
        if isinstance(p.expr1, list) and (len(p.expr1) == 1):
            var1 = p.expr1[0]
        else:
            var1 = p.expr1
        if isinstance(var0, float) and isinstance(var1, float):
            return var0 ** var1
        else:
            return None

    @_('expr MULTIPY expr')
    def expr(self, p):
        '''
        multiply two expressions
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if isinstance(p.expr0, list) and (len(p.expr0) == 1):
            var0 = p.expr0[0]
        else:
            var0 = p.expr0
        if isinstance(p.expr1, list) and (len(p.expr1) == 1):
            var1 = p.expr1[0]
        else:
            var1 = p.expr1
        if isinstance(var0, int) and isinstance(var1, float):               # Year, month duration * number
            return int(var0 * var1)
        if isinstance(var0, float) and isinstance(var1, int):               # number * Year, month duration
            return int(var0 * var1)
        if isinstance(var0, float) and isinstance(var1, float):
            return var0 * var1
        if isinstance(var0, datetime.timedelta) and isinstance(var1, float):
            return var0 * var1
        if isinstance(var1, datetime.timedelta) and isinstance(var0, float):
            return var0 * var1
        return None

    @_('expr DIVIDE expr')
    def expr(self, p):
        '''
        multiply two expressions
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if isinstance(p.expr0, list) and (len(p.expr0) == 1):
            var0 = p.expr0[0]
        else:
            var0 = p.expr0
        if isinstance(p.expr1, list) and (len(p.expr1) == 1):
            var1 = p.expr1[0]
        else:
            var1 = p.expr1
        if isinstance(p.expr1, list) and (len(p.expr1) == 1):
            var1 = p.expr1[0]
        else:
            var1 = p.expr1
        if var1 == 0:
            return None
        if isinstance(var0, int) and isinstance(var1, float):               # Year, month duration / number
            try:
                return int(var0 / var1)
            except:
                 return None
        if isinstance(var0, int) and isinstance(var1, int):               # Year, month duration / Year, month duration
            try:
                return int(var0 / var1)
            except:
                 return None
        if isinstance(var0, float) and isinstance(var1, float):
            try:
                return var0 / var1
            except:
                 return None
        if isinstance(var0, datetime.timedelta) and isinstance(var1, float):
            try:
                return var0 / var1
            except:
                return None
        if isinstance(var0, datetime.timedelta) and isinstance(var1, datetime.timedelta):
            try:
                return var0 / var1
            except:
                return None
        return None

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        '''
        unary minus
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if isinstance(p.expr, list) and (len(p.expr) == 1):
            var = p.expr[0]
        else:
            var = p.expr
        if isinstance(var, int):                # Year, month duration
            return -var
        if isinstance(var, float):
            return -var
        if isinstance(var, bool):
            return not var
        return None

    @_('expr EQUALS expr')
    def expr(self, p):
        '''
        expression = expression
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            x0 = p.expr0[0]
        else:
            x0 = p.expr0
        if (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            x1 = p.expr1[0]
        else:
            x1 = p.expr1
        try:
            return x0 == x1
        except:
            False

    @_('expr NOTEQUALS expr')
    def expr(self, p):
        '''
        expression != expression
        For convenience of notation, a singleton list L,
        when used in an expression where a list is not expected, behaves as if L[1] is written.
        '''
        if (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            x0 = p.expr0[0]
        else:
            x0 = p.expr0
        if (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            x1 = p.expr1[0]
        else:
            x1 = p.expr1
        try:
            return x0 != x1
        except:
            False


    @_('LBRACKET RBRACKET')
    def expr(self, p):
        return []
        
    @_('LBRACKET expr RBRACKET')
    def listFilter(self, p):
        return p.expr

    @_('LBRACKET ITEM NAME LTTHANEQUAL expr RBRACKET')
    def listFilter(self, p):
        return (p.NAME, p.LTTHANEQUAL, p.expr)

    @_('LBRACKET ITEM LTTHANEQUAL expr RBRACKET')
    def listFilter(self, p):
        return (p.LTTHANEQUAL, p.expr)

    @_('LBRACKET LTTHANEQUAL expr RBRACKET')
    def listFilter(self, p):
        return (p.LTTHANEQUAL, p.expr)

    @_('LBRACKET ITEM NAME LTTHAN expr RBRACKET')
    def listFilter(self, p):
        return (p.NAME, p.LTTHAN, p.expr)

    @_('LBRACKET ITEM LTTHAN expr RBRACKET')
    def listFilter(self, p):
        return (p.LTTHAN, p.expr)

    @_('LBRACKET LTTHAN expr RBRACKET')
    def listFilter(self, p):
        return (p.LTTHAN, p.expr)

    @_('LBRACKET ITEM NAME GTTHANEQUAL expr RBRACKET')
    def listFilter(self, p):
        return (p.NAME, p.GTTHANEQUAL, p.expr)

    @_('LBRACKET ITEM GTTHANEQUAL expr RBRACKET')
    def listFilter(self, p):
        return (p.GTTHANEQUAL, p.expr)

    @_('LBRACKET GTTHANEQUAL expr RBRACKET')
    def listFilter(self, p):
        return (p.GTTHANEQUAL, p.expr)

    @_('LBRACKET ITEM NAME GTTHAN expr RBRACKET')
    def listFilter(self, p):
        return (p.NAME, p.GTTHAN, p.expr)

    @_('LBRACKET ITEM GTTHAN expr RBRACKET')
    def listFilter(self, p):
        return (p.GTTHAN, p.expr)

    @_('LBRACKET GTTHAN expr RBRACKET')
    def listFilter(self, p):
        return (p.GTTHAN, p.expr)

    @_('LBRACKET ITEM NAME EQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.NAME, p.EQUALS, p.expr)

    @_('LBRACKET ITEM EQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.EQUALS, p.expr)

    @_('LBRACKET EQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.EQUALS, p.expr)

    @_('LBRACKET ITEM NAME NOTEQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.NAME, p.NOTEQUALS, p.expr)

    @_('LBRACKET ITEM NOTEQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.NOTEQUALS, p.expr)

    @_('LBRACKET NOTEQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.NOTEQUALS, p.expr)

    @_('expr listFilter')
    def expr(self, p):
        ''' select items from a list '''
        if isinstance(p.expr, list):
            if isinstance(p.listFilter, float):     # a specific element from the list [...][n]
                if len(p.expr) < int(p.listFilter):
                    return None
                if int(p.listFilter) < 1:
                    return None
                return p.expr[int(p.listFilter) - 1]
            if isinstance(p.listFilter, tuple):
                if len(p.listFilter) == 2:          # specific items from a list of numbers or strings
                    (equality, value) = p.listFilter
                    retList = []
                    for i in range(len(p.expr)):
                        if (isinstance(p.expr[i], list)) or (isinstance(p.expr[i], dict)):
                            continue
                        item = p.expr[i]
                        if item is None:
                            continue
                        if equality == '>=':
                            if item >= value:
                                retList.append(item)
                        elif equality == '>':
                            if item > value:
                                retList.append(item)
                        elif equality == '<=':
                            if item <= value:
                                retList.append(item)
                        elif equality == '<':
                            if item < value:
                                retList.append(item)
                        elif equality == '=':
                            if item == value:
                                retList.append(item)
                        elif equality == '!=':
                            if item != value:
                                retList.append(item)
                        else:
                            return None
                    return retList
                elif len(p.listFilter) == 3:    # specific things from a list of contexts
                    (key, equality, value) = p.listFilter
                    retList = []
                    for i in range(len(p.expr)):
                        if not isinstance(p.expr[i], dict):
                            continue
                        if key in p.expr[i]:
                            item = p.expr[i][key]
                            if item is None:
                                continue
                            if equality == '>=':
                                if item >= value:
                                    retList.append(p.expr[i])
                            elif equality == '>':
                                if item > value:
                                    retList.append(p.expr[i])
                            elif equality == '<=':
                                if item <= value:
                                    retList.append(p.expr[i])
                            elif equality == '<':
                                if item < value:
                                    retList.append(p.expr[i])
                            elif equality == '=':
                                if item == value:
                                    retList.append(p.expr[i])
                            elif equality == '!=':
                                if item != value:
                                    retList.append(p.expr[i])
                            else:
                                return None
                    return retList
                else:
                    return None
            return None
        return None

    @_('expr PERIOD STARTINCLUDED')
    def expr(self, p):
        if isinstance(p.expr, tuple) and (len(p.expr) == 4):
            (end0, low0, high1, end1) = p.expr
            if end0 == '[':
                return True
            else:
                return False
        return False

    @_('expr PERIOD ENDINCLUDED')
    def expr(self, p):
        if isinstance(p.expr, tuple) and (len(p.expr) == 4):
            (end0, low0, high1, end1) = p.expr
            if end1 == ']':
                return True
            else:
                return False
        return False

    @_('expr PERIOD TIMEOFFSET')
    def expr(self, p):
        if isinstance(p.expr, datetime.datetime):
            if p.expr.tzinfo is None:
                return None
            return p.expr.utcoffset()
        if isinstance(p.expr, datetime.time):
            if p.expr.tzinfo == None:
                return None
            tmpDateTime = datetime.datetime.combine(datetime.date.today(), p.expr)
            return tmpDateTime.utcoffset()
        return None

    @_('PERIOD NAME')
    def listSelect(self, p):
        return p.NAME

    @_('expr listSelect')
    def expr(self, p):
        ''' select value(s) for name p.listSelect from a list of contexts '''
        key = p.listSelect
        if isinstance(p.expr, list):
            retList = []
            for i in range(len(p.expr)):
                if not isinstance(p.expr[i], dict):
                    continue
                if key in p.expr[i]:
                    retList.append(p.expr[i][key])
            return retList
        elif isinstance(p.expr, dict):
            if key in p.expr:
                return p.expr[key]
            else:
                return None
        elif isinstance(p.expr, datetime.date):         # True for both dates and datetimes
            if type(p.expr) is datetime.datetime:           # Only true for datetimes
                if key == 'year':
                    return p.expr.year
                elif key == 'month':
                    return p.expr.month
                elif key == 'day':
                    return p.expr.day
                elif key == 'weekday':
                    return p.expr.weekday()
                elif key == 'hour':
                    return p.expr.hour
                elif key == 'minute':
                    return p.expr.minute
                elif key == 'second':
                    return p.expr.second
                elif key == 'timezone':
                    if p.expr.tzinfo == None:
                        return None
                    return p.expr.tzname()
                elif key == 'time_offset':
                    if p.expr.tzinfo == None:
                        return None
                    return p.expr.utcoffset()
                else:
                    return None
            else:                                           # datetime.date
                if key == 'year':
                    return p.expr.year
                elif key == 'month':
                    return p.expr.month
                elif key == 'day':
                    return p.expr.day
                elif key == 'weekday':
                    return p.expr.weekday()
                else:
                    return None
        elif isinstance(p.expr, datetime.time):
            if key == 'hour':
                return p.expr.hour
            elif key == 'minute':
                return p.expr.minute
            elif key == 'second':
                return p.expr.second
            elif key == 'timezone':
                if p.expr.tzinfo == None:
                    return None
                tmpDateTime = datetime.datetime.combine(datetime.date.today(), p.expr)
                return tmpDateTime.tzname()
            elif key == 'time_offset':
                if p.expr.tzinfo == None:
                    return None
                tmpDateTime = datetime.datetime.combine(datetime.date.today(), p.expr)
                return tmpDateTime.utcoffset()
            else:
                return None
        elif isinstance(p.expr, datetime.timedelta):
            if key == 'days':
                return int(p.expr.total_seconds() / 60 / 60 / 24)
            elif key == 'hours':
                return int(p.expr.total_seconds() / 60 / 60) % 24
            elif key == 'minutes':
                return int(p.expr.total_seconds() / 60) % 60
            elif key == 'seconds':
                return p.expr.total_seconds() % 60
            else:
                return None
        elif isinstance(p.expr, int):           # Year, month duration
            if key == 'years':
                return int(p.expr / 12)
            elif key == 'months':
                return p.expr % 12
            else:
                return None
        elif isinstance(p.expr, tuple) and (len(p.expr) == 4):
            (end0, low0, high1, end1) = p.expr
            if key == 'start':
                return low0
            elif key == 'end':
                return high1
            else:
                return None
        return None            

    @_('expr LTTHANEQUAL expr')
    def expr(self, p):
        if (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            x0 = p.expr0[0]
        else:
            x0 = p.expr0
        if (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            x1 = p.expr1[0]
        else:
            x1 = p.expr1
        try:
            return x0 <= x1
        except:
            False

    @_('expr LTTHAN expr')
    def expr(self, p):
        if (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            x0 = p.expr0[0]
        else:
            x0 = p.expr0
        if (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            x1 = p.expr1[0]
        else:
            x1 = p.expr1
        try:
            return x0 < x1
        except:
            False

    @_('expr GTTHANEQUAL expr')
    def expr(self, p):
        if (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            x0 = p.expr0[0]
        else:
            x0 = p.expr0
        if (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            x1 = p.expr1[0]
        else:
            x1 = p.expr1
        try:
            return x0 >= x1
        except:
            False

    @_('expr GTTHAN expr')
    def expr(self, p):
        if (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            x0 = p.expr0[0]
        else:
            x0 = p.expr0
        if (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            x1 = p.expr1[0]
        else:
            x1 = p.expr1
        try:
            return x0 > x1
        except:
            False

    @_('expr BETWEEN expr')
    def betweenExpr(self, p):
        return (p.expr0, p.expr1)

    @_('AND expr')
    def andExpr(self, p):
        return p.expr

    @_('betweenExpr andExpr')
    def expr(self, p):
        (expr0, expr1) = p.betweenExpr
        if (isinstance(expr0, list) and (len(expr0) == 1)):
            if (isinstance(expr1, list) and (len(expr1) == 1)):
                if (isinstance(p.andExpr, list) and (len(p.andExpr) == 1)):
                    return (expr0[0] > expr1[0]) and (expr0[0] < p.andExpr[0])
            else:
                    return (expr0[0] > expr1[0]) and (expr0[0] < p.andExpr)
        elif (isinstance(expr1, list) and (len(expr1) == 1)):
            if (isinstance(p.andExpr, list) and (len(p.andExpr) == 1)):
                return (expr0 > expr1[0]) and (expr0 < p.andExpr[0])
            else:
                return (expr0 > expr1[0]) and (expr0 < p.andExpr)
        elif (isinstance(p.andExpr, list) and (len(p.andExpr) == 1)):
            return (expr0 > expr1) and (expr0 < p.andExpr[0])
        else:
            return (expr0 > expr1) and (expr0 < p.andExpr)

    @_('expr andExpr')
    def expr(self, p):
        if isinstance(p.expr, bool):
            if isinstance(p.andExpr, bool):
                return p.expr and p.andExpr  # True/True, True/False, False/True, False/False
            elif not p.expr:
                return False    # False/Otherwise
            else:
                return None     # True/Otherwise
        elif isinstance(p.andExpr, bool):
            if not p.andExpr:
                return False    # Otherwise/False
            else:
                return None     # Otherwise/True
        else:
            return None         # Otherwise/Otherwise

    @_('expr OR expr')
    def expr(self, p):
        if isinstance(p.expr0, bool):
            if isinstance(p.expr1, bool):
                return p.expr0 or p.expr1  # True/True, True/False, False/True, False/False
            elif p.expr0:       # True/Otherwise
                return True
            else:               # False/Otherwise
                return None
        else:
            if isinstance(p.expr1, bool):
                if p.expr1:     # Otherwise/True
                    return True
                else:           # Otherwise/False
                    return None
            return None         # Otherwise/Otherwise

    @_('NOT expr %prec UMINUS')
    def expr(self, p):
        if isinstance(p.expr, bool):
            return not p.expr
        else:
            None

    @_('LBRACKET expr')
    def listStart(self, p):
        return [p.expr]

    @_('COMMA expr')
    def listPart(self, p):
        return [p.expr]

    @_('listPart COMMA expr')
    def listPart(self, p):
        if isinstance(p.expr, list):
            if (len(p.expr) > 0):
                retval = p.listPart
                retval.append(p.expr)
                return retval
            else:
                 return p.listPart + p.expr
        else:
            return p.listPart + [p.expr]

    @_('NAME COLON expr')
    def contextPart(self, p):
        return {p.NAME:p.expr}

    @_('contextPart COMMA NAME COLON expr')
    def contextPart(self, p):
        p.contextPart[p.NAME] = p.expr
        return p.contextPart

    @_('LPAREN expr ELLIPSE expr RPAREN')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, p.RPAREN)

    @_('LPAREN expr ELLIPSE expr RBRACKET')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, p.RBRACKET)

    @_('LPAREN expr ELLIPSE expr LBRACKET')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, p.LBRACKET)

    @_('listStart ELLIPSE expr RPAREN')
    def expr(self, p):
        return ('[', p.listStart[0], p.expr, p.RPAREN)

    @_('listStart ELLIPSE expr RBRACKET')
    def expr(self, p):
        return ('[', p.listStart[0], p.expr, p.RBRACKET)

    @_('listStart ELLIPSE expr LBRACKET')
    def expr(self, p):
        return ('[', p.listStart[0], p.expr, p.LBRACKET)

    @_('LCURLY contextPart RCURLY')
    def expr(self, p):
        return p.contextPart

    @_('RBRACKET expr ELLIPSE expr RPAREN')
    def expr(self, p):
        return (p.RBRACKET, p.expr0, p.expr1, p.RPAREN)

    @_('RBRACKET expr ELLIPSE expr RBRACKET')
    def expr(self, p):
        return (p.RBRACKET0, p.expr0, p.expr1, p.RBRACKET1)

    @_('RBRACKET expr ELLIPSE expr LBRACKET')
    def expr(self, p):
        return (p.RBRACKET, p.expr0, p.expr1, p.LBRACKET)

    @_('listStart RBRACKET')
    def expr(self, p):
        return p.listStart

    @_('listStart listPart RBRACKET')
    def expr(self, p):
        if p.listStart is None:
            if p.listPart is None:
                return []
            else:
                return p.listPart
        elif p.listPart is None:
            return p.listStart
        if isinstance(p.listPart, list):
            return p.listStart + p.listPart
        return p.listStart + [p.listPart]

    @_('DATEFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert datetime.date/datetime.time/str into datetime.date '''
        if isinstance(p.expr, datetime.time):
            return datetime.date(year=0, month=0, day=0)
        elif isinstance(p.expr, datetime.date):         # True for both dates and datetimes
            if type(p.expr) is datetime.datetime:           # Only true for datetimes
                return p.expr.date()
            else:
                return p.expr
        elif isinstance(p.expr, str):
            try:
                return dateutil.parser.parse(p.expr).date()
            except:
                return None
        else:
            return None

    @_('DATEFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Convert year, month, day into datetime.date '''
        try:
            return datetime.date(year=int(p.expr0), month=int(p.expr1), day=int(p.expr2))
        except:
            return None

    @_('TIMEFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Convert hour, minute, second into datetime.time '''
        hour = int(p.expr0)
        min = int(p.expr1)
        sec = int(p.expr2)
        while sec < 0:
            sec += 60
            min -= 1
        while sec > 59:
            sec -= 60
            min += 1
        while min < 0:
            min += 60
            hour -= 1
        while min > 59:
            min -= 60
            hour += 1
        hour %= 24
        try:
            return datetime.time(hour=int(hour), minute=int(min), second=int(sec))
        except:
            return None

    @_('TIMEFUNC expr COMMA expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Convert hour, minute, second, offset into datetime.time '''
        hour = int(p.expr0)
        min = int(p.expr1)
        sec = int(p.expr2)
        while sec < 0:
            sec += 60
            min -= 1
        while sec > 59:
            sec -= 60
            min += 1
        while min < 0:
            min += 60
            hour -= 1
        while min > 59:
            min -= 60
            hour += 1
        hour %= 24
        thisTime = '%02d:%02d:%02d' % (hour, min, sec)
        if isinstance(p.expr3, datetime.timedelta):
            offset = p.expr3.total_seconds()
            if offset > 0:
                sign = '+'
            else:
                sign = '-'
                offset = -offset
            HH = int(offset / 60 / 60)
            MM = int(offset / 60) % 60
            thisTime += sign + '%02d:%02d' % (HH, MM)
        try:
            return datetime.time.fromisoformat(thisTime)
        except:
            return None

    @_('TIMEFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert datetime.date/datetime.time/str into datetime.time '''
        if isinstance(p.expr, datetime.time):
            return p.expr
        elif isinstance(p.expr, datetime.date):             # True for dates and datetimes
            if type(p.expr) is datetime.datetime:               # Only true for datetimes
                return p.expr.timetz()
            else:                                               # A date - return midnight
                return datetime.time(hour=0, minute=0, second=0)
        elif isinstance(p.expr, str):
            parts = p.expr.split('@')
            try:
                thisTime =  dateutil.parser.parse(parts[0]).timetz()     # A time with timezone
            except:
                return None
            if len(parts) == 1:
                return thisTime
            thisZone = dateutil.tz.gettz(parts[1])
            if thisZone is None:
                return thisTime
            try:
                retTime = thisTime.replace(tzinfo=thisZone)
            except:
                return thisTime
            return retTime
        return None

    @_('DATEANDTIMEFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Convert date, time into datetime.datetime '''
        if isinstance(p.expr0, datetime.date) and (type(p.expr0) is datetime.date):
            if isinstance(p.expr1, datetime.time):
                return datetime.datetime.combine(p.expr0, p.expr1)
        return None

    @_('DATEANDTIMEFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert str into datetime.datetime '''
        if isinstance(p.expr, str):
            parts = p.expr.split('@')
            try:
                thisDateTime = dateutil.parser.parse(parts[0])
            except:
                return None
            if len(parts) == 1:
                return thisDateTime
            thisZone = dateutil.tz.gettz(parts[1])
            if thisZone is None:
                return thisDateTime
            try:
                retDateTime = thisDateTime.replace(tzinfo=thisZone)
            except:
                return thisDateTime
            return retDateTime
        return None

    @_('NUMBERFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Float from formatted string'''
        number = p.expr0
        grouping = p.expr1
        decimal = p.expr2
        if not isinstance(number, str):
            return None
        if grouping is not None:
            if not isinstance(grouping, str):
                return None
            if grouping not in [' ', ',', '.']:
                return None
        if decimal is not None:
            if not isinstance(decimal, str):
                return None
            if decimal not in ['.', ',']:
                return None
        if (grouping is not None) and (decimal is not None) and (grouping == decimal):
            return None
        if grouping is not None:
            number = number.replace(grouping, '')
        if decimal is not None:
            parts = number.split(decimal)
            if len(parts) > 2:
                return None
            elif len(parts) == 2:
                return float(parts[0]) + float(parts[1])/10.0
            else:
                return float(number)
        else:
            return float(number)

    @_('STRINGFUNC expr RPAREN')
    def expr(self, p):
        ''' string from value'''
        if p.expr == None:
            return 'null'
        if isinstance(p.expr, bool):
            if p.expr:
                return 'true'
            else:
                return 'false'
        if isinstance(p.expr, float):
            return str(p.expr)
        if isinstance(p.expr, str):
            return p.expr
        if isinstance(p.expr, datetime.date):         # True for both dates and datetimes
            if type(p.expr) is datetime.datetime:           # Only true for datetimes
                return p.expr.isoformat(sep='T')
            else:
                return p.expr.isoformat()
        if isinstance(p.expr, datetime.time):
            return p.expr.isoformat()
        if isinstance(p.expr, datetime.timedelta):
            duration = p.expr.total_seconds()
            secs = duration % 60
            duration = int(duration / 60)
            mins = duration % 60
            duration = int(duration / 60)
            hours = duration % 24
            days = int(duration / 24)
            return 'P%dDT%dH%dM%dS' % (days, hours, mins, secs)
        if isinstance(p.expr, int):                  # Year, month duration
            year = int(p.expr / 12)
            month = p.expr % 12
            return 'P%dY%dM' % (year, month)
        return None

    @_('NOTFUNC expr RPAREN')
    def expr(self, p):
        ''' negate a boolean'''
        if not isinstance(p.expr, bool):
            return None
        return not p.expr

    def inFunc(self, thisList):
        # This is the 'in()' function where the parameters are a list of tests
        # The first item in thisList is tested against each of the remaining items in thisList
        # The in() function returns True if one of those test is True
        inValue = thisList[0]
        for i in range(1,len(thisList)):
            if isinstance(thisList[i], tuple) and (len(thisList[i]) == 4):
                # This test is 'in a range'
                (end0, lowVal, highVal, end1) = thisList[i]
                if isinstance(inValue, str):
                    if not isinstance(lowVal, str) or not isinstance(highVal, str):
                        continue
                elif isinstance(inValue, int):              # a list of Year, month durations
                    if not isinstance(lowVal, int) or not isinstance(highVal, int):
                        continue
                elif isinstance(inValue, float):
                    if not isinstance(lowVal, float) or not isinstance(highVal, float):
                        continue
                elif isinstance(inValue, datetime.date):            # True for both dates and datetimes
                    if not isinstance(lowVal, datetime.date) or not isinstance(highVal, datetime.date):
                        continue
                elif isinstance(inValue, datetime.timedelta):
                    if not isinstance(lowVal, datetime.timedelta) or not isinstance(highVal, datetime.timedelta):
                        continue
                else:
                    continue
                if lowVal > inValue:
                    continue
                if highVal < inValue:
                    continue
                if (end0 != '[') and (lowVal == inValue):
                    continue
                if (end1 != ']') and (highVal == inValue):
                    continue
                return True
            else:
                if not isinstance(thisList[i], tuple):
                    continue
                (comparitor, toValue) = thisList[i]
                if comparitor == '=':
                    try:
                        if(inValue == toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '<=':
                    try:
                        if(inValue <= toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '<':
                    try:
                        if(inValue < toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '>=':
                    try:
                        if(inValue >= toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '>':
                    try:
                        if(inValue > toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '!=':
                    try:
                        if(inValue != toValue):
                            return True
                    except:
                        pass
                    continue
        return False

    @_('expr INFUNC expr')
    def inStart(self, p):
        ''' item in list of items'''
        if isinstance(p.expr1, list):
            thisList = []
            for i in range(len(p.expr1)):
                thisList.append([('=', p.expr1[i])])
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('=', p.expr1)]

    @_('expr INFUNC LTTHANEQUAL expr')
    def inStart(self, p):
        ''' item <= list of items'''
        if isinstance(p.expr1, list):
            thisList = []
            for i in range(len(p.expr1)):
                thisList.append([('<=', p.expr1[i])])
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('<=', p.expr1)]

    @_('expr INFUNC LTTHAN expr')
    def inStart(self, p):
        ''' item < list of items'''
        if isinstance(p.expr1, list):
            thisList = []
            for i in range(len(p.expr1)):
                thisList.append([('<', [p.expr1][i])])
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('<', p.expr1)]

    @_('expr INFUNC GTTHANEQUAL expr')
    def inStart(self, p):
        ''' item >= list of items'''
        if isinstance(p.expr1, list):
            thisList = []
            for i in range(len(p.expr1)):
                thisList.append([('>=', p.expr1[i])])
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('>=', p.expr1)]

    @_('expr INFUNC GTTHAN expr')
    def inStart(self, p):
        ''' item > list of items'''
        if isinstance(p.expr1, list):
            thisList = []
            for i in range(len(p.expr1)):
                thisList.append([('>', p.expr1[i])])
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('>', p.expr1)]

    @_('expr INFUNC EQUALS expr')
    def inStart(self, p):
        ''' item = list of items'''
        if isinstance(p.expr1, list):
            thisList = []
            for i in range(len(p.expr1)):
                thisList.append([('=', p.expr1[i])])
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('=', p.expr1)]

    @_('expr INFUNC NOTEQUALS expr')
    def inStart(self, p):
        ''' item != list of items'''
        if isinstance(p.expr1, list):
            thisList = []
            for i in range(len(p.expr1)):
                thisList.append([('!=', p.expr1[i])])
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('!=', p.expr1)]

    @_('COMMA LTTHANEQUAL expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('<=', p.expr[i])])
            return thisList
        else:
            return [('<=', p.expr)]

    @_('COMMA LTTHAN expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('<', p.expr[i])])
            return thisList
        else:
            return [('<', p.expr)]

    @_('COMMA GTTHANEQUAL expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('>=', p.expr[i])])
            return thisList
        else:
            return [('>=', p.expr)]

    @_('COMMA GTTHAN expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('>', p.expr[i])])
            return thisList
        else:
            return [('>', p.expr)]

    @_('COMMA NOTEQUALS expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('!=', p.expr[i])])
            return thisList
        else:
            return [('!=', p.expr)]

    @_('COMMA EQUALS expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('=', p.expr[i])])
            return thisList
        else:
            return [('=', p.expr)]

    @_('inPart COMMA LTTHANEQUAL expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('<=', p.expr[i])])
            return p.inPart + thisList
        else:
            return p.inPart + [('<=', p.expr)]

    @_('inPart COMMA LTTHAN expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('<', p.expr[i])])
            return p.inPart + thisList
        else:
            return p.inPart + [('<', p.expr)]

    @_('inPart COMMA GTTHANEQUAL expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('>=', p.expr[i])])
            return p.inPart + thisList
        else:
            return p.inPart + [('>=', p.expr)]

    @_('inPart COMMA GTTHAN expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('>', p.expr[i])])
            return p.inPart + thisList
        else:
            return p.inPart + [('>', p.expr)]

    @_('inPart COMMA NOTEQUALS expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('!=', p.expr[i])])
            return p.inPart + thisList
        else:
            return p.inPart + [('!=', p.expr)]

    @_('inPart COMMA EQUALS expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('=', p.expr[i])])
            return p.inPart + thisList
        else:
            return p.inPart + [('=', p.expr)]

    @_('inPart COMMA expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = []
            for i in range(len(p.expr)):
                thisList.append([('=', p.expr[i])])
            return p.inPart + thisList
        else:
            return p.inPart + [('=', p.expr)]

    @_('listPart COMMA LTTHANEQUAL expr')
    def inPart(self, p):
        thisList = []
        for i in range(len(p.listPart)):
            thisList.append(('<=', p.listPart[i]))
        if isinstance(p.expr, list):
            for i in range(len(p.expr)):
                thisList.append([('<=', p.expr[i])])
        else:
            thisList.append([('<=', p.expr)])
        return thisList

    @_('listPart COMMA LTTHAN expr')
    def inPart(self, p):
        thisList = []
        for i in range(len(p.listPart)):
            thisList.append(('<', p.listPart[i]))
        if isinstance(p.expr, list):
            for i in range(len(p.expr)):
                thisList.append([('<', p.expr[i])])
        else:
            thisList.append([('<', p.expr)])
        return thisList

    @_('listPart COMMA GTTHANEQUAL expr')
    def inPart(self, p):
        thisList = []
        for i in range(len(p.listPart)):
            thisList.append(('>=', p.listPart[i]))
        if isinstance(p.expr, list):
            for i in range(len(p.expr)):
                thisList.append([('>=', p.expr[i])])
        else:
            thisList.append([('>=', p.expr)])
        return thisList

    @_('listPart COMMA GTTHAN expr')
    def inPart(self, p):
        thisList = []
        for i in range(len(p.listPart)):
            thisList.append(('>', p.listPart[i]))
        if isinstance(p.expr, list):
            for i in range(len(p.expr)):
                thisList.append([('>', p.expr[i])])
        else:
            thisList.append([('>', p.expr)])
        return thisList

    @_('listPart COMMA NOTEQUALS expr')
    def inPart(self, p):
        thisList = []
        for i in range(len(p.listPart)):
            thisList.append(('!=', p.listPart[i]))
        if isinstance(p.expr, list):
            for i in range(len(p.expr)):
                thisList.append([('!=', p.expr[i])])
        else:
            thisList.append([('!=', p.expr)])
        return thisList

    @_('listPart COMMA EQUALS expr')
    def inPart(self, p):
        thisList = []
        for i in range(len(p.listPart)):
            thisList.append(('=', p.listPart[i]))
        if isinstance(p.expr, list):
            for i in range(len(p.expr)):
                thisList.append([('=', p.expr[i])])
        else:
            thisList.append([('=', p.expr)])
        return thisList

    @_('inStart listPart RPAREN')
    def expr(self, p):
        partList = []
        for i in range(len(p.listPart)):
            partList.append(('=', p.listPart[i]))
        thisList = p.inStart + partList
        return self.inFunc(thisList)

    @_('inStart inPart RPAREN')
    def expr(self, p):
        thisList = p.inStart + p.inPart
        return self.inFunc(thisList)

    @_('inStart RPAREN')
    def expr(self, p):
        thisList = p.inStart
        return self.inFunc(thisList)

    @_('inStart ELLIPSE expr RPAREN')
    def expr(self, p):
        thisList = p.inStart
        (comparitor, lowVal) = thisList[1]
        thisList[1] = ('(', lowVal, p.expr, ')')
        return self.inFunc(thisList)

    @_('inStart ELLIPSE expr RBRACKET')
    def expr(self, p):
        thisList = p.inStart
        (comparitor, lowVal) = thisList[1]
        thisList[1] = ('(', lowVal, p.expr, ']')
        return self.inFunc(thisList)

    @_('inStart ELLIPSE expr LBRACKET')
    def expr(self, p):
        thisList = p.inStart
        (comparitor, lowVal) = thisList[1]
        thisList[1] = ('(', lowVal, p.expr, '[')
        return self.inFunc(thisList)

    @_('SUBSTRINGFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' substring from a substring'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, float) or (int(p.expr1) != p.expr1):
            return None
        if not isinstance(p.expr2, float) or (int(p.expr2) != p.expr2) or (p.expr2 < 0):
            return None
        start = int(p.expr1)
        length = int(p.expr2)
        if start == 0:
           return None
        elif start > 0:
            return p.expr0[start - 1:start - 1 + length]
        else:
            if abs(start) <= length:
                return p.expr0[start:]
            return p.expr0[start:start + length]
 
    @_('SUBSTRINGFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' substring from a string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, float) or (int(p.expr1) != p.expr1):
            return None
        start = int(p.expr1)
        if start == 0:
            return None
        elif start > 0:
            return p.expr0[start - 1:]
        else:
            return p.expr0[start:]


    @_('STRINGLENFUNC expr RPAREN')
    def expr(self, p):
        ''' length of a string'''
        if not isinstance(p.expr, str):
            return None
        return float(len(p.expr))

    @_('UPPERCASEFUNC expr RPAREN')
    def expr(self, p):
        ''' uppercase of a string'''
        if not isinstance(p.expr, str):
            return None
        return p.expr.upper()

    @_('LOWERCASEFUNC expr RPAREN')
    def expr(self, p):
        ''' lowercase of a string'''
        if not isinstance(p.expr, str):
            return None
        return p.expr.lower()

    @_('SUBSTRINGBEFOREFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' substring before string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        subAt = p.expr0.find(p.expr1)
        if subAt == -1:
            return ''
        return p.expr0[:subAt] 

    @_('SUBSTRINGAFTERFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' substring after string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        subAt = p.expr0.find(p.expr1)
        if subAt == -1:
            return ''
        return p.expr0[subAt + len(p.expr1):]

    @_('REPLACEFUNC expr COMMA expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' replace substring in string with flags'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        if not isinstance(p.expr2, str):
            return None
        if not isinstance(p.expr3, str):
            return None
        reFlags = 0
        if 's' in p.expr3:
            reFlags += re.S
        if 'm' in p.expr3:
            reFlags += re.M
        if 'i' in p.expr3:
            reFlags += re.I
        if 'x' in p.expr3:
            reFlags += re.X
        replace = p.expr2
        replace = re.sub(pattern=r'\$(\d+)', repl=r'\\\1', string=replace)    # Convert SFEEL regular expressions to Python
        return re.sub(pattern=p.expr1, repl=replace, string=p.expr0, flags=reFlags)

    @_('REPLACEFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' replace substring in string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        if not isinstance(p.expr2, str):
            return None
        reFlags = 0
        replace = p.expr2
        replace = re.sub(pattern=r'\$(\d+)', repl=r'\\\1', string=replace)    # Convert SFEEL regular expressions to Python
        return re.sub(pattern=p.expr1, repl=replace, string=p.expr0, flags=reFlags)

    @_('CONTAINSFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' string contain substring'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        return p.expr1 in p.expr0

    @_('STARTSWITHFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' string start with substring'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        return p.expr0.startswith(p.expr1)

    @_('ENDSWITHFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' string ends with substring'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        return p.expr0.endswith(p.expr1)

    @_('MATCHESFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' string re matchs string with flags'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        if not isinstance(p.expr2, str):
            return None
        reFlags = 0
        if 's' in p.expr2:
            reFlags += re.S
        if 'm' in p.expr2:
            reFlags += re.M
        if 'i' in p.expr2:
            reFlags += re.I
        if 'x' in p.expr2:
            reFlags += re.X
        thisMatch = re.match(p.expr1, p.expr0, flags=reFlags)
        if thisMatch is not None:
            return True
        return False

    @_('MATCHESFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' string re match string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        reFlags = 0
        thisMatch = re.match(p.expr1, p.expr0, flags=reFlags)
        if thisMatch is not None:
            return True
        return False

    @_('SPLITFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' split string on pattern'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        return re.split(p.expr1, p.expr0)

    @_('LISTCONTAINSFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' list contains value'''
        if not isinstance(p.expr0, list):
            return None
        return p.expr1 in p.expr0

    @_('COUNTFUNC expr RPAREN')
    def expr(self, p):
        ''' count of list items'''
        if not isinstance(p.expr, list):
            return None
        return float(len(p.expr))

    def minFunc(self, thisList):
        minValue = None
        for i in range(len(thisList)):
            if minValue is None:
                minValue = thisList[i]
            elif type(minValue) != type(thisList[i]):
                return None
            elif thisList[i] < minValue:
                minValue = thisList[i]
        return minValue

    @_('MINFUNC expr')
    def minStart(self, p):
        ''' minimum item in list items'''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('minStart listPart RPAREN')
    def expr(self, p):
        thisList = p.minStart + p.listPart
        return self.minFunc(thisList)

    @_('minStart RPAREN')
    def expr(self, p):
        thisList = p.minStart
        return self.minFunc(thisList)

    def maxFunc(self, thisList):
        maxValue = None
        for i in range(len(thisList)):
            if maxValue is None:
                maxValue = thisList[i]
            elif type(maxValue) != type(thisList[i]):
                return None
            elif thisList[i] > maxValue:
                maxValue = thisList[i]
        return maxValue

    @_('MAXFUNC expr')
    def maxStart(self, p):
        ''' maximum item in list items'''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('maxStart listPart RPAREN')
    def expr(self, p):
        thisList = p.maxStart + p.listPart
        return self.maxFunc(thisList)

    @_('maxStart RPAREN')
    def expr(self, p):
        thisList = p.maxStart
        return self.maxFunc(thisList)

    def sumFunc(self, thisList):
        sumValue = 0.0
        if len(thisList) == 0:
            return None
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
            sumValue += thisList[i]
        return sumValue

    @_('SUMFUNC expr')
    def sumStart(self, p):
        ''' sum of items in list items'''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('sumStart listPart RPAREN')
    def expr(self, p):
        thisList = p.sumStart + p.listPart
        return self.sumFunc(thisList)

    @_('sumStart RPAREN')
    def expr(self, p):
        thisList = p.sumStart
        return self.sumFunc(thisList)

    def mean(self, thisList):
        if len(thisList) == 0:
            return None
        try:
            return statistics.fmean(thisList)
        except:
            return None

    @_('MEANFUNC expr')
    def meanStart(self, p):
        ''' mean of items in list items'''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('meanStart listPart RPAREN')
    def expr(self, p):
        thisList = p.meanStart + p.listPart
        return self.mean(thisList)

    @_('meanStart RPAREN')
    def expr(self, p):
        thisList = p.meanStart
        return self.mean(thisList)

    def allFunc(self, thisList):
        if len(thisList) == 0:
            return True
        for i in range(len(thisList)):
            if not isinstance(thisList[i], bool):
                if thisList[i] is None:
                    return False
                else:
                    return None
            if not thisList[i]:
                return False
        return True

    @_('ALLFUNC expr')
    def allStart(self, p):
        ''' all items in list are true '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('allStart listPart RPAREN')
    def expr(self, p):
        thisList = p.allStart + p.listPart
        return self.allFunc(thisList)

    @_('allStart RPAREN')
    def expr(self, p):
        thisList = p.allStart
        return self.allFunc(thisList)

    def anyFunc(self, thisList):
        if len(thisList) == 0:
            return False
        for i in range(len(thisList)):
            if isinstance(thisList[i], bool):
                if thisList[i]:
                    return True
            elif thisList[i] is None:
                continue
            else:
                return None
        return False

    @_('ANYFUNC expr')
    def anyStart(self, p):
        ''' any item in list is true '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('anyStart listPart RPAREN')
    def expr(self, p):
        thisList = p.anyStart + p.listPart
        return self.anyFunc(thisList)

    @_('anyStart RPAREN')
    def expr(self, p):
        thisList = p.anyStart
        return self.anyFunc(thisList)

    @_('SUBLISTFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' sublist from a list with start and end '''
        if not isinstance(p.expr0, list):
            return None
        if not isinstance(p.expr1, float):
            return None
        if not isinstance(p.expr2, float):
            return None
        start = int(p.expr1) - 1
        length = int(p.expr2)
        if start >= 0:
            if start + length < len(p.expr0):
                return p.expr0[start:start + length]
            elif start + length == len(p.expr0):
                return p.expr0[start:]
            else:
                return None
        else:
            if abs(start) > len(p.expr0):
                return None
            if abs(start) < length:
                return None
            if start + length > 0:
                return p.expr0[start:start + length]
            elif start + length == 0:
                return p.expr0[start:]
            else:
                return None

    @_('SUBLISTFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' sublist from a list from start '''
        if not isinstance(p.expr0, list):
            return None
        if not isinstance(p.expr1, float):
            return None
        start = int(p.expr1) - 1
        if abs(start) < len(p.expr0):
            return p.expr0[start:]
        else:
            return None

    @_('APPENDFUNC expr')
    def appendStart(self, p):
        ''' append item(s) to a list '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('appendStart listPart RPAREN')
    def expr(self, p):
        return p.appendStart + p.listPart

    @_('appendStart RPAREN')
    def expr(self, p):
        return p.appendStart

    @_('CONCATENATEFUNC expr')
    def concatenateStart(self, p):
        ''' concatenate lists '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('concatenateStart listPart RPAREN')
    def expr(self, p):
        retval = p.concatenateStart
        for i in range(len(p.listPart)):
            retval += p.listPart[i]
        return retval

    @_('concatenateStart RPAREN')
    def expr(self, p):
        return p.concatenateStart

    @_('INSERTBEFOREFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' insert before in list '''
        if not isinstance(p.expr0, list):
            return None
        if not isinstance(p.expr1, float):
            return None
        insertAt = int(p.expr1) - 1
        if insertAt < 0:
            return None
        if insertAt > len(p.expr0):
            return None
        p.expr0.insert(insertAt, p.expr2)
        return p.expr0

    @_('REMOVEFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' remove from a list an item '''
        if not isinstance(p.expr0, list):
            return None
        if not isinstance(p.expr1, float):
            return None
        removeAt = int(p.expr1) - 1
        if removeAt < 0:
            return None
        if removeAt >= len(p.expr0):
            return None
        if removeAt == 0:
            return p.expr0[1:]
        elif removeAt == len(p.expr0) - 1:
            return p.expr0[:-1]
        else:
            return p.expr0[:removeAt] + p.expr0[removeAt + 1:]

    @_('REVERSEFUNC expr RPAREN')
    def expr(self, p):
        ''' reverse a list '''
        if not isinstance(p.expr, list):
            return None
        newList = p.expr[:]
        newList.reverse()
        return newList

    @_('INDEXOFFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' list of indexes of a value in a list '''
        if not isinstance(p.expr0, list):
            return None
        newList = []
        for i in range(len(p.expr0)):
            if p.expr0[i] == p.expr1:
                newList.append(i + 1)
        return newList

    def unionFunc(self, thisList):
        newList = []
        for i in range(len(thisList)):
            if thisList[i] not in newList:
                newList.append(thisList[i])
        return newList

    @_('UNIONFUNC expr')
    def unionStart(self, p):
        ''' union lists '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('unionStart listPart RPAREN')
    def expr(self, p):
        retval = []
        for i in range(len(p.unionStart)):
            if p.unionStart[i] not in retval:
                retval.append(p.unionStart[i])
        for i in range(len(p.listPart)):
            for j in range(len(p.listPart[i])):
                if p.listPart[i][j] not in retval:
                    retval.append(p.listPart[i][j])
        return retval

    @_('unionStart RPAREN')
    def expr(self, p):
        thisList = p.unionStart
        return self.unionFunc(thisList)

    @_('DISTINCTVALUESFUNC expr RPAREN')
    def expr(self, p):
        ''' distinct list items '''
        if not isinstance(p.expr, list):
            return None
        newList = []
        for i in range(len(p.expr)):
            if p.expr[i] not in newList:
                newList.append(p.expr[i])
        return newList

    def flatten(self, this):
        newList = []
        for i in range(len(this)):
            if isinstance(this[i], list):
                newList += self.flatten(this[i])
            else:
                newList.append(this[i])
        return newList

    @_('FLATTENFUNC expr RPAREN')
    def expr(self, p):
        ''' flattern a list of lists '''
        if not isinstance(p.expr, list):
            return None
        newList = self.flatten(p.expr)
        return newList

    def product(self, thisList):
        product = 1.0
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
            product *= thisList[i]
        return product

    @_('PRODUCTFUNC expr')
    def productStart(self, p):
        ''' product of numbers in a list of numbers '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('productStart listPart RPAREN')
    def expr(self, p):
        thisList = p.productStart + p.listPart
        return self.product(thisList)

    @_('productStart RPAREN')
    def expr(self, p):
        thisList = p.productStart
        return self.product(thisList)

    def median(self, thisList):
        try:
            return float(statistics.median(thisList))
        except:
            return None

    @_('MEDIANFUNC expr')
    def medianStart(self, p):
        ''' median item in list of numbers '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('medianStart listPart RPAREN')
    def expr(self, p):
        thisList = p.medianStart + p.listPart
        return self.median(thisList)

    @_('medianStart RPAREN')
    def expr(self, p):
        thisList = p.medianStart
        return self.median(thisList)

    def stddev(self, thisList):
        try:
            return float(statistics.stdev(thisList))
        except:
            return None

    @_('STDDEVFUNC expr')
    def stddevStart(self, p):
        ''' stddev of a list of numbers '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('stddevStart listPart RPAREN')
    def expr(self, p):
        thisList = p.stddevStart + p.listPart
        return self.stddev(thisList)

    @_('stddevStart RPAREN')
    def expr(self, p):
        thisList = p.stddevStart
        return self.stddev(thisList)

    def mode(self, thisList):
        try:
            thisMode = statistics.multimode(thisList)
        except:
            return None
        if isinstance(thisMode, list):
            return sorted(thisMode)
        else:
            return thisMode

    @_('MODEFUNC expr')
    def modeStart(self, p):
        ''' mode number in list of numbers '''
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('modeStart listPart RPAREN')
    def expr(self, p):
        thisList = p.modeStart + p.listPart
        return self.mode(thisList)

    @_('modeStart RPAREN')
    def expr(self, p):
        thisList = p.modeStart
        return self.mode(thisList)

    @_('DECIMALFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' scale a number '''
        if not isinstance(p.expr0, float):
            return None
        if not isinstance(p.expr1, float):
            return None
        if int(p.expr1) != p.expr1:
            return None
        return round(p.expr0, int(p.expr1))

    @_('FLOORFUNC expr RPAREN')
    def expr(self, p):
        ''' floor of a number '''
        if not isinstance(p.expr, float):
            return None
        return float(math.floor(p.expr))
        
    @_('CEILINGFUNC expr RPAREN')
    def expr(self, p):
        ''' ceiling of a number '''
        if not isinstance(p.expr, float):
            return None
        return float(math.ceil(p.expr))
        
    @_('ABSFUNC expr RPAREN')
    def expr(self, p):
        ''' absolute of a number '''
        if isinstance(p.expr, float) or isinstance(p.expr, int) or isinstance(p.expr, datetime.timedelta):
            return abs(p.expr)
        return None
        
    @_('MODULOFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' scale a number '''
        if not isinstance(p.expr0, float):
            return None
        if not isinstance(p.expr1, float):
            return None
        return float(p.expr0 % p.expr1)

    @_('SQRTFUNC expr RPAREN')
    def expr(self, p):
        ''' absolute of a number '''
        if not isinstance(p.expr, float):
            return None
        return float(math.sqrt(p.expr))
        
    @_('LOGFUNC expr RPAREN')
    def expr(self, p):
        ''' log of a number '''
        if not isinstance(p.expr, float):
            return None
        return float(math.log(p.expr))
        
    @_('EXPFUNC expr RPAREN')
    def expr(self, p):
        ''' exponential of a number '''
        if not isinstance(p.expr, float):
            return None
        return float(math.exp(p.expr))
        
    @_('ODDFUNC expr RPAREN')
    def expr(self, p):
        ''' test if a number is odd '''
        if not isinstance(p.expr, float):
            return None
        if (int(p.expr) % 2) == 0:
            return False
        else:
            return True
        
    @_('EVENFUNC expr RPAREN')
    def expr(self, p):
        ''' test if a number is even '''
        if not isinstance(p.expr, float):
            return None
        if (int(p.expr) % 2) == 0:
            return True
        else:
            return False
        
    @_('VALUETFUNC expr RPAREN')
    def expr(self, p):
        ''' Time in seconds '''
        if isinstance(p.expr, datetime.datetime):
            return ((p.hour * 60) + p.minute) * 60 + p.second
        elif isinstance(p.expr, datetime.date):
            return 0
        elif isinstance(p.expr, datetime.time):
            return ((p.hour * 60) + p.minute) * 60 + p.second
        else:
            return None

    @_('VALUET1FUNC expr RPAREN')
    def expr(self, p):
        ''' Number of seconds turned into datetime.time '''
        if isinstance(p.expr, float):
            val = p.expr
            while val < 0:
                val += 86400
            while val >= 86400:
                val -= 86400
            second = val % 60
            val = int(val / 60)
            minute = val % 60
            hour = int(val / 60)
            return datetime.time(hour=hour, minute=minute, second=second)
        else:
            return None
    
    @_('VALUEDTFUNC expr RPAREN')
    def expr(self, p):
        ''' Seconds since the epoch '''
        if isinstance(p.expr, datetime.datetime):           # Only valid for datetimes
            try:
                return p.expr.timestamp()
            except:
                return None
        else:
            return None
        
    @_('VALUEDT1FUNC expr RPAREN')
    def expr(self, p):
        ''' Seconds of time since epoch turned into a datetime.time '''
        if isinstance(p.expr, float):
            try:
                return datetime.datetime.fromtimestamp(p.expr)
            except:
                return None
        else:
            return None
        
    @_('VALUEDTDFUNC expr RPAREN')
    def expr(self, p):
        ''' datetime.timedelta into float(seconds) '''
        if isinstance(p.expr, datetime.timedelta):
            return float(p.expr.total_seconds())
        else:
            return None
        
    @_('VALUEDTD1FUNC expr RPAREN')
    def expr(self, p):
        ''' Seconds of time turned into a datetime.timedelta '''
        if isinstance(p.expr, float):
            try:
                return datetime.timedelta(seconds=int(p.expr))
            except:
                return None
        else:
            return None
        
    @_('VALUEYMDFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert YM duration to months'''
        # Internally, YM durations are ints
        if isinstance(p.expr, int):
            return p.expr
        else:
            return None
        
    @_('VALUEYMD1FUNC expr RPAREN')
    def expr(self, p):
        ''' Convert a number of 'months' to YM duration'''
        # internally, YM durations are ints '''
        if isinstance(p.expr, float):
            return int(p.expr)
        else:
            return None
        
    @_('DURATIONFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert a duration string to datetime.timedelta or int '''
        if not isinstance(p.expr, str):
            return None
        duration = p.expr
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        if duration[0] != 'P':
            return None
        duration = duration[1:]         # skip P
        parts = duration.split('T')     # look for T (dayTimeDuration)
        if len(parts) == 1:             # no T - must be yearMonthDuration
            months = 0
            parts = duration.split('Y')
            if len(parts) != 2:
                return None
            if len(parts[0]) > 0:
                try:
                    months = int(parts[0]) * 12
                except:
                    return None
            if len(parts[1]) > 0:
                duration = parts[1]
                parts = duration.split('M')
                if len(parts) != 2:
                    return None
                if parts[1] != '':
                    return None
                if len(parts[0]) > 0:
                    try:
                        months += int(parts[0])
                    except:
                        return None
            if sign == 0:
                return int(months)
            else:
                return -int(months)
        else:
            days = seconds = milliseconds = 0
            if parts[0] != '':          # days is optional
                if parts[0][-1] != 'D':
                    return None
                try:
                    days = int(parts[0][:-1])
                except:
                    return None
            duration = parts[1]
            parts = duration.split('H')
            if len(parts) > 2:
                return None
            if len(parts) == 2:
                try:
                    seconds = int(parts[0]) * 60 * 60
                except:
                    return None
                duration = parts[1]
            parts = duration.split('M')
            if len(parts) > 2:
                return None
            if len(parts) == 2:
                try:
                    seconds += int(parts[0]) * 60
                except:
                    return None
                duration = parts[1]
            parts = duration.split('S')
            if len(parts) > 2:
                return None
            if len(parts) == 2:
                try:
                    sPart = float(parts[0])
                    seconds += int(sPart)
                    milliseconds = int((sPart * 1000)) % 1000
                except:
                    return None
            if sign == 0:
                return datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
            else:
                return -datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
        
    @_('YEARSANDMONTHSDURATIONFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Convert difference betwen two dates (from, to) to 'months' as a float '''
        if not isinstance(p.expr0, datetime.date):          # True for dates and datetimes
            return None
        if not isinstance(p.expr1, datetime.date):
            return None
        months = (p.expr1.year - p.expr0.year) * 12
        months += p.expr1.month - p.expr0.month
        if p.expr1.day < p.expr0.day:
            if p.expr1 > p.expr0:
                months -= 1
            else:
                months += 1
        return int(months)


    @_('GETVALUEFUNC expr COMMA NAME RPAREN')
    def expr(self, p):
        ''' Get a value from a Context by key '''
        if isinstance(p.expr, dict):
            if isinstance(p.NAME, str):
                if p.NAME in p.expr:
                    return p.expr[p.NAME]
        return None

    @_('GETENTRIESFUNC expr RPAREN')
    def expr(self, p):
        ''' Get a list of 'key','value' pairs from a context'''
        if isinstance(p.expr, dict):
            retList = []
            i = 0
            for item in p.expr:
                retList.append({})
                retList[i]['key'] = item
                retList[i]['value'] = p.expr[item]
                i += 1
            return retList
        return None

    @_('ISFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test that two expressions are the same FEEL semantic domain'''
        if type(p.expr0) != type(p.expr1):
            return False
        if (not isinstance(p.expr0, datetime.datetime)) and (not isinstance(p.expr0, datetime.time)):
            return True
        if p.expr0.tzinfo == p.expr1.tzinfo:
            return True
        if p.expr0.dst() == p.expr1.dst():
            return True
        return False

    @_('BEFOREFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test point or range is before point or range'''
        if isinstance(p.expr0, tuple):      # a range before
            (lowEnd0, lowVal0, lowPoint, lowEnd) = p.expr0
        else:           # a point before
            lowEnd = ']'
            lowPoint = p.expr0
        if isinstance(p.expr1, tuple):     # before a range
            (highEnd, highPoint, highVal1, highEnd1) = p.expr1
        else:                               # a point before a point
            highEnd = '['
            highPoint = p.expr1
        # Check lowPoint is 'before' highPoint
        if isinstance(lowPoint, str) and not isinstance(highPoint, str):
            return False
        elif isinstance(lowPoint, int) and not isinstance(highPoint, int):              # a range of Year, month durations
            return False
        elif isinstance(lowPoint, float) and not isinstance(highPoint, float):
            return False
        elif isinstance(lowPoint, datetime.date) and not isinstance(highPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowPoint, datetime.timedelta) and not isinstance(highPoint, datetime.timedelta):
            return False
        if lowPoint < highPoint:
            return True
        if lowPoint > highPoint:
            return False
        if (lowEnd != ']') or (highEnd != '['):
            return True
        return False

    @_('AFTERFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test point or range is after point or range'''
        if isinstance(p.expr0, tuple):      # a range after
            (highEnd, highPoint, highVal1, highEnd1) = p.expr0
        else:           # a point before
            highEnd = '['
            highPoint = p.expr0
        if isinstance(p.expr1, tuple):     # before a range
            (lowEnd0, lowVal0, lowPoint, lowEnd) = p.expr1
        else:                               # a point before a point
            lowEnd = ']'
            lowPoint = p.expr1
        # Check lowPoint is 'before' highPoint
        if isinstance(lowPoint, str) and not isinstance(highPoint, str):
            return False
        elif isinstance(lowPoint, int) and not isinstance(highPoint, int):                      # a range of Year, month durations
            return False
        elif isinstance(lowPoint, float) and not isinstance(highPoint, float):
            return False
        elif isinstance(lowPoint, datetime.date) and not isinstance(highPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowPoint, datetime.timedelta) and not isinstance(highPoint, datetime.timedelta):
            return False
        if lowPoint < highPoint:
            return True
        if lowPoint > highPoint:
            return False
        if (lowEnd != ']') or (highEnd != '['):
            return True
        return False

    @_('MEETSFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test range meets range'''
        if isinstance(p.expr0, tuple):      # a range meets
            (lowEnd0, lowVal0, highPoint, highEnd) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):      # a range meets a range
            (lowEnd, lowPoint, highVal1, highEnd1) = p.expr1
        else:
            return False
        # Check highPoint matches lowPoint
        if isinstance(highPoint, str) and not isinstance(lowPoint, str):
            return False
        elif isinstance(highPoint, int) and not isinstance(lowPoint, int):                          # a range of Year, month durations
            return False
        elif isinstance(highPoint, float) and not isinstance(lowPoint, float):
            return False
        elif isinstance(highPoint, datetime.date) and not isinstance(lowPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(highPoint, datetime.timedelta) and not isinstance(lowPoint, datetime.timedelta):
            return False
        if (highPoint != lowPoint):
            return False
        if (highEnd != ']') or (lowEnd != '['):
            return False
        return True

    @_('METBYFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test range meets range'''
        if isinstance(p.expr0, tuple):      # a range meets
            (lowEnd, lowPoint, highVal0, highEnd0) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):      # a range meets a range
            (lowEnd0, lowVal0, highPoint, highEnd) = p.expr1
        else:
            return False
        # Check lowPoint matches highPoint
        if isinstance(lowPoint, str) and not isinstance(highPoint, str):
            return False
        elif isinstance(lowPoint, int) and not isinstance(highPoint, int):                      # a range of Year, month durations
            return False
        elif isinstance(lowPoint, float) and not isinstance(highPoint, float):
            return False
        elif isinstance(lowPoint, datetime.date) and not isinstance(highPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowPoint, datetime.timedelta) and not isinstance(highPoint, datetime.timedelta):
            return False
        if (lowPoint != highPoint):
            return False
        if (lowEnd != '[') or (highEnd != ']'):
            return False
        return True

    @_('OVERLAPSFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test range overlaps range'''
        if isinstance(p.expr0, tuple):      # a range overlaps
            (end00, low0Val, high0Val, end01) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):      # a range overlaps a range
            (end10, low1Val, high1Val, end11) = p.expr1
        else:
            return False
        if isinstance(low0Val, str):
            if not isinstance(low1Val, str) or not isinstance(high1Val, str):
                return False
        elif isinstance(low0Val, int):                                          # a range of Year, month durations
            if not isinstance(low1Val, int) or not isinstance(high1Val, int):
                return False
        elif isinstance(low0Val, float):
            if not isinstance(low1Val, float) or not isinstance(high1Val, float):
                return False
        elif isinstance(low0Val, datetime.date):            # True for both dates and datetimes
            if not isinstance(low1Val, datetime.date) or not isinstance(high1Val, datetime.date):
                return False
        elif isinstance(low0Val, datetime.timedelta):
            if not isinstance(low1Val, datetime.timedelta) or not isinstance(high1Val, datetime.timedelta):
                return False
        # Check range p.expr0 overlaps range p.expr1
        if low0Val < low1Val:       # range p.expr0 starts before the start of range p.expr1
            if high0Val < low1Val:      # but doesn't get to range p.expr1 - doesn't overlap
                return False
            elif high0Val == low1Val:   # reaches, but does it overlap
                if (end01 == ')') or (end10 == '('):    # One is a closed range
                    return False
                return True
            return True     # reaches and overlaps
        elif low0Val == low1Val:     # range p.expr0 and range p.expr1 start at the same point
            # Deal with the bizzare case of empty ranges
            if (low0Val == high0Val) and (end00 == '(') and (end01 == ')'):
                return False
            if (low1Val == high1Val) and (end10 == '(') and (end11 == ')'):
                return False
            return True
        else:                       # range p.expr1 start before start of range p.expr0
            if high1Val < low0Val:      # but doesn't get to range p.exp0 - doesn't overlap
                return False
            elif high1Val == low0Val:   # reaches, but does it overlap
                if (end11 == ')') or (end00 == '('):    # One is a closed range
                    return False
                return True
            return True     # reaches and overlaps

    @_('OVERLAPSBEFOREFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test range p.expr0 starts before (does not start or coincide) and overlaps, but does not include, range p.expr1'''
        if isinstance(p.expr0, tuple):      # a range overlaps
            (end00, low0Val, high0Val, end01) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):      # a range overlaps a range
            (end10, low1Val, high1Val, end11) = p.expr1
        else:
            return False
        if isinstance(low0Val, str):
            if not isinstance(low1Val, str):
                return False
        elif isinstance(low0Val, int):                      # a range of Year, month durations
            if not isinstance(low1Val, int):
                return False
        elif isinstance(low0Val, float):
            if not isinstance(low1Val, float):
                return False
        elif isinstance(low0Val, datetime.date):            # True for both dates and datetimes
            if not isinstance(low1Val, datetime.date):
                return False
        elif isinstance(low0Val, datetime.timedelta):
            if not isinstance(low1Val, datetime.timedelta):
                return False
        # Check range p.expr0 starts before and overlaps range p.expr1
        if low0Val > low1Val:       # range p.expr0 starts after the start of range p.expr1
            return False
        if low0Val == low1Val:     # range p.expr0 and range p.expr1 start at the same point
            if (end00 != '[') or (end10 != '('):          # make sure we have 'starts before'
                return False
        if high0Val < low1Val:      # range p.expr0 doesn't get to range p.expr1 - doesn't overlap
                return False
        if high0Val == low1Val:   # reaches, but does it overlap
            if (end01 == ')') or (end10 == '('):    # One is a closed range
                return False
        if high0Val > high1Val:     # includes - which isn't overlaps
            return False
        if high0Val == high1Val:    # range p.expr0 and range p.expr1 end at the same point
            if (end01 == ']') and (end11 == ')'):        # includes - which isn't overlaps
                return False
        return True 

    @_('OVERLAPSAFTERFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test range p.expr0 starts after and overlaps range p.expr1'''
        if isinstance(p.expr0, tuple):      # a range overlaps
            (end00, low0Val, high0Val, end01) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):      # a range overlaps a range
            (end10, low1Val, high1Val, end11) = p.expr1
        else:
            return False
        if isinstance(low0Val, str):
            if not isinstance(low1Val, str) or not isinstance(high1Val, str):
                return False
        elif isinstance(low0Val, int):                          # a range of Year, month durations
            if not isinstance(low1Val, int) or not isinstance(high1Val, int):
                return False
        elif isinstance(low0Val, float):
            if not isinstance(low1Val, float) or not isinstance(high1Val, float):
                return False
        elif isinstance(low0Val, datetime.date):            # True for both dates and datetimes
            if not isinstance(low1Val, datetime.date) or not isinstance(high1Val, datetime.date):
                return False
        elif isinstance(low0Val, datetime.timedelta):
            if not isinstance(low1Val, datetime.timedelta) or not isinstance(high1Val, datetime.timedelta):
                return False
        # Check range p.expr0 starts after and overlaps range p.expr1
        if low0Val < low1Val:       # range p.expr0 starts before the start of range p.expr1
            return False
        if low0Val == low1Val:     # range p.expr0 and range p.expr1 start at the same point
            if (end00 != '(') or (end10 != '['):    # Make sure we have 'starts after'
                return False
        if low0Val > high1Val:      # range p.expr0 doesn't stretch back to range p.exp1 - doesn't overlap
            return False
        if low0Val == high1Val:   # p.expr0 stretches back to p.expr1, but does it overlap
            if (end00 == '(') or (end11 == ')'):    # One is a closed range
                return False
        if high0Val == high1Val:    # range p.expr0 and range p.expr1 end at the same point
            if (end01 == ')') or (end11 == ']'):        # make sure there is some overlap 'after' the end
                return False
        return True     # reaches and overlaps
        
    @_('FINISHESFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test point or range finishes a range'''
        if isinstance(p.expr0, tuple):      # a range finishes
            (lowEnd0, lowVal0, highPoint, highEnd) = p.expr0
        else:           # a point finishes
            highEnd = ']'
            highPoint = p.expr0
        if isinstance(p.expr1, tuple):     # a range
            (lowEnd1, lowVal1, thePoint, theEnd) = p.expr1
        else:
            return False
        # Check highPoint is thePoint
        if isinstance(thePoint, str) and not isinstance(highPoint, str):
            return False
        elif isinstance(thePoint, int) and not isinstance(highPoint, int):              # a range of Year, month durations
            return False
        elif isinstance(thePoint, float) and not isinstance(highPoint, float):
            return False
        elif isinstance(thePoint, datetime.date) and not isinstance(highPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(thePoint, datetime.timedelta) and not isinstance(highPoint, datetime.timedelta):
            return False
        if thePoint != highPoint:
            return False
        if highEnd != theEnd:
            return False
        return True

    @_('FINISHEDBYFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test a range is finished by point or range'''
        if isinstance(p.expr0, tuple):      # a range
            (lowEnd0, lowVal0, highPoint, highEnd) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):     # before a range
            (highEnd1, highVal1, thePoint, theEnd) = p.expr1
        else:                               # a point before a point
            theEnd = ']'
            thePoint = p.expr1
        # Check thePoint is highPoint
        if isinstance(thePoint, str) and not isinstance(highPoint, str):
            return False
        elif isinstance(thePoint, int) and not isinstance(highPoint, int):                  # a range of Year, month durations
            return False
        elif isinstance(thePoint, float) and not isinstance(highPoint, float):
            return False
        elif isinstance(thePoint, datetime.date) and not isinstance(highPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(thePoint, datetime.timedelta) and not isinstance(highPoint, datetime.timedelta):
            return False
        if thePoint != highPoint:
            return False
        if theEnd != highEnd:
            return False
        return True

    @_('INCLUDESFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test range includes point or range'''
        if isinstance(p.expr0, tuple):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = p.expr1
        else:                               # includes a point
            lowEnd1 = '['
            highEnd1 = ']'
            lowVal1 = highVal1 = p.expr1
        # Check lowVal0..highVal0 include lowVa1..highVal1
        if isinstance(lowVal0, str) and not isinstance(highVal0, str):
            return False
        elif isinstance(lowVal0, int) and not isinstance(highVal0, int):                        # a range of Year, month durations
            return False
        elif isinstance(lowVal0, float) and not isinstance(highVal0, float):
            return False
        elif isinstance(lowVal0, datetime.date) and not isinstance(highVal0, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowVal0, datetime.timedelta) and not isinstance(highVal0, datetime.timedelta):
            return False
        if lowVal0 > lowVal1:       # p.expr1 starts before p.expr0
            return False
        if lowVal0 == lowVal1:      # Same starting point
            if (lowEnd0 != lowEnd1) and (lowEnd0 == '('):        # p.expr0 is closed
                return False
        if highVal0 < highVal1:     # p.expr1 ends after p.expr0
            return False
        if highVal0 == highVal1:
            if (highEnd0 != highEnd1) and (highEnd0 == ')'):    # p.expr0 is closed
                return False
        return True

    @_('DURINGFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test point or range p.expr0 is included in range p.expr1'''
        if isinstance(p.expr0, tuple):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = p.expr0
        else:           # a point before
            lowEnd0 = '['
            highEnd0 = ']'
            lowVal0 = highVal0 = p.expr0
        if isinstance(p.expr1, tuple):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = p.expr1
        else:
            return False                               # a point before a point
        # Check highVal0..highVal1 includes lowVal0..lowVal1
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif isinstance(lowVal0, int) and not isinstance(lowVal1, int):                     # a range of Year, month durations
            return False
        elif isinstance(lowVal0, float) and not isinstance(lowVal1, float):
            return False
        elif isinstance(lowVal0, datetime.date) and not isinstance(lowVal1, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowVal0, datetime.timedelta) and not isinstance(lowVal1, datetime.timedelta):
            return False
        if lowVal0 < lowVal1:       # p.expr0 start before p.expr1
            return False
        if lowVal0 == lowVal1:
            if (lowEnd0 != lowEnd1) and (lowEnd1 == '('):            # p.expr1 is closed
                return False
        if highVal0 > highVal1:     # p.expr0 ends after p.expr1
            return False
        if (highVal0 == highVal1):
            if (highEnd0 != highEnd1) and (highEnd1 == ')'):        # p.expr1 is closed
                return False
        return True

    @_('STARTSFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test point or range starts a range'''
        if isinstance(p.expr0, tuple):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = p.expr0
        else:           # a point before
            lowEnd0 = '['
            highEnd0 = ']'
            lowVal0 = highVal0 = p.expr0
        if isinstance(p.expr1, tuple):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = p.expr1
        else:
            return False
        # Check lowVal0..highVal0 starts lowVal1..highVal1, but doesn't go beyond
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif isinstance(lowVal0, int) and not isinstance(lowVal1, int):                     # a range of Year, month durations
            return False
        elif isinstance(lowVal0, float) and not isinstance(lowVal1, float):
            return False
        elif isinstance(lowVal0, datetime.date) and not isinstance(lowVal1, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowVal0, datetime.timedelta) and not isinstance(lowVal1, datetime.timedelta):
            return False
        if lowVal0 != lowVal1:
            return False
        if lowEnd0 != lowEnd1:
            return False
        if highVal0 > highVal1:
            return False
        if highVal0 == highVal1:
            if (highEnd0 != highEnd1) and (highEnd1 == ')'):
                return False
        return True

    @_('STARTEDBYFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test range is started by point or range'''
        if isinstance(p.expr0, tuple):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = p.expr0
        else:
            return False
        if isinstance(p.expr1, tuple):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = p.expr1
        else:                               # a point before a point
            lowEnd1 = '['
            highEnd1 = ']'
            lowVal1 = highVal1 = p.expr1
        # Check lowVal0..highVal0 is started by lowVal1..highVal1, but doesn't go beyond
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif isinstance(lowVal0, int) and not isinstance(lowVal1, int):                 # a range of Year, month durations
            return False
        elif isinstance(lowVal0, float) and not isinstance(lowVal1, float):
            return False
        elif isinstance(lowVal0, datetime.date) and not isinstance(lowVal1, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowVal0, datetime.timedelta) and not isinstance(lowVal1, datetime.timedelta):
            return False
        if lowVal1 != lowVal0:
            return False
        if lowEnd1 != lowEnd0:
            return False
        if highVal1 > highVal0:
            return False
        if highVal1 == highVal0:
            if (highEnd1 != highEnd0) and (highEnd0 == ')'):
                return False
        return True

    @_('COINCIDESFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Test point or range is coincides with point or range'''
        if not isinstance(p.expr0, tuple):      # a point
            if isinstance(p.expr1, tuple):
                return False
            return p.expr0 == p.expr1
        (lowEnd0, lowVal0, highVal0, highEnd0) = p.expr0
        if not isinstance(p.expr1, tuple):     # not a range
            return False
        (lowEnd1, lowVal1, highVal1, highEnd1) = p.expr1
        # Check range p.expr0 coincides with range p.expr1
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif isinstance(lowVal0, int) and not isinstance(lowVal1, int):                     # a range of Year, month durations
            return False
        elif isinstance(lowVal0, float) and not isinstance(lowVal1, float):
            return False
        elif isinstance(lowVal0, datetime.date) and not isinstance(lowVal1, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowVal0, datetime.timedelta) and not isinstance(lowVal1, datetime.timedelta):
            return False
        if lowVal0 != lowVal1:
            return False
        if highVal0 != highVal1:
            return False
        if lowEnd0 != lowEnd1:
            return False
        if highEnd0 != highEnd1:
            return False
        return True

    @_('DAYOFYEARFUNC expr RPAREN')
    def expr(self, p):
        if isinstance(p.expr, datetime.date) or isinstance(p.expr, datetime.datetime):
            return p.expr.timetuple().tm_yday
        return False

    @_('DAYOFWEEKFUNC expr RPAREN')
    def expr(self, p):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if isinstance(p.expr, datetime.date) or isinstance(p.expr, datetime.datetime):
            return days[p.expr.weekday()]
        return False

    @_('MONTHOFYEARFUNC expr RPAREN')
    def expr(self, p):
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        if isinstance(p.expr, datetime.date) or isinstance(p.expr, datetime.datetime):
            return months[p.expr.month]
        return False

    @_('WEEKOFYEARFUNC expr RPAREN')
    def expr(self, p):
        if isinstance(p.expr, datetime.date) or isinstance(p.expr, datetime.datetime):
            (year, week, weekday) = p.expr.isocalendar()
            return week
        return False

    @_('BOOLEAN')
    def expr(self, p):
        if str(p.BOOLEAN) == 'true':
            return True
        else:
            return False

    @_('NAME')
    def expr(self, p):
        if p.NAME in self.names:
            return self.names[p.NAME]
        elif p.NAME.endswith('.year') and p.NAME[:-5] in self.names:
            value = self.names[p.NAME[:-5]]
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                return value.year
        elif p.NAME.endswith('.month') and p.NAME[:-6] in self.names:
            value = self.names[p.NAME[:-6]]
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                return value.month
        elif p.NAME.endswith('.day') and p.NAME[:-4] in self.names:
            value = self.names[p.NAME[:-4]]
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                return value.day
        elif p.NAME.endswith('.weekday') and p.NAME[:-8] in self.names:
            value = self.names[p.NAME[:-8]]
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                return value.weekday()
        elif p.NAME.endswith('.hour') and p.NAME[:-5] in self.names:
            value = self.names[p.NAME[:-5]]
            if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                return value.hour
        elif p.NAME.endswith('.minute') and p.NAME[:-7] in self.names:
            value = self.names[p.NAME[:-7]]
            if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                return value.minute
        elif p.NAME.endswith('.second') and p.NAME[:-7] in self.names:
            value = self.names[p.NAME[:-7]]
            if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                return value.second
        elif p.NAME.endswith('.timezone') and p.NAME[:-9] in self.names:
            value = self.names[p.NAME[:-9]]
            if isinstance(value, datetime.datetime):
                if value.tzinfo == None:
                    return None
                return value.tzname()
            elif isinstance(value, datetime.time):
                if value.tzinfo == None:
                    return None
                tmpDateTime = datetime.datetime.combine(datetime.date.today(), value)
                return tmpDateTime.tzname()
        elif p.NAME.endswith('.time_offset') and p.NAME[:-12] in self.names:
            value = self.names[p.NAME[:-12]]
            if isinstance(value, datetime.datetime):
                if value.tzinfo == None:
                    return None
                return value.utcoffset()
            elif isinstance(value, datetime.time):
                if value.tzinfo == None:
                    return None
                tmpDateTime = datetime.datetime.combine(datetime.date.today(), value)
                return tmpDateTime.utcoffset()
        elif p.NAME.endswith('.days') and p.NAME[:-5] in self.names:
            value = self.names[p.NAME[:-5]]
            if isinstance(value, datetime.timedelta):
                return int(ValuesView.total_seconds() / 60 / 60 / 24)
        elif p.NAME.endswith('.hours') and p.NAME[:-6] in self.names:
            value = self.names[p.NAME[:-6]]
            if isinstance(value, datetime.timedelta):
                return int(value.total_seconds() / 60 / 60) % 24
        elif p.NAME.endswith('.minutes') and p.NAME[:-8] in self.names:
            value = self.names[p.NAME[:-8]]
            if isinstance(value, datetime.timedelta):
                return int(value.total_seconds() / 60) % 60
        elif p.NAME.endswith('.seconds') and p.NAME[:-8] in self.names:
            value = self.names[p.NAME[:-8]]
            if isinstance(value, datetime.timedelta):
                return value.total_seconds() % 60
        elif p.NAME.endswith('.years') and p.NAME[:-6] in self.names:
            value = self.names[p.NAME[:-6]]
            if isinstance(value, int):
                return int(value / 12)
        elif p.NAME.endswith('.months') and p.NAME[:-7] in self.names:
            value = self.names[p.NAME[:-7]]
            if isinstance(value, int):
                return value % 12
        elif p.NAME.endswith('.start') and p.NAME[:-6] in self.names:
            value = self.names[p.NAME[:-6]]
            if isinstance(value, tuple) and (len(value) == 4):
                (end0, low0, high1, end1) = value
                return low0
        elif p.NAME.endswith('.start_included') and p.NAME[:-13] in self.names:
            value = self.names[p.NAME[:-13]]
            if isinstance(value, tuple) and (len(value) == 4):
                (end0, low0, high1, end1) = value
                if end0 == '[':
                    return True
                else:
                    return False
        elif p.NAME.endswith('.end') and p.NAME[:-4] in self.names:
            value = self.names[p.NAME[:-4]]
            if isinstance(value, tuple) and (len(value) == 4):
                (end0, low0, high1, end1) = value
                return p.high1
        elif p.NAME.endswith('.end_included') and p.NAME[:-11] in self.names:
            value = self.names[p.NAME[:-11]]
            if isinstance(value, tuple) and (len(value) == 4):
                (end0, low0, high1, end1) = value
                if end1 == ']':
                    return True
                else:
                    return False
        self.errors.append(f'Undefined name {p.NAME!r}')
        return 0

    @_('ATSTRING')
    def expr(self, p):
        thisString = p.ATSTRING[2:-1]
        isDateTime = re.fullmatch(SFeelLexer.DATETIME, thisString)
        if isDateTime is not None:
            return self.dateTimeFunc(thisString)
        isDate = re.fullmatch(SFeelLexer.DATE, thisString)
        if isDate is not None:
            return self.dateFunc(thisString)
        isTime = re.fullmatch(SFeelLexer.TIME, thisString)
        if isTime is not None:
            return self.timeFunc(thisString)
        dtd = re.fullmatch(SFeelLexer.DTDURATION, thisString)
        if dtd is not None:
            return self.dtdFunc(thisString)
        ymd = re.fullmatch(SFeelLexer.YMDURATION, thisString)
        if ymd is not None:
            return self.ymdFunc(thisString)
        return str(thisString)

    @_('STRING')
    def expr(self, p):
        return str(p.STRING[1:-1])

    @_('DATE')
    def expr(self, p):
        ''' Convert string to datetime.date '''
        thisDate = p.DATE
        return self.dateFunc(thisDate)

    def dateFunc(self, thisDate):
        ''' Convert string to datetime.date '''
        try:
            return dateutil.parser.parse(thisDate).date()
        except:
            return None

    @_('TIME')
    def expr(self, p):
        ''' Convert string to datetime.time '''
        thisTimeString = p.TIME
        return self.timeFunc(thisTimeString)

    def timeFunc(self, thisTimeString):
        ''' Convert string to datetime.time '''
        parts = thisTimeString.split('@')
        try:
            thisTime =  dateutil.parser.parse(parts[0]).timetz()     # A time with timezone
        except:
            return None
        if len(parts) == 1:
            return thisTime
        thisZone = dateutil.tz.gettz(parts[1])
        if thisZone is None:
            return thisTime
        try:
            retTime = thisTime.replace(tzinfo=thisZone)
        except:
            return thisTime
        return retTime

    @_('DATETIME')
    def expr(self, p):
        ''' Convert string to datetime.datetime '''
        thisDateTimeString = p.DATETIME
        return self.dateTimeFunc(thisDateTimeString)

    def dateTimeFunc(self, thisDateTimeString):
        ''' Convert string to datetime.datetime '''
        parts = thisDateTimeString.split('@')
        try:
            thisDateTime = dateutil.parser.parse(parts[0])
        except:
            return None
        if len(parts) == 1:
            return thisDateTime
        thisZone = dateutil.tz.gettz(parts[1])
        if thisZone is None:
            return thisDateTime
        try:
            retDateTime = thisDateTime.replace(tzinfo=thisZone)
        except:
            return thisDateTime
        return retDateTime

    @_('DTDURATION')
    def expr(self, p):
        ''' Convert duration string into datetime.timedelta '''
        duration = p.DTDURATION
        return self.dtdFunc(duration)

    def dtdFunc(self, duration):
        ''' Convert duration string into datetime.timedelta '''
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        if duration[0] != 'P':
            return None
        duration = duration[1:]         # skip P
        days = seconds = milliseconds = 0
        if duration[0] != 'T':          # days is optional
            parts = duration.split('D')
            if len(parts) == 2:
                if len(parts[0]) > 0:
                    try:
                        days = int(parts[0])
                    except:
                        return None
                if len(parts[1]) == 0:
                    if sign == 0:
                        return datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
                    else:
                        return -datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
                duration = parts[1]
            else:
                return None
        if duration[0] != 'T':
            return None
        duration = duration[1:]         # Skip T
        parts = duration.split('H')
        if len(parts) == 2:
            if len(parts[0]) > 0:
                try:
                    seconds = int(parts[0]) * 60 * 60
                except:
                    return None
            duration = parts[1]
        parts = duration.split('M')
        if len(parts) == 2:
            if len(parts[0]) > 0:
                try:
                    seconds += int(parts[0]) * 60
                except:
                    return None
            duration = parts[1]
        parts = duration.split('S')
        if len(parts) == 2:
            if len(parts[0]) > 0:
                try:
                    sPart = float(parts[0])
                    seconds += int(sPart)
                    milliseconds = int((sPart * 1000)) % 1000
                except:
                    return None
        if sign == 0:
            return datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
        else:
            return -datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)

    @_('YMDURATION')
    def expr(self, p):
        ''' Convert year/month duration string into int '''
        duration = p.YMDURATION
        return self.ymdFunc(duration)

    def ymdFunc(self, duration):
        ''' Convert year/month duration string into int '''
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        if duration[0] != 'P':
            return None
        duration = duration[1:]         # skip P
        months = 0
        parts = duration.split('Y')
        if len(parts) != 2:
            return None
        if len(parts[0]) > 0:
            try:
                months = int(parts[0]) * 12
            except:
                return None
        duration = parts[1]
        parts = duration.split('M')
        if len(parts) != 2:
            return None
        if parts[1] != '':
            return None
        if len(parts[0]) > 0:
            try:
                months += int(parts[0])
            except:
                return None
        if sign == 0:
            return int(months)
        else:
            return -int(months)

    @_('NUMBER')
    def expr(self, p):
        return float(p.NUMBER)

    def error(self, p):
        if p:
            self.errors.append("Syntax error at token '{!s}'".format(p.value))
            tok = next(self.tokens, None)
            self.errok()
            return tok
        else:
            self.errors.append("Syntax error at EOF")
            self.errok()
            return

    def sFeelParse(self, text):
        """
        Parse S-FEEL text

        This routine parses the passed text, which must be valid S-FEEL

        Args:
            param1 (str): The S-FEEL text to be parsed

        Returns:
            tuple: (status, value)

            'status' is alist of any parsing errors.

            'value' is the Python native value of the parsed S-FEEL text.

            For an assignment statement the 'value' will be the Python native value assigned to the named variable.

            For all other expressions the 'value' will be the Python native value of the S-FEEL expression.
        """

        # print("S-FEEL parsing '{!s}'".format(text))
        if (text == '') or text.isspace():
            return None

        lexErrors = []
        tokens = self.lexer.tokenize(text)
        yaccTokens = []
        for token in tokens:
            if token.type == 'ERROR':
                lexErrors.append(token.value)
            else:
                yaccTokens.append(token)
        self.clearErrors()
        retVal = self.parse(iter(yaccTokens))
        yaccErrors = self.collectErrors()
        status = {}
        if (len(lexErrors) > 0) or (len(yaccErrors) > 0):
            status['errors'] = lexErrors + yaccErrors
        # print("S-FEEL returning '{!s}'".format(retVal))
        return (status, retVal)


if __name__ == '__main__':
    parser = SFeelParser()
    while True:
        try:
            text = input('s-feel+ > ')
        except EOFError:
            break

        if text == 'quit()':
            break

        (status, retVal) = parser.sFeelParse(text)

        print(text)
        print(retVal)
        if 'errors' in status:
            print('With errors:', status['errors'])
