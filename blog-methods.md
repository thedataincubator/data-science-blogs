# [Draft] Top R packages for ML: Building a ranking is not easy

In another post, we showed the results of our ranking of the top R packages for
Machine Learning. This post describes the methodology.

# Step 1: Obtain an exhaustive list of ML packages

From the beginning, we envisioned our ranking being built on a combination of
package downloads and Stack Overflow and Github activity. We knew that APIs
existed that would provide us with these metrics.

However, obtaining an initial list of all the R packages for Machine Learning
was a tougher task. This list needed to be exhaustive, objective, and
up-to-date. A bad initial list would affect our ranking dramatically.

A friend helped us find
the
["CRAN Task View: Machine Learning & Statistical Learning"](https://cran.r-project.org/web/views/MachineLearning.html) which
has a great list at the bottom, and is easy to scrape.

Its advantages are that the package list comes from an authoritative source
(CRAN is the "official" R package repository) and it is regularly updated (last
update: January 6, 2017). Kudos to the
author, [Torsten Hothorn](http://user.math.uzh.ch/hothorn/), who is also very
responsive via email.

A previous thought was to use Google to look up lists of "top R ML packages"
and then trying to scrape all the package names, combine them, and use that
list as a starting point. But set aside the engineering task, we also found
that the currently available lists were of poor quality relative to our
needs. They were outdated, didn't clearly specify methods, and were often quite
subjective.


# Determine objective metrics

A good ranking needs a definition of what "best" means, and needs to be
constructed with good metrics.

We defined "best" as "most popular". This doesn't necessarily mean the packages
are widely-loved (users could be frequently searching Stack Overflow because
the API is horrible).

We chose 3 components for our ranking:

  * Downloads: number of downloads from a CRAN mirror
  * Github: number of stars for package on its main repository page
  * Stack Overflow: number of questions containing the package name and tagged
    with 'R'
    
# CRAN downloads

There are a few CRAN mirrors, and we used the R-Studio mirror since it has a
convenient API. RStudio must be the most widely used IDE for R, but it is not
the only one. Our ranking could be improved (though maybe not significantly) if
we aggregated downloads from other CRAN mirrors.


# GitHub

Initially, we looked for the packages' Github page by querying Github's search
API for the package name, perhaps with "language:R", but this proved
unreliable. It was sometimes hard to pick out the correct Github repo, and not
all R packages are implemented using the R language (the "language:R" parameter
in the search API seems to refer to the most popular language that the
repository is written in).

Instead, we went back to CRAN to find these urls. Each package has an official
CRAN page, which includes useful information, including source code links. This
is where we got the packages' Github repository location.

After that, obtaining the Github stars was easy with the API.

# Stack Overflow

Getting useful results from Stack Overflow was tricky. Some R package names
like `tree` and `earth` present obvious difficulties: Stack overflow results
may not be filter to results just for the R package, so we first added an 'r'
string to the query, which greatly helped.

A good (optimal?) strategy was to look for the package's name in the question
body, and then add an 'r' tag (which is different from adding the 'r' string).


# Building the ranking

We simply ranked the packages within each of the 3 metrics, and took the
average ranking. Nothing fancy.

# Miscellaneous notes

All data was downloaded on January 19, 2017. CRAN download counts were from the
past 365 days: January 19, 2016 to January 19, 2017.

# Top R packages for Data Science?

This project started as a ranking of the top packages for "Data Science", but
we soon found that the scope was too broad.

Data scientists do many different things, and you can classify almost any R
package as helping a data scientist. Should we include string manipulation
packages? How about packages to read data from databases?

A longer project, for another day, could be to use even more "Data Science" to
come up with a ranking of the top "Data Science" packages.
