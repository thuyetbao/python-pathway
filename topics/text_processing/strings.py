import string
from string import Template
import datetime

# `string` library has 4 main 
# a) Built-in variables
# b) Custom String Format
# c) Template

# A. BUILT-IN VARIABLE

# What is ASCII:
# Shortcut of American Standard Code for Information Interchange
# Its is a character encoding standard for electronic communication. 
# ASCII codes represent text in computers, telecommunications equipment, and other devices
# Read more: [ASCII](https://en.wikipedia.org/wiki/ASCII)

# Built in variables with self-explain name
# Seperated into 3 groups: letters, digits, punctation and whitespace 
# Special case contain 4 group is `printable`.
# This support to reduce memory to remember all of this together
# and very helpful in text analysis.

# Group 1:
string.ascii_letters
string.ascii_lowercase
string.ascii_uppercase

# Group 2:
string.digits
string.hexdigits
string.octdigits

# Group 3:
string.punctuation

# Group 4:
string.whitespace

# Contain 4 groups:
string.printable

# B. CUSTOM FORMAT

# Type 1: Index based with exists index or not (upper 3.1+)
# Normal Case
'{0}, {1}, {2}'.format('a', 'b', 'c')
# Index Position
'{2}, {1}, {0}'.format('a', 'b', 'c')
# Auto index without using index
'{}, {}, {}'.format('a', 'b', 'c')
# Unpacking using *
'{0}, {1}, {2}'.format(*'abc')
# Repeat
'{0}, {1}, {0}'.format('F', 'S')

# Type 2: Naming arguments
# Normal case
'Coordinates: {lat}, {lon}'.format(lat = '24.7N', lon='-12.4E')
# Unpack dict using **
coord = {'lat': '24.7N', 'lon':'-12.4E'}
'Coordinates: {lat}, {lon}'.format(**coord) 

# Standard Format Specifier:
# format_spec     ::=  [[fill]align][sign][#][0][width][grouping_option][.precision][type]
# fill            ::=  <any character>
# align           ::=  "<" | ">" | "=" | "^"
# sign            ::=  "+" | "-" | " "
# width           ::=  digit+
# grouping_option ::=  "_" | ","
# precision       ::=  digit+
# type            ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "

# Fill and Align
# Case 1: Fill * and align with > (Left)
# E.g: '*****************************************************Tunnels'
'{:*>60}'.format('Tunnels')

# Case 2: Fill ~ and align with ^ (Middle)
# E.g: '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Python Pathway~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
'{:~^80}'.format('Python Pathway')

# Case 3: 
# E.g: Number with positive and negative number
'{:+f}; {:+f}'.format(4.6, -12.14)
'{: f}; {: f}'.format(3.14, -3.14)
'{:-f}; {:-f}'.format(5.94, -9.14)

# Case 4:
# E.g: Format Number in different alias
'int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}'.format(93)

# Case 5: With 0x, 0o, or 0b as prefix
# E.g: Such as hex and oct type
'int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}'.format(47)

# Case 6: Using the comma as a thousands separator
# E.g: 1234 into 1,234
'{:,}'.format(1234)
'{:_}'.format(123456)

# Case 7: Percentage with number of precisions
'{:.3%}'.format(0.05821)

# C. TEMPLATE

# Template strings support $-based substitutions, using the following rules:
# ====
# $$ is an escape; it is replaced with a single $.
# $identifier names a substitution placeholder matching a mapping key of "identifier". By default, "identifier" is restricted to any case-insensitive ASCII alphanumeric string (including underscores) that starts with an underscore or ASCII letter. The first non-identifier character after the $ character terminates this placeholder specification.
# ${identifier} is equivalent to $identifier. It is required when valid identifier characters follow the placeholder but are not part of the placeholder, such as "${noun}ification".
# Any other appearance of $ in the string will result in a ValueError being raised.

# Basic concept
# 2 steps:
# a) Define template through Template
# b) Binding argument with `substitute`

# Template
s = Template("$user has been reviewed by $reviewer at $time")

# Binding
s.substitute(user="Pja", reviewer="Sungri", time=datetime.datetime.now())

# KeyError when:
# Mising $time
s.substitute(user="Pja", reviewer="Sungri")

# Not err when using safe_subtitule
# Its replace missing arguments by itself
s.safe_substitute(user="Pja", reviewer="Sungri")

# D. HELPFUL FUNCTIONS

# In my opinions, it not help much. 
# But i like this idea, using multiple resources like split, capitalize then join of `str` library
string.capwords("Capitalize Word by seperator", sep=" ")
