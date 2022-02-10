# Text - Text - Text

## **Overview**

There are a lot of data that exists in text types. For example:

a) Text in legal documents

b) Text in analysis investment brochure

c) Text in transaction billings

d) Text in scanned trading registed documents

And so on, ...

Its in differents kind of storage but its has a lot of information that 
we can parse it into data and give us a various general inforamtion.
And if we can put into a system, it like a charm.
## **Transformation**

### Transform types of sources

In the examples, you can see text that appear in various, from dirty spaces to very useful way.

E.g:

PDF types to Text

PNG types to Text

Online Newspaper types is something go to text

### Extract information of data

1. **Text to number**


| Example | Target | Information |
|----|----|----|
| This is increased 40 percentage revenue | 40% | Positive, for revenue |
| There are has 3 types of flowers | 3 | Category, Number of class |

So its has a pattern for this

```py
import re

patterns = re.match("\d+|0123456789|\d+\,\d+")
```

2. **Text to Date**


3. **Text Padding**


## **Libraries**

## **Source Referrences**
