# Ranking Popular Distributed Computing Packages for Data Science

At [The Data Incubator](https://www.thedataincubator.com/), we pride ourselves on having the latest data science curriculum. Much of our curriculum is based on feedback from corporate and government partners about the technologies they are looking to learn.  However, we wanted to develop a more data-driven approach to what we should be teaching in our [data science corporate training](https://www.thedataincubator.com/training.html) and our [free fellowship](https://www.thedataincubator.com/fellowship.html) for masters and PhDs looking to enter data science careers in industry. Here are the results.

# The Rankings

Below is a ranking of open-source distributed computing packages that are useful for Data Science, based on Github and Stack Overflow activity, as well as Google Search results. The table shows standardized scores, where a value of 1 means one standard deviation above average (average = score of 0). For example, `Apache Hadoop` is 6.4 standard deviations above average in Stack Overflow activity, while `Apache Storm` is close to average. See [below for methods](#Methods).

<img src="img/DC_packages_rank.png" width=500px></img>


# Results and Discussion

The ranking is based on equally weighing its three components: Github (stars and forks), Stack Overflow (tags and questions), and number of Google search results. These were obtained using available APIs. Coming up with a comprehensive list of distributed computing packages was tricky - in the end, we scraped three different lists that we thought were representative. We chose to focus on 76 open-source frameworks and distributed programing packages and save databases, database management, and data ingestion for another time (see [methods](#Methods) below for details). Computing standardized scores for each metric allows us to see which packages stand out in each category. The [full ranking is here](output/DL_libraries_final_Rankings.csv), while the [raw data is here](output/distributed_computing_data.csv).

## Apache frameworks sweep the top 3 spots in our rankings
`Apache Spark` (1) dominated the Github activity metric with forks and stars more than seven standard deviations above the mean. `Apache Spark` is the most popular distributed computing framework capable of both batch and stream processing. It can be used on its own or along with modules from the Hadoop ecosystem. `Apache Hadoop` (2) outperformed `Apache Spark` in Stack Overflow activity and Google search results. The disconnect between Hadoop's Github activity and the other two metrics is likely due to the fact that the meaning of `Apache Hadoop` has evolved over time. Rather than refering to just the framework, the term "Hadoop" can also mean all 11 Hadoop-related projects that make up the ecosystem. This results in a somewhat inflated StackOverflow and Google search results scores. Another part of the Hadoop ecosystem is `Apache Storm` (3), an open-source framework for distributed computing. Unlike the batch-only processing power of `Apache Hadoop`, `Apache Storm` is a stream-only framework best for near real-time processing. 

## `Apache Flink` and `Apache Sanza` are the least popular Apache frameworks
Similiar to `Apache Spark`, `Apache Flink` (10) is also framework capable of both batch and stream processing. However, `Apache Spark` bills itself as a batch-processor that can handle streaming, while `Apache Flink` is suited for heavy stream processoring with some batch tasks. This alternative may not garner the same activity as the top three frameworks, but it is enough to round out the top 10 of our rankings. `Apache Sanza` on the other hand trails all the frameworks, coming in at number 42 in our rankings. `Apache Sanza` is a stream-only processing framework developed by LinkedIn in conjuction with `Apache Kafka`, a messaging service. Perhaps it is these strong ties to one other module that make `Apache Sanza` more specialized and less popular overall.

## Simplicity wins users over with `Blaze` 
`Blaze` (5) is a NumPy and Pandas interface to Big Data. It offers very few functions outside of being able to use NumPy/Pandas syntax to send queries off to distributed databases. Likely feeding off the popularity of Pandas, `Blaze` provides a familiar syntax to do simple computations on data too big to fit in memory.

## Several popular modules were developed by Twitter 
Three of the top 20 packages on our list come from Twitter. The most popular of the three, `Twitter Scalding` (14) is a higher-level Scala library build on top of the Hadoop API, `Cascading` (12). `Twitter Heron` (16) is a direct successor to `Apache Storm` released in June 2016. `Twitter Heron` offers improved realtime, fault-tolerant stream processing with higher throughput than Storm. It will be interesting to see if `Twitter Heron` can climb farther up the ranks with time.

## The Hadoop Ecosystem dominates
The Hadoop Ecosystem modules are the most prevalent and widely adopted distributed computing packages. 16 of the top 20 packages we ranked are part of the Hadoop Ecosystem or designed to integrate with it. While independent frameworks like `druid` (6), `Nokia Disco` (7), and `Onyx` (9) are gaining traction and popularity, Hadoop has been the leader in open-source distributed computing since it's creation. 

# Limitations

As with [any analysis](https://twitter.com/benhamner/status/732392995610198016), decisions were made along the way. All source code and data is on [our Github Page](https://github.com/thedataincubator/data-science-blogs). The full list of distributed computing packages [came from a few sources](#Methods). 

Naturally, some libraries that have been around longer will have higher metrics, and therefore higher ranking. This is not adjusted for in any way.

The data presented a few difficulties:

*  Several of the libraries were common words (onyx, kite, drools), for this reason the search terms used to determine the number of google search results included an additional descriptive term("onyx platform", "kite API", "kiegroup drools"). All search terms can be found [here](/data/DC_packages_results_google.csv).
*  Manual checks were done to confirm Stack Overflow tags and Github repository locations
*  Stack Overflow tags can be found [here](/data/DC_packages_results_stackoverflow.csv).
*  Github repository names can be found [here](/data/DC_packages_results_github.csv).


# Methods

All source code and data is on [our Github Page](https://github.com/thedataincubator/data-science-blogs).

We first generated a list of deep learning libraries from [these](https://www.digitalocean.com/community/tutorials/hadoop-storm-samza-spark-and-flink-big-data-frameworks-compared) [three](https://github.com/onurakpolat/awesome-bigdata) [sources](http://bigdata.andreamostosi.name/), and then collected metrics for all of them, to come up with the ranking. Github data is based on both stars and forks, while Stack Overflow data is based on tags and questions containing the package name. Search results are from Google.

A few other notes:
 * Any unavailable Stack Overflow counts were converted to zero count. 
 * Counts were standardized to mean 0 and deviation 1, and then averaged to
  get Github and Stack Overflow scores, and, combined with Serch Results, the Overall score. 

All data was downloaded on September 6, 2017.

# Resources

Source code is available on [The Data Incubator](https://www.thedataincubator.com/)'s [Github (https://github.com/thedataincubator/data-science-blogs/). If you're interested in learning more, consider

1. [Data science corporate training](https://www.thedataincubator.com/training.html)
2. [Free eight-week fellowship](https://www.thedataincubator.com/fellowship.html) for masters and PhDs looking to enter industry
3. [Hiring Data Scientists](https://www.thedataincubator.com/hiring.html)

# Authors:
[Michael Li](https://github.com/tianhuil/) and [Rachel Allen](https://github.com/raykallen/).