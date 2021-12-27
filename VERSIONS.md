### 1.3.2 - Changed Year, month duration
* Year, month durations are now represented internally as 'int' - giving them their own data type  
(required to make is() function work correctly. Also tightens up validation of expressions involving year and month durations, some of which were incorrectly allowed)
* Implemented x.name for attributes of dates/datetimes/times/durations/ranges.  
NOTE: For the attributes 'time offset', 'start included' and 'end included' the names need to be enclosed in (); space is not a valid character in a name/attribute 
if fred is a range then (fred).start included will return True if the start of the range is included in the range.  
However, fred.start included will generate a syntax error at 'included', as 'fred.start' is a valid variable name.
### 1.3.1 - Added DMN 1.3 functions
* Fixed bug in string(duration)
* Fixed bugs in date and duration arithmatic
* Fixed bug in floor and ceil functions
### 1.2.1 - Fixed bug in in() function
### 1.2.0 - First candidate for a production release
* fixed addition and subtraction of durations
* removed addition of Contexts [not defined in DMN and non-commutative, result depended upon order of Contexts]
* fixed an issue with slicing
* this complete the development of pySFeel for DMN 1.2
### 0.1.11 - This is a bug fix release.
* fixed 'false and otherwise' - now returns False
* fixed 'otherwise and false' - now return False
* fixed 'in' a list of ranges
* fixed substring() function - returning wrong string
* fixed substring before() function when there is no match
* fixed replace - different 're' syntax for replacement groups
* fixed count - thank you Gabriel Galibourg ([g6g8](https://github.com/g6g8))
* fixed bug with the parser not recognizing empty lists
* fixed bug with lists within lists
* fixed bug with all() function - thank you Gabriel Galibourg ([g6g8](https://github.com/g6g8))
* fixed bug with any() function
* fixed bug in sublist() function where the start was 1
* fixed bug in flatten() function
* fixed product() function - for parameters as well as list
* fixed sort order in mode() function for multiple returned values
* fixed decimal() function so that decimal(1.5, 0) == decimal(2.5, 0) == 2
* fixed list select - thank you Gabriel Galibourg ([g6g8](https://github.com/g6g8))
* fixed list select [item=x] - thank you Gabriel Galibourg ([g6g8](https://github.com/g6g8))
* fixed date(), time() and data and time() functions - incorrect differenciaton between dates and datetimes
* added date/time addition and subtraction
* fixed number() function where 'number' is null - thank you Gabriel Galibourg ([g6g8](https://github.com/g6g8))
* added lots of pytest tests
### 0.1.10 - the first release

