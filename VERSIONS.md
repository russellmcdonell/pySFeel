### 1.4.0 - BREAKING Bug fix release - released to PyPI
 - Changed parsing so that ranges with closed intervals are returned with round brackets    
   (reverse facing square brackets are allowed on input, but will be converted to their equivalent round bracket form)    
   **NOTE BREAKING CHANGE:** this effected some of the tests in test_pySFeel.py
 - Fixed equality test - now returns 'null' (Python value None) if values are of different data types    
   **NOTE BREAKING CHANGE:** this may effected some existing tests
 - Bug fix - string() function now returns timezones for datetimes/time that have a timezone
   **NOTE BREAKING CHANGE:** this may effected some existing implementations
 - Bug fix - .weekday now returns isoweekday() (now 1 - 7, was 0 - 6)
   **NOTE BREAKING CHANGE:** this may effected some existing implementations
 - Bug fix - any()/all() functions return False/True for empty lists.
 - Bug fix - Context filters were expecting '[item x=1]'. Correct syntax is '[item.x=1]'. Old syntax supported for backward compatibility.
 - Bug fix - fixed regex pattern for year and month durations (when months is missing)
 - Fixed bug - strings were not being recognised as valid names in Contexts
 - Added support fo single endpoint and operator ranges
 - Added singleton list conversions for parameters passed to built-in functions
 - Fix list indexing bugs ([true] returns full list, [-n] returns item from end of list)
 - Added support for 'instance of'
 - Improved the parsing of year month and date time durations
 - Added support for named parameters in built-in functions
 - Added support for context scoped variables - {a:1,b:a+1} - 'a' is a valid variable, but only inside the context and only after it has been defined.
 - Added support for Java like comments (// to end of line, /* .. */)
 - Added support for DMN 1.4 functions today() and now()
### 1.3.10 - Added limited support for the sort() function - released to PyPI
 - Added limited support for the sort() function - only the anonymous form [ sort(expr, function(name0, name1) expression)) ]. And 'expression' is limited to 'name0 < name1' or 'name0 > name1'. If the list to be sorted ('expr) is a list of Contexts, the name0 and name1 must take the form of name0.attr and name1.attr, and 'attr' must be the same attribute for both name0 and name1.
### 1.3.9 - Fixed bugs found when testing with tck-DMN - released to PyPI
 - Fixed bug - numbers beginning with a period were not being parses as numbers
 - Modified string() function to return str() of an int() when expr was a whole number
 - Modified replace() function to emulate Java regular expression behaviour (the FEEL standard)
 - Fixed bug - variable names, matching words in function names, corrupted FEEL expressions
 - Fixed bug - time functions were not supporting decimal seconds (microseconds)
 - Fixed bug in concatenate() function
 - Fixed insert() and remove() functions - now returns copy() - doesn't modify source
 - Fixed bug - negative start position in substring() function
 - Made 'item' optional in List filters
 - Added limited support for 'some/every in ... satifies expression'. 'expression' must be 'name relop expr'.
 - Fixed bug in math() - wrapped try/except for math failures - e.g. sqrt(-1.0)
### 1.3.8 - Fixed Feb 29 bug - released to PyPI
 - Addition and subtraction of years from a valid leap year date would fail
### 1.3.7 - Bug fix - released to PyPI
* Made arithmetic operators invalid in names
### 1.3.6 - Another minor bug fix
* Fixed typo in .days attribute of a data/time durations
* Fixed priority bug for .day/.days etc.
* Fixed workaround implemented in version 1.3.2 for 'start included', 'end included' and 'time offset'. Underscore nolonger required for these attributes.
### 1.3.5 - A minor bug fix release - released to PyPI
* Tightened up is() function to disallow comparisions of ranges, Lists and Contexts
* Fixed but in overlaps after() function when we have matching end points
### 1.3.4 - A build for release to PyPI
### 1.3.3 - Implemented support for @region/location timezones
* Implemented support for string literals (@"xx")  
a string literal of a Years, months duration will return an int (@"P2Y3M" == 27)  
a string litteral of a Days, time duration will return a datetime.timedelta (@"P2DT15H12M" == 2 day, 15:12:00)
### 1.3.2 - Changed Year, month duration
* Year, month durations are now represented internally as 'int' - giving them their own data type  
(required to make is() function work correctly. Also tightens up validation of expressions involving year and month durations, some of which were incorrectly allowed)
* Implemented x.name for attributes of dates/datetimes/times/durations/ranges.  
NOTE: For the attributes 'time offset', 'start included' and 'end included' the names need to be enclosed in (); space is not a valid character in a name/attribute 
    - If fred is a range then (fred).start included will return True if the start of the range is included in the range.  
    - However, fred.start included will generate a syntax error at 'included', as 'fred.start' is a valid variable name.    
    NOTE: start_included, end_included and time_offset have been implemented as equivalent attributes.    
If fred is a range then fred.start_included will return True if the start of the range is included in the range.  
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

