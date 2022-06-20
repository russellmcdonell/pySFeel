.. pySFeel documentation master file, created by
   sphinx-quickstart on Wed Jan 22 12:16:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pySFeel Documentation
=====================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


the sFeelParse function
-----------------------

.. py:module:: pySFeel

.. py:class:: SFeelParser

   .. automethod:: sFeelParse

Data Types
----------
pySFeel converts S-FEEL data into the nearest equivalent Python native data type.

+--------------------------+-------------------------------------------------+
|     S-Feel data type     |   Python native data type                       |
+==========================+=================================================+
|         number           |            float                                |
+--------------------------+-------------------------------------------------+
|         string           |             str                                 |
+--------------------------+-------------------------------------------------+
|        boolean           |            bool                                 |
+--------------------------+-------------------------------------------------+
|  days and time duration  |      datetime.timedelta                         |
+--------------------------+-------------------------------------------------+
| year and months duration |             int                                 |
+--------------------------+-------------------------------------------------+
|        time              |        datetime.time                            |
+--------------------------+-------------------------------------------------+
|        date              |        datetime.date                            |
+--------------------------+-------------------------------------------------+
|   date and time          |      datetime.datetime                          |
+--------------------------+-------------------------------------------------+
|        List              |            list                                 |
+--------------------------+-------------------------------------------------+
|      Context             |            dict                                 |
+--------------------------+-------------------------------------------------+
|       Range              | tuple(end0, low0, high1, end1)                  |
+--------------------------+-------------------------------------------------+
|                          | where end0 is '[' or '(' and end1 is ')' or ']' |    
+--------------------------+-------------------------------------------------+

| Literal strings (@"PT5H") are implemented as both literal strings (@"PT5H") and as bare strings (PT5H).
| @"PT5H" > @"PT4H" can be written as PT5H > PT4H and would return True
| NOTE: For safety, enclose 'codes' in double quotes.
| The ICD-10 code P04D, if not enclosed in double qoutes, will be interpreted as a day and time duration of 4 days.
| The AN-SNAP code if 499A will throw a syntax error if not enclosed in double quotes, as '499' will be interpreted as a number that should be followed by an operator.

List and Context Filters
------------------------
pySFeel supports List and Context filters with one deviation from the standard - the dot operator requires the List to be enclosed in brackets.

| Hence, fred.y is **not** the 'y' filter on the List of Contexts named 'fred' (as fred.y is a valid name).
| However (fred).y is the 'y' filter on the List of Contexts named fred.

Assignment and Variable names
-----------------------------
There's one extension - an assignment operator (<-) which will store a Python internal value against a named variable.
Named variables are valid in S-FEEL expressions in pySFeel.

    fred <- 7
    bill <- 9
    fred = bill

This will return False

    fred <- [{x:1,y:2},{x:2,y:3}]
    (fred).y

This will return [2,3]

Usage
-----

::

    import pySFeel
    parser = pySFeel.SFeelParser()
    sfeelText = '7.3 in [2.0 .. 9.1]'
    (status, retVal) = parser.sFeelParse(sfeelText)
    if 'errors' in status:
        print('With errors:', status['errors'])

- retVal will be True
- The dictonary 'status' will have the key 'errors' if you have errors in your sfeelText.
- status['errors'] is a list of strings. It may help in diagnosing your S-FEEL syntax errors.

Built-in Functions
------------------
pySFeel has support all the standard FEEL built-in functions [except sort()] with some differences because pySFeel is a Python implementation.

+-------------------------------+---------------------+---------------------------------------------------------------+
| Name(paramters)               | Parameter Domain    | pySFeel implementation notes                                  |
+===============================+=====================+===============================================================+
| date(from)                    | date string         | Uses dateutil.parser - strict ISO format is not required.     |
|                               |                     | pySFeel will convert a string that is in ISO format into      |
|                               |                     | a datetime.date, datetime.time or datetime.datetime           |
+-------------------------------+---------------------+---------------------------------------------------------------+
| date(from)                    | date and time       | Truncates datetime.datetime to datetime.date                  |
+-------------------------------+---------------------+---------------------------------------------------------------+
| date(year,month,day)          | year,month,day      |                                                               |
|                               | are numbers         |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| date and time(date,time)      | date is a date or   |                                                               |
|                               | date time; time is  |                                                               |
|                               | a time              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| date and time(from)           | date time string    | Uses dateutil.parser - strict ISO format is not required.     |
|                               |                     | pySFeel will convert a string that is in ISO format into      |
|                               |                     | a datetime.date, datetime.time or datetime.datetime           |
+-------------------------------+---------------------+---------------------------------------------------------------+
| time(from)                    | time string         | Uses dateutil.parser - strict ISO format is not required.     |
|                               |                     | pySFeel will convert a string that is in ISO format into      |
|                               |                     | a datetime.date, datetime.time or datetime.datetime           |
+-------------------------------+---------------------+---------------------------------------------------------------+
| time(from)                    | time, date and time |                                                               |
|                               |                     |                                                               |
|                               |                     |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| number(from,grouping,         | string,string,      | pySFeel does the approriate rounding, but the returned value  |
| separator,decimal separator)  | string              | is a float. Trailing zeros are not retained.                  |
+-------------------------------+---------------------+---------------------------------------------------------------+
| string(from)                  | non null            |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| duration(from)                | duration string     |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| years and months              | both are date or    |                                                               |
| duration(from, to)            | both are date and   |                                                               |
|                               | time                |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| not(negand)                   | boolean             |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| substring(string,start,       | string,number       |                                                               |
| position,length?)             |                     |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| string length(string)         | string              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| upper case(string)            | string              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| lower case(string)            | string              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| substring before              | string,string       |                                                               |
| (string,match)                |                     |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| substring after               | string,string       |                                                               |
| (string,match)                |                     |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| replace(input,pattern,        | string              |                                                               |
| replacement,flags?)           |                     |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| contains(string,match)        | string              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| starts with(string,match)     | string              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| ends with(string,match)       | string              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| matches(input,pattern,        | string              |                                                               |
| flags?)                       |                     |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| split(string,delimiter)       | string              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| list contains(list,element)   | list,any element of |                                                               |
|                               | the semantic domain |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| count(list)                   | list                |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| min(list)                     | non-empty list of   |                                                               |
| min(C1,...,Cn),N>0            | comparable items    |                                                               |
| max(list)                     | or argument list of |                                                               |
| max(C1,...,Cn),N>0            | one or more         |                                                               |
|                               | comparable items    |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| sum(list)                     | list of 0 or more   |                                                               |
| sum(N1,...,Nn),N>0            | numbers or          |                                                               |
|                               | argument list of    |                                                               |
|                               | one or more numbers |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| mean(list)                    | non-empty list of   |                                                               |
| mean(N1,...,Nn),N>0           | numbers or          |                                                               |
|                               | argument list of    |                                                               |
|                               | one or more numbers |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| all(list)                     | list of Boolean     |                                                               |
| all(B1,...,Bn),N>0            | items of argument   |                                                               |
|                               | list of one or more |                                                               |
|                               | Boolean items       |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| any(list)                     | list of Boolean     |                                                               |
| any(B1,...,Bn),N>0            | items of argument   |                                                               |
|                               | list of one or more |                                                               |
|                               | Boolean items       |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| sublist(list,start position,  | list,number,        |                                                               |
| length?)                      | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| append(list,item...)          | list,any element    |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| concatenate(list...)          | list                |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| insert before(list,position,  | list,number,any     |                                                               |
| newItem)                      | element             |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| remove(list,position)         | list,number         |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| reverse(list)                 | list                |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| index of(list,match)          | list,any element    |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| union(list,...)               | list                |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| distinct values(list)         | list                |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| flattern(list)                | list                |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| product(list)                 | list is a list of   |                                                               |
| product(N1,...,Nn)            | numbers. N1..Nn     |                                                               |
|                               | are numbers         |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| median(list)                  | list is a list of   |                                                               |
| median(N1,...,Nn)             | numbers. N1..Nn     |                                                               |
|                               | are numbers         |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| stddev(list)                  | list is a list of   |                                                               |
| stddev(N1,...,Nn)             | numbers. N1..Nn     |                                                               |
|                               | are numbers         |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| mode(list)                    | list is a list of   |                                                               |
| mode(N1,...,Nn)               | numbers. N1..Nn     |                                                               |
|                               | are numbers         |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| deciman(n,scale)              | number,number       | pySFeel does the approriate rounding, but the returned value  |
|                               |                     | is a float. Trailing zeros are not retained.                  |
+-------------------------------+---------------------+---------------------------------------------------------------+
| floor(n)                      | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| ceiling(n)                    | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| abs(n)                        | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| modulo(dividend,divisor)      | number,number       |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| sqrt(n)                       | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| log(n)                        | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| exp(n)                        | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| odd(n)                        | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| even(n)                       | number              |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| is(expr, expr)                | expr, expr          |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| before(range, range)          | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| after(range, range)           | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| meets(range, range)           | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| met by(range, range)          | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| overlaps(range, range)        | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| overlaps before(range, range) | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| overlaps after(range, range)  | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| finishes(range, range)        | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| finished by(range, range)     | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| includes(range, range)        | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| during(range, range)          | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| starts(range, range)          | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| started by(range, range       | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| coincides(range, range)       | range, range        |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| day of year(date)             | date, date and time |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| day of week(date)             | date, date and time |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| month of year(date)           | date, date and time |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| week of year(date)            | date, date and time |                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+
| sort(list, function(x,y) expr)+ list                +                                                               |
+-------------------------------+---------------------+---------------------------------------------------------------+

**Note:** The support for the sort() function is very, very limited. Only the anonymous form is supported (function is defined within the sort call).
Also, 'expr' is limited to 'name0 < name1' or 'name0 > name1' (ascending or decending). However, list can be a list of Contexts, in which case
name0 and name1 must be 'name0.attr' and 'name1.attr' and 'attr' must be the same attribute for both 'name0' and 'name1'.

**Note:** The support for 'some/every in ... satifies expression' is also limited in that 'expression' must be 'name relop expr'.
Again, the 'name.attr' form is suported where a list of Contexts is being tested.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
