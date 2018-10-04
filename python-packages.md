# Ranking Popular Python Packages for Data Science

At [The Data Incubator](https://www.thedataincubator.com/), we pride ourselves
on having the latest data science curriculum.  Much of our curriculum is based
on feedback from corporate and government partners about the technologies they
are looking to learn.  However, we wanted to develop a more data-driven
approach to what we should be teaching in
our
[data science corporate training](https://www.thedataincubator.com/training.html) and
our [free fellowship](https://www.thedataincubator.com/fellowship.html) for
masters and PhDs looking to enter data science careers in industry.  Here are
the results.

# The Ranking

Below is a ranking of Python packages that are useful for Data Science, based
on Github and Stack Overflow activity, as well
as [PyPI (The Python Package Index)](https://pypi.python.org/pypi) downloads.

The table shows standardized scores, where a value of 1 means one standard
deviation above average (average = score of 0). For example, `numpy` is 2
standard deviations above average in Stack Overflow activity, while
`tensorflow` is close to average. See [below for methods](#Methods).

<img src="img/python-rank.png" width=500px></img>

# Results and Discussion

The ranking is based on equally weighing its three components: Github (stars
and forks), Stack Overflow (tags and questions), and PyPI downloads. These were
obtained using available APIs and a fork of the `vanity` project. Coming up
with a comprehensive list of data science packages was tricky - in the end, we
scraped three different lists that we thought were representative
(see [methods](#Methods) below for details). Computing standardized scores for
each metric allows us to see which packages stand out in each category (look at
`tensorflow`'s Github score!).

## `numpy`, `tensorflow`, and `pandas` are top 3

Due to massive total downloads and strong Stack Overflow activity, the clear
leader is `numpy` (a fundamental package for scientific computing with
Python).

However, the scalable machine learning package `tensorflow` (stared at Google)
trounces the other libraries in Github activity (based on both stars and
forks), with the more general machine learning module `scikit-learn` a distant
second, but fifth overall.

Both `numpy` and `pandas` (high-performance data structures and data analysis
package) are only average on Github, but strong in the other two categories.

The interactive interpreter `ipython` is fourth overall, while the `jupyter`
project (of the popular notebook) is 19th overall (not shown).

The [full ranking is here](output/python-ranks-with-na.csv), while
the [raw data is here](output/python-data-wide.csv).

## Github vs. Stack Overflow activity
There appears to be an inverse correlation in Github activity compared to Stack
Overflow and Downloads for the top packages. For example, there are a lot of
Stack Overflow questions for `numpy` and `pandas` compared to `tensorflow` and
`scikit-learn`, but the latter two have an edge on Github. Since `numpy` and
`pandas` are two "utility" packages, perhaps more people are actually using
them (and need help).

## `numpy` most popular core library (beats `pandas`, `scipy`)

Among the core libraries, `numpy` is a clear first, with `pandas` third,
`ipython` fourth, and `scipy` (an ecosystem of open-source software for
mathematics, science, and engineering) ninth.

## `tensorflow` outperforms `theano` in Neural Networks

The other deep-learning package, `Theano`, is a big distance behind
`tensorflow` in this ranking. The interactive and
polished [TensorFlow Playground](http://playground.tensorflow.org) could be a
factor.

## `matplotlib` most popular graphics library

As expected, `matplotlib` (2D plotting library) is the most popular graphics
package, but the ranking also features `plotly` (interactive,
publication-quality graphs that can be easily published online) and `bokeh` (an
interactive visualization library that targets modern web browsers for
presentation). `ggpy` (Python port for R's popular `ggplot2` package) was 18th
overall, but the data is less reliable, as noted in the next section.

# Limitations

As
with [any analysis](https://twitter.com/benhamner/status/732392995610198016),
decisions were made along the way. All source code and data is on [our Github Page](https://github.com/thedataincubator/data-science-blogs).

The full list of machine learning packages [came from a few sources](#Methods),
and a few packages were unranked, due to unavailable downloads or Github
data. These are: `basemap` (mapping with `matplotlib`), `d3py` (D3-like
plotting), `jupyter-notebook`, `mlpy` (machine learning based on `scipy` and
`numpy`), `pylearn2` (machine learning, based on `theano`), `pytables` (big
tables), and `shogun` (machine learning). They were all below average compared
to the ranked packages, in all categories.

Importantly,
the [Anaconda distribution](https://www.anaconda.com/what-is-anaconda/) bundles
together many of these packages, and this was not considered.

Further, naturally, some packages that have been around longer will have higher
metrics, and therefore higher ranking. This is not adjusted for in any way.

The data presented a few difficulties:

* The python port for `ggplot` was recently renamed to `ggpy`, and we used the
  latter for all metrics, except downloads (which used `ggplot`).
* `ipython notebook` is now `jupyter notebook`. Stack overflow auto-corrected
  `ipython-notebook` to `jupyter-notebook` so we combined these results with
  `jupyter-notebook` results from the other two sources. But `jupyter-notebook`
  didn't have a downloads count, so it doesn't feature in the final
  ranking. Instead, we also performed analyses for `ipython` and `jupyter`
  individually, which do appear in the ranking.
* The [Pattern package](https://github.com/clips/pattern) has inflated Stack
  Overflow (SO) question metrics since it's a common word. It has no tags data,
  as SO auto-corrects the query "[pattern]" to something unrelated.
* SO data for `plotly` may also be inflated, as it's both an R and Python
  package.

# Methods

All source code and data is on [our Github Page](https://github.com/thedataincubator/data-science-blogs).

We first generated a list of Data Science packages
from
[these](https://github.com/rasbt/pattern_classification/blob/master/resources/python_data_libraries.md) [three](https://www.upwork.com/hiring/data/15-python-libraries-data-science/) [sources](http://www.datasciencecentral.com/profiles/blogs/9-python-analytics-libraries-1),
and then collected metrics for all of them, to come up with the ranking.

Github data is based on both stars and forks, while Stack Overflow data is based
on tags and questions containing the package name. Downloads are from PyPI,
using
a [fork of the `vanity` project](https://github.com/pavopax/vanity). Other
projects to get download counts
include [`pypi-download-stats`](https://github.com/jantman/pypi-download-stats)
(couldn't get it to work)
and [`pypi-ranking.info`](http://pypi-ranking.info/alltime) (gives smaller
numbers than `vanity`).

A few other notes:

  * `sqlite3` was removed from analysis, as it is a base Python module.
  * `ggplot` downloads were combined with `ggpy` results from Github and Stack
    Overflow.
  * Any unavailable Stack Overflow counts were converted to zero count. 
  * Counts were standardized to mean 0 and deviation 1, and then averaged to
  get Github and Stack Overflow scores, and, combined with the Downloads, the
  Overall score. 
  * Some manual checks were done to confirm Github repository location.

All data was downloaded on January 26, 2017.

# Resources
Source code is available
on
[The Data Incubator](https://www.thedataincubator.com/)'s
[Github](https://github.com/thedataincubator/data-science-blogs/).  If you're
interested in learning more, consider

1. [Data science corporate training](https://www.thedataincubator.com/training.html)
2. [Free eight-week fellowship](https://www.thedataincubator.com/fellowship.html) for masters and PhDs looking to enter industry
3. [Hiring Data Scientists](https://www.thedataincubator.com/hiring.html)

# Authors:
[Michael Li](https://github.com/tianhuil/) and [Paul Paczuski](https://github.com/pavopax/).
