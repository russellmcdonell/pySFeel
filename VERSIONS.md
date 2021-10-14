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

