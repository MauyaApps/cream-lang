# Cream Standard Library

All 450+ built-in operations. Commands marked with * accept multiple operations as second argument.

---

## Output & Input

```cream
say "Hello!"                    -- print to console
say value                       -- print any value
x = input("Enter name: ")       -- read from console
print_("Hello", "color", "red") -- colored output
print_("Hello", "bold")         -- bold output
print_("line")                  -- print separator line
```

---

## Math *

```cream
math(x)                    -- return x
math(x, "sqrt")            -- square root
math(x, "pow", n)          -- x to the power of n
math(x, "log")             -- natural logarithm
math(x, "log", base)       -- log with base
math(x, "log2")            -- log base 2
math(x, "log10")           -- log base 10
math(x, "sin")             -- sine (degrees)
math(x, "cos")             -- cosine (degrees)
math(x, "tan")             -- tangent (degrees)
math(x, "asin")            -- arc sine
math(x, "acos")            -- arc cosine
math(x, "atan")            -- arc tangent
math(x, "floor")           -- round down
math(x, "ceil")            -- round up
math(x, "round")           -- round to nearest
math(x, "round", n)        -- round to n decimal places
math(x, "abs")             -- absolute value
math(x, "factorial")       -- factorial of x
math(x, "gcd", y)          -- greatest common divisor
math(x, "lcm", y)          -- least common multiple
math(x, "prime")           -- is x a prime number?
math(x, "digits")          -- list of digits
math(x, "binary")          -- binary string
math(x, "hex")             -- hex string
math(x, "octal")           -- octal string
math(x, "clamp", min, max) -- clamp value to range
math(x, "sign")            -- -1, 0, or 1
math(x, "percent", total)  -- x as % of total
```

**Constants:** `PI`, `E`, `INF`

---

## Numbers *

```cream
num(x)                    -- convert to number
num(x, "int")             -- convert to integer
num(x, "float")           -- convert to float
num(x, "is")              -- is x a valid number?
num(x, "between", a, b)   -- a <= x <= b?
num(x, "format", n)       -- format to n decimal places
num(x, "positive")        -- x > 0?
num(x, "negative")        -- x < 0?
num(x, "zero")            -- x == 0?
num(x, "even")            -- x is even?
num(x, "odd")             -- x is odd?
```

---

## Random *

```cream
rand()                    -- random float 0.0 – 1.0
rand(n)                   -- random int 0 – n
rand(a, b)                -- random int a – b
rand(list)                -- random element from list
rand("dice")              -- random 1 – 6
rand("dice", n)           -- random 1 – n
rand("coin")              -- yes or no
rand("uuid")              -- unique ID string
rand("list", lst)         -- random element
rand("shuffle", lst)      -- shuffled list
rand("sample", lst, n)    -- n random elements
```

---

## Statistics *

```cream
stats(lst)                -- table with all metrics
stats(lst, "mean")        -- average
stats(lst, "median")      -- median value
stats(lst, "mode")        -- most common value
stats(lst, "std")         -- standard deviation
stats(lst, "variance")    -- variance
stats(lst, "min")         -- minimum
stats(lst, "max")         -- maximum
stats(lst, "sum")         -- sum
stats(lst, "count")       -- count
stats(lst, "range")       -- max - min
stats(lst, "unique")      -- deduplicated list
stats(lst, "freq")        -- frequency table
```

---

## Convert *

```cream
convert(x, "km",    "miles")   -- kilometers to miles
convert(x, "miles", "km")
convert(x, "m",     "ft")      -- meters to feet
convert(x, "kg",    "lbs")     -- kilograms to pounds
convert(x, "g",     "kg")
convert(x, "c",     "f")       -- Celsius to Fahrenheit
convert(x, "f",     "c")
convert(x, "c",     "k")       -- Celsius to Kelvin
convert(x, "bytes", "kb")      -- bytes to kilobytes
convert(x, "bytes", "mb")
convert(x, "bytes", "gb")
convert(x, "kb",    "mb")
convert(x, "mb",    "gb")
convert(x, "deg",   "rad")     -- degrees to radians
convert(x, "rad",   "deg")
convert(x, "hours", "min")
convert(x, "min",   "sec")
convert(x, "hours", "sec")
```

---

## Strings *

```cream
str_(x)                         -- convert to string
str_(x, "upper")                -- UPPERCASE
str_(x, "lower")                -- lowercase
str_(x, "title")                -- Title Case
str_(x, "capitalize")           -- Capitalize first
str_(x, "trim")                 -- remove spaces
str_(x, "trim", "left")         -- remove left spaces
str_(x, "trim", "right")        -- remove right spaces
str_(x, "replace", a, b)        -- replace a with b
str_(x, "remove", s)            -- remove substring
str_(x, "split", sep)           -- split into list
str_(x, "join", list)           -- join list with x
str_(x, "contains", s)          -- contains substring?
str_(x, "starts", s)            -- starts with s?
str_(x, "ends", s)              -- ends with s?
str_(x, "count", s)             -- count occurrences
str_(x, "index", s)             -- position of s
str_(x, "slice", a, b)          -- substring from a to b
str_(x, "repeat", n)            -- repeat n times
str_(x, "reverse")              -- reverse string
str_(x, "length")               -- string length
str_(x, "words")                -- list of words
str_(x, "lines")                -- list of lines
str_(x, "chars")                -- list of characters
str_(x, "pad", n)               -- pad right to length n
str_(x, "pad", n, "left")       -- pad left
str_(x, "pad", n, "both")       -- center
str_(x, "is_num")               -- is numeric?
str_(x, "is_alpha")             -- is alphabetic?
str_(x, "is_empty")             -- is empty/whitespace?
str_(x, "between", a, b)        -- text between a and b
str_(x, "match", pattern)       -- first regex match
str_(x, "match_all", pattern)   -- all regex matches
```

---

## Text *

```cream
text_(x)                        -- convert to string
text_(x, "clean")               -- remove special chars
text_(x, "words")               -- word count
text_(x, "sentences")           -- split into sentences
text_(x, "truncate", n)         -- truncate to n chars
text_(x, "truncate", n, "...")  -- truncate with suffix
text_(x, "slug")                -- URL-friendly slug
text_(x, "ascii")               -- ASCII chars only
text_(x, "palindrome")          -- is palindrome?
text_(x, "anagram", y)          -- are anagrams?
text_(x, "distance", y)         -- Levenshtein distance
text_(x, "similarity", y)       -- similarity 0.0 – 1.0
text_(x, "extract", "emails")   -- find all emails
text_(x, "extract", "urls")     -- find all URLs
text_(x, "extract", "numbers")  -- find all numbers
text_(x, "extract", "hashtags") -- find all #hashtags
text_(x, "extract", "mentions") -- find all @mentions
```

---

## Regex *

```cream
regex(pattern, text)              -- first match
regex(pattern, text, "all")       -- all matches
regex(pattern, text, "test")      -- matches? yes/no
regex(pattern, text, "replace", r) -- replace matches
regex(pattern, text, "split")     -- split by pattern
regex(pattern, text, "groups")    -- capture groups
regex(pattern, text, "count")     -- count matches
```

---

## Lists *

```cream
list(lst)                     -- copy list
list(lst, "add", x)           -- append element
list(lst, "remove", x)        -- remove first x
list(lst, "pop")              -- remove last element
list(lst, "pop", i)           -- remove at index i
list(lst, "insert", i, x)     -- insert at index
list(lst, "has", x)           -- contains x?
list(lst, "index", x)         -- index of x (-1 if not found)
list(lst, "count", x)         -- count occurrences of x
list(lst, "slice", a, b)      -- sublist from a to b
list(lst, "flat")             -- flatten nested lists
list(lst, "zip", lst2)        -- pair elements
list(lst, "chunk", n)         -- split into chunks of n
list(lst, "unique")           -- remove duplicates
list(a,   "concat", b)        -- join two lists
list(lst, "reverse")          -- reverse
list(lst, "sort")             -- sort ascending
list(lst, "shuffle")          -- random order
list(lst, "sum")              -- sum
list(lst, "min")              -- minimum
list(lst, "max")              -- maximum
list(lst, "first")            -- first element
list(lst, "last")             -- last element
list(lst, "empty")            -- is empty?
list(lst, "fill", n, val)     -- list of n copies of val
```

---

## Tables *

```cream
table(t)                      -- copy table
table(t, "get", key)          -- get value by key
table(t, "set", key, val)     -- set value
table(t, "has", key)          -- has key?
table(t, "delete", key)       -- remove key
table(t, "keys")              -- list of keys
table(t, "values")            -- list of values
table(t, "merge", t2)         -- merge two tables
table(t, "size")              -- number of keys
table(t, "empty")             -- is empty?
table(t, "to_list")           -- convert to [[k,v], ...]
```

---

## Files *

```cream
file(path)                    -- read file as text
file(path, content)           -- write text to file
file(path, "append", text)    -- append to file
file(path, "delete")          -- delete file
file(path, "exists")          -- file exists?
file(path, "size")            -- file size in bytes
file(path, "copy", dest)      -- copy to destination
file(path, "move", dest)      -- move to destination
file(path, "rename", newname) -- rename file
file(path, "lines")           -- read as list of lines
file(path, "json")            -- read and parse JSON
file(path, "json", data)      -- write data as JSON
file(path, "csv")             -- read CSV as list
file(path, "csv", data)       -- write list as CSV
file(path, "ext")             -- file extension
file(path, "name")            -- filename
file(path, "dir")             -- directory path
file(path, "info")            -- file metadata table
```

---

## Folders *

```cream
folder(path)                  -- list files in folder
folder("current")             -- current working directory
folder("home")                -- home directory
folder(path, "create")        -- create folder
folder(path, "delete")        -- delete folder
folder(path, "exists")        -- folder exists?
folder(path, "copy", dest)    -- copy folder
folder(path, "move", dest)    -- move folder
folder(path, "find", "*.txt") -- find files by pattern
folder(path, "files")         -- list files only
folder(path, "folders")       -- list subfolders only
```

---

## System *

```cream
sys_("os")                    -- operating system name
sys_("cwd")                   -- current directory
sys_("cd", path)              -- change directory
sys_("args")                  -- command line arguments
sys_("env", name)             -- get env variable
sys_("env", name, value)      -- set env variable
sys_("run", command)          -- run shell command
sys_("sleep", seconds)        -- pause execution
sys_("time")                  -- current unix timestamp
sys_("cpu")                   -- CPU core count
sys_("exit")                  -- exit program
sys_("exit", code)            -- exit with code
```

---

## Encode *

```cream
encode(x, "base64")           -- encode to base64
encode(x, "base64", "decode") -- decode base64
encode(x, "md5")              -- MD5 hash
encode(x, "sha256")           -- SHA-256 hash
encode(x, "sha1")             -- SHA-1 hash
encode(x, "url")              -- URL encode
encode(x, "url", "decode")    -- URL decode
encode(x, "json")             -- serialize to JSON string
encode(x, "json", "decode")   -- parse JSON string
encode(x, "hex")              -- hex string
```

---

## Network *

```cream
net(url)                      -- GET request → text
net(url, "get")               -- GET request → text
net(url, "json")              -- GET → parsed table
net(url, "post", data)        -- POST with form data
net(url, "post_json", data)   -- POST with JSON body
net(url, "put", data)         -- PUT request
net(url, "delete")            -- DELETE request
net(url, "status")            -- HTTP status code
net(url, "head")              -- response headers table
net(url, "download", path)    -- download file to disk
net(url, "headers", headers)  -- GET with custom headers
net("ip")                     -- my public IP address
net("encode", params)         -- URL-encode parameters
```

---

## Date & Time *

```cream
date()                        -- table: year/month/day/hour/minute/second
date("now")                   -- same as date()
date("today")                 -- "2026-03-19"
date("time")                  -- "14:30:00"
date("timestamp")             -- unix timestamp integer
date("format", "%d/%m/%Y")    -- custom format string
```

---

## Basic Utilities

```cream
length(x)          -- length of list or string
sum(lst)           -- sum of list
min(lst)           -- minimum value
max(lst)           -- maximum value
abs(x)             -- absolute value
round(x, n)        -- round to n decimal places
range(from, to)    -- list of integers
sort(lst)          -- sorted list
reverse(lst)       -- reversed list
first(lst)         -- first element
last(lst)          -- last element
join(lst, sep)     -- join list to string
split(x, sep)      -- split string to list
upper(x)           -- UPPERCASE
lower(x)           -- lowercase
trim(x)            -- strip whitespace
contains(x, s)     -- contains substring?
number(x)          -- convert to number
text(x)            -- convert to string
bool(x)            -- convert to boolean
```
