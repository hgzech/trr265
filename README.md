# TRR 265
> This module handle's analysis of the TRR265 data.


stub: To get started, download all the required data. Into the following folder structures:

## Install

`pip install trr265`

## How to use

Fill me in please! Don't forget code examples:

!pip install trr265

```python
from trr265.data_provider import DataProvider
dp = DataProvider('/Users/hilmarzech/Projects/trr265/trr265/data/') # Path to data folder (containing raw, interim, external, and processed)
dp.get_two_day_data().iloc[:20]
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    /var/folders/16/2wxbnpk5321f8g40bxf0ht_h0000gn/T/ipykernel_84713/2255965172.py in <module>
          1 from trr265.data_provider import DataProvider
          2 dp = DataProvider('/Users/hilmarzech/Projects/trr265/trr265/data/') # Path to data folder (containing raw, interim, external, and processed)
    ----> 3 dp.get_two_day_data().iloc[:20]
    

    AttributeError: 'DataProvider' object has no attribute 'get_two_day_data'

