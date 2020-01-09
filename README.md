# pySFeel
An implementation S-FEEL in Python with many FEEL features.
* Lists and Context (and filters)
* Built in functions
* Dates, Times and Intervals

It is not intended to be a syntacically perfect implemtation of S-FEEL,
but rather an enable for implementation of DMN (Decision Model Notation).
The internal data types are float, string, datetime.date, datetime.time, and datetime.timedelta.
YearMonth intervals are stored as floats. DayTime intervals are stored as datetime.timedelta

There's one extension - an assignment operator (<-)

    fred <- 7
    bill <- 9
    fred = bill
    
This will return true

USAGE:

    import pySFeel
    lexer = SFeelLexer()
    parser = SFeelParser()
    sfeelText = '7.3 in [2.0 .. 9.1]'
    retVal = parser.parser(lexer.tokenize(sfeelText))
   
(retVal will be True)

