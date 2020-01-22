# -----------------------------------------------------------------------------
# pySFeel.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
import re
import datetime
import dateutil.parser
import math
import statistics

class SFeelLexer(Lexer):
    tokens = {BOOLEAN, DATEFUNC, TIMEFUNC, DATETIMEFUNC,DATEANDTIMEFUNC,
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
              VALUETFUNC, VALUEDTFUNC, VALUEDT1FUNC, VALUEDTDFUNC, VALUEDTD1FUNC,
              VALUEYMDFUNC, VALUEYMD1FUNC,
              DURATIONFUNC, YEARSANDMONTHSDURATIONFUNC, GETVALUEFUNC, GETENTRIESFUNC,
              NAME, STRING, NULL,
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
    DATETIMEFUNC = r'datetime\('
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
    DTDURATION = r'-?P((([0-9]+D)(T(([0-9]+H)([0-9]+M)?([0-9]+(\.[0-9]+)?S)?|([0-9]+M)([0-9]+(\.[0-9]+)?S)?|([0-9]+(\.[0-9]+)?S)))?)|(T(([0-9]+H)([0-9]+M)?([0-9]+(\.[0-9]+)?S)?|([0-9]+M)([0-9]+(\.[0-9]+)?S)?|([0-9]+(\.[0-9]+)?S))))'
    YMDURATION = r'-?P[0-9]+Y[0-9]+M'
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

    STRING = r'"(' + r"\\'" + r'|\\"|\\\\|\\n|\\r|\\t|\\u[0-9]{4}|[^"])*"'
    DATETIME = r'-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?'
    DATE = r'([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?'
    TIME = r'(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?'
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
        if p.expr is None:
            return None
        elif isinstance(p.expr, list):
            if len(p.expr) == 1:
                return p.expr[0]
            else:
                return p.expr
        else:
            return p.expr

    @_(NULL)
    def expr(self, p):
        return None

    @_('expr IN expr')
    def expr(self, p):
        if isinstance(p.expr1, tuple) :
            (end0, lowVal, highVal, end1) = p.expr1
            if isinstance(p.expr0, str):
                if not isinstance(lowVal, str) or not isinstance(highVal, str):
                    return False
            elif isinstance(p.expr0, float):
                if not isinstance(lowVal, float) or not isinstance(highVal, float):
                    return False
            elif isinstance(p.expr0, datetime.date):
                if not isinstance(lowVal, datetime.date) or not isinstance(highVal, datetime.date):
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
        elif isinstance(p.expr1, list) :
            return p.expr0 in p.expr1
        else:
            return None

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        if isinstance(p.expr0, dict) and isinstance(p.expr1, dict):
            return {**p.expr0, **p.expr1}
        elif isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 + p.expr1
        elif isinstance(p.expr0, str) and isinstance(p.expr1, str):
            return p.expr0 + p.expr1
        elif isinstance(p.expr0, list) and isinstance(p.expr1, list):
            return p.expr0 + p.expr1
        elif (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            if isinstance(p.expr0[0], str) and isinstance(p.expr1, str):
                return p.expr0[0] + p.expr1
            elif isinstance(p.expr0[0], float) and isinstance(p.expr1, float):
                return p.expr0[0] + p.expr1
            else:
                return None
        elif (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            if isinstance(p.expr1[0], str) and isinstance(p.expr0, str):
                return p.expr0 + p.expr1[0]
            elif isinstance(p.expr1[0], float) and isinstance(p.expr0, float):
                return p.expr0 + p.expr1[0]
            else:
                return None
        else:
            return None

    @_('expr MINUS expr')
    def expr(self, p):
        if isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 - p.expr1
        elif (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            if isinstance(p.expr0[0], float) and isinstance(p.expr1, float):
                return p.expr0[0] - p.expr1
            else:
                return None
        elif (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            if isinstance(p.expr1[0], float) and isinstance(p.expr0, float):
                return p.expr0 - p.expr1[0]
            else:
                return None
        else:
            return None

    @_('expr EXPONENT expr')
    def expr(self, p):
        if isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 ** p.expr1
        elif (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            if isinstance(p.expr0[0], float) and isinstance(p.expr1, float):
                return p.expr0[0] ** p.expr1
            else:
                return None
        elif (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            if isinstance(p.expr1[0], float) and isinstance(p.expr0, float):
                return p.expr0 ** p.expr1[0]
            else:
                return None
        else:
            return None

    @_('expr MULTIPY expr')
    def expr(self, p):
        if isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return p.expr0 * p.expr1
        elif (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            if isinstance(p.expr0[0], float) and isinstance(p.expr1, float):
                return p.expr0[0] * p.expr1
            else:
                return None
        elif (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            if isinstance(p.expr1[0], float) and isinstance(p.expr0, float):
                return p.expr0 * p.expr1[0]
            else:
                return None
        else:
            return None

    @_('expr DIVIDE expr')
    def expr(self, p):
        if isinstance(p.expr0, float) and isinstance(p.expr1, float):
            if p.expr1 == 0.0:
                return None
            else:
                return p.expr0 / p.expr1
        elif (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            if isinstance(p.expr0[0], float) and isinstance(p.expr1, float):
                if p.expr1 == 0.0:
                    return None
                return p.expr0[0] / p.expr1
            else:
                return None
        elif (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            if isinstance(p.expr1[0], float) and isinstance(p.expr0, float):
                if p.expr1[0] == 0.0:
                    return None
                return p.expr0 / p.expr1[0]
            else:
                return None
        else:
            return None

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        if isinstance(p.expr, float):
            return -p.expr
        elif (isinstance(p.expr, list) and (len(p.expr) == 1)):
            if isinstance(p.expr[0], float):
                return -p.expr[0]
            else:
                return None
        elif isinstance(p.expr, bool):
            return not p.expr
        else:
            return None

    @_('expr EQUALS expr')
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
            return x0 == x1
        except:
            False

    @_('expr NOTEQUALS expr')
    def expr(self, p):
        if (isinstance(p.expr0, list) and (len(p.expr0) == 1)):
            if (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
                return p.expr0[0] != p.expr1[0]
            else:
                return p.expr0[0] != p.expr1
        elif (isinstance(p.expr1, list) and (len(p.expr1) == 1)):
            return p.expr0 != p.expr1[0]
        else:
            return p.expr0 != p.expr1

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
        return (p.ITEM, p.EQUALS, p.expr)

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
        if isinstance(p.expr, list):
            if isinstance(p.listFilter, float):
                if len(p.expr) < int(p.listFilter):
                    return None
                if int(p.listFilter) < 1:
                    return None
                return p.expr[int(p.listFilter) - 1]
            if isinstance(p.listFilter, tuple):
                if len(p.listFilter) == 2:
                    if (not isinstance(p.expr[0], str)) and (not isinstance(p.expr[0], float)):
                        return None
                    (equality, value) = p.listFilter
                    retList = []
                    for i in range(len(p.expr)):
                        if equality == '>=':
                            if p.expr[i] >= value:
                                retList.append(value)
                        elif equality == '>':
                            if p.expr[i] > value:
                                retList.append(value)
                        elif equality == '<=':
                            if p.expr[i] <= value:
                                retList.append(value)
                        elif equality == '<':
                            if p.expr[i] < value:
                                retList.append(value)
                        elif equality == '=':
                            if p.expr[i] == value:
                                retList.append(value)
                        elif equality == '!=':
                            if p.expr[i] != value:
                                retList.append(value)
                        else:
                            return None
                    return retList
                elif len(p.listFilter) == 3:
                    if not isinstance(p.expr[0], dict):
                        return None
                    (key, equality, value) = p.listFilter
                    retList = []
                    for i in range(len(p.expr)):
                        if key in p.expr[i]:
                            if equality == '>=':
                                if p.expr[i][key] >= value:
                                    retList.append(p.expr[i])
                            elif equality == '>':
                                if p.expr[i][key] > value:
                                    retList.append(p.expr[i])
                            elif equality == '<=':
                                if p.expr[i][key] <= value:
                                    retList.append(p.expr[i])
                            elif equality == '<':
                                if p.expr[i][key] < value:
                                    retList.append(p.expr[i])
                            elif equality == '=':
                                if p.expr[i][key] == value:
                                    retList.append(p.expr[i])
                            elif equality == '!=':
                                if p.expr[i][key] != value:
                                    retList.append(p.expr[i])
                            else:
                                return None
                    return retList
                else:
                    return None
            return None
        return None

    @_('PERIOD NAME')
    def listSelect(self, p):
        return p.NAME

    @_('expr listSelect')
    def expr(self, p):
        key = p.listSelect
        if isinstance(p.expr, list):
            if not isinstance(p.expr[0], dict):
                return None
            retList = []
            for i in range(len(p.expr)):
                if key in p.expr[i]:
                    retList.append(p.expr[i][key])
            return retList
        elif isinstance(p.expr, dict):
            if key in p.expr:
                return p.expr[key]
            else:
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
            elif p.expr:       # True/Otherwise
                return None
            else:               # False/Otherwise
                return False
        else:
            if isinstance(p.andExpr, bool):
                if p.andExpr:     # Otherwise/True
                    return None
                else:           # Otherwise/False
                    return False
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
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('COMMA expr')
    def listPart(self, p):
        if isinstance(p.expr, list):
            return p.expr
        else:
            return [p.expr]

    @_('listPart COMMA expr')
    def listPart(self, p):
        if isinstance(p.expr, list):
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
        return (p.LPAREN, p.expr0, p.expr1, p.RPAREN)

    @_('LPAREN expr ELLIPSE expr RBRACKET')
    def expr(self, p):
        return (p.LPAREN, p.expr0, p.expr1, p.RBRACKET)

    @_('LPAREN expr ELLIPSE expr LBRACKET')
    def expr(self, p):
        return (p.LPAREN, p.expr0, p.expr1, p.LBRACKET)

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
        return p.listStart + p.listPart

    @_('DATEFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert datetime.date/datetime.time/str into datetime.date '''
        if isinstance(p.expr, datetime.date):
            return p.expr
        elif isinstance(p.expr, datetime.time):
            return datetime.date(year=0, month=0, day=0)
        elif isinstance(p.expr, datetime.datetime):
            return p.expr.date()
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

    @_('TIMEFUNC expr COMMA expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Convert hour, minute, second, offset into datetime.time '''
        hour = int(p.expr0)
        min = int(p.expr1)
        sec = int(p.expr2)
        if (p.expr3 != None) and isinstance(p.expr3, datetime.timedelta):
            sec += int(p.expr3.total_seconds())
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

    @_('TIMEFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert datetime.date/datetime.time/str into datetime.time '''
        if isinstance(p.expr, datetime.date):
            return datetime.time(hour=0, minute=0, second=0)
        elif isinstance(p.expr, datetime.time):
            return p.expr
        elif isinstance(p.expr, datetime.datetime):
            return p.expr.time()
        elif isinstance(p.expr, str):
            return dateutil.parser.parse(p.expr).time()
        else:
            return None

    @_('DATETIMEFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert datetime.date/datetime.time/str into datetime.datetime '''
        if isinstance(p.expr, datetime.date):
            return datetime.combine(p.expr, datetime.time(hour=0, minute=0, second=0))
        elif isinstance(p.expr, datetime.time):
            return datetime.combine(datetime.date(year=0, month=0, day=0), p.expr)
        elif isinstance(p.expr, datetime.datetime):
            return p.expr
        elif isinstance(p.expr, str):
            return dateutil.parser.parse(p.expr)
        else:
            return None

    @_('DATEANDTIMEFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Convert date, time into datetime.datetime '''
        if isinstance(p.expr0, datetime.date):
            if isinstance(p.expr1, datetime.time):
                return datetime.combine(p.expr0, p.expr1)
        return None

    @_('DATEANDTIMEFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert str into datetime.datetime '''
        if isinstance(p.expr, str):
            return dateutil.parser.parse(p.expr)
        return None

    @_('NUMBERFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' Float from formatted string'''
        number = p.expr0
        grouping = p.expr1
        decimal = p.expr2
        if (grouping is not None) and (grouping not in [' ', ',', '.']):
            return None
        if (decimal is not None) and (decimal not in ['.', ',']):
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
        elif isinstance(p.expr, bool):
            if p.expr:
                return 'true'
            else:
                return 'false'
        elif isinstance(p.expr, float):
            return str(p.expr)
        if isinstance(p.expr, str):
            return p.expr
        elif isinstance(p.expr, datetime.date):
            return p.expr.isoformat()
        elif isinstance(p.expr, datetime.datetime):
            return p.expr.isoformat(sep='T')
        elif isinstance(p.expr, datetime.time):
            return p.expr.isoformat()
        elif isinstance(p.expr, datetime.timedelta):
            duration = p.expr.total_seconds()
            secs = duration % 60
            duration = int(duration / 60)
            mins = duration % 60
            duration = int(duration / 60)
            hour = duration % 24
            days = int(duration / 24)
            return 'P%dDT%dH%dM%dS' % (days, hours, mins, secs)

    @_('NOTFUNC expr RPAREN')
    def expr(self, p):
        ''' negate a boolean'''
        if not isinstance(p.expr, bool):
            return None
        return not p.expr

    def inFunc(self, thisList):
        inValue = thisList[0]
        for i in range(1,len(thisList)):
            (comparitor, toValue) = thisList[i]
            if comparitor == '=':
                try:
                    if(inValue == toValue):
                        return True
                except:
                    return False
            elif comparitor == '<=':
                try:
                    if(inValue <= toValue):
                        return True
                except:
                    return False
            elif comparitor == '<':
                try:
                    if(inValue < toValue):
                        return True
                except:
                    return False
            elif comparitor == '>=':
                try:
                    if(inValue >= toValue):
                        return True
                except:
                    return False
            elif comparitor == '>':
                try:
                    if(inValue > toValue):
                        return True
                except:
                    return False
            elif comparitor == '!=':
                try:
                    if(inValue != toValue):
                        return True
                except:
                    return False
        return False

    @_('expr INFUNC expr')
    def inStart(self, p):
        ''' item in list items'''
        if isinstance(p.expr1, list):
            thisList = p.expr1
            for i in range(len(thisList)):
                thisList[i] = [('=', thisList[i])]
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('=', p.expr1)]

    @_('expr INFUNC LTTHANEQUAL expr')
    def inStart(self, p):
        ''' item in list items'''
        if isinstance(p.expr1, list):
            thisList = p.expr1
            for i in range(len(thisList)):
                thisList[i] = [('<=', thisList[i])]
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('<=', p.expr1)]

    @_('expr INFUNC LTTHAN expr')
    def inStart(self, p):
        ''' item in list items'''
        if isinstance(p.expr1, list):
            thisList = p.expr1
            for i in range(len(thisList)):
                thisList[i] = [('<', thisList[i])]
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('<', p.expr1)]

    @_('expr INFUNC GTTHANEQUAL expr')
    def inStart(self, p):
        ''' item in list items'''
        if isinstance(p.expr1, list):
            thisList = p.expr1
            for i in range(len(thisList)):
                thisList[i] = [('>=', thisList[i])]
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('>=', p.expr1)]

    @_('expr INFUNC GTTHAN expr')
    def inStart(self, p):
        ''' item in list items'''
        if isinstance(p.expr1, list):
            thisList = p.expr1
            for i in range(len(thisList)):
                thisList[i] = [('>', thisList[i])]
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('>', p.expr1)]

    @_('expr INFUNC NOTEQUALS expr')
    def inStart(self, p):
        ''' item in list items'''
        if isinstance(p.expr1, list):
            thisList = p.expr1
            for i in range(len(thisList)):
                thisList[i] = [('!=', thisList[i])]
            return [p.expr0] + thisList
        else:
            return [p.expr0] + [('!=', p.expr1)]

    @_('COMMA LTTHANEQUAL expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = p.expr
            for i in range(len(thisList)):
                thisList[i] = [('<=', thisList[i])]
            return thisList
        else:
            return [('<=', p.expr)]

    @_('COMMA LTTHAN expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = p.expr
            for i in range(len(thisList)):
                thisList[i] = [('<', thisList[i])]
            return thisList
        else:
            return [('<=', p.expr)]

    @_('COMMA GTTHANEQUAL expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = p.expr
            for i in range(len(thisList)):
                thisList[i] = [('>=', thisList[i])]
            return thisList
        else:
            return [('<=', p.expr)]

    @_('COMMA GTTHAN expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = p.expr
            for i in range(len(thisList)):
                thisList[i] = [('>', thisList[i])]
            return thisList
        else:
            return [('<=', p.expr)]

    @_('COMMA NOTEQUALS expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = p.expr
            for i in range(len(thisList)):
                thisList[i] = [('!=', thisList[i])]
            return thisList
        else:
            return [('<=', p.expr)]

    @_('inPart COMMA expr')
    def inPart(self, p):
        if isinstance(p.expr, list):
            thisList = p.expr
            for i in range(len(thisList)):
                thisList[i] = [('=', thisList[i])]
            return p.inPart + thisList
        else:
            return p.inPart + [('=', p.expr)]

    @_('inPart COMMA listPart')
    def inPart(self, p):
        if isinstance(p.listPart, list):
            thisList = p.listPart
            for i in range(len(thisList)):
                thisList[i] = [('=', thisList[i])]
            return p.inPart + thisList
        else:
            return p.inPart + [('=', p.listPart)]

    @_('listPart COMMA inPart')
    def inPart(self, p):
        if isinstance(p.listPart, list):
            thisList = p.listPart
            for i in range(len(thisList)):
                thisList[i] = [('=', thisList[i])]
            return thisList + p.inPart
        else:
            return [('=', p.listPart)] + p.inPart

    @_('inStart listPart RPAREN')
    def expr(self, p):
        partList = p.listPart
        for i in range(len(partList)):
            partList[i] = ('=', partList[i])
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

    @_('SUBSTRINGFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' substring from a string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, float):
            return None
        if not isinstance(p.expr2, float):
            return None
        start = int(p.expr1) - 1
        length = int(p.expr2)
        if start > 0:
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

    @_('SUBSTRINGFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' substring from a string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, float):
            return None
        start = int(p.expr1) - 1
        if abs(start) < len(p.expr0):
            return p.expr0[start:]
        else:
            return None

    @_('STRINGLENFUNC expr RPAREN')
    def expr(self, p):
        ''' length of a string'''
        if not isinstance(p.expr, str):
            return None
        return float(len(p.expr))

    @_('UPPERCASEFUNC expr RPAREN')
    def expr(self, p):
        ''' length of a string'''
        if not isinstance(p.expr, str):
            return None
        return p.expr.upper()

    @_('LOWERCASEFUNC expr RPAREN')
    def expr(self, p):
        ''' length of a string'''
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
            return None
        return p.expr0[:subAt] 

    @_('SUBSTRINGAFTERFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' substring before string'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        subAt = p.expr0.find(p.expr1)
        if subAt == -1:
            return None
        return p.expr0[subAt + len(p.expr1):]

    @_('REPLACEFUNC expr COMMA expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' replace substring in string'''
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
        return re.sub(p.expr1, p.expr2, p.expr0, flags=reFlags)

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
        return re.sub(p.expr1, p.expr2, p.expr0, flags=reFlags)

    @_('CONTAINSFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' does string contain substring'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        return p.expr1 in p.expr0

    @_('STARTSWITHFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' does string start with substring'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        return p.expr0.startswith(p.expr1)

    @_('ENDSWITHFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' does string end with substring'''
        if not isinstance(p.expr0, str):
            return None
        if not isinstance(p.expr1, str):
            return None
        return p.expr0.endswith(p.expr1)

    @_('MATCHESFUNC expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        ''' does string match string'''
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
        ''' does string match string'''
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
        return float(len(p.expr0))

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

    def allFunc(self, thisList):
        if len(thisList) == 0:
            return False
        for i in range(len(thisList)):
            if not isinstance(thisList[i], bool):
                return None
            if thisList[i]:
                return True
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
        ''' sublist from a list'''
        if not isinstance(p.expr0, list):
            return None
        if not isinstance(p.expr1, float):
            return None
        if not isinstance(p.expr2, float):
            return None
        start = int(p.expr1) - 1
        length = int(p.expr2)
        if start > 0:
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
        ''' sublist from a list'''
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
        ''' append item(s) to list '''
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
        return p.concatenateStart + p.listPart

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
        ''' concatinate lists '''
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
        ''' list of indexes of value in a list '''
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
        thisList = p.unionStart + p.listPart
        return self.unionFunc(thisList)

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
                newList += flatten(this[i])
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

    @_('PRODUCTFUNC expr RPAREN')
    def expr(self, p):
        ''' product number in a list '''
        if not isinstance(p.expr, list):
            return None
        product = 1.0
        for i in range(len(p.expr)):
            if not isinstance(p.expr[i], float):
                return None
            product *= p.expr[i]
        return product

    def median(self, thisList):
        try:
            return float(statistics.median(thisList))
        except:
            return None

    @_('MEDIANFUNC expr')
    def medianStart(self, p):
        ''' median item in list '''
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
        ''' stddev item in list '''
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
            return statistics.multimode(thisList)
        except:
            return None

    @_('MODEFUNC expr')
    def modeStart(self, p):
        ''' mode item in list '''
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
        return float(int(p.expr0 * 10**p.expr1 + 0.5))/(10**p.expr1)

    @_('FLOORFUNC expr RPAREN')
    def expr(self, p):
        ''' floor of a number '''
        if not isinstance(p.expr, float):
            return None
        return math.floor(p.expr)
        
    @_('CEILINGFUNC expr RPAREN')
    def expr(self, p):
        ''' ceiling of a number '''
        if not isinstance(p.expr, float):
            return None
        return math.ceil(p.expr)
        
    @_('ABSFUNC expr RPAREN')
    def expr(self, p):
        ''' absolute of a number '''
        if not isinstance(p.expr, float):
            return None
        return abs(p.expr)
        
    @_('MODULOFUNC expr COMMA expr RPAREN')
    def expr(self, p):
        ''' scale a number '''
        if not isinstance(p.expr0, float):
            return None
        if not isinstance(p.expr1, float):
            return None
        return float(int(p.expr0) % int(p.expr1))

    @_('SQRTFUNC expr RPAREN')
    def expr(self, p):
        ''' absolute of a number '''
        if not isinstance(p.expr, float):
            return None
        return math.sqrt(p.expr)
        
    @_('LOGFUNC expr RPAREN')
    def expr(self, p):
        ''' log of a number '''
        if not isinstance(p.expr, float):
            return None
        return math.log(p.expr)
        
    @_('EXPFUNC expr RPAREN')
    def expr(self, p):
        ''' exponential of a number '''
        if not isinstance(p.expr, float):
            return None
        return math.exp(p.expr)
        
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
        
    @_('VALUEDTFUNC expr RPAREN')
    def expr(self, p):
        ''' String expression turned into datetime.date '''
        if isinstance(p.expr, str):
            return dateutil.parser.parse(p.expr).date()
        else:
            return None
        
    @_('VALUEDT1FUNC expr RPAREN')
    def expr(self, p):
        ''' Seconds of time turned into a datetime.time '''
        if isinstance(p.expr, float):
            thisTime = int(p.expr) % (24 * 60 * 60)
            second = thisTime % 60
            thisTime = int(thisTime / 60)
            minute = thisTime % 60
            hour = int(thisTime / 60)
            return datetime.time(hour=hour, minute=minute, second=second)
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
            return datetime.timedelta(seconds=int(p.expr))
        else:
            return None
        
    @_('VALUEYMDFUNC expr RPAREN')
    def expr(self, p):
        ''' internally, YMD durations are floats '''
        return p.expr
        
    @_('VALUEYMD1FUNC expr RPAREN')
    def expr(self, p):
        ''' internally, YMD durations are floats '''
        return p.expr
        
    @_('DURATIONFUNC expr RPAREN')
    def expr(self, p):
        ''' Convert string to datetime.timedelta or float '''
        if not isinstance(p.expr, str):
            return None
        duration = p.expr
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        duration = duration[1:]         # skip P
        parts = duration.split('T')     # look for T (dayTimeDuration)
        if len(parts) == 1:             # no T - must be yearMonthDuration
            months = 0
            parts = duration.split('Y')
            if len(parts) != 2:
                return None
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
            try:
                months += int(parts[0])
            except:
                return None
            if sign == 0:
                return float(months)
            else:
                return -float(months)
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
        ''' Convert datetime.timedelta betwen two dates to float '''
        if not isinstance(p.expr0, datetime.date):
            return None
        if not isinstance(p.expr1, datetime.date):
            return None
        sign = 0
        months = 0
        if p.expr0 < p.expr1:
            months = (p.expr0.year - p.expr1.year) * 12
            months += p.expr0.month - p.expr1.month
            sign = -1
        else:
            months = (p.expr1.year - p.expr0.year) * 12
            months += p.expr1.month - p.expr0.month
        if sign == 0:
            return float(months)
        else:
            return -float(months)


    @_('GETVALUEFUNC expr COMMA NAME RPAREN')
    def expr(self, p):
        if isinstance(p.expr, dict):
            if isinstance(p.NAME, str):
                if p.NAME in p.expr:
                    return p.expr[p.NAME]
        return None

    @_('GETENTRIESFUNC expr RPAREN')
    def expr(self, p):
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

    @_('BOOLEAN')
    def expr(self, p):
        if str(p.BOOLEAN) == 'true':
            return True
        else:
            return False

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            self.errors.append(f'Undefined name {p.NAME!r}')
            return 0

    @_('STRING')
    def expr(self, p):
        return str(p.STRING[1:-1])

    @_('DATE')
    def expr(self, p):
        ''' Convert string to datetime.date '''
        try:
            return dateutil.parser.parse(p.DATE).date()
        except:
            return None

    @_('TIME')
    def expr(self, p):
        ''' Convert string to datetime.time '''
        try:
            return dateutil.parser.parse(p.TIME).time()
        except:
            return None

    @_('DATETIME')
    def expr(self, p):
        ''' Convert string to datetime.datetime '''
        try:
            return dateutil.parser.parse(p.DATETIME)
        except:
            return None

    @_('DTDURATION')
    def expr(self, p):
        ''' Convert duration string into datetime.timedelta '''
        duration = p.DTDURATION
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        duration = duration[1:]         # skip P
        days = seconds = milliseconds = 0
        if duration[0] != 'T':          # days is optional
            parts = duration.split('D')
            if len(parts) == 2:
                days = int(parts[0])
                duration = parts[1]
        duration = duration[1:]         # Skip T
        parts = duration.split('H')
        if len(parts) == 2:
            seconds = int(parts[0]) * 60 * 60
            duration = parts[1]
        parts = duration.split('M')
        if len(parts) == 2:
            seconds += int(parts[0]) * 60
            duration = parts[1]
        parts = duration.split('S')
        if len(parts) == 2:
            sPart = float(parts[0])
            seconds += int(sPart)
            milliseconds = int((sPart * 1000)) % 1000
        if sign == 0:
            return datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)
        else:
            return -datetime.timedelta(days=days, seconds=seconds, milliseconds=milliseconds)

    @_('YMDURATION')
    def expr(self, p):
        ''' Convert year/month duration string into float '''
        duration = p.YMDURATION
        sign = 0
        if duration[0] == '-':
            sign = -1
            duration = duration[1:]     # skip -
        duration = duration[1:]         # skip P
        months = 0
        parts = duration.split('Y')
        if len(parts) != 2:
            return None
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
        try:
            months += int(parts[0])
        except:
            return None
        if sign == 0:
            return float(months)
        else:
            return -float(months)

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
        '''
        Parse S-FEEL text)
        '''
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


        (status, retVal) = parser.sFeelParse(text)

        print(retVal)
        if 'errors' in status:
            print('With errors:', status['errors'])
