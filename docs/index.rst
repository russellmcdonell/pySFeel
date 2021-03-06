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

+--------------------------+-------------------------+
|     S-Feel data type     | Python native data type |
+==========================+=========================+
|         number           |         float           |
+--------------------------+-------------------------+
|         string           |          str            |
+--------------------------+-------------------------+
|        boolean           |         bool            |
+--------------------------+-------------------------+
|  days and time duration  |   datetime.timedelta    |
+--------------------------+-------------------------+
| year and months duration |         float           |
+--------------------------+-------------------------+
|        time              |     datetime.time       |
+--------------------------+-------------------------+
|        date              |     datetime.date       |
+--------------------------+-------------------------+
|   date and time          |   datetime.datetime     |
+--------------------------+-------------------------+
|        List              |         list            |
+--------------------------+-------------------------+
|      Context             |         dict            |
+--------------------------+-------------------------+



List and Context Filters
------------------------
pySFeel supports List and Context filters with one deliberate deviation from the standard - the key word 'item' in a Context filters is **not** optional.

| [{x:1,y:2},{x:2,y:3}][x=1] is not valid (as x=1 is either True or False)
| [{x:1,y:2},{x:2,y:3}][item x=1] is valid and will return {x:1,y:2}.

| Similarly, fred.y is **not** the 'y' filter on the List of Contexts named 'fred' (as fred.y is a valid name).
| However (fred).y is the 'y' filter on the list of Contexts named fred.

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
pySFeel has support all the standard FEEL built-in functions with some differences because if is a Python implementation.

+------------------------------+---------------------+---------------------------------------------------------------+
| Name(paramters)              | Parameter Domain    | pySFeel implementation notes                                  |
+==============================+=====================+===============================================================+
| date(from)                   | date string         | Uses dateutil.parser - strict ISO format is not required.     |
|                              |                     | pySFeel will convert a string that is in ISO format into      |
|                              |                     | a datetime.date, datetime.time or datetime.datetime           |
+------------------------------+---------------------+---------------------------------------------------------------+
| date(from)                   | date and time       | Truncates datetime.datetime to datetime.date                  |
+------------------------------+---------------------+---------------------------------------------------------------+
| date(year,month,day)         | year,month,day      |                                                               |
|                              | are numbers         |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| date and time(date,time)     | date is a date or   |                                                               |
|                              | date time; time is  |                                                               |
|                              | a time              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| date and time(from)          | date time string    | Uses dateutil.parser - strict ISO format is not required.     |
|                              |                     | pySFeel will convert a string that is in ISO format into      |
|                              |                     | a datetime.date, datetime.time or datetime.datetime           |
+------------------------------+---------------------+---------------------------------------------------------------+
| time(from)                   | time string         | Uses dateutil.parser - strict ISO format is not required.     |
|                              |                     | pySFeel will convert a string that is in ISO format into      |
|                              |                     | a datetime.date, datetime.time or datetime.datetime           |
+------------------------------+---------------------+---------------------------------------------------------------+
| time(from)                   | time, date and time |                                                               |
|                              |                     |                                                               |
|                              |                     |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| number(from,grouping,        | string,string,      | pySFeel does the approriate rounding, but the returned value  |
| separator,decimal separator) | string              | is a float. Trailing zeros are not retained.                  |
+------------------------------+---------------------+---------------------------------------------------------------+
| string(from)                 | non null            |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| duration(from)               | duration string     |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| years and months             | both are date or    |                                                               |
| duration(from, to)           | both are date and   |                                                               |
|                              | time                |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| not(negand)                  | boolean             |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| substring(string,start,      | string,number       |                                                               |
| position,length?)            |                     |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| string length(string)        | string              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| upper case(string)           | string              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| lower case(string)           | string              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| substring before             | string,string       |                                                               |
| (string,match)               |                     |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| substring after              | string,string       |                                                               |
| (string,match)               |                     |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| replace(input,pattern,       | string              |                                                               |
| replacement,flags?)          |                     |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| contains(string,match)       | string              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| starts with(string,match)    | string              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| ends with(string,match)      | string              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| matches(input,pattern,       | string              |                                                               |
| flags?)                      |                     |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| split(string,delimiter)      | string              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| list contains(list,element)  | list,any element of |                                                               |
|                              | the semantic domain |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| count(list)                  | list                |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| min(list)                    | non-empty list of   |                                                               |
| min(C1,...,Cn),N>0           | comparable items    |                                                               |
| max(list)                    | or argument list of |                                                               |
| max(C1,...,Cn),N>0           | one or more         |                                                               |
|                              | comparable items    |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| sum(list)                    | list of 0 or more   |                                                               |
| sum(N1,...,Nn),N>0           | numbers or          |                                                               |
|                              | argument list of    |                                                               |
|                              | one or more numbers |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| mean(list)                   | non-empty list of   |                                                               |
| mean(N1,...,Nn),N>0          | numbers or          |                                                               |
|                              | argument list of    |                                                               |
|                              | one or more numbers |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| all(list)                    | list of Boolean     |                                                               |
| all(B1,...,Bn),N>0           | items of argument   |                                                               |
|                              | list of one or more |                                                               |
|                              | Boolean items       |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| any(list)                    | list of Boolean     |                                                               |
| any(B1,...,Bn),N>0           | items of argument   |                                                               |
|                              | list of one or more |                                                               |
|                              | Boolean items       |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| sublist(list,start position, | list,number,        |                                                               |
| length?)                     | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| append(list,item...)         | list,any element    |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| concatenate(list...)         | list                |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| insert before(list,position, | list,number,any     |                                                               |
| newItem)                     | element             |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| remove(list,position)        | list,number         |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| reverse(list)                | list                |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| index of(list,match)         | list,any element    |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| union(list,...)              | list                |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| distinct values(list)        | list                |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| flattern(list)               | list                |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| product(list)                | list is a list of   |                                                               |
| product(N1,...,Nn)           | numbers. N1..Nn     |                                                               |
|                              | are numbers         |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| median(list)                 | list is a list of   |                                                               |
| median(N1,...,Nn)            | numbers. N1..Nn     |                                                               |
|                              | are numbers         |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| stddev(list)                 | list is a list of   |                                                               |
| stddev(N1,...,Nn)            | numbers. N1..Nn     |                                                               |
|                              | are numbers         |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| mode(list)                   | list is a list of   |                                                               |
| mode(N1,...,Nn)              | numbers. N1..Nn     |                                                               |
|                              | are numbers         |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| deciman(n,scale)             | number,number       | pySFeel does the approriate rounding, but the returned value  |
|                              |                     | is a float. Trailing zeros are not retained.                  |
+------------------------------+---------------------+---------------------------------------------------------------+
| floor(n)                     | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| ceiling(n)                   | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| abs(n)                       | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| modulo(dividend,divisor)     | number,number       |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| sqrt(n)                      | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| log(n)                       | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| exp(n)                       | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| odd(n)                       | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+
| even(n)                      | number              |                                                               |
+------------------------------+---------------------+---------------------------------------------------------------+



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
