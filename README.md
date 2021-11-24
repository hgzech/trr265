# TRR 265
> This module handles analysis of the TRR265 data.


## Install

`pip install trr265`

`pip install biuR` (optional but needed for most analyses)

## How to use

```python
from pygments.formatters import HtmlFormatter
from pygments import highlight
import IPython
import inspect
from pygments.lexers import PythonLexer


def display_function(the_function):
    formatter = HtmlFormatter()
    return IPython.display.HTML('<style type="text/css">{}</style>{}'.format(
        formatter.get_style_defs('.highlight'),
        highlight(inspect.getsource(the_function), PythonLexer(), formatter)))
```

```python
display_function(dp.get_mov_data)
```




<style type="text/css">pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.highlight .hll { background-color: #ffffcc }
.highlight { background: #f8f8f8; }
.highlight .c { color: #408080; font-style: italic } /* Comment */
.highlight .err { border: 1px solid #FF0000 } /* Error */
.highlight .k { color: #008000; font-weight: bold } /* Keyword */
.highlight .o { color: #666666 } /* Operator */
.highlight .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.highlight .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.highlight .cp { color: #BC7A00 } /* Comment.Preproc */
.highlight .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.highlight .c1 { color: #408080; font-style: italic } /* Comment.Single */
.highlight .cs { color: #408080; font-style: italic } /* Comment.Special */
.highlight .gd { color: #A00000 } /* Generic.Deleted */
.highlight .ge { font-style: italic } /* Generic.Emph */
.highlight .gr { color: #FF0000 } /* Generic.Error */
.highlight .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.highlight .gi { color: #00A000 } /* Generic.Inserted */
.highlight .go { color: #888888 } /* Generic.Output */
.highlight .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.highlight .gt { color: #0044DD } /* Generic.Traceback */
.highlight .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: #008000 } /* Keyword.Pseudo */
.highlight .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: #B00040 } /* Keyword.Type */
.highlight .m { color: #666666 } /* Literal.Number */
.highlight .s { color: #BA2121 } /* Literal.String */
.highlight .na { color: #7D9029 } /* Name.Attribute */
.highlight .nb { color: #008000 } /* Name.Builtin */
.highlight .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.highlight .no { color: #880000 } /* Name.Constant */
.highlight .nd { color: #AA22FF } /* Name.Decorator */
.highlight .ni { color: #999999; font-weight: bold } /* Name.Entity */
.highlight .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.highlight .nf { color: #0000FF } /* Name.Function */
.highlight .nl { color: #A0A000 } /* Name.Label */
.highlight .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.highlight .nt { color: #008000; font-weight: bold } /* Name.Tag */
.highlight .nv { color: #19177C } /* Name.Variable */
.highlight .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.highlight .w { color: #bbbbbb } /* Text.Whitespace */
.highlight .mb { color: #666666 } /* Literal.Number.Bin */
.highlight .mf { color: #666666 } /* Literal.Number.Float */
.highlight .mh { color: #666666 } /* Literal.Number.Hex */
.highlight .mi { color: #666666 } /* Literal.Number.Integer */
.highlight .mo { color: #666666 } /* Literal.Number.Oct */
.highlight .sa { color: #BA2121 } /* Literal.String.Affix */
.highlight .sb { color: #BA2121 } /* Literal.String.Backtick */
.highlight .sc { color: #BA2121 } /* Literal.String.Char */
.highlight .dl { color: #BA2121 } /* Literal.String.Delimiter */
.highlight .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.highlight .s2 { color: #BA2121 } /* Literal.String.Double */
.highlight .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.highlight .sh { color: #BA2121 } /* Literal.String.Heredoc */
.highlight .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.highlight .sx { color: #008000 } /* Literal.String.Other */
.highlight .sr { color: #BB6688 } /* Literal.String.Regex */
.highlight .s1 { color: #BA2121 } /* Literal.String.Single */
.highlight .ss { color: #19177C } /* Literal.String.Symbol */
.highlight .bp { color: #008000 } /* Name.Builtin.Pseudo */
.highlight .fm { color: #0000FF } /* Name.Function.Magic */
.highlight .vc { color: #19177C } /* Name.Variable.Class */
.highlight .vg { color: #19177C } /* Name.Variable.Global */
.highlight .vi { color: #19177C } /* Name.Variable.Instance */
.highlight .vm { color: #19177C } /* Name.Variable.Magic */
.highlight .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="nd">@patch</span>
<span class="nd">@get_efficiently</span>
<span class="k">def</span> <span class="nf">get_mov_data</span><span class="p">(</span><span class="bp">self</span><span class="p">:</span><span class="n">DataProvider</span><span class="p">):</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    This function gets Movisense data</span>
<span class="sd">    1) We create unique participnat IDs (e.g. &quot;b001&quot;; this is necessary as sites use overapping IDs)</span>
<span class="sd">    2) We merge double IDs, so participants with two IDs only have one (for this duplicate_ids.csv has to be updated)</span>
<span class="sd">    3) We remove pilot participants</span>
<span class="sd">    4) We get starting dates (from the participant overviews in movisense; downloaded as html)</span>
<span class="sd">    5) We calculate sampling days and end dates based on the starting dates</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="c1"># Loading raw data</span>
    <span class="n">mov_berlin</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">mov_berlin_path</span><span class="p">,</span> <span class="n">sep</span> <span class="o">=</span> <span class="s1">&#39;;&#39;</span><span class="p">)</span>
    <span class="n">mov_dresden</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">mov_dresden_path</span><span class="p">,</span> <span class="n">sep</span> <span class="o">=</span> <span class="s1">&#39;;&#39;</span><span class="p">)</span>
    <span class="n">mov_mannheim</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">mov_mannheim_path</span><span class="p">,</span> <span class="n">sep</span> <span class="o">=</span> <span class="s1">&#39;;&#39;</span><span class="p">)</span>

    <span class="c1"># Merging (participant numbers repeat so we add the first letter of location)</span>
    <span class="n">mov_berlin</span><span class="p">[</span><span class="s1">&#39;location&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;berlin&#39;</span>
    <span class="n">mov_dresden</span><span class="p">[</span><span class="s1">&#39;location&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;dresden&#39;</span>
    <span class="n">mov_mannheim</span><span class="p">[</span><span class="s1">&#39;location&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;mannheim&#39;</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">concat</span><span class="p">([</span><span class="n">mov_berlin</span><span class="p">,</span><span class="n">mov_dresden</span><span class="p">,</span><span class="n">mov_mannheim</span><span class="p">])</span>
    <span class="n">df</span><span class="p">[</span><span class="s1">&#39;participant&#39;</span><span class="p">]</span> <span class="o">=</span>  <span class="n">df</span><span class="p">[</span><span class="s1">&#39;location&#39;</span><span class="p">]</span><span class="o">.</span><span class="n">str</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">+</span> <span class="n">df</span><span class="o">.</span><span class="n">Participant</span><span class="o">.</span><span class="n">apply</span><span class="p">(</span><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="s1">&#39;</span><span class="si">%03d</span><span class="s1">&#39;</span><span class="o">%</span><span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">))</span>
    <span class="n">df</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span> <span class="o">=</span> <span class="s1">&#39;Participant&#39;</span><span class="p">,</span> <span class="n">inplace</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span> <span class="c1"># Dropping old participant column to avoid mistakes</span>
    <span class="n">df</span><span class="p">[</span><span class="s1">&#39;trigger_date&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">to_datetime</span><span class="p">(</span><span class="n">df</span><span class="o">.</span><span class="n">Trigger_date</span> <span class="o">+</span> <span class="s1">&#39; &#39;</span> <span class="o">+</span> <span class="n">df</span><span class="o">.</span><span class="n">Trigger_time</span><span class="p">)</span>

    <span class="c1"># Merging double IDs (for participants with several movisense IDs)</span>
    <span class="n">df</span><span class="p">[</span><span class="s1">&#39;participant&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">participant</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">get_duplicate_mov_ids</span><span class="p">())</span>

    <span class="c1"># Removing pilot participants</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="o">~</span><span class="n">df</span><span class="o">.</span><span class="n">participant</span><span class="o">.</span><span class="n">astype</span><span class="p">(</span><span class="nb">str</span><span class="p">)</span><span class="o">.</span><span class="n">str</span><span class="o">.</span><span class="n">contains</span><span class="p">(</span><span class="s1">&#39;test&#39;</span><span class="p">)]</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="o">~</span><span class="n">df</span><span class="o">.</span><span class="n">participant</span><span class="o">.</span><span class="n">isin</span><span class="p">([</span><span class="s1">&#39;m157&#39;</span><span class="p">,</span> <span class="s1">&#39;b010&#39;</span><span class="p">,</span> <span class="s1">&#39;b006&#39;</span><span class="p">,</span> <span class="s1">&#39;d001&#39;</span><span class="p">,</span> <span class="s1">&#39;d002&#39;</span><span class="p">,</span> <span class="s1">&#39;d042&#39;</span><span class="p">,</span> <span class="s1">&#39;m024&#39;</span><span class="p">,</span> <span class="s1">&#39;m028&#39;</span><span class="p">,</span> <span class="s1">&#39;m071&#39;</span><span class="p">,</span> <span class="s1">&#39;m079&#39;</span><span class="p">,</span> <span class="s1">&#39;m107&#39;</span><span class="p">])]</span>


    <span class="c1"># Adding starting dates to get sampling days</span>
    <span class="k">def</span> <span class="nf">get_starting_dates</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">pp_prefix</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">):</span>
        <span class="n">soup</span> <span class="o">=</span> <span class="n">bs</span><span class="p">(</span><span class="nb">open</span><span class="p">(</span><span class="n">path</span><span class="p">)</span><span class="o">.</span><span class="n">read</span><span class="p">())</span>
        <span class="n">ids</span> <span class="o">=</span> <span class="p">[</span><span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="o">.</span><span class="n">text</span><span class="p">)</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">soup</span><span class="o">.</span><span class="n">find_all</span><span class="p">(</span><span class="s2">&quot;td&quot;</span><span class="p">,</span> <span class="n">class_</span> <span class="o">=</span> <span class="s1">&#39;simpleId&#39;</span><span class="p">)]</span>
        <span class="n">c_dates</span> <span class="o">=</span> <span class="p">[</span><span class="n">x</span><span class="o">.</span><span class="n">find_all</span><span class="p">(</span><span class="s2">&quot;span&quot;</span><span class="p">)[</span><span class="mi">0</span><span class="p">][</span><span class="s1">&#39;title&#39;</span><span class="p">]</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">soup</span><span class="o">.</span><span class="n">find_all</span><span class="p">(</span><span class="s2">&quot;td&quot;</span><span class="p">,</span> <span class="n">class_</span> <span class="o">=</span> <span class="s1">&#39;coupleDate&#39;</span><span class="p">)]</span>
        <span class="n">s_dates</span> <span class="o">=</span> <span class="p">[</span><span class="n">x</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">soup</span><span class="o">.</span><span class="n">find_all</span><span class="p">(</span><span class="s2">&quot;input&quot;</span><span class="p">,</span> <span class="n">class_</span> <span class="o">=</span> <span class="s1">&#39;dp startDate&#39;</span><span class="p">)]</span>
        <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">({</span><span class="s1">&#39;participant&#39;</span><span class="p">:</span><span class="n">ids</span><span class="p">,</span><span class="s1">&#39;coupling_date&#39;</span><span class="p">:</span><span class="n">c_dates</span><span class="p">,</span><span class="s1">&#39;starting_date&#39;</span><span class="p">:</span><span class="n">s_dates</span><span class="p">})</span>
        <span class="n">df</span><span class="p">[</span><span class="s1">&#39;coupling_date&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">to_datetime</span><span class="p">(</span><span class="n">df</span><span class="o">.</span><span class="n">coupling_date</span><span class="p">)</span>
        <span class="n">df</span><span class="p">[</span><span class="s1">&#39;starting_date&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">to_datetime</span><span class="p">(</span><span class="n">df</span><span class="o">.</span><span class="n">starting_date</span><span class="p">)</span>
        <span class="n">df</span><span class="o">.</span><span class="n">starting_date</span><span class="o">.</span><span class="n">fillna</span><span class="p">(</span><span class="n">df</span><span class="o">.</span><span class="n">coupling_date</span><span class="p">,</span><span class="n">inplace</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>
        <span class="n">df</span><span class="p">[</span><span class="s1">&#39;participant&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">pp_prefix</span> <span class="o">+</span> <span class="n">df</span><span class="o">.</span><span class="n">participant</span><span class="o">.</span><span class="n">apply</span><span class="p">(</span><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="s1">&#39;</span><span class="si">%03d</span><span class="s1">&#39;</span><span class="o">%</span><span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">))</span>
        <span class="k">return</span> <span class="n">df</span>

    <span class="n">starting_dates</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">concat</span><span class="p">([</span>
    <span class="n">get_starting_dates</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">mov_berlin_starting_dates_path</span><span class="p">,</span> <span class="s1">&#39;b&#39;</span><span class="p">),</span>
    <span class="n">get_starting_dates</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">mov_dresden_starting_dates_path</span><span class="p">,</span> <span class="s1">&#39;d&#39;</span><span class="p">),</span>
    <span class="n">get_starting_dates</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">mov_mannheim_starting_dates_path</span><span class="p">,</span> <span class="s1">&#39;m&#39;</span><span class="p">)</span>
    <span class="p">])</span>
    <span class="c1"># For participants with several movisense IDs we use the first coupling date</span>
    <span class="n">starting_dates</span><span class="o">.</span><span class="n">participant</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">get_duplicate_mov_ids</span><span class="p">(),</span> <span class="n">inplace</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>
    <span class="n">starting_dates</span> <span class="o">=</span> <span class="n">starting_dates</span><span class="o">.</span><span class="n">groupby</span><span class="p">(</span><span class="s1">&#39;participant&#39;</span><span class="p">)[[</span><span class="s1">&#39;starting_date&#39;</span><span class="p">,</span><span class="s1">&#39;coupling_date&#39;</span><span class="p">]]</span><span class="o">.</span><span class="n">min</span><span class="p">()</span><span class="o">.</span><span class="n">reset_index</span><span class="p">()</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">merge</span><span class="p">(</span><span class="n">starting_dates</span><span class="p">,</span> <span class="n">on</span><span class="o">=</span><span class="s2">&quot;participant&quot;</span><span class="p">,</span> <span class="n">how</span> <span class="o">=</span> <span class="s1">&#39;left&#39;</span><span class="p">,</span> <span class="n">indicator</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>
    <span class="c1"># Checking if starting dates were downloaded</span>
    <span class="k">if</span> <span class="s2">&quot;left_only&quot;</span> <span class="ow">in</span> <span class="n">df</span><span class="o">.</span><span class="n">_merge</span><span class="o">.</span><span class="n">unique</span><span class="p">():</span>
        <span class="n">no_starting_dates</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="s1">&#39;_merge == &quot;left_only&quot;&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">participant</span><span class="o">.</span><span class="n">unique</span><span class="p">()</span>
        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Starting dates missing for participants below.  Did you download the participant overviews as html?&quot;</span><span class="p">,</span> <span class="n">no_starting_dates</span><span class="p">)</span>
    <span class="c1"># Calculating movisense sampling day, adding date and end_date</span>
    <span class="n">df</span><span class="p">[</span><span class="s1">&#39;sampling_day&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">(</span><span class="n">df</span><span class="p">[</span><span class="s1">&#39;trigger_date&#39;</span><span class="p">]</span> <span class="o">-</span> <span class="n">df</span><span class="p">[</span><span class="s1">&#39;starting_date&#39;</span><span class="p">])</span><span class="o">.</span><span class="n">dt</span><span class="o">.</span><span class="n">days</span> <span class="o">+</span> <span class="mi">1</span>
    <span class="n">df</span><span class="p">[</span><span class="s1">&#39;date&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">trigger_date</span><span class="o">.</span><span class="n">dt</span><span class="o">.</span><span class="n">date</span>
    <span class="n">df</span><span class="p">[</span><span class="s1">&#39;end_date&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">date</span> <span class="o">+</span> <span class="n">pd</span><span class="o">.</span><span class="n">DateOffset</span><span class="p">(</span><span class="n">days</span> <span class="o">=</span> <span class="mi">365</span><span class="p">)</span>
    <span class="n">df</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="s1">&#39;mov_index&#39;</span><span class="p">,</span><span class="n">inplace</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>
    <span class="c1"># Adding redcap IDs</span>
    <span class="n">ids_table</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">get_ba_data</span><span class="p">()[[</span><span class="s1">&#39;participant_id&#39;</span><span class="p">,</span><span class="s1">&#39;mov_id&#39;</span><span class="p">]]</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="s1">&#39;mov_id==mov_id&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">groupby</span><span class="p">(</span><span class="s1">&#39;mov_id&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">first</span><span class="p">()</span>
    <span class="n">ids_table</span><span class="o">.</span><span class="n">columns</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;redcap_id&#39;</span><span class="p">]</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">merge</span><span class="p">(</span><span class="n">ids_table</span><span class="p">,</span> <span class="n">left_on</span><span class="o">=</span><span class="s1">&#39;participant&#39;</span><span class="p">,</span> <span class="n">right_index</span> <span class="o">=</span> <span class="kc">True</span><span class="p">,</span> <span class="n">how</span> <span class="o">=</span> <span class="s1">&#39;left&#39;</span><span class="p">)</span>
    <span class="c1"># Filtering out participants with no associated redcap data</span>
    <span class="n">no_redcap</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="s2">&quot;redcap_id.isna()&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">participant</span><span class="o">.</span><span class="n">unique</span><span class="p">()</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Participants: </span><span class="si">%s</span><span class="s2"> have no associated redcap IDs and are excluded from the following analyses.&quot;</span><span class="o">%</span><span class="s1">&#39;, &#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">no_redcap</span><span class="p">))</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="n">df</span><span class="o">.</span><span class="n">redcap_id</span><span class="o">.</span><span class="n">isna</span><span class="p">()</span><span class="o">==</span><span class="kc">False</span><span class="p">]</span>
    <span class="k">return</span> <span class="n">df</span>
</pre></div>




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



## Required data

### Phone screening
- data/external/b7_participants.xlsx <- from Hilmar
- data/raw/phonescreening.csv <- from redcap
- data/external/phone_codebook.html <- from redcap

### Basic assessment (from redcap)
- data/raw/ba.csv <- from redcap
- data/external/ba_codebook.html <- from redcap

### Movisens
- all basic assessment data (see above)
- data/raw/mov_data_b.csv
- data/raw/mov_data_d.csv
- data/raw/mov_data_m.csv
- data/raw/starting_dates_b.csv
- data/raw/starting_dates_d.csv
- data/raw/starting_dates_m.csv
- data/external/alcohol_per_drink.csv <- from Hilmar
