# -----------------------------------------------------------------------------
# SFeel.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
import re
import datetime
import dateutil.parser
import pytz
import copy
import math
import statistics
from operator import itemgetter
import ast
import warnings

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
              SORTFUNC, FUNCTIONFUNC, NOWFUNC, TODAYFUNC,
              YEARSANDMONTHSDURATIONTYPE, DAYSANDTIMEDURATIONTYPE, DATEANDTIMETYPE, TIMETYPE, DATETYPE,
              BOOLEANTYPE, STRINGTYPE, NUMBERTYPE, RANGETYPE, LISTTYPE, CONTEXTTYPE, ANYTYPE, NULLTYPE,
              NAME, ATSTRING, STRING, NULL,
              LBRACKET, RBRACKET,
              EQUALS, NOTEQUALS, LTTHANEQUAL, GTTHANEQUAL, LTTHAN, GTTHAN,
              AND, OR, NOT, BETWEEN,
              PLUS, MINUS, MULTIPY, DIVIDE, EXPONENT,
              ELLIPSE, COMMA, DATETIME, DATE, TIME, DTDURATION, YMDURATION,
              NUMBER,
              LPAREN, RPAREN,
              LCURLY, RCURLY, COLON, DOTYEARS, DOTMONTHS, DOTDAYS, DOTHOURS, DOTMINUTES, DOTSECONDS,
              DOTYEAR, DOTMONTH, DOTDAY, DOTWEEKDAY, DOTHOUR, DOTMINUTE, DOTSECOND, DOTTIMEZONE, DOTTIMEOFFSET, DOTTIME_OFFSET,
              DOTSTARTINCLUDED, DOTSTART_INCLUDED, DOTENDINCLUDED, DOTEND_INCLUDED, DOTSTART, DOTEND, PERIOD,
              SOME, EVERY, SATISFIES, IN, ITEM, ASSIGN
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
    SORTFUNC = r'sort\('
    FUNCTIONFUNC = r'function\('
    NOWFUNC = r'now\('
    TODAYFUNC = r'today\('
    DTDURATION = r'-?P((([0-9]+D)?T([0-9]+H([0-9]+M)?((([0-9]+(\.[0-9]+)?)|(\.[0-9]+))S)?|([0-9]+M((([0-9]+(\.[0-9]+)?)|(\.[0-9]+))S)?)|((([0-9]+(\.[0-9]+)?)|(\.[0-9]+))S)))|([0-9]+D)|([0-9]+H[0-9]+M(([0-9]+(\.[0-9]+)?)|(\.[0-9]+))S))'
    YMDURATION = r'-?P((([0-9]+Y)?[0-9]+M)|([0-9]+Y))'
    YEARSANDMONTHSDURATIONTYPE = r'instance\s+of\s+years and months duration'
    DAYSANDTIMEDURATIONTYPE = r'instance\s+of\s+days and time duration'
    DATEANDTIMETYPE = r'instance\s+of\s+date and time'
    TIMETYPE = r'instance\s+of\s+time'
    DATETYPE = r'instance\s+of\s+date'
    BOOLEANTYPE = r'instance\s+of\s+boolean'
    STRINGTYPE = r'instance\s+of\s+string'
    NUMBERTYPE = r'instance\s+of\s+number'
    RANGETYPE = r'instance\s+of\s+range'
    LISTTYPE = r'instance\s+of\s+list'
    CONTEXTTYPE = r'instance\s+of\s+context'
    ANYTYPE = r'instance\s+of\s+Any'
    NULLTYPE = r'instance\s+of\s+Null'
    NAME = (u'[?A-Z_a-z' +
            u'\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF' +
            u'\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF' +
            u'\u3001-\uD7FF\uF900-\uFDCF\uFDF0\uFFFD' + 
            u'\U00010000-\U000EFFFF]' +
            u'([?A-Z_a-z' +
            u'\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF' +
            u'\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF' +
            u'\u3001-\uD7FF\uF900-\uFDCF\uFDF0\uFFFD' + 
            u'\U00010000-\U000EFFFF' +
            u'0-9\u00B7\u0300-\u036F\u203F-\u2040]*|' +
            u'[/\\-\'+\\*]*)(\\.' +
            u'[?A-Z_a-z' +
            u'\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF' +
            u'\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF' +
            u'\u3001-\uD7FF\uF900-\uFDCF\uFDF0\uFFFD' + 
            u'\U00010000-\U000EFFFF]' +
            u'([?A-Z_a-z' +
            u'\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF' +
            u'\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF' +
            u'\u3001-\uD7FF\uF900-\uFDCF\uFDF0\uFFFD' + 
            u'\U00010000-\U000EFFFF' +
            u'0-9\u00B7\u0300-\u036F\u203F-\u2040]*|' +
            u'[/\\-\'+\\*]*))*')

    # Special cases of name
    NAME['in'] = IN
    NAME['and'] = AND
    NAME['or'] = OR
    NAME['not'] = NOT
    NAME['between'] = BETWEEN
    NAME['null'] = NULL
    NAME['item'] = ITEM
    NAME['some'] = SOME
    NAME['every'] = EVERY
    NAME['satisfies'] = SATISFIES

    ATSTRING = r'@"(' + r"\\'" + r'|\\"|\\\\|\\n|\\r|\\t|\\u[0-9]{4}|[^"])*"'
    STRING = r'"(' + r"\\'" + r'|\\"|\\\\|\\n|\\r|\\t|\\u[0-9]{4}|[^"])*"'
    DATETIME = r'([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)|@[A-Za-z0-9_-]+/[A-Za-z0-9_-]+)?'
    DATE = r'([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(Z|(\+|-)(0[0-9]|1[0-3]):[0-5][0-9]|14:00)?'
    TIME = r'(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))(Z|(\+|-)([0-1][0-9]|2[0-3]):[0-5][0-9]|@[A-Za-z0-9_-]+/[A-Za-z0-9_-]+)?'
    NUMBER = r'(\.\d+|\d+(\.(\d+|\s)){0,1})'

    # Ignored patterns
    ignore_newline = r'(\n+)|(//.*)|(/\*[^*]*\*/)'

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
    DOTTIMEZONE = r'\.timezone'
    DOTTIMEOFFSET = r'\.time offset'
    DOTTIME_OFFSET = r'\.time_offset'
    DOTYEARS = r'\.years'
    DOTMONTHS = r'\.months'
    DOTDAYS = r'\.days'
    DOTHOURS = r'\.hours'
    DOTMINUTES = r'\.minutes'
    DOTSECONDS = r'\.seconds'
    DOTYEAR = r'\.year'
    DOTMONTH = r'\.month'
    DOTDAY = r'\.day'
    DOTWEEKDAY = r'\.weekday'
    DOTHOUR = r'\.hour'
    DOTMINUTE = r'\.minute'
    DOTSECOND = r'\.second'
    DOTSTARTINCLUDED = r'\.start included'
    DOTSTART_INCLUDED = r'\.start_included'
    DOTENDINCLUDED = r'\.end included'
    DOTEND_INCLUDED = r'\.end_included'
    DOTSTART = r'\.start'
    DOTEND = r'\.end'
    PERIOD = r'\.'
    SOME = r'some'
    EVERY = r'every'
    SATISFIES = r'satisfies'
    IN = r'in'

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
        ('left', NAME),
        ('left', EQUALS, NOTEQUALS, LTTHANEQUAL, GTTHANEQUAL, LTTHAN, GTTHAN),
        ('left', PLUS, MINUS),
        ('left', MULTIPY, DIVIDE),
        ('left', EXPONENT),
        ('right', UMINUS),
        ('left', AND, OR, NOT, BETWEEN),
        ('left', LBRACKET, COMMA, RBRACKET),
        ('left', DOTYEARS, DOTMONTHS, DOTDAYS, DOTHOURS, DOTMINUTES, DOTSECONDS),
        ('left', DOTYEAR, DOTMONTH, DOTDAY, DOTWEEKDAY,DOTHOUR, DOTMINUTE, DOTSECOND, DOTTIMEZONE, DOTTIMEOFFSET, DOTTIME_OFFSET, DOTSTART, DOTEND),
        ('left', PERIOD),
        ('left', LPAREN, RPAREN),
        ('left', SOME, EVERY, SATISFIES, IN)
        )


    def __init__(self):
        self.names = {}
        self.contextNames = []
        self.inContext = 0
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

    def someFunc(self, name0, thisList, name1, relop, thisValue):
        # Some in a list of value, or a list of dictionaries
        if not isinstance(thisList, list):
            return None
        if name0 == name1:
            thisKey = None
            isValues = True
        elif name1.startswith(name0 + '.'):
            thisKey = name1[len(name0) + 1:]
            isValues = False
        else:
            return None
        for i in range(len(thisList)):
            if isValues:
                if thisList[i] == thisValue:
                    return True
            else:
                if not isinstance(thisList[i], dict):
                    continue
                if thisKey not in thisList[i].keys():
                    continue
                if relop == '=':
                    if thisList[i][thisKey] == thisValue:
                        return True
                elif relop == '!=':
                    if thisList[i][thisKey] != thisValue:
                        return True
                elif relop == '<':
                    if thisList[i][thisKey] < thisValue:
                        return True
                elif relop == '>':
                    if thisList[i][thisKey] > thisValue:
                        return True
                elif relop == '<=':
                    if thisList[i][thisKey] <= thisValue:
                        return True
                elif relop == '>=':
                    if thisList[i][thisKey] >= thisValue:
                        return True
                else:
                    return None
        return False

    @_('SOME NAME IN expr SATISFIES NAME EQUALS expr')
    def expr(self, p):
        # Some in a list of value, or a list of dictionaries
        return self.someFunc(p.NAME0, p.expr0, p.NAME1, p.EQUALS, p.expr1)

    @_('SOME NAME IN expr SATISFIES NAME NOTEQUALS expr')
    def expr(self, p):
        # Some in a list of value, or a list of dictionaries
        return self.someFunc(p.NAME0, p.expr0, p.NAME1, p.NOTEQUALS, p.expr1)

    @_('SOME NAME IN expr SATISFIES NAME ltrange')
    def expr(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        # Some in a list of value, or a list of dictionaries
        if end1 == ')':
            return self.someFunc(p.NAME0, p.expr, p.NAME1, '<', highVal)
        else:
            return self.someFunc(p.NAME0, p.expr, p.NAME1, '<=', highVal)

    @_('SOME NAME IN expr SATISFIES NAME gtrange')
    def expr(self, p):
        # Some in a list of value, or a list of dictionaries
        (end0, lowVal, highVal, end1) = p.gtrange
        if end0 == '(':
            return self.someFunc(p.NAME0, p.expr, p.NAME1, '>', lowVal)
        else:
            return self.someFunc(p.NAME0, p.expr, p.NAME1, '>=', lowVal)

    @_('SOME NAME IN expr SATISFIES NOTFUNC NAME RPAREN', 'SOME NAME IN expr SATISFIES ODDFUNC NAME RPAREN', 'SOME NAME IN expr SATISFIES EVENFUNC NAME RPAREN')
    def expr(self, p):
        if not isinstance(p[3], list):
            return None
        if p[1] != p[6]:
            return None
        for i in p[3]:
            if p[5] == 'not(':
                if not isinstance(i, bool):
                    continue
                if not i:
                    return True
            elif p[5] == 'odd(':
                if not isinstance(i, float):
                    continue
                if not i.is_integer():
                    continue
                if (int(i) % 2) == 1:
                    return True
            elif p[5] == 'even(':
                if not isinstance(i, float):
                    continue
                if not i.is_integer():
                    continue
                if (int(i) % 2) == 0:
                    return True
        return False

    def everyFunc(self, name0, thisList, name1, relop, thisValue):
        # Some in a list of value, or a list of dictionaries
        if not isinstance(thisList, list):
            return None
        if name0 == name1:
            thisKey = None
            isValues = True
        elif name1.startswith(name0 + '.'):
            thisKey = name1[len(name0) + 1:]
            isValues = False
        else:
            return None
        for i in range(len(thisList)):
            if isValues:
                if thisList[i] != thisValue:
                    return False
            else:
                if not isinstance(thisList[i], dict):
                    return False
                if thisKey not in thisList[i].keys():
                    return False
                if relop == '=':
                    if thisList[i][thisKey] != thisValue:
                        return False
                elif relop == '!=':
                    if thisList[i][thisKey] == thisValue:
                        return False
                elif relop == '<':
                    if thisList[i][thisKey] >= thisValue:
                        return False
                elif relop == '>':
                    if thisList[i][thisKey] <= thisValue:
                        return False
                elif relop == '<=':
                    if thisList[i][thisKey] > thisValue:
                        return False
                elif relop == '>=':
                    if thisList[i][thisKey] < thisValue:
                        return False
                else:
                    return None
        return True

    @_('EVERY NAME IN expr SATISFIES NAME EQUALS expr')
    def expr(self, p):
        # Every in a list of value, or a list of dictionaries
        return self.everyFunc(p.NAME0, p.expr0, p.NAME1, p.EQUALS, p.expr1)

    @_('EVERY NAME IN expr SATISFIES NAME NOTEQUALS expr')
    def expr(self, p):
        # Every in a list of value, or a list of dictionaries
        return self.everyFunc(p.NAME0, p.expr0, p.NAME1, p.NOTEQUALS, p.expr1)

    @_('EVERY NAME IN expr SATISFIES NAME ltrange')
    def expr(self, p):
        # Every in a list of value, or a list of dictionaries
        (end0, lowVal, highVal, end1) = p.ltrange
        if end1 == ')':
            return self.everyFunc(p.NAME0, p.expr, p.NAME1, '<', highVal)
        else:
            return self.everyFunc(p.NAME0, p.expr, p.NAME1, '<=', highVal)

    @_('EVERY NAME IN expr SATISFIES NAME gtrange')
    def expr(self, p):
        # Every in a list of value, or a list of dictionaries
        (end0, lowVal, highVal, end1) = p.gtrange
        if end0 == '(':
            return self.everyFunc(p.NAME0, p.expr, p.NAME1, '>', lowVal)
        else:
            return self.everyFunc(p.NAME0, p.expr, p.NAME1, '>=', lowVal)

    @_('EVERY NAME IN expr SATISFIES NOTFUNC NAME RPAREN', 'EVERY NAME IN expr SATISFIES ODDFUNC NAME RPAREN', 'EVERY NAME IN expr SATISFIES EVENFUNC NAME RPAREN')
    def expr(self, p):
        if not isinstance(p[3], list):
            return None
        if p[1] != p[6]:
            return None
        for i in p[3]:
            if p[5] == 'not(':
                if not isinstance(i, bool):
                    return False
                if i:
                    return False
            elif p[5] == 'odd(':
                if not isinstance(i, float):
                    return False
                if not i.is_integer():
                    return False
                if (int(i) % 2) != 1:
                    return False
            elif p[5] == 'even(':
                if not isinstance(i, float):
                    return False
                if not i.is_integer():
                    return False
                if (int(i) % 2) != 0:
                    return False
        return True

    @_('expr IN expr', 'expr IN ltrange', 'expr IN gtrange')
    def expr(self, p):
        # This is 'in' as in 'in a list' or 'in a range' or simply 'in' as an alternative to '='
        # Grammer Rule 49.c
        if isinstance(p[2], tuple) and (len(p[2]) == 4):      # in a range
            (end0, lowVal, highVal, end1) = p[2]
            if isinstance(p[0], str):
                if lowVal is None:
                    if not isinstance(highVal, str):
                        return False
                elif highVal is None:
                    if not isinstance(lowVal, str):
                        return False
                elif not isinstance(lowVal, str) or not isinstance(highVal, str):
                    return False
            elif type(p[0]) == int:              # Year, month durations
                if lowVal is None:
                    if type(highVal) != int:
                        return False
                elif highVal is None:
                    if type(lowVal) != int:
                        return False
                elif (type(lowVal) != int) or (type(highVal) != int):
                    return False
            elif isinstance(p[0], float):
                if lowVal is None:
                    if not isinstance(highVal, float):
                        return False
                elif highVal is None:
                    if not isinstance(lowVal, float):
                        return False
                elif not isinstance(lowVal, float) or not isinstance(highVal, float):
                    return False
            elif isinstance(p[0], datetime.date):                # True for both dates and datetimes
                if lowVal is None:
                    if not isinstance(highVal, datetime.date):
                        return False
                elif highVal is None:
                    if not isinstance(lowVal, datetime.date):
                        return False
                if (not isinstance(lowVal, datetime.date)) and (not isinstance(highVal, datetime.date)):
                    return False
            elif isinstance(p[0], datetime.time):
                if lowVal is None:
                    if not isinstance(highVal, datetime.time):
                        return False
                elif highVal is None:
                    if not isinstance(lowVal, datetime.time):
                        return False
                elif (not isinstance(lowVal, datetime.time)) or (not isinstance(highVal, datetime.time)):
                    return False
            elif isinstance(p[0], datetime.timedelta):
                if lowVal is None:
                    if not isinstance(highVal, datetime.timedelta):
                        return False
                elif highVal is None:
                    if not isinstance(lowVal, datetime.timedelta):
                        return False
                elif (not isinstance(lowVal, datetime.timedelta)) or (not isinstance(highVal, datetime.timedelta)):
                    return False
            else:
                return False
            if (lowVal is not None) and (lowVal > p[0]):
                return False
            if (highVal is not None) and (highVal < p[0]):
                return False
            if (end0 != '[') and (lowVal is not None) and (lowVal == p[0]):
                return False
            if (end1 != ']') and (highVal is not None) and (highVal == p[0]):
                return False
            return True
        elif isinstance(p[2], list):     # in a list
            for i in range(len(p[2])):
                if isinstance(p[2][i], tuple) and (len(p[2][i]) == 4):
                    (end0, lowVal, highVal, end1) = p[2][i]
                    if isinstance(p[0], str):
                        if lowVal is None:
                            if  not isinstance(highVal, str):
                                continue
                        elif highVal is None:
                            if not isinstance(lowVal, str):
                                continue
                        elif not isinstance(lowVal, str) or not isinstance(highVal, str):
                            continue
                    elif type(p[0]) == int:              # Year, month durations
                        if lowVal is None:
                            if type(highVal) != int:
                                continue
                        elif highVal is None:
                            if type(lowVal) != int:
                                continue
                        elif (type(lowVal) != int) or (type(highVal) != int):
                            continue
                    elif isinstance(p[0], float):
                        if lowVal is None:
                            if not isinstance(highVal, float):
                                continue
                        elif highVal is None:
                            if not isinstance(lowVal, float):
                                continue
                        elif not isinstance(lowVal, float) or not isinstance(highVal, float):
                            continue
                    elif isinstance(p[0], datetime.date):                # True for both dates and datetimes
                        if lowVal is None:
                            if not isinstance(highVal, datetime.date):
                                continue
                        elif highVal is None:
                            if not isinstance(lowVal, datetime.date):
                                continue
                        elif (not isinstance(lowVal, datetime.date)) or (not isinstance(highVal, datetime.date)):
                            continue
                    elif isinstance(p[0], datetime.time):
                        if lowVal is None:
                            if not isinstance(highVal, datetime.time):
                                continue
                        elif highVal is None:
                            if not isinstance(lowVal, datetime.time):
                                continue
                        elif (not isinstance(lowVal, datetime.time)) or (not isinstance(highVal, datetime.time)):
                            continue
                    elif isinstance(p[0], datetime.timedelta):
                        if (lowVal is None) and not isinstance(highVal, datetime.timedelta):
                            return False
                        elif (highVal is None) and not isinstance(lowVal, datetime.timedelta):
                            return False
                        elif (not isinstance(lowVal, datetime.timedelta)) or (not isinstance(highVal, datetime.timedelta)):
                            continue
                    else:
                        return False
                    if (lowVal is not None) and (lowVal > p[0]):
                        continue
                    if (highVal is not None) and (highVal < p[0]):
                        continue
                    if (end0 != '[') and (lowVal is not None) and (lowVal == p[0]):
                        continue
                    if (end1 != ']') and (highVal is not None) and (highVal == p[0]):
                        continue
                    return True
                elif isinstance(p[2], dict):     # in a dict
                    if isinstance(p[0], dict):      # dictionary is a subset of a dictionary
                        for thisKey in p[0]:
                            if thisKey not in p[2]:
                                break
                            if type(p[0][thisKey]) != type(p[2][thisKey]):
                                break
                            if p[0][thisKey] != p[2][thisKey]:
                                break
                        else:
                            return True
                        continue
                    else:
                        return False
                elif p[0] == p[2][i]:
                    return True
            return False
        elif isinstance(p[2], dict):     # in a dict
            if isinstance(p[0], dict):      # dictionary is a subset of a dictionary
                for thisKey in p[0]:
                    if thisKey not in p[2]:
                        return False
                    if type(p[0][thisKey]) != type(p[2][thisKey]):
                        return False
                    if p[0][thisKey] != p[2][thisKey]:
                        return False
                return True
            else:
                return False
        elif (p[0] is None) and (p[2] is None):
             return True
        elif isinstance(p[0], bool) and isinstance(p[2], bool):
             return p[0] == p[2]
        elif isinstance(p[0], str) and isinstance(p[2], str):
             return p[0] == p[2]
        elif (type(p[0]) == int) and (type(p[2]) == int):             # Year, month durations
            return p[0] == p[2]
        elif isinstance(p[0], float) and isinstance(p[2], float):
            return p[0] == p[2]
        elif isinstance(p[0], datetime.date) and isinstance(p[2], datetime.date):         # True for both dates and datetimes
            return p[0] == p[2]
        elif isinstance(p[0], datetime.time) and isinstance(p[2], datetime.time):
            return p[0] == p[2]
        elif isinstance(p[0], datetime.timedelta) and isinstance(p[2], datetime.timedelta):
            return p[0] == p[2]
        else:
            return None

    @_('LPAREN expr RPAREN', 'LPAREN ltrange RPAREN', 'LPAREN gtrange RPAREN')
    def expr(self, p):
        return p[1]

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
        if (type(var0) == int) and (type(var1) == int):         #  Addition of two durations(yearMonth)
            return var0 + var1
        if isinstance(var0, float) and isinstance(var1, float):
            return var0 + var1
        if isinstance(var0, str) and isinstance(var1, str):         # Concatenation of strings
            return var0 + var1
        if isinstance(var0, datetime.date):                     # True for both dates and datetimes
            if isinstance(var1, datetime.timedelta):            # date/datetime plus days and time duration
                return var0 + var1
            elif type(var1) == int:                       # date/datetime plus year and month duration
                year = (var0).year
                month = (var0).month + var1
                while month < 1:                                # Allow for addition of a negative duration
                    year -= 1
                    month += 12
                while month > 12:                               # Bring month into range 1-12
                    year += 1
                    month -= 12
                try:
                    newDate = (var0).replace(year=int(year), month=int(month))
                except:
                    newDate = (var0).replace(year=int(year), month=int(month), day=28)
                return newDate
            else:
                return None
        if isinstance(var1, datetime.date):                 # True for both dates and datetimes
            if isinstance(var0, datetime.timedelta):         # day and time duration plus date/datetime
                return var0 + var1
            elif type(var0) == int:                    # year and month duration plus date/datetime
                year = (var1).year
                month = (var1).month + var0
                while month < 1:                            # Allow for the addtion of a negative duration
                    year -= 1
                    month += 12
                while month > 12:                           # Bring month into range 1-12
                    year += 1
                    month -= 12
                try:
                    newDate = (var1).replace(year=int(year), month=int(month))
                except:
                    newDate = (var1).replace(year=int(year), month=int(month), day=28)
                return newDate
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
        if (type(var0) == int) and (type(var1) == int):         # Subtraction of two durations(yearMonth)
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
            if type(var1) == int:                       # date/datetime minus years and months duration
                year = (var0).year
                month = (var0).month - p.expr1
                while month > 12:
                    year += 1
                    month -= 12
                while month < 1:
                    year -= 1
                    month += 12
                try:
                    newDate = (var0).replace(year=int(year), month=int(month))
                except:
                    newDate = (var0).replace(year=int(year), month=int(month), day=28)
                return newDate
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
        if (type(var0) == int) and isinstance(var1, float):               # Year, month duration * number
            return int(var0 * var1)
        if isinstance(var0, float) and (type(var1) == int):               # number * Year, month duration
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
        if (type(var0) == int) and isinstance(var1, float):               # Year, month duration / number
            try:
                return int(var0 / var1)
            except:
                 return None
        if (type(var0) == int) and (type(var1) == int):               # Year, month duration / Year, month duration
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
        '''
        var = p.expr
        if isinstance(var, bool):
            return not var
        if isinstance(var, int):                # Year, month duration
            return -var
        if isinstance(var, float):
            return -var
        return None

    @_('expr EQUALS expr', 'ltrange EQUALS expr', 'expr EQUALS ltrange', 'gtrange EQUALS expr', 'expr EQUALS gtrange',
       'ltrange EQUALS ltrange', 'gtrange EQUALS gtrange', 'ltrange EQUALS gtrange', 'gtrange EQUALS ltrange')
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
        if x0 is None:
            if x1 is None:
                return True
            return False
        if x1 is None:
            return False
        if isinstance(x0, bool):
            if not isinstance(x1, bool):
                return None
            return x0 == x1
        if isinstance(x1, bool):
            if not isinstance(x0, bool):
                return None
            return x0 == x1
        if type(x0) != type(x1):
            return None
        if isinstance(x0, datetime.datetime):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        if isinstance(x0, datetime.time):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        try:
            return x0 == x1
        except:
            return False

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
        if x0 is None:
            if x1 is None:
                return False
            return True
        if x1 is None:
            return True
        if isinstance(x0, bool):
            if not isinstance(x1, bool):
                return None
            return x0 != x1
        if isinstance(x1, bool):
            if not isinstance(x0, bool):
                return None
            return x0 != x1
        if type(x0) != type(x1):
            return None
        if isinstance(x0, datetime.datetime):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        if isinstance(x0, datetime.time):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        try:
            return x0 != x1
        except:
            return True


    @_('LBRACKET RBRACKET')
    def expr(self, p):
        return []

    @_('LCURLY RCURLY')
    def expr(self, p):
        return {}
        
    @_('expr LBRACKET ITEM NAME ltrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        if end1 == ')':
            return (p.expr, p.NAME, '<', highVal)
        else:
            return (p.expr, p.NAME, '<=', highVal)

    @_('expr LBRACKET NAME ltrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        thisName = p.NAME
        if p.NAME.startswith('item.') and (len(p.NAME) > 5):
            thisName = p.NAME[5:]
        if end1 == ')':
            return (p.expr, thisName, '<', highVal)
        else:
            return (p.expr, thisName, '<=', highVal)

    @_('expr LBRACKET ITEM ltrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        if end1 == ')':
            return (p.expr, '<', highVal)
        else:
            return (p.expr, '<=', highVal)

    @_('expr LBRACKET ltrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        if end1 == ')':
            return (p.expr, '<', highVal)
        else:
            return (p.expr, '<=', highVal)

    @_('expr LBRACKET ITEM NAME gtrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        if end0 == '(':
            return (p.expr, p.NAME, '>', lowVal)
        else:
            return (p.expr, p.NAME, '>=', lowVal)

    @_('expr LBRACKET NAME gtrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        thisName = p.NAME
        if p.NAME.startswith('item.') and (len(p.NAME) > 5):
            thisName = p.NAME[5:]
        if end0 == '(':
            return (p.expr, thisName, '>', lowVal)
        else:
            return (p.expr, thisName, '>=', lowVal)

    @_('expr LBRACKET ITEM gtrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        if end0 == '(':
            return (p.expr, '>', lowVal)
        else:
            return (p.expr, '>=', lowVal)

    @_('expr LBRACKET gtrange RBRACKET')
    def listFilter(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        if end0 == '(':
            return (p.expr, '>', lowVal)
        else:
            return (p.expr, '>=', lowVal)

    @_('expr LBRACKET ITEM NAME EQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.expr0, p.NAME, p.EQUALS, p.expr1)

    @_('expr LBRACKET NAME EQUALS expr RBRACKET')
    def listFilter(self, p):
        thisName = p.NAME
        if p.NAME.startswith('item.') and (len(p.NAME) > 5):
            thisName = p.NAME[5:]
        return (p.expr0, thisName, p.EQUALS, p.expr1)

    @_('expr LBRACKET ITEM EQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.expr0, p.EQUALS, p.expr1)

    @_('expr LBRACKET EQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.expr0, p.EQUALS, p.expr1)

    @_('expr LBRACKET ITEM NAME NOTEQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.expr0, p.NAME, p.NOTEQUALS, p.expr1)

    @_('expr LBRACKET NAME NOTEQUALS expr RBRACKET')
    def listFilter(self, p):
        thisName = p.NAME
        if p.NAME.startswith('item.') and (len(p.NAME) > 5):
            thisName = p.NAME[5:]
        return (p.expr0, thisName, p.NOTEQUALS, p.expr1)

    @_('expr LBRACKET ITEM NOTEQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.expr0, p.NOTEQUALS, p.expr1)

    @_('expr LBRACKET NOTEQUALS expr RBRACKET')
    def listFilter(self, p):
        return (p.expr0, p.NOTEQUALS, p.expr1)

    @_('listFilter')
    def expr(self, p):
        ''' select items from a list '''
        if not isinstance(p.listFilter, tuple):
            return None
        if len(p.listFilter) == 3:          # specific items from a list of numbers or strings
            (thisList, equality, value) = p.listFilter
            if not isinstance(thisList, list):
                return None
            retList = []
            for i in range(len(thisList)):
                if (isinstance(thisList[i], list)) or (isinstance(thisList[i], dict)):
                    continue
                item = thisList[i]
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
        elif len(p.listFilter) == 4:    # specific things from a list of contexts
            (thisList, key, equality, value) = p.listFilter
            if not isinstance(thisList, list):
                return None
            retList = []
            for i in range(len(thisList)):
                if not isinstance(thisList[i], dict):
                    continue
                if key in thisList[i]:
                    item = thisList[i][key]
                    if item is None:
                        continue
                    try:
                        if equality == '>=':
                            if item >= value:
                                retList.append(thisList[i])
                        elif equality == '>':
                            if item > value:
                                retList.append(thisList[i])
                        elif equality == '<=':
                            if item <= value:
                                retList.append(thisList[i])
                        elif equality == '<':
                            if item < value:
                                retList.append(thisList[i])
                        elif equality == '=':
                            if item == value:
                                retList.append(thisList[i])
                        elif equality == '!=':
                            if item != value:
                                retList.append(thisList[i])
                        else:
                            return None
                    except:
                        pass
            return retList
        else:
            return None

    @_('expr LBRACKET expr RBRACKET')
    def expr(self, p):
        if isinstance(p.expr1, bool):
            if p.expr1:                 # The listFilter 'true'
                if isinstance(p.expr0, list):
                    return p.expr0
                else:
                    return [p.expr0]
            else:
                return []
        if not isinstance(p.expr1, float):
            return None
        if not isinstance(p.expr0, list):
            if int(p.expr1) == 1:           # The first element, of a non-list, is the element itself
                return p.expr0
        if int(p.expr1) == 0:
            return None
        if len(p.expr0) < abs(int(p.expr1)):
            return None
        if int(p.expr1) > 0:
            return p.expr0[int(p.expr1) - 1]
        else:
            return p.expr0[int(p.expr1)]

    @_('DOTYEARS')
    def listSelect(self, p):
        return 'years'

    @_('DOTMONTHS')
    def listSelect(self, p):
        return 'months'

    @_('DOTDAYS')
    def listSelect(self, p):
        return 'days'

    @_('DOTHOURS')
    def listSelect(self, p):
        return 'hours'

    @_('DOTMINUTES')
    def listSelect(self, p):
        return 'minutes'

    @_('DOTSECONDS')
    def listSelect(self, p):
        return 'seconds'

    @_('DOTYEAR')
    def listSelect(self, p):
        return 'year'

    @_('DOTMONTH')
    def listSelect(self, p):
        return 'month'

    @_('DOTDAY')
    def listSelect(self, p):
        return 'day'

    @_('DOTWEEKDAY')
    def listSelect(self, p):
        return 'weekday'

    @_('DOTHOUR')
    def listSelect(self, p):
        return 'hour'

    @_('DOTMINUTE')
    def listSelect(self, p):
        return 'minute'

    @_('DOTSECOND')
    def listSelect(self, p):
        return 'second'

    @_('DOTTIMEZONE')
    def listSelect(self, p):
        return 'timezone'

    @_('DOTTIMEOFFSET')
    def listSelect(self, p):
        return 'time offset'

    @_('DOTTIME_OFFSET')
    def listSelect(self, p):
        return 'time_offset'

    @_('DOTSTARTINCLUDED')
    def listSelect(self, p):
        return 'start included'

    @_('DOTSTART_INCLUDED')
    def listSelect(self, p):
        return 'start_included'

    @_('DOTENDINCLUDED')
    def listSelect(self, p):
        return 'end included'

    @_('DOTEND_INCLUDED')
    def listSelect(self, p):
        return 'end_included'

    @_('DOTSTART')
    def listSelect(self, p):
        return 'start'

    @_('DOTEND')
    def listSelect(self, p):
        return 'end'

    @_('PERIOD NAME')
    def listSelect(self, p):
        return p.NAME

    @_('expr listSelect')
    def expr(self, p):
        ''' select value(s) for name p.listSelect from a list/context/date/datetime/time/duration/range '''
        key = p.listSelect
        thisList = p.expr
        # if isinstance(thisList, list) and (len(thisList) == 1):
        #     thisList = thisList[0]
        if isinstance(thisList, list):
            retList = []
            for i in range(len(thisList)):
                if not isinstance(thisList[i], dict):
                    continue
                if key in thisList[i]:
                    retList.append(thisList[i][key])
            return retList
        elif isinstance(thisList, dict):
            if key in thisList:
                return thisList[key]
            else:
                return None
        elif isinstance(thisList, datetime.date):         # True for both dates and datetimes
            if type(thisList) is datetime.datetime:           # Only true for datetimes
                if key == 'year':
                    return float(thisList.year)
                elif key == 'month':
                    return float(thisList.month)
                elif key == 'day':
                    return float(thisList.day)
                elif key == 'weekday':
                    return float(thisList.isoweekday())
                elif key == 'hour':
                    return float(thisList.hour)
                elif key == 'minute':
                    return float(thisList.minute)
                elif key == 'second':
                    return float(thisList.second)
                elif key == 'timezone':
                    if thisList.tzinfo is None:
                        return None
                    try:
                        return str(thisList.tzinfo.zone)
                    except:
                        return str(thisList.tzname())
                elif key == 'time offset':
                    if thisList.tzinfo is None:
                        return None
                    return thisList.utcoffset()
                elif key == 'time_offset':
                    if thisList.tzinfo is None:
                        return None
                    return thisList.utcoffset()
                else:
                    return None
            else:                                           # datetime.date
                if key == 'year':
                    return float(thisList.year)
                elif key == 'month':
                    return float(thisList.month)
                elif key == 'day':
                    return float(thisList.day)
                elif key == 'weekday':
                    return float(thisList.isoweekday())
                else:
                    return None
        elif isinstance(thisList, datetime.time):
            if key == 'hour':
                return float(thisList.hour)
            elif key == 'minute':
                return float(thisList.minute)
            elif key == 'second':
                return float(thisList.second)
            elif key == 'timezone':
                if thisList.tzinfo is None:
                    return None
                try:
                    return str(thisList.tzinfo.zone)
                except:
                    return str(thisList.tzname())
            elif key == 'time offset':
                if thisList.tzinfo is None:
                    return None
                tmpDateTime = datetime.datetime.combine(datetime.date.today(), thisList)
                return tmpDateTime.utcoffset()
            elif key == 'time_offset':
                if thisList.tzinfo is None:
                    return None
                tmpDateTime = datetime.datetime.combine(datetime.date.today(), thisList)
                return tmpDateTime.utcoffset()
            else:
                return None
        elif isinstance(thisList, datetime.timedelta):
            if key == 'days':
                return int(thisList.total_seconds() / 60 / 60 / 24)
            elif key == 'hours':
                return int(thisList.total_seconds() / 60 / 60) % 24
            elif key == 'minutes':
                return int(thisList.total_seconds() / 60) % 60
            elif key == 'seconds':
                return thisList.total_seconds() % 60
            else:
                return None
        elif type(thisList) == int:           # Year, month duration
            if key == 'years':
                return int(thisList / 12)
            elif key == 'months':
                return thisList % 12
            else:
                return None
        elif isinstance(thisList, tuple) and (len(thisList) == 4):
            (end0, low0, high1, end1) = thisList
            if key == 'start':
                return low0
            elif key == 'end':
                return high1
            elif key == 'start included':
                if end0 == '[':
                    return True
                else:
                    return False
            elif key == 'start_included':
                if end0 == '[':
                    return True
                else:
                    return False
            elif key == 'end included':
                if end1 == ']':
                    return True
                else:
                    return False
            elif key == 'end_included':
                if end1 == ']':
                    return True
                else:
                    return False
            else:
                return None
        return None            

    @_('expr ltrange')
    def expr(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        if (isinstance(p.expr, list) and (len(p.expr) == 1)):
            x0 = p.expr[0]
        else:
            x0 = p.expr
        if (isinstance(highVal, list) and (len(highVal) == 1)):
            x1 = highVal[0]
        else:
            x1 = highVal
        if isinstance(x0, bool):
            return False
        if isinstance(x1, bool):
            return False
        if type(x0) != type(x1):
            return None
        if isinstance(x0, datetime.datetime):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        if isinstance(x0, datetime.time):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        try:
            if end1 == ')':
                return x0 < x1
            else:
                return x0 <= x1
        except:
            return False

    @_('expr gtrange')
    def expr(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        if (isinstance(p.expr, list) and (len(p.expr) == 1)):
            x0 = p.expr[0]
        else:
            x0 = p.expr
        if (isinstance(lowVal, list) and (len(lowVal) == 1)):
            x1 = lowVal[0]
        else:
            x1 = lowVal
        if isinstance(x0, bool):
            return False
        if isinstance(x1, bool):
            return False
        if type(x0) != type(x1):
            return None
        if isinstance(x0, datetime.datetime):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        if isinstance(x0, datetime.time):
            if x0.tzinfo is not None:
                if x1.tzinfo is None:
                    tzinfo = x0.tzinfo
                    x1 = x1.replace(tzinfo=tzinfo)
            elif x1.tzinfo is not None:
                tzinfo = x1.tzinfo
                x0 = x0.replace(tzinfo=tzinfo)
        try:
            if end0 == '(':
                return x0 > x1
            else:
                return x0 >= x1
        except:
            return False

    @_('expr BETWEEN expr')
    def betweenExpr(self, p):
        return (p.expr0, p.expr1)

    @_('AND expr')
    def andExpr(self, p):
        return p.expr

    @_('betweenExpr andExpr')
    def expr(self, p):
        (expr0, expr1) = p.betweenExpr
        expr2 = p.andExpr
        if (isinstance(expr0, list) and (len(expr0) == 1)):
            expr0 = expr0[0]
        if (isinstance(expr1, list) and (len(expr1) == 1)):
            expr1 = expr1[0]
        if (isinstance(expr2, list) and (len(expr2) == 1)):
            expr2 = expr2[0]
        try:
            return (expr0 >= expr1) and (expr0 <= expr2)
        except:
            return None

    @_('expr andExpr')
    def expr(self, p):
        if isinstance(p.expr, bool):
            if isinstance(p.andExpr, bool):
                return p.expr and p.andExpr  # True/True, True/False, False/True, False/False
            if not p.expr:
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
            if p.expr0:         # True/Otherwise
                return True
            else:               # False/Otherwise
                return None
        elif isinstance(p.expr1, bool):
            if p.expr1:     # Otherwise/True
                return True
            else:           # Otherwise/False
                return None
        else:
            return None     # Otherwise/Otherwise

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
        if isinstance(p.expr, list):        # A list
            if (len(p.expr) > 0):
                retval = p.listPart
                retval.append(p.expr)
                return retval
            else:                           # A list of only 1 element is treated as value, not a list
                 return p.listPart + p.expr
        else:
            return p.listPart + [p.expr]

    @_('LCURLY NAME COLON expr', 'LCURLY ITEM COLON expr')
    def contextStart(self, p):
        self.inContext += 1
        self.contextNames.append({})
        self.contextNames[-1][p[1]] = p[3]
        return {p[1]: p[3]}

    @_('LCURLY STRING COLON expr')
    def contextStart(self, p):
        self.inContext += 1
        self.contextNames.append({})
        self.contextNames[-1][p[1][1:-1]] = p[3]
        return {p[1][1:-1]: p[3]}

    @_('NAME COLON expr', 'ITEM COLON expr')
    def contextPart(self, p):
        if self.inContext > 0:
            if p[0] in self.contextNames[-1]:
                self.error(p[0])
                return None
            else:
                self.contextNames[-1][p[0]] = p[2]
        return {p[0]: p[2]}

    @_('STRING COLON expr')
    def contextPart(self, p):
        if self.inContext > 0:
            if p[0][1:-1] in self.contextNames[-1]:
                self.error(p[0])
                return None
            else:
                self.contextNames[-1][p[0][1:-1]] = p[2]
        return {p[0][1:-1]: p[2]}

    @_('contextPart COMMA contextPart')
    def contextPart(self, p):
        if (p.contextPart0 is None) or (p.contextPart1 is None):
            return None
        return p.contextPart0 | p.contextPart1
   
    @_('LTTHAN expr')
    def ltrange(self, p):
        return ('(', None, p.expr, ')')

    @_('LTTHANEQUAL expr')
    def ltrange(self, p):
        return ('(', None, p.expr, ']')

    @_('GTTHAN expr')
    def gtrange(self, p):
        return ('(', p.expr, None, ')')

    @_('GTTHANEQUAL expr')
    def gtrange(self, p):
        return ('[', p.expr, None, ')')

    @_('LPAREN expr ELLIPSE expr RPAREN')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, p.RPAREN)

    @_('LPAREN expr ELLIPSE expr RBRACKET')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, p.RBRACKET)

    @_('LPAREN expr ELLIPSE expr LBRACKET')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, ')')

    @_('listStart ELLIPSE expr RPAREN')
    def expr(self, p):
        return ('[', p.listStart[0], p.expr, p.RPAREN)

    @_('listStart ELLIPSE expr RBRACKET')
    def expr(self, p):
        return ('[', p.listStart[0], p.expr, p.RBRACKET)

    @_('listStart ELLIPSE expr LBRACKET')
    def expr(self, p):
        return ('[', p.listStart[0], p.expr, ')')

    @_('contextStart RCURLY')
    def expr(self, p):
        self.inContext -= 1
        discard = self.contextNames.pop()
        return p.contextStart

    @_('contextStart COMMA contextPart RCURLY')
    def expr(self, p):
        self.inContext -= 1
        discard = self.contextNames.pop()
        if (p.contextStart is None) or (p.contextPart is None):
            return None
        return p.contextStart | p.contextPart

    @_('RBRACKET expr ELLIPSE expr RPAREN')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, p.RPAREN)

    @_('RBRACKET expr ELLIPSE expr RBRACKET')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, p.RBRACKET1)

    @_('RBRACKET expr ELLIPSE expr LBRACKET')
    def expr(self, p):
        return ('(', p.expr0, p.expr1, ')')

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

    @_('DATEFUNC expr RPAREN', 'DATEFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert datetime.date/datetime.time/str into datetime.date '''
        if len(p) == 3:
            fromParam = p[1]
        elif p[1] == 'from':
            fromParam = p[3]
        else:
            return None
        if isinstance(fromParam, list) and (len(fromParam) == 1):
            fromParam = fromParam[0]
        if isinstance(fromParam, datetime.time):
            return datetime.date(year=0, month=0, day=0)
        elif isinstance(fromParam, datetime.date):         # True for both dates and datetimes
            if type(fromParam) is datetime.datetime:           # Only true for datetimes
                return fromParam.date()
            else:
                return fromParam
        elif isinstance(fromParam, str):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("error")
                    return dateutil.parser.parse(fromParam).date()
            except:
                return None
        else:
            return None

    @_('DATEFUNC expr COMMA expr COMMA expr RPAREN', 'DATEFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert year, month, day into datetime.date '''
        yearParam = monthParam = dayParam = None
        if len(p) == 7:
            yearParam = p[1]
            monthParam = p[3]
            dayParam = p[5]
        else:
            for i in [1, 5, 9]:
                if (p[i] == 'year') and (yearParam is None):
                    if p[i + 2] is not None:
                        yearParam = p[i + 2]
                elif (p[i] == 'month') and (monthParam is None):
                    if p[i + 2] is not None:
                        monthParam = p[i + 2]
                elif (p[i] == 'day') and (dayParam is None):
                    if p[i + 2] is not None:
                        dayParam = p[i + 2]
                else:
                    return None
        if isinstance(yearParam, list) and (len(yearParam) == 1):
            yearParam = yearParam[0]
        if isinstance(monthParam, list) and (len(monthParam) == 1):
            monthParam = monthParam[0]
        if isinstance(dayParam, list) and (len(dayParam) == 1):
            dayParam = dayParam[0]
        if (yearParam is None) or (monthParam is None) or (dayParam is None):
            return None
        try:
            return datetime.date(year=int(yearParam), month=int(monthParam), day=int(dayParam))
        except:
            return None

    @_('TIMEFUNC expr COMMA expr COMMA expr RPAREN',
       'TIMEFUNC expr COMMA expr COMMA expr COMMA expr RPAREN',
       'TIMEFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN',
       'TIMEFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert hour, minute, second, offset into datetime.time '''
        hourParam = minuteParam = secondParam = offsetParam = None
        if len(p) <= 9:
            hourParam = p[1]
            minuteParam = p[3]
            secondParam = p[5]
            if len(p) == 9:
                offsetParam = p[7]
        else:
            params = [1, 5, 9]
            if len(p) == 17:
                params.append(13)
            for i in params:
                if (p[i] == 'hour') and (hourParam is None):
                    if p[i + 2] is not None:
                        hourParam = p[i + 2]
                elif (p[i] == 'minute') and (minuteParam is None):
                    if p[i + 2] is not None:
                        minuteParam = p[i + 2]
                elif (p[i] == 'second') and (secondParam is None):
                    if p[i + 2] is not None:
                        secondParam = p[i + 2]
                elif (len(p) == 17) and (p[i] == 'offset') and (offsetParam is None):
                    if p[i + 2] is not None:
                        offsetParam = p[i + 2]
                else:
                    return None
        if isinstance(hourParam, list) and (len(hourParam) == 1):
            hourParam = hourParam[0]
        if isinstance(minuteParam, list) and (len(minuteParam) == 1):
            minuteParam = minuteParam[0]
        if isinstance(secondParam, list) and (len(secondParam) == 1):
            secondParam = secondParam[0]
        if isinstance(offsetParam, list) and (len(offsetParam) == 1):
            offsetParam = offsetParam[0]
        if (hourParam is None) or (minuteParam is None) or (secondParam is None):
            return None
        if not isinstance(hourParam, float):
            return None
        if not isinstance(minuteParam, float):
            return None
        if not isinstance(secondParam, float):
            return None
        hour = int(hourParam)
        min = int(minuteParam)
        sec = secondParam
        while sec < 0.0:
            sec += 60.0
            min -= 1
        while sec >= 60.0:
            sec -= 60.0
            min += 1
        microSeconds = int((sec - int(sec)) * 1000000)
        sec = int(sec)
        while min < 0:
            min += 60
            hour -= 1
        while min > 59:
            min -= 60
            hour += 1
        hour %= 24
        thisTime = '%02d:%02d:%02d.%06d' % (hour, min, sec, microSeconds)
        if isinstance(offsetParam, datetime.timedelta):
            offset = offsetParam.total_seconds()
            if offset > 0:
                sign = '+'
            else:
                sign = '-'
                offset = -offset
            HH = int(offset / 60 / 60)
            MM = int(offset / 60) % 60
            SS = int(offset) % 60
            thisTime += sign + '%02d:%02d:%02d' % (HH, MM, SS)
        try:
            return datetime.time.fromisoformat(thisTime)
        except:
            return None

    @_('TIMEFUNC expr RPAREN', 'TIMEFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert datetime.date/datetime.time/str into datetime.time '''
        if len(p) == 3:
            fromParam = p[1]
        elif p[1] == 'from':
            fromParam = p[3]
        else:
            return None
        if isinstance(fromParam, list) and (len(fromParam) == 1):
            fromParam = fromParam[0]
        if isinstance(fromParam, datetime.time):
            return fromParam
        elif isinstance(fromParam, datetime.date):             # True for dates and datetimes
            if type(fromParam) is datetime.datetime:               # Only true for datetimes
                return fromParam.timetz()
            else:                                               # A date - return midnight
                return datetime.time(hour=0, minute=0, second=0)
        elif isinstance(fromParam, str):
            parts = fromParam.split('@')
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("error")
                    thisTime =  dateutil.parser.parse(parts[0]).timetz()     # A time with timezone
            except:
                return None
            if len(parts) == 1:
                if thisTime.utcoffset() is not None:
                    try:
                        if thisTime.utcoffset().total_seconds() > 50400:
                            return None
                        if thisTime.utcoffset().total_seconds() < -43200:
                            return None
                    except:
                        return None
                return thisTime
            try:
                thisZone = pytz.timezone(parts[1])
            except:
                return None
            if thisZone is None:
                return None
            try:
                retTime = datetime.datetime.combine(datetime.date.today(), thisTime)
                retTime = thisZone.localize(retTime)
                retTime = retTime.timetz()
            except:
                return thisTime
            return retTime
        return None

    @_('DATEANDTIMEFUNC expr COMMA expr RPAREN', 'DATEANDTIMEFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert date, time into datetime.datetime '''
        dateParam = timeParam = None
        if len(p) == 5:
            dateParam = p[1]
            timeParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'date') and (dateParam is None):
                    if p[i + 2] is not None:
                        dateParam = p[i + 2]
                elif (p[i] == 'time') and (timeParam is None):
                    if p[i + 2] is not None:
                        timeParam = p[i + 2]
                else:
                    return None
        if isinstance(dateParam, list) and (len(dateParam) == 1):
            dateParam = dateParam[0]
        if isinstance(timeParam, list) and (len(timeParam) == 1):
            timeParam = timeParam[0]
        if isinstance(timeParam, datetime.time):
            if isinstance(dateParam, datetime.date):
                if type(dateParam) is datetime.date:
                    return datetime.datetime.combine(dateParam, timeParam)
                else:
                    return datetime.datetime.combine(dateParam.date(), timeParam)
        return None

    @_('DATEANDTIMEFUNC expr RPAREN', 'DATEANDTIMEFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert str into datetime.datetime '''
        if len(p) == 3:
            fromParam = p[1]
        elif p[1] == 'from':
            fromParam = p[3]
        else:
            return None
        if isinstance(fromParam, list) and (len(fromParam) == 1):
            fromParam = fromParam[0]
        if isinstance(fromParam, str):
            parts = fromParam.split('@')
            subParts = parts[0].split('T')
            if len(subParts) != 2:     # One of date or time is missing - fail if it's date
                subParts = subParts[0].split(':')
                if len(subParts) > 1:
                    return None
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("error")
                    thisDateTime = dateutil.parser.parse(parts[0])
            except:
                return None
            if len(parts) == 1:
                if thisDateTime.utcoffset() is not None:
                    try:
                        if thisDateTime.utcoffset().total_seconds() > 50400:
                            return None
                        if thisDateTime.utcoffset().total_seconds() < -43200:
                            return None
                    except:
                        return None
                return thisDateTime
            try:
                thisZone = pytz.timezone(parts[1])
            except:
                return None
            if thisZone is None:
                return None
            try:
                retDateTime = thisZone.localize(thisDateTime)
            except:
                return thisDateTime
            return retDateTime
        return None

    @_('NUMBERFUNC expr COMMA expr COMMA expr RPAREN',
       'NUMBERFUNC NAME COLON expr COMMA NAME NAME COLON expr COMMA NAME NAME COLON expr RPAREN',
       'NUMBERFUNC NAME NAME COLON expr COMMA NAME COLON expr COMMA NAME NAME COLON expr RPAREN',
       'NUMBERFUNC NAME NAME COLON expr COMMA NAME NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Float from formatted string'''
        number = grouping = decimal = None
        groupingFound = decimalFound = False
        if len(p) == 7:
            number = p[1]
            grouping = p[3]
            decimal = p[5]
            groupingFound = decimalFound = True
        else:
            i = 1
            while (i < 14) and (i < len(p)):
                if (p[i] == 'from'):
                    if number is None:
                        number = p[i + 2]
                    i += 4
                elif (p[i] == 'grouping') and (p[i + 1] == 'separator'):
                    if not groupingFound:
                        grouping = p[i + 3]
                        groupingFound = True
                    i += 5
                elif (p[i] == 'decimal') and (p[i + 1] == 'separator'):
                    if not decimalFound:
                        decimal = p[i + 3]
                        decimalFound = True
                    i += 5
                else:
                    return None
        if isinstance(number, list) and (len(number) == 1):
            number = number[0]
        if isinstance(grouping, list) and (len(grouping) == 1):
            grouping = grouping[0]
        if isinstance(decimal, list) and (len(decimal) == 1):
            decimal = decimal[0]
        if (number is None):
            return None
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
            number = number.replace(decimal, '.')
        try:
            return float(number)
        except:
            return None

    @_('STRINGFUNC expr RPAREN', 'STRINGFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' string from value'''
        if len(p) == 3:
            fromParam = p[1]
        elif p[1] == 'from':
                fromParam = p[3]
        else:
            return None
        if isinstance(fromParam, list) and (len(fromParam) == 1):
            fromParam = fromParam[0]
        if fromParam == None:
            return 'null'
        if isinstance(fromParam, bool):
            if fromParam:
                return 'true'
            else:
                return 'false'
        if isinstance(fromParam, float):
            if float(int(fromParam)) == fromParam:
                return str(int(fromParam))
            else:
                return str(fromParam)
        if isinstance(fromParam, str):
            return fromParam
        if isinstance(fromParam, datetime.date):         # True for both dates and datetimes
            if type(fromParam) is datetime.datetime:           # Only true for datetimes
                if fromParam.tzinfo is not None:        # Try and return a timezone if possible
                    thisZone = None
                    try:
                        thisZone = str(fromParam.tzinfo.zone)
                    except:
                        try:
                            thisZone = str(fromParam.tzname())
                            if (thisZone.startswith('UTC')) and (len(thisZone) > 3):
                                thisZone = None
                        except:
                            pass
                    if thisZone is not None:
                        if fromParam.microsecond > 0:
                            thisDateTime = fromParam.strftime('%Y-%m-%dT%H:%M:%S.%f@') + thisZone
                        else:
                            thisDateTime = fromParam.strftime('%Y-%m-%dT%H:%M:%S@') + thisZone
                        return thisDateTime
                    else:
                        return fromParam.isoformat(sep='T')
                else:
                    return fromParam.isoformat(sep='T')
            else:
                return fromParam.isoformat()
        if isinstance(fromParam, datetime.time):
            if fromParam.tzinfo is not None:        # Try and return a timezone if possible
                thisZone = None
                try:
                    thisZone = str(fromParam.tzinfo.zone)
                except:
                    try:
                        thisZone = str(fromParam.tzname())
                        if (thisZone.startswith('UTC')) and (len(thisZone) > 3):
                            thisZone = None
                    except:
                        pass
                if thisZone is not None:
                    if fromParam.microsecond > 0:
                        thisTime = fromParam.strftime('%H:%M:%S.%f@') + thisZone
                    else:
                        thisTime = fromParam.strftime('%H:%M:%S@') + thisZone
                    return thisTime
                else:
                    return fromParam.isoformat()
            else:
                return fromParam.isoformat()
        if isinstance(fromParam, datetime.timedelta):
            duration = fromParam.total_seconds()
            secs = duration % 60
            duration = int(duration / 60)
            mins = duration % 60
            duration = int(duration / 60)
            hours = duration % 24
            days = int(duration / 24)
            return 'P%dDT%dH%dM%dS' % (days, hours, mins, secs)
        if type(fromParam,) == int:                  # Year, month duration
            year = int(fromParam / 12)
            month = fromParam % 12
            return 'P%dY%dM' % (year, month)
        return None

    @_('NOTFUNC expr RPAREN', 'NOTFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' negate a boolean'''
        if len(p) == 3:
            negandParam = p[1]
        elif p[1] == 'negand':
                negandParam = p[3]
        else:
            return None
        if isinstance(negandParam, list) and (len(negandParam) == 1):
            negandParam = negandParam[0]
        if not isinstance(negandParam, bool):
            return None
        return not negandParam

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
                    if lowVal is None:
                        if not isinstance(highVal, str):
                            continue
                    elif highVal is None:
                        if not isinstance(lowVal, str):
                            continue
                    elif not isinstance(lowVal, str) or not isinstance(highVal, str):
                        continue
                elif type(inValue) == int:              # a list of Year, month durations
                    if lowVal is None:
                        if type(highVal) != int:
                            continue
                    elif highVal is None:
                        if type(lowVal) != int:
                            continue
                    elif (type(lowVal) != int) or (type(highVal) != int):
                        continue
                elif isinstance(inValue, float):
                    if lowVal is None:
                        if not isinstance(highVal, float):
                            return False
                    elif highVal is None:
                        if not isinstance(lowVal, float):
                            return False
                    elif not isinstance(lowVal, float) or not isinstance(highVal, float):
                        continue
                elif isinstance(inValue, datetime.date):            # True for both dates and datetimes
                    if lowVal is None:
                        if not isinstance(highVal, datetime.date):
                            continue
                    elif highVal is None:
                        if not isinstance(lowVal, datetime.date):
                            continue
                    elif not isinstance(lowVal, datetime.date) or not isinstance(highVal, datetime.date):
                        continue
                elif isinstance(inValue, datetime.time):
                    if lowVal is None:
                        if not isinstance(highVal, datetime.time):
                            continue
                    elif highVal is None:
                        if not isinstance(lowVal, datetime.time):
                            continue
                    elif (not isinstance(lowVal, datetime.time)) or (not isinstance(highVal, datetime.time)):
                        continue
                elif isinstance(inValue, datetime.timedelta):
                    if lowVal is None:
                        if not isinstance(highVal, datetime.timedelta):
                            continue
                    elif highVal is None:
                        if not isinstance(lowVal, datetime.timedelta):
                            continue
                    elif not isinstance(lowVal, datetime.timedelta) or not isinstance(highVal, datetime.timedelta):
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
                if not isinstance(thisList[i], tuple) or (len(thisList[i]) != 2):
                    continue
                (comparitor, toValue) = thisList[i]
                if comparitor == '=':
                    try:
                        if (inValue == toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '<=':
                    try:
                        if (inValue <= toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '<':
                    try:
                        if (inValue < toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '>=':
                    try:
                        if (inValue >= toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '>':
                    try:
                        if (inValue > toValue):
                            return True
                    except:
                        pass
                    continue
                if comparitor == '!=':
                    try:
                        if (inValue != toValue):
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

    @_('expr INFUNC ltrange')
    def inStart(self, p):
        ''' item <= list of items'''
        (end0, lowVal, highVal, end1) = p.ltrange
        if isinstance(highVal, list):
            thisList = []
            for i in range(len(highVal)):
                if end1 == ')':
                    thisList.append([('<', highVal[i])])
                else:
                    thisList.append([('<=', highVal[i])])
            return [p.expr] + thisList
        else:
            if end1 == ')':
                return [p.expr] + [('<', highVal)]
            else:
                return [p.expr] + [('<=', highVal)]

    @_('expr INFUNC gtrange')
    def inStart(self, p):
        ''' item >= list of items'''
        (end0, lowVal, highVal, end1) = p.gtrange
        if isinstance(lowVal, list):
            thisList = []
            for i in range(len(lowVal)):
                if end0 == '(':
                    thisList.append([('>', lowVal[i])])
                else:
                    thisList.append([('>=', lowVal[i])])
            return [p.expr] + thisList
        else:
            if end0 == '(':
                return [p.expr] + [('>', lowVal)]
            else:
                return [p.expr] + [('>=', lowVal)]

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

    @_('COMMA ltrange')
    def inPart(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        if isinstance(highVal, list):
            thisList = []
            for i in range(len(highVal)):
                if end1 == ')':
                    thisList.append([('<', highVal[i])])
                else:
                    thisList.append([('<=', highVal[i])])
            return thisList
        else:
            if end1 == ')':
                return [('<', highVal)]
            else:
                return [('<=', highVal)]

    @_('COMMA gtrange')
    def inPart(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        if isinstance(lowVal, list):
            thisList = []
            for i in range(len(lowVal)):
                if end0 == '(':
                    thisList.append([('>', lowVal[i])])
                else:
                    thisList.append([('>=', lowVal[i])])
            return thisList
        else:
            if end0 == '(':
                return [('>', lowVal)]
            else:
                return [('>=', lowVal)]

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

    @_('inPart COMMA ltrange')
    def inPart(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        if isinstance(highVal, list):
            thisList = []
            for i in range(len(highVal)):
                if end1 == ')':
                    thisList.append([('<', highVal[i])])
                else:
                    thisList.append([('<=', highVal[i])])
            return p.inPart + thisList
        else:
            if end1 == ')':
                return p.inPart + [('<', highVal)]
            else:
                return p.inPart + [('<=', highVal)]

    @_('inPart COMMA gtrange')
    def inPart(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        if isinstance(lowVal, list):
            thisList = []
            for i in range(len(lowVal)):
                if end0 == '(':
                    thisList.append([('>', lowVal[i])])
                else:
                    thisList.append([('>=', lowVal[i])])
            return p.inPart + thisList
        else:
            if end0 == '(':
                return p.inPart + [('>', lowVal)]
            else:
                return p.inPart + [('>=', lowVal)]

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

    @_('listPart COMMA ltrange')
    def inPart(self, p):
        (end0, lowVal, highVal, end1) = p.ltrange
        thisList = []
        for i in range(len(p.listPart)):
            if end1 == ')':
                thisList.append(('<', p.listPart[i]))
            else:
                thisList.append(('<=', p.listPart[i]))
        if isinstance(highVal, list):
            for i in range(len(highVal)):
                if end1 == ')':
                    thisList.append([('<', p.expr[i])])
                else:
                    thisList.append([('<=', p.expr[i])])
        else:
            if end1 == ')':
                thisList.append([('<', highVal)])
            else:
                thisList.append([('<=', highVal)])
        return thisList

    @_('listPart COMMA gtrange')
    def inPart(self, p):
        (end0, lowVal, highVal, end1) = p.gtrange
        thisList = []
        for i in range(len(p.listPart)):
            if end0 == '(':
                thisList.append(('>', p.listPart[i]))
            else:
                thisList.append(('>=', p.listPart[i]))
        if isinstance(lowVal, list):
            for i in range(len(lowVal)):
                if end0 == '(':
                    thisList.append([('>', lowVal[i])])
                else:
                    thisList.append([('>=', lowVal[i])])
        else:
            if end0 == '(':
                thisList.append([('>', lowVal)])
            else:
                thisList.append([('>=', lowVal)])
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
        thisList[1] = ('(', lowVal, p.expr, ')')
        return self.inFunc(thisList)

    @_('SUBSTRINGFUNC expr COMMA expr RPAREN', 'SUBSTRINGFUNC expr COMMA expr COMMA expr RPAREN',
       'SUBSTRINGFUNC NAME COLON expr COMMA NAME NAME COLON expr RPAREN', 'SUBSTRINGFUNC NAME NAME COLON expr COMMA NAME COLON expr RPAREN',
       'SUBSTRINGFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME NAME COLON expr RPAREN',
       'SUBSTRINGFUNC NAME COLON expr COMMA NAME NAME COLON expr COMMA NAME COLON expr RPAREN',
       'SUBSTRINGFUNC NAME NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' substring from a substring'''
        stringParam = startParam = lengthParam = None
        if len(p) <= 7:
            stringParam = p[1]
            startParam = p[3]
            if len(p) == 7:
                lengthParam = p[5]
        else:
            i = 1
            while (i < 13) and (i < len(p)):
                if (p[i] == 'string'):
                    if stringParam is None:
                        stringParam = p[i + 2]
                    i += 4
                elif (p[i] == 'start') and (p[i + 1] == 'position'):
                    if startParam is None:
                        startParam = p[i + 3]
                    i += 5
                elif (p[i] == 'length'):
                    if lengthParam is None:
                        lengthParam = p[i + 2]
                    i += 4
                else:
                    return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if isinstance(startParam, list) and (len(startParam) == 1):
            startParam = startParam[0]
        if isinstance(lengthParam, list) and (len(lengthParam) == 1):
            lengthParam = lengthParam[0]
        if (stringParam is None) or (startParam is None):
            return None
        if not isinstance(stringParam, str):
            return None
        if not isinstance(startParam, float) or (int(startParam) != startParam):
            return None
        start = int(startParam)
        if lengthParam is None:
            if start == 0:
                return None
            elif start > 0:
                return stringParam[start - 1:]
            else:
                return stringParam[start:]
        if not isinstance(lengthParam, float) or (lengthParam < 0):
            return None
        length = int(lengthParam)
        if start == 0:
           return None
        elif start > 0:
            return stringParam[start - 1:start - 1 + length]
        else:
            if abs(start) <= length:
                return stringParam[start:]
            return stringParam[start:start + length]
 
    @_('STRINGLENFUNC expr RPAREN', 'STRINGLENFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' length of a string'''
        if len(p) == 3:
            stringParam = p[1]
        elif p[1] == 'string':
            stringParam = p[3]
        else:
            return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if not isinstance(stringParam, str):
            return None
        return float(len(stringParam))

    @_('UPPERCASEFUNC expr RPAREN', 'UPPERCASEFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        if len(p) == 3:
            stringParam = p[1]
        elif p[1] == 'string':
            stringParam = p[3]
        else:
            return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if not isinstance(stringParam, str):
            return None
        return copy.copy(stringParam.upper())

    @_('LOWERCASEFUNC expr RPAREN', 'LOWERCASEFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' lowercase of a string'''
        if len(p) == 3:
            stringParam = p[1]
        elif p[1] == 'string':
            stringParam = p[3]
        else:
            return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if not isinstance(stringParam, str):
            return None
        return stringParam.lower()

    @_('SUBSTRINGBEFOREFUNC expr COMMA expr RPAREN', 'SUBSTRINGBEFOREFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' substring before string'''
        stringParam = matchParam = None
        if len(p) == 5:
            stringParam = p[1]
            matchParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'string') and (stringParam is None):
                    stringParam = p[i + 2]
                elif (p[i] == 'match') and (matchParam is None):
                    matchParam = p[i + 2]
                else:
                    return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if isinstance(matchParam, list) and (len(matchParam) == 1):
            matchParam = matchParam[0]
        if (stringParam is None) or (matchParam is None):
            return None
        if not isinstance(stringParam, str):
            return None
        if not isinstance(matchParam, str):
            return None
        subAt = stringParam.find(matchParam)
        if subAt == -1:
            return ''
        return stringParam[:subAt] 

    @_('SUBSTRINGAFTERFUNC expr COMMA expr RPAREN', 'SUBSTRINGAFTERFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' substring after string'''
        stringParam = matchParam = None
        if len(p) == 5:
            stringParam = p[1]
            matchParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'string') and (stringParam is None):
                    stringParam = p[i + 2]
                elif (p[i] == 'match') and (matchParam is None):
                    matchParam = p[i + 2]
                else:
                    return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if isinstance(matchParam, list) and (len(matchParam) == 1):
            matchParam = matchParam[0]
        if (stringParam is None) or (matchParam is None):
            return None
        if not isinstance(stringParam, str):
            return None
        if not isinstance(matchParam, str):
            return None
        subAt = stringParam.find(matchParam)
        if subAt == -1:
            return ''
        return stringParam[subAt + len(matchParam):]

    @_('REPLACEFUNC expr COMMA STRING COMMA expr RPAREN', 'REPLACEFUNC expr COMMA STRING COMMA expr COMMA expr RPAREN',
       'REPLACEFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN', 'REPLACEFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' replace substring in string with flags'''
        inputParam = patternParam = replacementParam = flagsParam = None
        if len(p) <= 9:
            inputParam = p[1]
            patternParam = self.unicodeString(str(p[3][1:-1]))
            replacementParam = p[5]
            if len(p) == 9:
                flagsParam = p[7]
        else:
            params = [1, 5, 9]
            if len(p) == 17:
                params.append(13)
            for i in params:
                if (p[i] == 'input') and (inputParam is None):
                    inputParam = p[i + 2]
                elif (p[i] == 'pattern') and (patternParam is None):
                    patternParam = p[i + 2]
                elif (p[i] == 'replacement') and (replacementParam is None):
                    replacementParam = p[i + 2]
                elif (len(p) == 17) and (p[i] == 'flags') and (flagsParam is None):
                    flagsParam = p[i + 2]
                else:
                    return None
        if isinstance(inputParam, list) and (len(inputParam) == 1):
            inputParam = inputParam[0]
        if isinstance(patternParam, list) and (len(patternParam) == 1):
            patternParam = patternParam[0]
        if isinstance(replacementParam, list) and (len(replacementParam) == 1):
            replacementParam = replacementParam[0]
        if (inputParam is None) or (patternParam is None) or (replacementParam is None):
            return None
        if not isinstance(inputParam, str):
            return None
        if not isinstance(patternParam, str):
            return None
        if not isinstance(replacementParam, str):
            return None
        reFlags = 0
        if flagsParam is not None:
            if not isinstance(flagsParam, str):
                return None
            if 's' in flagsParam:
                reFlags += re.S
            if 'm' in flagsParam:
                reFlags += re.M
            if 'i' in flagsParam:
                reFlags += re.I
            if 'x' in flagsParam:
                reFlags += re.X
        replace = re.sub(pattern=r'\$(\d+)', repl=lambda x: '\\' + str(int(x.group(1)) + 1), string=replacementParam)    # Convert SFEEL regular expressions to Python
        return re.sub(pattern=r'(' + patternParam + r')', repl=replace, string=inputParam, flags=reFlags)

    @_('CONTAINSFUNC expr COMMA expr RPAREN', 'CONTAINSFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' string contain substring'''
        stringParam = matchParam = None
        if len(p) == 5:
            stringParam = p[1]
            matchParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'string') and (stringParam is None):
                    stringParam = p[i + 2]
                elif (p[i] == 'match') and (matchParam is None):
                    matchParam = p[i + 2]
                else:
                    return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if isinstance(matchParam, list) and (len(matchParam) == 1):
            matchParam = matchParam[0]
        if (stringParam is None) or (matchParam is None):
            return None
        if not isinstance(stringParam, str):
            return None
        if not isinstance(matchParam, str):
            return None
        return matchParam in stringParam

    @_('STARTSWITHFUNC expr COMMA expr RPAREN', 'STARTSWITHFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' string start with substring'''
        stringParam = matchParam = None
        if len(p) == 5:
            stringParam = p[1]
            matchParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'string') and (stringParam is None):
                    stringParam = p[i + 2]
                elif (p[i] == 'match') and (matchParam is None):
                    matchParam = p[i + 2]
                else:
                    return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if isinstance(matchParam, list) and (len(matchParam) == 1):
            matchParam = matchParam[0]
        if (stringParam is None) or (matchParam is None):
            return None
        if not isinstance(stringParam, str):
            return None
        if not isinstance(matchParam, str):
            return None
        return stringParam.startswith(matchParam)

    @_('ENDSWITHFUNC expr COMMA expr RPAREN', 'ENDSWITHFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' string ends with substring'''
        stringParam = matchParam = None
        if len(p) == 5:
            stringParam = p[1]
            matchParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'string') and (stringParam is None):
                    stringParam = p[i + 2]
                elif (p[i] == 'match') and (matchParam is None):
                    matchParam = p[i + 2]
                else:
                    return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            stringParam = stringParam[0]
        if isinstance(matchParam, list) and (len(matchParam) == 1):
            matchParam = matchParam[0]
        if (stringParam is None) or (matchParam is None):
            return None
        if not isinstance(stringParam, str):
            return None
        if not isinstance(matchParam, str):
            return None
        return stringParam.endswith(matchParam)

    @_('MATCHESFUNC expr COMMA STRING RPAREN', 'MATCHESFUNC expr COMMA STRING COMMA expr RPAREN',
       'MATCHESFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'MATCHESFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' string re matchs string with flags'''
        inputParam = patternParam = flagsParam = None
        if len(p) <= 7:
            inputParam = p[1]
            patternParam = self.unicodeString(str(p[3][1:-1]))
            if len(p) == 7:
                flagsParam = p[5]
        else:
            params = [1, 5]
            if len(p) == 13:
                params.append(9)
            for i in params:
                if (p[i] == 'input') and (inputParam is None):
                    inputParam = p[i + 2]
                elif (p[i] == 'pattern') and (patternParam is None):
                    patternParam = p[i + 2]
                elif (len(p) == 13) and (p[i] == 'flags') and (flagsParam is None):
                    flagsParam = p[i + 2]
                else:
                    return None
        if isinstance(inputParam, list) and (len(inputParam) == 1):
            inputParam = inputParam[0]
        if isinstance(patternParam, list) and (len(patternParam) == 1):
            patternParam = patternParam[0]
        if isinstance(flagsParam, list) and (len(flagsParam) == 1):
            flagsParam = flagsParam[0]
        if (inputParam is None) or (patternParam is None):
            return None
        if not isinstance(inputParam, str):
            return None
        if not isinstance(patternParam, str):
            return None
        reFlags = 0
        if flagsParam is not None:
            if not isinstance(flagsParam, str):
                return None
            if 's' in flagsParam:
                reFlags += re.S
            if 'm' in flagsParam:
                reFlags += re.M
            if 'i' in flagsParam:
                reFlags += re.I
            if 'x' in flagsParam:
                reFlags += re.X
        thisMatch = re.match(patternParam, inputParam, flags=reFlags)
        if thisMatch is not None:
            return True
        return False

    @_('SPLITFUNC expr COMMA STRING RPAREN', 'SPLITFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' split string on pattern'''
        stringParam = delimiterParam = None
        if len(p) == 5:
            stringParam = p[1]
            delimiterParam = self.unicodeString(str(p[3][1:-1]))
        else:
            for i in [1, 5]:
                if (p[i] == 'string') and (stringParam is None):
                    stringParam = p[i + 2]
                elif (p[i] == 'delimiter') and (delimiterParam is None):
                    delimiterParam = p[i + 2]
                else:
                    return None
        if isinstance(stringParam, list) and (len(stringParam) == 1):
            inputParam = inputParam[0]
        if isinstance(delimiterParam, list) and (len(delimiterParam) == 1):
            delimiterParam = delimiterParam[0]
        if (stringParam is None) or (delimiterParam is None):
            return None
        if not isinstance(stringParam, str):
            return None
        if not isinstance(delimiterParam, str):
            return None
        return re.split(delimiterParam, stringParam)

    @_('LISTCONTAINSFUNC expr COMMA expr RPAREN', 'LISTCONTAINSFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' list contains value'''
        if len(p) == 5:
            listParam = p[1]
            elementParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'list') and (listParam is None):
                    listParam = p[i + 2]
                elif (p[i] == 'element') and (elementParam is None):
                    elemenntParam = p[i + 2]
                else:
                    return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        if isinstance(elementParam, list) and (len(elementParam) == 1):
            elementParam = elementParam[0]
        if (listParam is None) or (elementParam is None):
            return None
        if not isinstance(listParam, list):
            return None
        return elementParam in listParam

    @_('COUNTFUNC expr RPAREN', 'COUNTFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' count of list items'''
        if len(p) == 3:
            listParam = p[1]
        elif p[1] == 'list':
            listParam = p[3]
        else:
            return None
        if not isinstance(listParam, list):
            return 1.0
        return float(len(listParam))

    def minFunc(self, thisList):
        # thisList must be a list of compariable items
        minValue = None
        for i in range(len(thisList)):
            if minValue is None:
                minValue = thisList[i]
            elif type(minValue) != type(thisList[i]):
                return None
            elif thisList[i] < minValue:
                minValue = thisList[i]
        return minValue

    @_('MINFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' minimum item in list parameter '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.minFunc(p.expr)
    
    
    @_('MINFUNC expr')
    def minStart(self, p):
        ''' minimum item in list of items'''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('minStart listPart RPAREN')
    def expr(self, p):
        thisList = p.minStart + p.listPart
        return self.minFunc(thisList)

    @_('minStart RPAREN')
    def expr(self, p):
        thisList = p.minStart
        return self.minFunc(thisList)

    def maxFunc(self, thisList):
        # thisList must be a list of comparable items
        maxValue = None
        for i in range(len(thisList)):
            if maxValue is None:
                maxValue = thisList[i]
            elif type(maxValue) != type(thisList[i]):
                return None
            elif thisList[i] > maxValue:
                maxValue = thisList[i]
        return maxValue

    @_('MAXFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' maximum item in list parameter '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.maxFunc(p.expr)
        
    @_('MAXFUNC expr')
    def maxStart(self, p):
        ''' maximum item in list of items'''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('maxStart listPart RPAREN')
    def expr(self, p):
        thisList = p.maxStart + p.listPart
        return self.maxFunc(thisList)

    @_('maxStart RPAREN')
    def expr(self, p):
        thisList = p.maxStart
        return self.maxFunc(thisList)

    def sumFunc(self, thisList):
        # thisList must be a list of floats
        sumValue = 0.0
        if len(thisList) == 0:
            return None
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
            sumValue += thisList[i]
        return sumValue

    @_('SUMFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' sum of items in list parameter '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None            
        return self.sumFunc(p.expr)

    @_('SUMFUNC expr')
    def sumStart(self, p):
        ''' sum of items in list of items '''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('sumStart listPart RPAREN')
    def expr(self, p):
        thisList = p.sumStart + p.listPart
        return self.sumFunc(thisList)

    @_('sumStart RPAREN')
    def expr(self, p):
        thisList = p.sumStart
        return self.sumFunc(thisList)

    def mean(self, thisList):
        # thisList must be a list of floats (statistics.fmean() fails if it isn't)
        if len(thisList) == 0:
            return None
        try:
            return statistics.fmean(thisList)
        except:
            return None

    @_('MEANFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' mean of items in list parameter '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.mean(p.expr)

    @_('MEANFUNC expr')
    def meanStart(self, p):
        ''' mean of items in list items'''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('meanStart listPart RPAREN')
    def expr(self, p):
        thisList = p.meanStart + p.listPart
        return self.mean(thisList)

    @_('meanStart RPAREN')
    def expr(self, p):
        thisList = p.meanStart
        return self.mean(thisList)

    def allFunc(self, thisList):
        # thisList must be a list of booleans - True if everything is 'true'
        if len(thisList) == 0:
            return True
        for i in range(len(thisList)):
            if isinstance(thisList[i], bool) and (not thisList[i]):
                return False
            elif isinstance(thisList[i], bool) and thisList[i]:
                continue
            else:
                return None
        return True

    @_('ALLFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.allFunc(p.expr)

    @_('ALLFUNC expr')
    def allStart(self, p):
        ''' all items in list are true '''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('allStart listPart RPAREN')
    def expr(self, p):
        thisList = p.allStart + p.listPart
        return self.allFunc(thisList)

    @_('allStart RPAREN')
    def expr(self, p):
        thisList = p.allStart
        return self.allFunc(thisList)

    def anyFunc(self, thisList):
        # thisList must be a list of booleans - True if anything is True - 'null' if there are no booleans in the list
        if len(thisList) == 0:
            return False
        for i in range(len(thisList)):
            if isinstance(thisList[i], bool) and thisList[i]:
                return True
            elif isinstance(thisList[i], bool) and (not thisList[i]):
                continue
            else:
                return None
        return False

    @_('ANYFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' any item in parameter list is true '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.anyFunc(p.expr)

    @_('ANYFUNC expr')
    def anyStart(self, p):
        ''' any item in list is true '''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('anyStart listPart RPAREN')
    def expr(self, p):
        thisList = p.anyStart + p.listPart
        return self.anyFunc(thisList)

    @_('anyStart RPAREN')
    def expr(self, p):
        thisList = p.anyStart
        return self.anyFunc(thisList)

    @_('SUBLISTFUNC expr COMMA expr RPAREN', 'SUBLISTFUNC expr COMMA expr COMMA expr RPAREN',
       'SUBLISTFUNC NAME COLON expr COMMA NAME NAME COLON expr RPAREN', 'SUBLISTFUNC NAME NAME COLON expr COMMA NAME COLON expr RPAREN',
       'SUBLISTFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME NAME COLON expr RPAREN',
       'SUBLISTFUNC NAME COLON expr COMMA NAME NAME COLON expr COMMA NAME COLON expr RPAREN',
       'SUBLISTFUNC NAME NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' sublist from a list with start and end '''
        listParam = startParam = lengthParam = None
        if len(p) <= 7:
            listParam = p[1]
            startParam = p[3]
            if len(p) == 7:
                lengthParam = p[5]
        else:
            i = 1
            while (i < 13) and (i < len(p)):
                if (p[i] == 'string'):
                    if listParam is None:
                        listParam = p[i + 2]
                    i += 4
                elif (p[i] == 'start') and (p[i + 1] == 'position'):
                    if startParam is None:
                        startParam = p[i + 3]
                    i += 5
                elif (len(p) > 13) and (p[i] == 'length'):
                    if lengthParam is None:
                        lengthParam = p[i + 2]
                    i += 4
                else:
                    return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        if isinstance(startParam, list) and (len(startParam) == 1):
            startParam = startParam[0]
        if isinstance(lengthParam, list) and (len(lengthParam) == 1):
            lengthParam = lengthParam[0]
        if (listParam is None) or (startParam is None):
            return None
        if not isinstance(listParam, list):
            return None
        if not isinstance(startParam, float):
            return None
        if int(startParam) == 0:
            return None
        elif int(startParam) < 0:
            start = len(listParam) + int(startParam)
        else:
            start = int(startParam) - 1
        if start >= len(listParam):
            return None
        if lengthParam is None:
            return listParam[start:]
        if not isinstance(lengthParam, float):
            return None
        length = int(lengthParam)
        if start + length <= len(listParam):
            return listParam[start:start + length]
        else:
            return None

    @_('APPENDFUNC expr', 'APPENDFUNC NAME COLON expr')
    def appendStart(self, p):
        ''' append item(s) to a list '''
        if len(p) == 2:
            listParam = p[1]
        elif p[1] == 'list':
            listParam = p[3]
        else:
            return None
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('appendStart listPart RPAREN')
    def expr(self, p):
        return copy.copy(p.appendStart) + p.listPart

    @_('appendStart RPAREN')
    def expr(self, p):
        return p.appendStart

    @_('CONCATENATEFUNC expr')
    def concatenateStart(self, p):
        ''' concatenate lists '''
        # p.expr must be a list
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('concatenateStart listPart RPAREN')
    def expr(self, p):
        if p.concatenateStart is None:
            return None
        thisList = copy.copy(p.concatenateStart)
        for i in range(len(p.listPart)):
            if isinstance(p.listPart[i], list):
                thisList += p.listPart[i]
            else:
                return None
        return thisList

    @_('concatenateStart RPAREN')
    def expr(self, p):
        return p.concatenateStart

    @_('INSERTBEFOREFUNC expr COMMA expr COMMA expr RPAREN',
       'INSERTBEFOREFUNC NAME COLON expr COMMA NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' insert item before position in list '''
        listParam = positionParam = newItemParam = None
        itemFound = False
        if len(p) == 7:
            listParam = p[1]
            positionParam = p[3]
            newItemParam = p[5]
            itemFound = True
        else:
            for i in [1, 5, 9]:
                if (p[i] == 'list') and (listParam is None):
                    listParam = p[i + 2]
                elif (p[i] == 'position') and (positionParam is None):
                    positionParam = p[i + 2]
                elif (p[i] == 'newItem') and (newItemParam is None):
                    newItemParam = p[i + 2]
                    itemFound = True
                else:
                    return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        if isinstance(positionParam, list) and (len(positionParam) == 1):
            positionParam = positionParam[0]
        if isinstance(newItemParam, list) and (len(newItemParam) == 1):
            newItemParam = newItemParam[0]
        if not itemFound or (listParam is None) or (positionParam is None):
            return None
        if not isinstance(listParam, list):
            return None
        if not isinstance(positionParam, float):
            return None
        insertAt = int(positionParam) - 1
        if insertAt < 0:
            return None
        if insertAt > len(listParam):
            return None
        retval = copy.copy(listParam)
        retval.insert(insertAt, newItemParam)
        return retval

    @_('REMOVEFUNC expr COMMA expr RPAREN', 'REMOVEFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' remove item from a list '''
        listParam = positionParam = None
        if len(p) == 5:
            listParam = p[1]
            positionParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'list') and (listParam is None):
                    listParam = p[i + 2]
                elif (p[i] == 'position') and (positionParam is None):
                    positionParam = p[i + 2]
                else:
                    return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        if isinstance(positionParam, list) and (len(positionParam) == 1):
            positionParam = positionParam[0]
        if (listParam is None) or (positionParam is None):
            return None
        if not isinstance(listParam, list):
            return None
        if not isinstance(positionParam, float):
            return None
        removeAt = int(positionParam) - 1
        if removeAt < 0:
            return None
        if removeAt >= len(listParam):
            return None
        if removeAt == 0:
            return listParam[1:]
        elif removeAt == len(listParam) - 1:
            return listParam[:-1]
        else:
            return listParam[:removeAt] + listParam[removeAt + 1:]

    @_('REVERSEFUNC expr RPAREN', 'REVERSEFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' reverse a list '''
        if len(p) == 3:
            listParam = p[1]
        elif p[1] == 'list':
            listParam = p[3]
        else:
            return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        newList = copy.copy(listParam[:])
        newList.reverse()
        return newList

    @_('INDEXOFFUNC expr COMMA expr RPAREN', 'INDEXOFFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' list of indexes of a value in a list '''
        listParam = matchParam = None
        if len(p) == 5:
            listParam = p[1]
            matchParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'list') and (listParam is None):
                    listParam = p[i + 2]
                elif (p[i] == 'match') and (matchParam is None):
                    matchParam = p[i + 2]
                else:
                    return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        if isinstance(matchParam, list) and (len(matchParam) == 1):
            matchParam = matchParam[0]
        if (listParam is None) or (matchParam is None):
            return None
        if not isinstance(listParam, list):
            return None
        newList = []
        for i in range(len(listParam)):
            if listParam[i] == matchParam:
                newList.append(i + 1)
        return newList

    @_('UNIONFUNC expr')
    def unionStart(self, p):
        ''' union lists '''
        # p.expr must be a list
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('unionStart listPart RPAREN')
    def expr(self, p):
        # p.unionStart must be a list and p.listPart must be a list of lists
        if p.unionStart is None:
            return None
        retval = []
        for i in range(len(p.unionStart)):
            if p.unionStart[i] not in retval:
                retval.append(p.unionStart[i])
        for i in range(len(p.listPart)):
            if isinstance(p.listPart[i], list):
                for j in range(len(p.listPart[i])):
                    if p.listPart[i][j] not in retval:
                        retval.append(p.listPart[i][j])
            else:
                return None
        return retval

    @_('unionStart RPAREN')
    def expr(self, p):
        return p.unionStart

    @_('DISTINCTVALUESFUNC expr RPAREN', 'DISTINCTVALUESFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' distinct list items '''
        if len(p) == 3:
            listParam = p[1]
        elif p[1] == 'list':
            listParam = p[3]
        else:
            return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        newList = []
        for i in range(len(listParam)):
            if listParam[i] not in newList:
                newList.append(listParam[i])
        return newList

    def flatten(self, this):
        newList = []
        for i in range(len(this)):
            if isinstance(this[i], list):
                newList += self.flatten(this[i])
            else:
                newList.append(this[i])
        return newList

    @_('FLATTENFUNC expr RPAREN', 'FLATTENFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' flattern a list of lists '''
        if len(p) == 3:
            listParam = p[1]
        elif p[1] == 'list':
            listParam = p[3]
        else:
            return None
        if not isinstance(listParam, list):
            listParam = [listParam]
        newList = self.flatten(listParam)
        return newList

    def product(self, thisList):
        # thisList must be a list of floats
        if not isinstance(thisList, list):
            return None
        if len(thisList) == 0:
            return None
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
        product = 1.0
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
            product *= thisList[i]
        return product

    @_( 'PRODUCTFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' product of numbers in a list paramter '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.product(p.expr)

    @_('PRODUCTFUNC expr')
    def productStart(self, p):
        ''' product of numbers in a list of numbers '''
        if len(p) == 2:
            listParam = p[1]
        elif p[1] == 'list':
            listParam = p[3]
            if isinstance(listParam, list):
                return self.product(listParam)
            else:
                return self.product([listParam])
        else:
            return None
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('productStart listPart RPAREN')
    def expr(self, p):
        thisList = p.productStart + p.listPart
        return self.product(thisList)

    @_('productStart RPAREN')
    def expr(self, p):
        thisList = p.productStart
        return self.product(thisList)

    def median(self, thisList):
        # thisList must be a llist of floats (otherwise statistice.median() will fail)
        if not isinstance(thisList, list):
            return None
        if len(thisList) == 0:
            return None
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
        try:
            return float(statistics.median(thisList))
        except:
            return None

    @_('MEDIANFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' median item in parameter of a list of numbers '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.median(p.expr)

    @_('MEDIANFUNC expr')
    def medianStart(self, p):
        ''' median item in list of numbers '''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('medianStart listPart RPAREN')
    def expr(self, p):
        thisList = p.medianStart + p.listPart
        return self.median(thisList)

    @_('medianStart RPAREN')
    def expr(self, p):
        thisList = p.medianStart
        return self.median(thisList)

    def stddev(self, thisList):
        # thisList must be a list of floats (otherwise statistics.stddev() will fail)
        if not isinstance(thisList, list):
            return None
        if len(thisList) == 0:
            return None
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
        try:
            return float(statistics.stdev(thisList))
        except:
            return None

    @_('STDDEVFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' stddev of a list of numbers '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.stddev(p.expr)

    @_('STDDEVFUNC expr')
    def stddevStart(self, p):
        ''' stddev of a list of numbers '''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('stddevStart listPart RPAREN')
    def expr(self, p):
        thisList = p.stddevStart + p.listPart
        return self.stddev(thisList)

    @_('stddevStart RPAREN')
    def expr(self, p):
        thisList = p.stddevStart
        return self.stddev(thisList)

    def mode(self, thisList):
        # thisList must be a list of floats (otherwise statistics.multimode() will fail)
        if not isinstance(thisList, list):
            return None
        if len(thisList) == 0:
            return []
        for i in range(len(thisList)):
            if not isinstance(thisList[i], float):
                return None
        try:
            thisMode = statistics.multimode(thisList)
        except:
            return None
        if isinstance(thisMode, list):
            try:
                return sorted(thisMode)
            except:
                return thisMode
        else:
            return [thisMode]

    @_('MODEFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' mode number in paramter of list of numbers '''
        if p.NAME != 'list':
            return None
        if not isinstance(p.expr, list):
            return None
        return self.mode(p.expr)

    @_('MODEFUNC expr')
    def modeStart(self, p):
        ''' mode number in list of numbers '''
        listParam = p[1]
        if isinstance(listParam, list):
            return listParam
        else:
            return [listParam]

    @_('modeStart listPart RPAREN')
    def expr(self, p):
        thisList = p.modeStart + p.listPart
        return self.mode(thisList)

    @_('modeStart RPAREN')
    def expr(self, p):
        thisList = p.modeStart
        return self.mode(thisList)

    @_('DECIMALFUNC expr COMMA expr RPAREN', 'DECIMALFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' scale a number '''
        nParam = scaleParam = None
        if len(p) == 5:
            nParam = p[1]
            scaleParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'n') and (nParam is None):
                    nParam = p[i + 2]
                elif (p[i] == 'scale') and (scaleParam is None):
                    scaleParam = p[i + 2]
                else:
                    return None
        if isinstance(nParam, list) and (len(nParam) == 1):
            nParam = nParam[0]
        if isinstance(scaleParam, list) and (len(scaleParam) == 1):
            scaleParam = scaleParam[0]
        if (nParam is None) or (scaleParam is None):
            return None
        if not isinstance(nParam, float):
            return None
        if not isinstance(scaleParam, float):
            return None
        return round(nParam, int(scaleParam))

    @_('FLOORFUNC expr RPAREN', 'FLOORFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' floor of a number '''
        if len(p) == 3:
            nParam = p[1]
        elif p[1] == 'n':
            nParam = p[3]
        else:
            return None
        if isinstance(nParam, list) and (len(nParam) == 1):
            nParam = nParam[0]
        if not isinstance(nParam, float):
            return None
        try:
            return float(math.floor(nParam))
        except:
            return None
        
    @_('CEILINGFUNC expr RPAREN', 'CEILINGFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' ceiling of a number '''
        if len(p) == 3:
            nParam = p[1]
        elif p[1] == 'n':
            nParam = p[3]
        else:
            return None
        if isinstance(nParam, list) and (len(nParam) == 1):
            nParam = nParam[0]
        if not isinstance(nParam, float):
            return None
        try:
            return float(math.ceil(nParam))
        except:
            return None
        
    @_('ABSFUNC expr RPAREN', 'ABSFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' absolute of a number '''
        if len(p) == 3:
            nParam = p[1]
        elif p[1] == 'n':
            nParam = p[3]
        else:
            return None
        if isinstance(nParam, list) and (len(nParam) == 1):
            nParam = nParam[0]
        if isinstance(nParam, bool):
            return None
        if isinstance(nParam, float) or (type(nParam) == int) or isinstance(nParam, datetime.timedelta):
            return abs(nParam)
        return None
        
    @_('MODULOFUNC expr COMMA expr RPAREN', 'MODULOFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' compute modulo of a number '''
        dividendParam = divisorParam = None
        if len(p) == 5:
            dividendParam = p[1]
            divisorParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'dividend') and (dividendParam is None):
                    dividendParam = p[i + 2]
                elif (p[i] == 'divisor') and (divisorParam is None):
                    divisorParam = p[i + 2]
                else:
                    return None
        if isinstance(dividendParam, list) and (len(dividendParam) == 1):
            dividendParam = dividendParam[0]
        if isinstance(divisorParam, list) and (len(divisorParam) == 1):
            divisorParam = divisorParam[0]
        if (dividendParam is None) or (divisorParam is None):
            return None
        if not isinstance(dividendParam, float):
            return None
        if not isinstance(divisorParam, float):
            return None
        try:
            return float(dividendParam % divisorParam)
        except:
            return None

    @_('SQRTFUNC expr RPAREN', 'SQRTFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' absolute of a number '''
        if len(p) == 3:
            numberParam = p[1]
        elif p[1] == 'number':
            numberParam = p[3]
        else:
            return None
        if isinstance(numberParam, list) and (len(numberParam) == 1):
            numberParam = numberParam[0]
        if not isinstance(numberParam, float):
            return None
        try:
            return float(math.sqrt(numberParam))
        except:
            return None
        
    @_('LOGFUNC expr RPAREN', 'LOGFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' log of a number '''
        if len(p) == 3:
            numberParam = p[1]
        elif p[1] == 'number':
            numberParam = p[3]
        else:
            return None
        if isinstance(numberParam, list) and (len(numberParam) == 1):
            numberParam = numberParam[0]
        if not isinstance(numberParam, float):
            return None
        try:
            return float(math.log(numberParam))
        except:
            return None
        
    @_('EXPFUNC expr RPAREN', 'EXPFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' exponential of a number '''
        if len(p) == 3:
            numberParam = p[1]
        elif p[1] == 'number':
            numberParam = p[3]
        else:
            return None
        if isinstance(numberParam, list) and (len(numberParam) == 1):
            numberParam = numberParam[0]
        if not isinstance(numberParam, float):
            return None
        try:
            return float(math.exp(numberParam))
        except:
            return None
        
    @_('ODDFUNC expr RPAREN', 'ODDFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' test if a number is odd '''
        if len(p) == 3:
            numberParam = p[1]
        elif p[1] == 'number':
            numberParam = p[3]
        else:
            return None
        if isinstance(numberParam, list) and (len(numberParam) == 1):
            numberParam = numberParam[0]
        if not isinstance(numberParam, float):
            return None
        if (int(numberParam) % 2) == 0:
            return False
        else:
            return True
        
    @_('EVENFUNC expr RPAREN', 'EVENFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' test if a number is even '''
        if len(p) == 3:
            numberParam = p[1]
        elif p[1] == 'number':
            numberParam = p[3]
        else:
            return None
        if isinstance(numberParam, list) and (len(numberParam) == 1):
            numberParam = numberParam[0]
        if not isinstance(numberParam, float):
            return None
        if (int(numberParam) % 2) == 0:
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
        if type(p.expr) == int:
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
        
    @_('DURATIONFUNC expr RPAREN', 'DURATIONFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert a duration string to datetime.timedelta or int '''
        if len(p) == 3:
            duration = p[1]
        elif p[1] == 'from':
            duration = p[3]
        else:
            return None
        if isinstance(duration, list) and (len(duration) == 1):
            duration = duration[0]
        if not isinstance(p.expr, str):
            return None
        if len(duration) == 0:
            return None
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        if duration[0] != 'P':
            return None
        duration = duration[1:]         # skip P
        isYM = False
        isDT = False
        if duration.find('Y') != -1:
            isYM = True
        if duration.find('D') != -1:
            isDT = True
        if duration.find('T') != -1:
            isDT = True
        if (duration.find('H') != -1) and (duration.find('M') != -1) and (duration.find('S') != -1):
            isDT = True
        if not isDT and (duration.find('H') == -1) and (duration.find('M') != -1) and (duration.find('S') == -1):
            isYM = True
        if (not isYM) and (not isDT):
            return None
        if isYM:             # yearMonthDuration
            months = 0
            valid = False   # Must be one of 'Y' or 'M'
            if duration.find('Y') != -1:
                parts = duration.split('Y')
                if len(parts) > 2:
                    return None
                if parts[0] == '':
                    return None
                try:
                    months = int(parts[0]) * 12
                    duration = parts[1]
                    valid = True
                except:
                    return None
            if duration.find('M') != -1:
                parts = duration.split('M')
                if len(parts) > 2:
                    return None
                if parts[0] == '':
                    return None
                try:
                    months += int(parts[0])
                    duration = parts[1]
                    valid = True
                except:
                    return None
            if not valid:
                return None
            if duration != '':
                return None
            if sign == 0:
                return int(months)
            else:
                return -int(months)
        else:
            days = seconds = milliseconds = 0
            if duration.find('D') != -1:          # days is optional
                parts = duration.split('D')
                if len(parts) > 2:
                    return None
                if parts[0] == '':
                    return None
                try:
                    days = int(parts[0])
                    duration = parts[1]
                except:
                    return None
                if duration =='':
                    if sign == 0:
                        return datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
                    else:
                        return -datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
            if (duration.find('H') != -1) and (duration.find('M') != -1) and (duration.find('S') != -1):
                if duration[0] == 'T':      # T need not be present if all time components are present
                    duration = duration[1:]
            elif duration[0] != 'T':
                return None
            else:
                duration = duration[1:]
            if len(duration) == 0:
                return None
            valid = False
            if duration.find('H') != -1:
                parts = duration.split('H')
                if len(parts) > 2:
                    return None
                if parts[0] == '':
                    return None
                try:
                    seconds = int(parts[0]) * 60 * 60
                    valid = True
                except:
                    return None
                duration = parts[1]
            if duration.find('M') != -1:
                parts = duration.split('M')
                if len(parts) > 2:
                    return None
                if parts[0] == '':
                    return None
                try:
                    seconds += int(parts[0]) * 60
                    valid = True
                except:
                    return None
                duration = parts[1]
            if duration.find('S') != -1:
                parts = duration.split('S')
                if len(parts) > 2:
                    return None
                if parts[0] == '':
                    return None
                try:
                    sPart = float(parts[0])
                    seconds += int(sPart)
                    milliseconds = int((sPart * 1000)) % 1000
                    valid = True
                except:
                    return None
                duration = parts[1]
            if not valid:
                return None
            if duration != '':
                return None
            if sign == 0:
                return datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
            else:
                return -datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
        
    @_('YEARSANDMONTHSDURATIONFUNC expr COMMA expr RPAREN', 'YEARSANDMONTHSDURATIONFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Convert difference betwen two dates (from, to) to 'months' as a float '''
        fromParam = toParam = None
        if len(p) == 5:
            fromParam = p[1]
            toParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'from') and (fromParam is None):
                    fromParam = p[i + 2]
                elif (p[i] == 'to') and (toParam is None):
                    toParam = p[i + 2]
                else:
                    return None
        if isinstance(fromParam, list) and (len(fromParam) == 1):
            fromParam = fromParam[0]
        if isinstance(toParam, list) and (len(toParam) == 1):
            toParam = toParam[0]
        if (fromParam is None) or (toParam is None):
            return None
        if not isinstance(fromParam, datetime.date):          # True for dates and datetimes
            return None
        if not isinstance(toParam, datetime.date):
            return None
        months = (toParam.year - fromParam.year) * 12
        months += toParam.month - fromParam.month
        if toParam.year > fromParam.year:     # from < to
            if toParam.day < fromParam.day:
                months -= 1
        elif toParam.year == fromParam.year:
            if toParam.month > fromParam.month:       # from < to
                if toParam.day < fromParam.day:
                    months -= 1
            elif toParam.month < fromParam.month:     # to < from
                if toParam.day > fromParam.day:
                    months -= 1
        else:                               # to < from
            if toParam.day > fromParam.day:
                months -= 1
        return int(months)


    @_('GETVALUEFUNC expr COMMA NAME RPAREN', 'GETVALUEFUNC expr COMMA expr RPAREN', 'GETVALUEFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Get a value from a Context by key '''
        mParam = keyParam = None
        if len(p) == 5:
            mParam = p[1]
            keyParam = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'm') and (mParam is None):
                    mParam = p[i + 2]
                elif (p[i] == 'key') and (keyParam is None):
                    keyParam = p[i + 2]
                else:
                    return None
        if isinstance(mParam, list) and (len(mParam) == 1):
            mParam = mParam[0]
        if isinstance(keyParam, list) and (len(keyParam) == 1):
            keyParam = keyParam[0]
        if (mParam is None) or (keyParam is None):
            return None
        if isinstance(mParam, dict):
            if isinstance(keyParam, str):
                if keyParam in mParam:
                    return mParam[keyParam]
        return None

    @_('GETENTRIESFUNC expr RPAREN', 'GETENTRIESFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Get a list of 'key','value' pairs from a context'''
        if len(p) == 3:
            mParam = p[1]
        elif p[1] == 'm':
            mParam = p[3]
        else:
            return None
        if isinstance(mParam, list) and (len(mParam) == 1):
            mParam = mParam[0]
        if isinstance(mParam, dict):
            retList = []
            i = 0
            for item in mParam:
                retList.append({})
                retList[i]['key'] = item
                retList[i]['value'] = mParam[item]
                i += 1
            return retList
        return None

    @_('expr YEARSANDMONTHSDURATIONTYPE', 'expr DATEANDTIMETYPE', 'expr DAYSANDTIMEDURATIONTYPE',
       'expr TIMETYPE', 'expr DATETYPE', 'expr BOOLEANTYPE', 'expr STRINGTYPE', 'expr NUMBERTYPE',
       'expr RANGETYPE', 'expr LISTTYPE', 'expr CONTEXTTYPE', 'expr ANYTYPE', 'expr NULLTYPE')
    def expr(self, p):
        ''' Test that an expressions is the specified FEEL type'''
        if p[1].endswith('Any'):
            if p[0] is None:
                return False
            else:
                return True
        if (p[0] is None) and (p[1].endswith('Null')):
            return True
        if (type(p[0]) == int) and (p[1].endswith('years and months duration')):
            return True
        if isinstance(p[0], datetime.timedelta) and (p[1].endswith('days and time duration')):
            return True
        if isinstance(p[0], datetime.datetime) and (p[1].endswith('date and time')):
            return True
        if isinstance(p[0], datetime.time) and (p[1].endswith('time')) and (not p[1].endswith('date and time')):
            return True
        if isinstance(p[0], datetime.date) and (p[1].endswith('date')):
            return True
        if isinstance(p[0], bool) and (p[1].endswith('boolean')):
            return True
        if isinstance(p[0], str) and (p[1].endswith('string')):
            return True
        if isinstance(p[0], float) and (p[1].endswith('number')):
            return True
        if isinstance(p[0], tuple) and (len(p[0]) == 4) and (p[1].endswith('range')):
            return True
        if isinstance(p[0], list) and (p[1].endswith('list')):
            return True
        if isinstance(p[0], dict) and (p[1].endswith('context')):
            return True
        return False

    @_('ISFUNC expr COMMA expr RPAREN', 'ISFUNC NAME COLON expr COMMA NAME COLON expr RPAREN')
    def expr(self, p):
        ''' Test that two expressions are the same FEEL semantic domain'''
        value1Param = value2Param = None
        if len(p) == 5:
            value1Param = p[1]
            value2Param = p[3]
        else:
            for i in [1, 5]:
                if (p[i] == 'value1') and (value1Param is None):
                    value1Param = p[i + 2]
                elif (p[i] == 'value2') and (value2Param is None):
                    value2Param = p[i + 2]
                else:
                    return None
        if (value1Param is None) or (value2Param is None):
            return None
        if type(value1Param) != type(value2Param):
            return False
        # Data structures are expressions, but they are not data types
        if isinstance(value1Param, tuple) or isinstance(value1Param, list) or isinstance(value1Param, dict):
            return False
        if (not isinstance(value1Param, datetime.datetime)) and (not isinstance(value1Param, datetime.time)):
            return True
        if value1Param.tzinfo == value2Param.tzinfo:
            return True
        if (value1Param.tzinfo is None) or (value2Param.tzinfo is None):
            return False
        zone1 = zone2 = None
        try:
            zone1 = value1Param.tzinfo.zone
        except:
            pass
        try:
            zone2 = value2Param.tzinfo.zone
        except:
            pass
        if (zone1 is None) and (zone2 is None):
            return True
        if (zone1 is not None) and (zone2 is not None):
            return True
        return False

    @_('BEFOREFUNC expr COMMA expr RPAREN', 'BEFOREFUNC expr COMMA ltrange RPAREN', 'BEFOREFUNC expr COMMA gtrange RPAREN',
       'BEFOREFUNC ltrange COMMA expr RPAREN', 'BEFOREFUNC ltrange COMMA ltrange RPAREN', 'BEFOREFUNC ltrange COMMA gtrange RPAREN',
       'BEFOREFUNC gtrange COMMA expr RPAREN', 'BEFOREFUNC gtrange COMMA ltrange RPAREN', 'BEFOREFUNC gtrange COMMA gtrange RPAREN',
       'BEFOREFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'BEFOREFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'BEFOREFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'BEFOREFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'BEFOREFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'BEFOREFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'BEFOREFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'BEFOREFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'BEFOREFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test point or range[end] is before point or range[start]'''
        param1 = param2 = None
        rangeFound = pointFound = False
        if len(p) == 5:
            param1 = p[1]
            param2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] in ['point1', 'range1']:
                    if param1 is None:
                        param1 = p[i + 2]
                elif p[i] in ['point2', 'range2']:
                    if param2 is None:
                        param2 = p[i + 2]
                elif p[i] == 'point':
                    if not pointFound:
                        if param1 is None:
                            param1 = p[i + 2]
                        elif param2 is None:
                            param2 = p[i + 2]
                        else:
                            return None
                        pointFound = True
                    else:
                        return None
                elif p[i] == 'range':
                    if not rangeFound:
                        if param1 is None:
                            param1 = p[i + 2]
                        elif param2 is None:
                            param2 = p[i + 2]
                        else:
                            return None
                        rangeFound = True
                    else:
                        return None
                else:
                    return None
        if isinstance(param1, list) and (len(param1) == 1):
            param1 = param1[0]
        if isinstance(param2, list) and (len(param2) == 1):
            param2 = param2[0]
        if (param1 is None) or (param2 is None):
            return None
        if isinstance(param1, tuple) and (len(param1) == 4):      # a range, ltrange or gtrange before
            (lowEnd0, lowVal0, lowPoint, lowEnd) = param1         # "lower" range[end]
        else:           # a point before
            lowEnd = ']'
            lowPoint = param1
        if isinstance(param2, tuple) and (len(param2) == 4):     # before a range, ltrange or gtrange
            (highEnd, highPoint, highVal1, highEnd1) = param2     # "higher" range[start]
        else:                               # a point before a point
            highEnd = '['
            highPoint = param2
        # Check lowPoint is 'before' highPoint
        if lowPoint is None:        # The "lower" range extends to infinity
            return False
        if highPoint is None:       # The "higher" range starts at -infinity
            return False
        if isinstance(lowPoint, str) and not isinstance(highPoint, str):
            return False
        elif (type(lowPoint) == int) and (type(highPoint) != int):              # a range of Year, month durations
            return False
        elif isinstance(lowPoint, float) and not isinstance(highPoint, float):
            return False
        elif isinstance(lowPoint, datetime.date) and not isinstance(highPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowPoint, datetime.timedelta) and not isinstance(highPoint, datetime.timedelta):
            return False
        if lowPoint < highPoint:        # Low end is before high start
            return True
        if lowPoint > highPoint:
            return False
        if (lowEnd != ']') or (highEnd != '['):
            return True
        return False

    @_('AFTERFUNC expr COMMA expr RPAREN', 'AFTERFUNC expr COMMA ltrange RPAREN', 'AFTERFUNC expr COMMA gtrange RPAREN',
       'AFTERFUNC ltrange COMMA expr RPAREN', 'AFTERFUNC ltrange COMMA ltrange RPAREN', 'AFTERFUNC ltrange COMMA gtrange RPAREN',
       'AFTERFUNC gtrange COMMA expr RPAREN', 'AFTERFUNC gtrange COMMA ltrange RPAREN', 'AFTERFUNC gtrange COMMA gtrange RPAREN',
       'AFTERFUNC NAME COLON expr NAME COLON COMMA expr RPAREN', 'AFTERFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'AFTERFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'AFTERFUNC NAME COLON ltrange NAME COLON COMMA expr RPAREN', 'AFTERFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'AFTERFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'AFTERFUNC NAME COLON gtrange NAME COLON COMMA expr RPAREN', 'AFTERFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'AFTERFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test point or range[start] is after point or range[end]'''
        param1 = param2 = None
        rangeFound = pointFound = False
        if len(p) == 5:
            param1 = p[1]
            param2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] in ['point1', 'range1']:
                    if param1 is None:
                        param1 = p[i + 2]
                elif p[i] in ['point2', 'range2']:
                    if param2 is None:
                        param2 = p[i + 2]
                elif p[i] == 'point':
                    if not pointFound:
                        if param1 is None:
                            param1 = p[i + 2]
                        elif param2 is None:
                            param2 = p[i + 2]
                        else:
                            return None
                        pointFound = True
                    else:
                        return None
                elif p[i] == 'range':
                    if not rangeFound:
                        if param1 is None:
                            param1 = p[i + 2]
                        elif param2 is None:
                            param2 = p[i + 2]
                        else:
                            return None
                        rangeFound = True
                    else:
                        return None
                else:
                    return None
        if isinstance(param1, list) and (len(param1) == 1):
            param1 = param1[0]
        if isinstance(param2, list) and (len(param2) == 1):
            param2 = param2[0]
        if (param1 is None) or (param2 is None):
            return None
        if isinstance(param1, tuple) and (len(param1) == 4):      # a point or range after
            (highEnd, highPoint, highVal1, highEnd1) = param1         # "higher" range start
        else:           # a point before
            highEnd = '['
            highPoint = param1
        if isinstance(param2, tuple) and (len(param2) == 4):     # before a point or range
            (lowEnd0, lowVal0, lowPoint, lowEnd) = param2             # "lower" range end
        else:                               # a point before a point
            lowEnd = ']'
            lowPoint = param2
        # Check lowPoint is 'before' highPoint
        if isinstance(lowPoint, str) and not isinstance(highPoint, str):
            return False
        elif (type(lowPoint) == int) and (type(highPoint) != int):                      # a range of Year, month durations
            return False
        elif isinstance(lowPoint, float) and not isinstance(highPoint, float):
            return False
        elif isinstance(lowPoint, datetime.date) and not isinstance(highPoint, datetime.date):      # True for both dates and datetimes
            return False
        elif isinstance(lowPoint, datetime.timedelta) and not isinstance(highPoint, datetime.timedelta):
            return False
        if highPoint is None:           # "higher" range starts at -infinity
            return False
        if lowPoint is None:            # "lower" range ends at infinity
            return False
        if lowPoint < highPoint:
            return True
        if lowPoint > highPoint:
            return False
        if (lowEnd != ']') or (highEnd != '['):
            return True
        return False

    @_('MEETSFUNC expr COMMA expr RPAREN', 'MEETSFUNC expr COMMA ltrange RPAREN', 'MEETSFUNC expr COMMA gtrange RPAREN',
       'MEETSFUNC ltrange COMMA expr RPAREN', 'MEETSFUNC ltrange COMMA ltrange RPAREN', 'MEETSFUNC ltrange COMMA gtrange RPAREN',
       'MEETSFUNC gtrange COMMA expr RPAREN', 'MEETSFUNC gtrange COMMA ltrange RPAREN', 'MEETSFUNC gtrange COMMA gtrange RPAREN',
       'MEETSFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'MEETSFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'MEETSFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'MEETSFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'MEETSFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'MEETSFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'MEETSFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'MEETSFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'MEETSFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test range meets range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] == 'range1':
                    if range1 is None:
                        range1 = p[i + 2]
                elif p[i] == 'range2':
                    if range2 is None:
                        range2 = p[i + 2]
                else:
                    return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range meets
            (lowEnd0, lowVal0, highPoint, highEnd) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):      # a range meets a range
            (lowEnd, lowPoint, highVal1, highEnd1) = range2
        else:
            return False
        # Check highPoint matches lowPoint
        if lowPoint is None:            # "lower" range extends to infinity
            return False
        if highPoint is None:           # "higher" range starts at -infinity
            return False
        if isinstance(highPoint, str) and not isinstance(lowPoint, str):
            return False
        elif (type(highPoint) == int) and (type(lowPoint) != int):                          # a range of Year, month durations
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

    @_('METBYFUNC expr COMMA expr RPAREN', 'METBYFUNC expr COMMA ltrange RPAREN', 'METBYFUNC expr COMMA gtrange RPAREN',
       'METBYFUNC ltrange COMMA expr RPAREN', 'METBYFUNC ltrange COMMA ltrange RPAREN', 'METBYFUNC ltrange COMMA gtrange RPAREN',
       'METBYFUNC gtrange COMMA expr RPAREN', 'METBYFUNC gtrange COMMA ltrange RPAREN', 'METBYFUNC gtrange COMMA gtrange RPAREN',
       'METBYFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'METBYFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'METBYFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'METBYFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'METBYFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'METBYFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'METBYFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'METBYFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'METBYFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test range meets range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] == 'range1':
                    if range1 is None:
                        range1 = p[i + 2]
                elif p[i] == 'range2':
                    if range2 is None:
                        range2 = p[i + 2]
                else:
                    return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a "higher" range met by
            (lowEnd, lowPoint, highVal0, highEnd0) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):      # a "higher" range met by a "lower" range
            (lowEnd0, lowVal0, highPoint, highEnd) = range2
        else:
            return False
        # Check lowPoint matches highPoint
        if lowPoint is None:            # "higher" range starts at -infinity
            return False
        if highPoint is None:           # "lower" range extends to infinity
            return False
        if isinstance(lowPoint, str) and not isinstance(highPoint, str):
            return False
        elif (type(lowPoint) == int) and (type(highPoint) != int):                      # a range of Year, month durations
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

    @_('OVERLAPSFUNC expr COMMA expr RPAREN', 'OVERLAPSFUNC expr COMMA ltrange RPAREN', 'OVERLAPSFUNC expr COMMA gtrange RPAREN',
       'OVERLAPSFUNC ltrange COMMA expr RPAREN', 'OVERLAPSFUNC ltrange COMMA ltrange RPAREN', 'OVERLAPSFUNC ltrange COMMA gtrange RPAREN',
       'OVERLAPSFUNC gtrange COMMA expr RPAREN', 'OVERLAPSFUNC gtrange COMMA ltrange RPAREN', 'OVERLAPSFUNC gtrange COMMA gtrange RPAREN',
       'OVERLAPSFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'OVERLAPSFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'OVERLAPSFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'OVERLAPSFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'OVERLAPSFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'OVERLAPSFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'OVERLAPSFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'OVERLAPSFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'OVERLAPSFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test range overlaps range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] == 'range1':
                    if range1 is None:
                        range1 = p[i + 2]
                elif p[i] == 'range2':
                    if range2 is None:
                        range2 = p[i + 2]
                else:
                    return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range overlaps
            (end00, low0Val, high0Val, end01) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):      # a range overlaps a range
            (end10, low1Val, high1Val, end11) = range2
        else:
            return False
        if (low0Val is None) and (low1Val is None):         # Both ranges start at -infinity, so the must overlap
            return True
        if (high0Val is None) and (high1Val is None):       # Both ranges extend to infinity, so they must overlap
            return True
        if low0Val is None:         # First range starts at -infinity. Only need to check high0Val > low1Val
            if isinstance(high0Val, str) and not isinstance(low1Val, str):
                return False
            elif (type(high0Val) == int) and (type(low1Val) != int):
                return False
            elif isinstance(high0Val, float) and not isinstance(low1Val, float):
                return False
            elif isinstance(high0Val, datetime.date) and not isinstance(low1Val, datetime.date):        # True for both dates and datetimes
                return False
            elif isinstance(high0Val, datetime.timedelta) and not isinstance(low1Val, datetime.timedelta):
                    return False
            # Check range p.expr0 overlaps range p.expr1
            if high0Val < low1Val:      # but doesn't get to range p.expr1 - doesn't overlap
                return False
            elif high0Val == low1Val:   # reaches, but does it overlap
                if (end01 == ')') or (end10 == '('):    # One is a closed range
                    return False
                return True
            return True     # reaches and overlaps
        if low1Val is None:         # Second range starts at -infinity. Only need to check high1Val > low0Val
            if isinstance(high1Val, str) and not isinstance(low0Val, str):
                return False
            elif (type(high1Val) == int) and (type(low0Val) != int):
                return False
            elif isinstance(high1Val, float) and not isinstance(low0Val, float):
                return False
            elif isinstance(high1Val, datetime.date) and not isinstance(low0Val, datetime.date):        # True for both dates and datetimes
                return False
            elif isinstance(high1Val, datetime.timedelta) and not isinstance(low0Val, datetime.timedelta):
                    return False
            # Check range p.expr0 overlaps range p.expr1
            if high1Val < low0Val:      # but doesn't get to range p.expr1 - doesn't overlap
                return False
            elif high1Val == low0Val:   # reaches, but does it overlap
                if (end11 == ')') or (end00 == '('):    # One is a closed range
                    return False
                return True
            return True     # reaches and overlaps
        if high0Val is None:         # First range end at infinity. Only need to check low0Val > high1Val
            if isinstance(low0Val, str) and not isinstance(high1Val, str):
                return False
            elif (type(low0Val) == int) and (type(high1Val) != int):
                return False
            elif isinstance(low0Val, float) and not isinstance(high1Val, float):
                return False
            elif isinstance(low0Val, datetime.date) and not isinstance(high1Val, datetime.date):        # True for both dates and datetimes
                return False
            elif isinstance(low0Val, datetime.timedelta) and not isinstance(high1Val, datetime.timedelta):
                    return False
            # Check range p.expr0 overlaps range p.expr1
            if low0Val < high1Val:      # but doesn't get to range p.expr1 - doesn't overlap
                return False
            elif low0Val == high1Val:   # reaches, but does it overlap
                if (end00 == '(') or (end11 == ')'):    # One is a closed range
                    return False
                return True
            return True     # reaches and overlaps
        if high1Val is None:         # Second range end at infinity. Only need to check low1Val > high0Val
            if isinstance(low1Val, str) and not isinstance(high0Val, str):
                return False
            elif (type(low1Val) == int) and (type(high0Val) != int):
                return False
            elif isinstance(low1Val, float) and not isinstance(high0Val, float):
                return False
            elif isinstance(low1Val, datetime.date) and not isinstance(high0Val, datetime.date):        # True for both dates and datetimes
                return False
            elif isinstance(low1Val, datetime.timedelta) and not isinstance(high0Val, datetime.timedelta):
                    return False
            # Check range p.expr0 overlaps range p.expr1
            if low1Val < high0Val:      # but doesn't get to range p.expr1 - doesn't overlap
                return False
            elif low1Val == high0Val:   # reaches, but does it overlap
                if (end10 == '(') or (end01 == ')'):    # One is a closed range
                    return False
                return True
            return True     # reaches and overlaps
        if isinstance(low0Val, str):
            if not isinstance(low1Val, str) or not isinstance(high1Val, str):
                return False
        elif type(low0Val) == int:                                          # a range of Year, month durations
            if (type(low1Val) != int) or (type(high1Val) != int):
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

    @_('OVERLAPSBEFOREFUNC expr COMMA expr RPAREN', 'OVERLAPSBEFOREFUNC expr COMMA ltrange RPAREN', 'OVERLAPSBEFOREFUNC expr COMMA gtrange RPAREN',
       'OVERLAPSBEFOREFUNC ltrange COMMA expr RPAREN', 'OVERLAPSBEFOREFUNC ltrange COMMA ltrange RPAREN', 'OVERLAPSBEFOREFUNC ltrange COMMA gtrange RPAREN',
       'OVERLAPSBEFOREFUNC gtrange COMMA expr RPAREN', 'OVERLAPSBEFOREFUNC gtrange COMMA ltrange RPAREN', 'OVERLAPSBEFOREFUNC gtrange COMMA gtrange RPAREN',
       'OVERLAPSBEFOREFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'OVERLAPSBEFOREFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'OVERLAPSBEFOREFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'OVERLAPSBEFOREFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'OVERLAPSBEFOREFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'OVERLAPSBEFOREFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'OVERLAPSBEFOREFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'OVERLAPSBEFOREFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'OVERLAPSBEFOREFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test range p.expr0 starts before and overlaps (but does not include) range p.expr1'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] == 'range1':
                    if range1 is None:
                        range1 = p[i + 2]
                elif p[i] == 'range2':
                    if range2 is None:
                        range2 = p[i + 2]
                else:
                    return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range overlaps
            (end00, low0Val, high0Val, end01) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):      # a range overlaps a range
            (end10, low1Val, high1Val, end11) = range2
        else:
            return False
        if low1Val is None:             # Second range starts at -infinity. Nothing starts before -infinity
            return False
        if high0Val is None:            # First range goes to infinity. If it starts before, it certainly contains
            return False
        if low0Val is None:             # First range starts at -infinity and second range doesn't - that's "before"
            if high1Val is None:            # Second range ends at infinity and first range doesn't - that's overlaps before and not include
                if isinstance(high0Val, str) and isinstance(low1Val, str):
                    return True
                elif (type(high0Val) == int) and (type(low1Val) == int):
                    return True
                elif isinstance(high0Val, float) and isinstance(low1Val, float):
                    return True
                elif isinstance(high0Val, datetime.date) and isinstance(low1Val, datetime.date):          # True for both dates and datetimes
                    return True
                elif isinstance(high0Val, datetime.timedelta) and isinstance(low1Val, datetime.timedelta):
                    return True
                return False        # Not comparing apples with apples
            if isinstance(high0Val, str) and not isinstance(high1Val, str):
                return False
            elif (type(high0Val) == int) and (type(high1Val) != int):
                return False
            elif isinstance(high0Val, float) and not isinstance(high1Val, float):
                return False
            elif isinstance(high0Val, datetime.date) and not isinstance(high1Val, datetime.date):          # True for both dates and datetimes
                return False
            elif isinstance(high0Val, datetime.timedelta) and not isinstance(high1Val, datetime.timedelta):
                return False
            if high0Val < low1Val:      # range p.expr0 doesn't get to range p.expr1 - doesn't overlap
                    return False
            if high0Val == low1Val:   # reaches, but does it overlap
                if (end01 == ')') or (end10 == '('):    # One is a closed range
                    return False
            if high0Val > high1Val:     # includes - which isn't overlaps
                return False
            if high0Val == high1Val:    # range p.expr0 and range p.expr1 end at the same point
                if (end01 == ']') and (end11 == ')'):        # end0 > end1
                    return False
            return True 
        if isinstance(low0Val, str):
            if not isinstance(low1Val, str):
                return False
        elif type(low0Val) == int:                      # a range of Year, month durations
            if type(low1Val) != int:
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
        if high1Val is None:        # Second range goes to infinity, for first range doesn't
            return True
        if high0Val > high1Val:     # includes - which isn't overlaps
            return False
        if high0Val == high1Val:    # range p.expr0 and range p.expr1 end at the same point
            if (end01 == ']') and (end11 == ')'):        # end0 > end1
                return False
        return True 

    @_('OVERLAPSAFTERFUNC expr COMMA expr RPAREN', 'OVERLAPSAFTERFUNC expr COMMA ltrange RPAREN', 'OVERLAPSAFTERFUNC expr COMMA gtrange RPAREN',
       'OVERLAPSAFTERFUNC ltrange COMMA expr RPAREN', 'OVERLAPSAFTERFUNC ltrange COMMA ltrange RPAREN', 'OVERLAPSAFTERFUNC ltrange COMMA gtrange RPAREN',
       'OVERLAPSAFTERFUNC gtrange COMMA expr RPAREN', 'OVERLAPSAFTERFUNC gtrange COMMA ltrange RPAREN', 'OVERLAPSAFTERFUNC gtrange COMMA gtrange RPAREN',
       'OVERLAPSAFTERFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'OVERLAPSAFTERFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'OVERLAPSAFTERFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'OVERLAPSAFTERFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'OVERLAPSAFTERFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'OVERLAPSAFTERFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'OVERLAPSAFTERFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'OVERLAPSAFTERFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'OVERLAPSAFTERFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test range p.expr0 starts after, overlaps (but is not included in) range p.expr1'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] == 'range1':
                    if range1 is None:
                        range1 = p[i + 2]
                elif p[i] == 'range2':
                    if range2 is None:
                        range2 = p[i + 2]
                else:
                    return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range overlaps
            (end00, low0Val, high0Val, end01) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):      # a range overlaps a range
            (end10, low1Val, high1Val, end11) = range2
        else:
            return False
        if low0Val is None:             # First range starts at -infinity. Can't start after anything
            return False
        if high1Val is None:            # Second range extends to infinity - will include anything that overlaps it
            return False
        if low1Val is None:             # Second range starts at -infinity and first range doesn't - that's "after"
            if high0Val is None:            # First range ends at infinity and second range doesn't - that's overlaps after and not included
                if isinstance(high1Val, str) and isinstance(low0Val, str):
                    return True
                elif (type(high1Val) == int) and (type(low0Val) == int):
                    return True
                elif isinstance(high1Val, float) and isinstance(low0Val, float):
                    return True
                elif isinstance(high1Val, datetime.date) and isinstance(low0Val, datetime.date):          # True for both dates and datetimes
                    return True
                elif isinstance(high1Val, datetime.timedelta) and isinstance(low0Val, datetime.timedelta):
                    return True
                return False        # Not comparing apples with apples
            if isinstance(high1Val, str) and not isinstance(low0Val, str):
                return False
            elif (type(high1Val) == int) and (type(low0Val) != int):
                return False
            elif isinstance(high1Val, float) and not isinstance(low0Val, float):
                return False
            elif isinstance(high1Val, datetime.date) and not isinstance(low0Val, datetime.date):          # True for both dates and datetimes
                return False
            elif isinstance(high1Val, datetime.timedelta) and not isinstance(low0Val, datetime.timedelta):
                return False
            if high1Val < low0Val:      # range p.expr1 doesn't get to range p.expr0 - doesn't overlap
                    return False
            if high1Val == low0Val:   # reaches, but does it overlap
                if (end11 == ')') or (end00 == '('):    # One is a closed range
                    return False
            if high1Val > high0Val:     # includes - which isn't overlaps
                return False
            if high1Val == high0Val:    # range p.expr0 and range p.expr1 end at the same point
                if (end11 == ']') and (end01 == ')'):        # end1 > end0
                    return False
            return True 
        if isinstance(low0Val, str):
            if not isinstance(low1Val, str) or not isinstance(high1Val, str):
                return False
        elif type(low0Val) == int:                          # a range of Year, month durations
            if (type(low1Val) != int) or (type(high1Val) != int):
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
            if (end01 == ')') and (end11 == ']'):        # make sure there is some overlap 'after' the end
                return False
        return True     # reaches and overlaps
        
    @_('FINISHESFUNC expr COMMA expr RPAREN', 'FINISHESFUNC expr COMMA ltrange RPAREN', 'FINISHESFUNC expr COMMA gtrange RPAREN',
       'FINISHESFUNC ltrange COMMA expr RPAREN', 'FINISHESFUNC ltrange COMMA ltrange RPAREN', 'FINISHESFUNC ltrange COMMA gtrange RPAREN',
       'FINISHESFUNC gtrange COMMA expr RPAREN', 'FINISHESFUNC gtrange COMMA ltrange RPAREN', 'FINISHESFUNC gtrange COMMA gtrange RPAREN',
       'FINISHESFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'FINISHESFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'FINISHESFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'FINISHESFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'FINISHESFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'FINISHESFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'FINISHESFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'FINISHESFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'FINISHESFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test point or range finishes a range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            if (p[1] == 'point') and (p[5] == 'range'):
                range1 = p[3]
                range2 = p[7]
            elif (p[1] == 'range1') and (p[5] == 'range2'):
                range1 = p[3]
                range2 = p[7]
            else:
                return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range finishes
            (lowEnd0, lowVal0, highPoint, highEnd) = range1
        else:           # a point finishes
            highEnd = ']'
            highPoint = range1
        if isinstance(range2, tuple) and (len(range2) == 4):     # a range
            (lowEnd1, lowVal1, thePoint, theEnd) = range2
        else:
            return False
        # Check highPoint is thePoint
        if (highPoint is None) and (thePoint is None):      # Both finish at infinity
            return True
        if (highPoint is None) or (thePoint is None):      # One finish at infinity
            return False
        if isinstance(thePoint, str) and not isinstance(highPoint, str):
            return False
        elif (type(thePoint) == int) and (type(highPoint) != int):              # a range of Year, month durations
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

    @_('FINISHEDBYFUNC expr COMMA expr RPAREN', 'FINISHEDBYFUNC expr COMMA ltrange RPAREN', 'FINISHEDBYFUNC expr COMMA gtrange RPAREN',
       'FINISHEDBYFUNC ltrange COMMA expr RPAREN', 'FINISHEDBYFUNC ltrange COMMA ltrange RPAREN', 'FINISHEDBYFUNC ltrange COMMA gtrange RPAREN',
       'FINISHEDBYFUNC gtrange COMMA expr RPAREN', 'FINISHEDBYFUNC gtrange COMMA ltrange RPAREN', 'FINISHEDBYFUNC gtrange COMMA gtrange RPAREN',
       'FINISHEDBYFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'FINISHEDBYFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'FINISHEDBYFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'FINISHEDBYFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'FINISHEDBYFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'FINISHEDBYFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'FINISHEDBYFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'FINISHEDBYFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'FINISHEDBYFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test a range is finished by point or range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            if (p[1] == 'range') and (p[5] == 'point'):
                range1 = p[3]
                range2 = p[7]
            elif (p[1] == 'range1') and (p[5] == 'range2'):
                range1 = p[3]
                range2 = p[7]
            else:
                return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range
            (lowEnd0, lowVal0, highPoint, highEnd) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):     # before a range
            (highEnd1, highVal1, thePoint, theEnd) = range2
        else:                               # a point before a point
            theEnd = ']'
            thePoint = range2
        # Check thePoint is highPoint
        if (highPoint is None) and (thePoint is None):      # Both finish at infinity
            return True
        if (highPoint is None) or (thePoint is None):      # One finish at infinity
            return False
        if isinstance(thePoint, str) and not isinstance(highPoint, str):
            return False
        elif (type(thePoint) == int) and (type(highPoint) != int):                  # a range of Year, month durations
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

    @_('INCLUDESFUNC expr COMMA expr RPAREN', 'INCLUDESFUNC expr COMMA ltrange RPAREN', 'INCLUDESFUNC expr COMMA gtrange RPAREN',
       'INCLUDESFUNC ltrange COMMA expr RPAREN', 'INCLUDESFUNC ltrange COMMA ltrange RPAREN', 'INCLUDESFUNC ltrange COMMA gtrange RPAREN',
       'INCLUDESFUNC gtrange COMMA expr RPAREN', 'INCLUDESFUNC gtrange COMMA ltrange RPAREN', 'INCLUDESFUNC gtrange COMMA gtrange RPAREN',
       'INCLUDESFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'INCLUDESFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'INCLUDESFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'INCLUDESFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'INCLUDESFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'INCLUDESFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'INCLUDESFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'INCLUDESFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'INCLUDESFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test range includes point or range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            if (p[1] == 'range') and (p[5] == 'point'):
                range1 = p[3]
                range2 = p[7]
            elif (p[1] == 'range1') and (p[5] == 'range2'):
                range1 = p[3]
                range2 = p[7]
            else:
                return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = range2
        else:                               # includes a point
            lowEnd1 = '['
            highEnd1 = ']'
            lowVal1 = highVal1 = range2
        # Check lowVal0..highVal0 include lowVa1..highVal1
        if lowVal1 is None:        # Second is a range that starts at -infinity - cannont be included
            return False
        if highVal1 is None:        # Second is a range that goes to infinity - cannont be included
            return False
        if lowVal0 is None:         # The range starts at -infinity and p.expr1 doesn't - we have inclusion at the lower end
            if isinstance(highVal0, str) and not isinstance(highVal1, str):
                return False
            elif (type(highVal0) == int) and (type(highVal1) != int):                        # a range of Year, month durations
                return False
            elif isinstance(highVal0, float) and not isinstance(highVal1, float):
                return False
            elif isinstance(highVal0, datetime.date) and not isinstance(highVal1, datetime.date):      # True for both dates and datetimes
                return False
            elif isinstance(highVal0, datetime.timedelta) and not isinstance(highVal1, datetime.timedelta):
                return False
            if highVal0 < highVal1:     # p.expr1 ends after p.expr0
                return False
            if highVal1 == highVal1:
                if (highEnd0 != highEnd1) and (highEnd0 == ')'):    # p.expr0 is closed
                    return False
            return True
        if highVal0 is None:         # The range starts ends infinity and p.expr1 doesn't - we have inclusion at the higher end
            if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
                return False
            elif (type(lowVal0) == int) and (type(lowVal1) != int):                        # a range of Year, month durations
                return False
            elif isinstance(lowVal0, float) and not isinstance(lowVal1, float):
                return False
            elif isinstance(lowVal0, datetime.date) and not isinstance(lowVal1, datetime.date):      # True for both dates and datetimes
                return False
            elif isinstance(lowVal0, datetime.timedelta) and not isinstance(lowVal1, datetime.timedelta):
                return False
            if lowVal0 > lowVal1:       # p.expr1 starts before p.expr0
                return False
            if lowVal0 == lowVal1:      # Same starting point
                if (lowEnd0 != lowEnd1) and (lowEnd0 == '('):        # p.expr0 is closed
                    return False
            return True
        if isinstance(lowVal0, str) and not isinstance(highVal0, str):
            return False
        elif (type(lowVal0) == int) and (type(highVal0) != int):                        # a range of Year, month durations
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

    @_('DURINGFUNC expr COMMA expr RPAREN', 'DURINGFUNC expr COMMA ltrange RPAREN', 'DURINGFUNC expr COMMA gtrange RPAREN',
       'DURINGFUNC ltrange COMMA expr RPAREN', 'DURINGFUNC ltrange COMMA ltrange RPAREN', 'DURINGFUNC ltrange COMMA gtrange RPAREN',
       'DURINGFUNC gtrange COMMA expr RPAREN', 'DURINGFUNC gtrange COMMA ltrange RPAREN', 'DURINGFUNC gtrange COMMA gtrange RPAREN',
       'DURINGFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'DURINGFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'DURINGFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'DURINGFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'DURINGFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'DURINGFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'DURINGFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'DURINGFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'DURINGFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test point or range p.expr0 is included in range p.expr1'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            if (p[1] == 'point') and (p[5] == 'range'):
                range1 = p[3]
                range2 = p[7]
            elif (p[1] == 'range1') and (p[5] == 'range2'):
                range1 = p[3]
                range2 = p[7]
            else:
                return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = range1
        else:           # a point before
            lowEnd0 = '['
            highEnd0 = ']'
            lowVal0 = highVal0 = range1
        if isinstance(range2, tuple) and (len(range2) == 4):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = range2
        else:
            return False                               # a point before a point
        # Check highVal0..highVal1 is included in lowVal0..lowVal1
        if lowVal0 is None:        # First is a range that starts at -infinity - cannont be included
            return False
        if highVal0 is None:        # First is a range that goes to infinity - cannont be included
            return False
        if lowVal1 is None:         # The range starts at -infinity and p.expr0 doesn't - we have inclusion at the lower end
            if isinstance(highVal0, str) and not isinstance(highVal1, str):
                return False
            elif (type(highVal0) == int) and (type(highVal1) != int):                        # a range of Year, month durations
                return False
            elif isinstance(highVal0, float) and not isinstance(highVal1, float):
                return False
            elif isinstance(highVal0, datetime.date) and not isinstance(highVal1, datetime.date):      # True for both dates and datetimes
                return False
            elif isinstance(highVal0, datetime.timedelta) and not isinstance(highVal1, datetime.timedelta):
                return False
            if highVal0 > highVal1:     # p.expr0 ends after p.expr1
                return False
            if highVal0 == highVal1:
                if (highEnd0 != highEnd1) and (highEnd1 == ')'):    # p.expr1 is closed
                    return False
            return True
        if highVal1 is None:         # The range starts ends infinity and p.expr0 doesn't - we have inclusion at the higher end
            if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
                return False
            elif (type(lowVal0) == int) and (type(lowVal1) != int):                        # a range of Year, month durations
                return False
            elif isinstance(lowVal0, float) and not isinstance(lowVal1, float):
                return False
            elif isinstance(lowVal0, datetime.date) and not isinstance(lowVal1, datetime.date):      # True for both dates and datetimes
                return False
            elif isinstance(lowVal0, datetime.timedelta) and not isinstance(lowVal1, datetime.timedelta):
                return False
            if lowVal0 < lowVal1:       # p.expr0 starts before p.expr1
                return False
            if lowVal0 == lowVal1:      # Same starting point
                if (lowEnd0 != lowEnd1) and (lowEnd1 == '('):        # p.expr1 is closed
                    return False
            return True
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif (type(lowVal0) == int) and (type(lowVal1) != int):                     # a range of Year, month durations
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

    @_('STARTSFUNC expr COMMA expr RPAREN', 'STARTSFUNC expr COMMA ltrange RPAREN', 'STARTSFUNC expr COMMA gtrange RPAREN',
       'STARTSFUNC ltrange COMMA expr RPAREN', 'STARTSFUNC ltrange COMMA ltrange RPAREN', 'STARTSFUNC ltrange COMMA gtrange RPAREN',
       'STARTSFUNC gtrange COMMA expr RPAREN', 'STARTSFUNC gtrange COMMA ltrange RPAREN', 'STARTSFUNC gtrange COMMA gtrange RPAREN',
       'STARTSFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'STARTSFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'STARTSFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'STARTSFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'STARTSFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'STARTSFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'STARTSFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'STARTSFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'STARTSFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test point or range starts a range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            if (p[1] == 'point') and (p[5] == 'range'):
                range1 = p[3]
                range2 = p[7]
            elif (p[1] == 'range1') and (p[5] == 'range2'):
                range1 = p[3]
                range2 = p[7]
            else:
                return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = range1
        else:           # a point before
            lowEnd0 = '['
            highEnd0 = ']'
            lowVal0 = highVal0 = range1
        if isinstance(range2, tuple) and (len(range2) == 4):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = range2
        else:
            return False
        # Check lowVal0..highVal0 starts lowVal1..highVal1, but doesn't go beyond
        if (lowVal0 is None) and (lowVal1 is None):         # Both ranges start at -infinity
            return True
        if (lowVal0 is None) or (lowVal1 is None):         # Only one ranges starts at -infinity
            return False
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif (type(lowVal0) == int) and (type(lowVal1) != int):                     # a range of Year, month durations
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
        if highVal0 is None:           # Starts, but consumes
            return False
        if highVal1 is None:
            return True
        if highVal0 > highVal1:
            return False
        if highVal0 == highVal1:
            if (highEnd0 != highEnd1) and (highEnd1 == ')'):
                return False
        return True

    @_('STARTEDBYFUNC expr COMMA expr RPAREN', 'STARTEDBYFUNC expr COMMA ltrange RPAREN', 'STARTEDBYFUNC expr COMMA gtrange RPAREN',
       'STARTEDBYFUNC ltrange COMMA expr RPAREN', 'STARTEDBYFUNC ltrange COMMA ltrange RPAREN', 'STARTEDBYFUNC ltrange COMMA gtrange RPAREN',
       'STARTEDBYFUNC gtrange COMMA expr RPAREN', 'STARTEDBYFUNC gtrange COMMA ltrange RPAREN', 'STARTEDBYFUNC gtrange COMMA gtrange RPAREN',
       'STARTEDBYFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'STARTEDBYFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'STARTEDBYFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'STARTEDBYFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'STARTEDBYFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'STARTEDBYFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'STARTEDBYFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'STARTEDBYFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'STARTEDBYFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test range is started by point or range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            if (p[1] == 'range') and (p[5] == 'point'):
                range1 = p[3]
                range2 = p[7]
            elif (p[1] == 'range1') and (p[5] == 'range2'):
                range1 = p[3]
                range2 = p[7]
            else:
                return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if (range1 is None) or (range2 is None):
            return None
        if isinstance(range1, tuple) and (len(range1) == 4):      # a range before
            (lowEnd0, lowVal0, highVal0, highEnd0) = range1
        else:
            return False
        if isinstance(range2, tuple) and (len(range2) == 4):     # before a range
            (lowEnd1, lowVal1, highVal1, highEnd1) = range2
        else:                               # a point before a point
            lowEnd1 = '['
            highEnd1 = ']'
            lowVal1 = highVal1 = range2
        # Check lowVal0..highVal0 is started by lowVal1..highVal1, but doesn't go beyond
        if (lowVal0 is None) and (lowVal1 is None):         # Both ranges start at -infinity
            return True
        if (lowVal0 is None) or (lowVal1 is None):         # Only one ranges starts at -infinity
            return False
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif (type(lowVal0) == int) and (type(lowVal1) != int):                 # a range of Year, month durations
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
        if highVal1 is None:        # Second range goes to infinity, and consumes first
            return False
        if highVal0 is None:        # First goes to inifinity
            return True
        if highVal1 > highVal0:
            return False
        if highVal1 == highVal0:
            if (highEnd1 != highEnd0) and (highEnd0 == ')'):
                return False
        return True

    @_('COINCIDESFUNC expr COMMA expr RPAREN', 'COINCIDESFUNC expr COMMA ltrange RPAREN', 'COINCIDESFUNC expr COMMA gtrange RPAREN',
       'COINCIDESFUNC ltrange COMMA expr RPAREN', 'COINCIDESFUNC ltrange COMMA ltrange RPAREN', 'COINCIDESFUNC ltrange COMMA gtrange RPAREN',
       'COINCIDESFUNC gtrange COMMA expr RPAREN', 'COINCIDESFUNC gtrange COMMA ltrange RPAREN', 'COINCIDESFUNC gtrange COMMA gtrange RPAREN',
       'COINCIDESFUNC NAME COLON expr COMMA NAME COLON expr RPAREN', 'COINCIDESFUNC NAME COLON expr COMMA NAME COLON ltrange RPAREN', 'COINCIDESFUNC NAME COLON expr COMMA NAME COLON gtrange RPAREN',
       'COINCIDESFUNC NAME COLON ltrange COMMA NAME COLON expr RPAREN', 'COINCIDESFUNC NAME COLON ltrange COMMA NAME COLON ltrange RPAREN', 'COINCIDESFUNC NAME COLON ltrange COMMA NAME COLON gtrange RPAREN',
       'COINCIDESFUNC NAME COLON gtrange COMMA NAME COLON expr RPAREN', 'COINCIDESFUNC NAME COLON gtrange COMMA NAME COLON ltrange RPAREN', 'COINCIDESFUNC NAME COLON gtrange COMMA NAME COLON gtrange RPAREN')
    def expr(self, p):
        ''' Test point or range is coincides with point or range'''
        range1 = range2 = None
        if len(p) == 5:
            range1 = p[1]
            range2 = p[3]
        else:
            for i in [1, 5]:
                if p[i] in ['point1', 'range1']:
                    if range1 is None:
                        range1 = p[i + 2]
                elif p[i] in ['point2', 'range2']:
                    if range2 is None:
                        range2 = p[i + 2]
                else:
                    return None
        if isinstance(range1, list) and (len(range1) == 1):
            renge1 = range1[0]
        if isinstance(range2, list) and (len(range2) == 1):
            range2 = range2[0]
        if not isinstance(range1, tuple) or (len(range1) != 4):      # a point
            if isinstance(range2, tuple) and (len(range2) == 4):
                return False
            return range1 == range2
        (lowEnd0, lowVal0, highVal0, highEnd0) = range1
        if not isinstance(range2, tuple) or (len(range2) != 4):     # not a range
            return False
        (lowEnd1, lowVal1, highVal1, highEnd1) = range2
        # Check range p.expr0 coincides with range p.expr1
        if isinstance(lowVal0, str) and not isinstance(lowVal1, str):
            return False
        elif (type(lowVal0) == int) and (type(lowVal1) != int):                     # a range of Year, month durations
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

    @_('DAYOFYEARFUNC expr RPAREN', 'DAYOFYEARFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' day of the year from date '''
        if len(p) == 3:
            dateParam = p[1]
        elif p[1] == 'date':
            dateParam = p[3]
        else:
            return None
        if isinstance(dateParam, list) and (len(dateParam) == 1):
            dateParam = dateParam[0]
        if isinstance(dateParam, datetime.date) or isinstance(dateParam, datetime.datetime):
            return dateParam.timetuple().tm_yday
        return None

    @_('DAYOFWEEKFUNC expr RPAREN', 'DAYOFWEEKFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' day of the week from a date '''
        if len(p) == 3:
            dateParam = p[1]
        elif p[1] == 'date':
            dateParam = p[3]
        else:
            return None
        if isinstance(dateParam, list) and (len(dateParam) == 1):
            dateParam = dateParam[0]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if isinstance(dateParam, datetime.date) or isinstance(dateParam, datetime.datetime):
            return days[dateParam.weekday()]
        return None

    @_('MONTHOFYEARFUNC expr RPAREN', 'MONTHOFYEARFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' month of the year from a date '''
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        if len(p) == 3:
            dateParam = p[1]
        elif p[1] == 'date':
            dateParam = p[3]
        else:
            return None
        if isinstance(dateParam, list) and (len(dateParam) == 1):
            dateParam = dateParam[0]
        if isinstance(dateParam, datetime.date) or isinstance(dateParam, datetime.datetime):
            return months[dateParam.month]
        return None

    @_('WEEKOFYEARFUNC expr RPAREN', 'WEEKOFYEARFUNC NAME COLON expr RPAREN')
    def expr(self, p):
        ''' week of the year from a date '''
        if len(p) == 3:
            dateParam = p[1]
        elif p[1] == 'date':
            dateParam = p[3]
        else:
            return None
        if isinstance(dateParam, list) and (len(dateParam) == 1):
            dateParam = dateParam[0]
        if isinstance(dateParam, datetime.date) or isinstance(dateParam, datetime.datetime):
            (year, week, weekday) = dateParam.isocalendar()
            return week
        return None


    def sortFunc(self, thisList, name0, name1, name2, relop, name3):
        ''' Sort a list according to an anonymous function '''
        if not isinstance(thisList, list):
            thisList = [thisList]
        if len(thisList) == 0:
            return []
        if isinstance(thisList[0], dict):
            reversed = False
            attrib = ''
            if not name2.startswith(name0 + '.'):
                if (not name3.startswith(name0 + '.')) or (not name2.startswith(name1 + '.')):
                    return None
                reversed = True
                attrib = name3[len(name0) + 1:]
                if attrib == '':
                    return None
                if attrib != name2[len(name1) + 1:]:
                    return None
            else:
                if not name3.startswith(name1 + '.'):
                    return None
                attrib = name2[len(name0) + 1:]
                if attrib == '':
                    return None
                if attrib != name3[len(name1) + 1:]:
                    return None
            try:
                if relop == '<':
                    if reversed:
                        return sorted(thisList, key=itemgetter(attrib), reverse=True)
                    else:
                        return sorted(thisList, key=itemgetter(attrib))
                else:
                    if reversed:
                        return sorted(thisList, key=itemgetter(attrib))
                    else:
                        return sorted(thisList, key=itemgetter(attrib), reverse=True)
            except:
                return None
        else:
            if name0 != name2:
                if (name0 != name3) or (name1 != name2):
                    return None
            elif name1 != name3:
                return None
            try:
                if relop == '<':
                    if name0 == name2:
                        return sorted(thisList)
                    else:
                        return sorted(thisList, reverse=True)
                else:
                    if name0 == name2:
                        return sorted(thisList, reverse=True)
                    else:
                        return sorted(thisList)
            except:
                return None
        pass

    @_('SORTFUNC expr COMMA FUNCTIONFUNC NAME COMMA NAME RPAREN NAME GTTHAN NAME RPAREN')
    def expr(self, p):
        return self.sortFunc(p.expr, p.NAME0, p.NAME1, p.NAME2, p.GTTHAN, p.NAME3)

    @_('SORTFUNC expr COMMA FUNCTIONFUNC NAME COMMA NAME RPAREN NAME LTTHAN NAME RPAREN')
    def expr(self, p):
        return self.sortFunc(p.expr, p.NAME0, p.NAME1, p.NAME2, p.LTTHAN, p.NAME3)

    @_('NOWFUNC RPAREN')
    def expr(self, p):
        return datetime.datetime.now()

    @_('TODAYFUNC RPAREN')
    def expr(self, p):
        return datetime.date.today()

    @_('BOOLEAN')
    def expr(self, p):
        if str(p.BOOLEAN) == 'true':
            return True
        else:
            return False

    def isContextName(self, name):
        if self.inContext == 0:
            return False
        for i in range(len(self.contextNames)):
            if name in self.contextNames[i]:
                return True
        return False

    def getContextValue(self, name):
        for i in range(len(self.contextNames) -1, -1, -1):
            if name in self.contextNames[i]:
                return self.contextNames[i][name]
        return  None

    @_('NAME')
    def expr(self, p):
        if p.NAME in self.names:
            return self.names[p.NAME]
        if self.isContextName(p.NAME):
            return self.getContextValue(p.NAME)
        if p.NAME.endswith('.year'):
            if p.NAME[:-5] in self.names:
                value = self.names[p.NAME[:-5]]
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.year)
            elif self.isContextName(p.NAME[:-5]):
                value = self.getContextValue(p.NAME[:-5])
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.year)
        if p.NAME.endswith('.month'):
            if p.NAME[:-6] in self.names:
                value = self.names[p.NAME[:-6]]
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.month)
            if self.isContextName(p.NAME[:-6]):
                value = self.getContextValue(p.NAME[:-6])
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.month)
        if p.NAME.endswith('.day'):
            if p.NAME[:-4] in self.names:
                value = self.names[p.NAME[:-4]]
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.day)
            if self.isContextName(p.NAME[:-4]):
                value = self.getContextValue(p.NAME[:-4])
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.day)
        elif p.NAME.endswith('.weekday'):
            if p.NAME[:-8] in self.names:
                value = self.names[p.NAME[:-8]]
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.isoweekday())
            if self.isContextName(p.NAME[:-8]):
                value = self.getContextValue(p.NAME[:-8])
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    return float(value.isoweekday())
        elif p.NAME.endswith('.hour'):
            if p.NAME[:-5] in self.names:
                value = self.names[p.NAME[:-5]]
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                    return float(value.hour)
            if self.isContextName(p.NAME[:-5]):
                value = self.getContextValue(p.NAME[:-5])
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                    return float(value.hour)
        elif p.NAME.endswith('.minute'):
            if p.NAME[:-7] in self.names:
                value = self.names[p.NAME[:-7]]
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                    return float(value.minute)
            if self.isContextName(p.NAME[:-7]):
                value = self.getContextValue(p.NAME[:-7])
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                    return float(value.minute)
        elif p.NAME.endswith('.second'):
            if p.NAME[:-7] in self.names:
                value = self.names[p.NAME[:-7]]
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                    return float(value.second)
            if self.isContextName(p.NAME[:-7]):
                value = self.getContextValue(p.NAME[:-7])
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                    return float(value.second)
        elif p.NAME.endswith('.timezone'):
            isTimeZone = False
            if p.NAME[:-9] in self.names:
                value = self.names[p.NAME[:-9]]
                isTimeZone = True
            if self.isContextName(p.NAME[:-9]):
                value = self.getContextValue(p.NAME[:-9])
                isTimeZone = True
            if isTimeZone:
                if isinstance(value, datetime.datetime):
                    if value.tzinfo is None:
                        return None
                    try:
                        return str(value.tzinfo.zone)
                    except:
                        return str(value.tzname())
                elif isinstance(value, datetime.time):
                    if value.tzinfo is None:
                        return None
                    try:
                        return str(value.tzinfo.zone)
                    except:
                        return str(value.tzname())
        elif p.NAME.endswith('.time_offset'):
            isTimeOffset = False
            if p.NAME[:-12] in self.names:
                value = self.names[p.NAME[:-12]]
                isTimeOffset = True
            if self.isContextName(p.NAME[:-12]):
                value = self.getContextValue(p.NAME[:-12])
                isTimeOffset = True
            if isTimeOffset:
                if isinstance(value, datetime.datetime):
                    if value.tzinfo == None:
                        return None
                    return value.utcoffset()
                elif isinstance(value, datetime.time):
                    if value.tzinfo == None:
                        return None
                    tmpDateTime = datetime.datetime.combine(datetime.date.today(), value)
                    return tmpDateTime.utcoffset()
        elif p.NAME.endswith('.days'):
            if p.NAME[:-5] in self.names:
                value = self.names[p.NAME[:-5]]
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() / 60 / 60 / 24)
            if self.isContextName(p.NAME[:-5]):
                value = self.getContextValue(p.NAME[:-5])
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() / 60 / 60 / 24)
        elif p.NAME.endswith('.hours'):
            if p.NAME[:-6] in self.names:
                value = self.names[p.NAME[:-6]]
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() / 60 / 60) % 24
            if self.isContextName(p.NAME[:-6]):
                value = self.getContextValue(p.NAME[:-6])
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() / 60 / 60) % 24
        elif p.NAME.endswith('.minutes'):
            if p.NAME[:-8] in self.names:
                value = self.names[p.NAME[:-8]]
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() / 60) % 60
            if self.isContextName(p.NAME[:-8]):
                value = self.getContextValue(p.NAME[:-8])
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() / 60) % 60
        elif p.NAME.endswith('.seconds'):
            if p.NAME[:-8] in self.names:
                value = self.names[p.NAME[:-8]]
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() % 60)
            if self.isContextName(p.NAME[:-8]):
                value = self.getContextValue(p.NAME[:-8])
                if isinstance(value, datetime.timedelta):
                    return float(value.total_seconds() % 60)
        elif p.NAME.endswith('.years'):
            if p.NAME[:-6] in self.names:
                value = self.names[p.NAME[:-6]]
                if type(value) == int:
                    return float(value / 12)
            if self.isContextName(p.NAME[:-6]):
                value = self.getContextValue(p.NAME[:-6])
                if type(value) == int:
                    return float(value / 12)
        elif p.NAME.endswith('.months'):
            if p.NAME[:-7] in self.names:
                value = self.names[p.NAME[:-7]]
                if type(value) == int:
                    return float(value % 12)
            if self.isContextName(p.NAME[:-7]):
                value = self.getContextValue(p.NAME[:-7])
                if type(value) == int:
                    return float(value % 12)
        elif p.NAME.endswith('.start'):
            isStart = False
            if p.NAME[:-6] in self.names:
                value = self.names[p.NAME[:-6]]
                isStart = True
            if self.isContextName(p.NAME[:-6]):
                value = self.getContextValue(p.NAME[:-6])
                isStart = True
            if isStart:
                if isinstance(value, tuple) and (len(value) == 4):
                    (end0, low0, high1, end1) = value
                    if low0 is None:
                        return None
                    try:
                        return float(low0)
                    except:
                        return None
        elif p.NAME.endswith('.start_included'):
            isStartIncluded = False
            if p.NAME[:-13] in self.names:
                value = self.names[p.NAME[:-13]]
                isStartIncluded = True
            if self.isContextName(p.NAME[:-13]):
                value = self.getContextValue(p.NAME[:-13])
                isStartIncluded = True
            if isStartIncluded:
                if isinstance(value, tuple) and (len(value) == 4):
                    (end0, low0, high1, end1) = value
                    if end0 == '[':
                        return True
                    else:
                        return False
        elif p.NAME.endswith('.end'):
            isEnd = False
            if p.NAME[:-4] in self.names:
                value = self.names[p.NAME[:-4]]
                isEnd = True
            if self.isContextName(p.NAME[:-4]):
                value = self.getContextValue(p.NAME[:-4])
                isEnd = True
            if isEnd:
                if isinstance(value, tuple) and (len(value) == 4):
                    (end0, low0, high1, end1) = value
                    if high1 is None:
                        return None
                    try:
                        return float(high1)
                    except:
                        return None
        elif p.NAME.endswith('.end_included'):
            isEndIncluded = False
            if p.NAME[:-11] in self.names:
                value = self.names[p.NAME[:-11]]
                isEndIncluded = True
            if self.isContextName(p.NAME[:-11]):
                value = self.getContextValue(p.NAME[:-11])
                isEndIncluded = True
            if isEndIncluded:
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
        return None

    def unicodeString(self, stringParam):
        lastEnd = 0
        thisString = ''
        for match in re.finditer(r'(^|[^\\])\\(u([0-9A-Fa-f]{4})|U([0-9A-Fa-f]{6}))', stringParam):
            thisString += stringParam[lastEnd:match.end(1)]
            lastEnd = match.end(2)
            if match.group(3) is not None:
                thisGroup = match.group(3)
            else:
                thisGroup = match.group(4)
            thisHex = 0
            for i in range(len(thisGroup)):
                thisHex *= 16
                if thisGroup[i] in '0123456789':
                    thisHex += ord(thisGroup[i]) - ord('0')
                elif thisGroup[i] in 'ABCDEF':
                    thisHex += ord(thisGroup[i]) - ord('A') + 10
                elif thisGroup[i] in 'abcdef':
                    thisHex += ord(thisGroup[i]) - ord('a') + 10
            thisString += chr(thisHex)
        thisString += stringParam[lastEnd:]
        return thisString

    @_('STRING')
    def expr(self, p):
        stringParam = p.STRING
        newParam = re.sub(r'(^|[^\\])\\U([0-9A-Fa-f]{6})', r'\1\\U00\2', stringParam)
        lastLen = -2
        thisLen = -1
        while thisLen != lastLen:
            try:
                newParam = ast.literal_eval(newParam)
            except:
                newParam = ast.literal_eval(str(newParam.encode('utf-16', 'surrogatepass').decode('utf-16')))
            lastLen = thisLen
            newParam = '"' + newParam + '"'
            thisLen = len(newParam)
            if thisLen != lastLen:
                newParam = newParam.replace('\\', '\\\\')     # Protect double backslashes
        return str(newParam[1:-1])

    @_('DATE')
    def expr(self, p):
        ''' Convert string to datetime.date '''
        thisDate = self.dateFunc(p.DATE)
        return thisDate

    def dateFunc(self, thisDate):
        ''' Convert string to datetime.date '''
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
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
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                thisTime =  dateutil.parser.parse(parts[0]).timetz()     # A time with timezone
        except:
            return None
        if len(parts) == 1:
            return thisTime
        try:
            thisZone = pytz.timezone(parts[1])
        except:
            return thisTime
        if thisZone is None:
            return thisTime
        try:
            retTime = datetime.datetime.combine(datetime.date.today(), thisTime)
            retTime = thisZone.localize(retTime)
            retTime = retTime.timetz()
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
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                thisDateTime = dateutil.parser.parse(parts[0])
        except:
            return None
        if len(parts) == 1:
            return thisDateTime
        try:
            thisZone = pytz.timezone(parts[1])
        except:
            return thisDateTime
        if thisZone is None:
            return thisDateTime
        try:
            retDateTime = thisZone.localize(thisDateTime)
        except:
            return thisDateTime
        return retDateTime

    @_('DTDURATION')
    def expr(self, p):
        ''' Convert duration string into datetime.timedelta '''
        duration = p.DTDURATION
        return self.dtdFunc(duration)

    def dtdFunc(self, duration):
        ''' Convert duration string (that passed regex) into datetime.timedelta '''
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        duration = duration[1:]         # skip P
        days = seconds = milliseconds = 0
        if duration.find('D') != -1:          # days is optional
            parts = duration.split('D')
            if len(parts) > 2:
                return None
            if parts[0] == '':
                return None
            try:
                days = int(parts[0])
                duration = parts[1]
            except:
                return None
            if duration == '':
                if sign == 0:
                    return datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
                else:
                    return -datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
        if (duration.find('H') != -1) and (duration.find('M') != -1) and (duration.find('S') != -1):
            if duration[0] == 'T':      # T need not be present if all time components are present
                duration = duration[1:]
        elif duration[0] != 'T':
            return None
        else:
            duration = duration[1:]
        if len(duration) == 0:
            return None
        if duration.find('H') != -1:
            parts = duration.split('H')
            if len(parts) > 2:
                return None
            if parts[0] == '':
                return None
            try:
                seconds = int(parts[0]) * 60 * 60
            except:
                return None
            duration = parts[1]
        if duration.find('M') != -1:
            parts = duration.split('M')
            if len(parts) > 2:
                return None
            if parts[0] == '':
                return None
            try:
                seconds += int(parts[0]) * 60
            except:
                return None
            duration = parts[1]
        if duration.find('S') != -1:
            parts = duration.split('S')
            if len(parts) > 2:
                return None
            if parts[0] == '':
                return None
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
        ''' Convert year/month duration string (that passed regex) into int '''
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        duration = duration[1:]         # skip P
        months = 0
        if duration.find('Y') != -1:
            parts = duration.split('Y')
            try:
                months = int(parts[0]) * 12
            except:
                return None
            duration = parts[1]
        if duration.find('M') != -1:
            parts = duration.split('M')
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
        try:
            return float(p.NUMBER)
        except:
            return None

    def error(self, p):
        if p:
            self.errors.append("Syntax error at token '{!s}'".format(p))
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
            # print('S-FEEL token', token.type, token.value)
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
