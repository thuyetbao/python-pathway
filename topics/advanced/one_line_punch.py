# Target
# 
# Description:
# Created date range since base (e.g: today) within a number of date range
# 
# Type: Snapshot code
# Source: https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python
import datetime

date_list = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)]

# IF-ELSE
# https://stackoverflow.com/questions/2802726/putting-a-simple-if-then-else-statement-on-one-line

'Yes' if 1==0 else 'No'
[True] if True is True else [False]

fruit = 'Apple'
isApple = True if fruit == 'Apple' else False
