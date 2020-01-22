# pySFeel
An implementation S-FEEL (Simple Expression Language), from DMN (Decision Model Notaion).
pySFeel is implemented in Python, using the sly module and has many FEEL features.
* **not**, **and** and **or** in logical expressions which can be enclosed in round brackets (())
* in() function, e.g. 5 in(<6)
* Lists and filters
* Contexts and filters
* Ranges
* Built in functions

pySFeel processes a single S-FEEL statement at a time.
It is not intended to be a syntacically perfect implemtation of S-FEEL,
but rather an enabler for an implementation of DMN (Decision Model Notation) [pyDMNrules](https://github.com/russellmcdonell/pyDMNrules).
The internal data types are float, string, boolean, datetime.date, datetime.time, and datetime.timedelta.
The S-FEEL constant null is mapped to None.
Years and months durations are stored as floats. Days and time durations are stored as datetime.timedelta

There is one deliberate deviation from the standard - the key word 'item' in a Context filters is **not** optional.
\[{x:1,y:2},{x:2,y:3}\]\[x=1\] is not valid, but \[{x:1,y:2},{x:2,y:3}\]\[item x=1\] is valid and will return {x:1,y:2}.
Similarly, fred.y is **not** the 'y' filter on the List of Contexts named 'fred' [as fred.y is valid name].
However (fred).y will is the 'y' filter on the list of Contexts name fred.

There's one extension - an assignment operator (<-)

    fred <- 7
    bill <- 9
    fred = bill
This will return False

    fred <- [{x:1,y:2},{x:2,y:3}]
    (fred).y
This will return [2,3]

USAGE:

    import pySFeel
    parser = pySFeel.SFeelParser()
    sfeelText = '7.3 in [2.0 .. 9.1]'
    (status, retVal) = parser.sFeelParse(sfeelText)
    if 'errors' in status:
        print('With errors:', status['errors'])
- retVal will be True
- The dictonary 'status' will have the key 'errors' if you have errors in your sfeelText.
- status['errors'] is a list of strings. It may help in diagnosing your S-FEEL syntax errors.
