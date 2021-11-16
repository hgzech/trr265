# TRR 265
> This module handles analysis of the TRR265 data.


## Install

`pip install trr265`

## How to use

Fill me in please! Don't forget code examples:

!pip install trr265

```python
#%load_ext autoreload
#%autoreload 2
from trr265.data_provider import DataProvider
dp = DataProvider('/Users/hilmarzech/Projects/trr265/trr265/data/') # Path to data folder (containing raw, interim, external, and processed)
dp.get_two_day_data().iloc[:20][['participant','date','MDBF_zufrieden','g_alc']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>participant</th>
      <th>date</th>
      <th>MDBF_zufrieden</th>
      <th>g_alc</th>
    </tr>
    <tr>
      <th>two_day_index</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>b001</td>
      <td>2020-02-22</td>
      <td>NaN</td>
      <td>6.4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b001</td>
      <td>2020-02-23</td>
      <td>NaN</td>
      <td>35.2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>b001</td>
      <td>2020-02-24</td>
      <td>2.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>b001</td>
      <td>2020-02-25</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>b001</td>
      <td>2020-02-26</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>b001</td>
      <td>2020-02-27</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>b001</td>
      <td>2020-02-28</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>b001</td>
      <td>2020-02-29</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>b001</td>
      <td>2020-03-01</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>b001</td>
      <td>2020-03-02</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>b001</td>
      <td>2020-03-03</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11</th>
      <td>b001</td>
      <td>2020-03-04</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>b001</td>
      <td>2020-03-05</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>b001</td>
      <td>2020-03-06</td>
      <td>NaN</td>
      <td>57.6</td>
    </tr>
    <tr>
      <th>14</th>
      <td>b001</td>
      <td>2020-03-07</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>15</th>
      <td>b001</td>
      <td>2020-03-08</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>16</th>
      <td>b001</td>
      <td>2020-03-09</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>17</th>
      <td>b001</td>
      <td>2020-03-10</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>18</th>
      <td>b001</td>
      <td>2020-03-11</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>19</th>
      <td>b001</td>
      <td>2020-03-12</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>


