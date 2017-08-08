# Ranking Popular Python Packages for Data Science

At [The Data Incubator](https://www.thedataincubator.com/), we pride ourselves
on having the latest data science curriculum.  Much of our curriculum is based
on feedback from corporate and government partners about the technologies they
are looking to learn.  However, we wanted to develop a more data-driven
approach to what we should be teaching in our
[data science corporate training](https://www.thedataincubator.com/training.html) and
our [free fellowship](https://www.thedataincubator.com/fellowship.html) for
masters and PhDs looking to enter data science careers in industry.  Here are
the results.

# The Ranking

Below is a ranking of JavaScript data visualization packages that are useful 
for Data Science, based on Github and Stack Overflow activity, as well
as [npmjs (javascript package manager)](https://www.npmjs.com/) downloads.

The table shows standardized scores, where a value of 1 means one standard
deviation above average (average = score of 0). For example, `chart.js` is 2.4
standard deviations above average in Github activity, while
`plotly.js` is close to average. See [below for methods](#Methods).

<img src="img/js-viz-rank.png" width=500px></img>

# Results and Discussion

The ranking is based on equally weighing its three components: Github (stars
and forks), Stack Overflow (tags and questions), and npm downloads(totals and 
compounded monthly growth rate). These were obtained using available APIs. 
Coming up with a comprehensive list of JavaScript visualization packages was 
tricky - in the end, we scraped four different lists that we thought were 
representative (see [methods](#Methods) below for details). Computing standardized 
scores for each metric allows us to see which packages stand out in each category.

## `D3.js` dominates the field

Has the largest community...
The [full ranking is here](output/js_viz_final_Rankings.csv), while
the [raw data is here](output/js_viz_data.csv).

## `sigma.js` most popular network visualization package (beats `cytoscape`)

## `chart.js`, `plottable`, and `highcharts` 


# Limitations

As with [any analysis](https://twitter.com/benhamner/status/732392995610198016),
decisions were made along the way. All source code and data is on [our Github Page](https://github.com/thedataincubator/data-science-blogs).

The full list of JavaScript visualization packages [came from a few sources](#Methods),
and a few paid packages were unranked, due to unavailable downloads and Github
data. These are: `CanvasJS`, `KoolCharts`, `TeeCharts`, `ZoomCharts`. 

Further, naturally, some packages that have been around longer will have higher
metrics, and therefore higher ranking. This is not adjusted for in any way other than
download metrics restricted to the past six months.

The data presented a few difficulties:

* The `plottable` has an inflated Stack Overflow (SO) question metrics since 
  it's a common word.
* SO data for `plotly` may also be inflated, as it's both an R and Python
  package.


# Methods

All source code and data is on [our Github Page](https://github.com/thedataincubator/data-science-blogs).

We first generated a list of Data Science packages
[from](https://github.com/showcases/data-visualization?s=language) [these](https://en.wikipedia.org/wiki/Comparison_of_JavaScript_charting_frameworks)[four](https://cssauthor.com/javascript-charting-libraries/) [sources](http://socialcompare.com/en/comparison/javascript-graphs-and-charts-libraries),
and then collected metrics for all of them, to come up with the ranking. 
Github data is based on both stars and forks, while Stack Overflow data is based
on tags and questions containing the package name. Downloads data is from npmjs.
Downloads were totaled over a six month period, and the compound monthly growth rate
was calculated over the same period. 
After scraping other sites for JS visualization package names, we had gathered over 
100 "unique" package names. Many of them were aliases for the same packages (d3, D3JS).
If a the first result of github search returned the same repo as another package, we 
treated them as the same package, but saved the aliases to search Stack Overflow questions. 

A few other notes:

  * Any unavailable Stack Overflow counts were converted to zero count. 
  * Counts were standardized to mean 0 and deviation 1, and then averaged to
  get Github, Stack Overflow, and Download scores, and combined to get the Overall 
  score. 
  * Some manual checks were done to confirm Github repository location.

All data was downloaded on August 6, 2017.

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
[Michael Li](https://github.com/tianhuil/) and [Rachel Allen](https://github.com/raykallen/).
