# [Draft] Most Popular R packages for Machine Learning

What are the most popular ML packages? Let's look at a ranking based on package
downloads and social website activity.

See [below](#Methods) for methodological details.

<img src="img/rank.png" width=400px></img>

*Also: OneR: 1 (SO); mlr: 2 (Github); ranger: 4 (Github); SuperLearner: 5 (Github)*
	
[ NB: Full list here](tmp_ranking.csv)

# Caret on top, neural nets feature strongly among other algorithm heavyweights

Perhaps not surprisingly, `caret` is on top. It's a general package for
creating machine learning workflows, and it integrates well with some
algorithm-specific packages, which come next in the ranking.

These include `e1071` (for SVMs), `rpart` (trees), `glmnet` (regularized
regressions), and, perhaps surprisingly, neural networks (`nnet`). See details
on all of these packages [below](#Package-details)

The ranking reveals the fragmentation of the R package community. Several of
the top packages, such as `rpart` and `tree`, implement the same algorithms,
which contrasts with the uniformity - and breadth - of Python's `scikit-learn`.

Still, if you're loving R's data manipulation capabilities (as in the
`tidyverse`), then you don't need to leave R to perform some powerful modeling
using some of the packages in this list. And as more features are added
to [`modelr`](https://github.com/hadley/modelr), we may soon see it included in
this list.



# Methods

Source code is available on Github [ADD LINK].

We first obtained a list of the R packages used for Machine Learning
from [this page](https://cran.r-project.org/web/views/MachineLearning.html).

Then, we obtained the following metrics for each package:

  * CRAN download count from https://cranlogs.r-pkg.org
  * Github stars count. Github repository link, if any, was obtained from the
  package's official CRAN page: http://cran.r-project.org/package=package_name
  * Count of Stack Overflow questions containing the package name and tagged
    `R`. We also considered counts of questions containing only the package
    name, or only the package name as the tag*

All metrics were downloaded on January 19, 2017. CRAN download counts were from
the past year: 1/19/2016 to 1/19/2017

*We describe our methods in detail in another post [ADD LINK]



# Package details

`caret` is a general package for creating machine learning workflows, and it
comes out on top of this ranking. Next come a few packages implementing
specific machine learning algorithms: Random Forests (`randomForest`), Support
Vector Machines (`e1071`), Classification and Regression Trees (`rpart`), and
regularized regression models (`glmnet`).

`nnet` implements neural networks (`nnet`), while the `tree` package also
implements trees. `party` is for recursive partitioning and visualization of
binary trees, and `arules` is for association mining. SVMs and other kernel
methods are implemented in `kernlab`. The `h2o` package is for scalable machine
learning, and is part of the larger H2O project. `ROCR` is for model
evaluation, including ROC curves, while `gbm` implements gradient
boosting. More partitioning algorithms can be accessed with `RWeka`, while
`rattle` is an R GUI for data mining.

A few packages feature strongly on Github only: `mlr` and `SuperLearner` are 2
other meta-packages that offer similar functionality to `caret`, while `ranger`
offers C++ implementations of random forests.

Last, `OneR` is number one on Stack Overflow, but the SO API often
auto-corrects this to "one" so the result is unreliable.

