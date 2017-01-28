library(tidyverse)
library(magrittr)
library(stringr)
library(testthat)


github <- read_csv("../data/python_results_github.csv") %>% arrange(package)
so <- read_csv("../data/python_results_so.csv") %>% arrange(package)
pypi <- read_csv("../data/python_results_pypi.csv") %>% arrange(package) 

github$package %<>% tolower
so$package %<>% tolower
pypi$package %<>% tolower


## ============================================================================
## FIX DATA
## ============================================================================
## github: ipython-notebook is ipython or jupyter/notebook
## so: jypyter-notebook is converted to ipython-notebook for tags
## pypi: yes ggplot, not ggpy
## sqlite3 is base python, so remove
bad_github <- c("ipython-notebook", "ggplot", "mlpy", "plotly")
bad_so <- c("design-patterns", "ggplot2", "ggplot", "jupyter-notebook")
bad_pypi <- c("notebook", "ggpy")
bad <- c("sqlite3")

github %<>% filter(!(package %in% bad_github))
so %<>% filter(!(package %in% bad_so))
pypi %<>% filter(!package %in% bad_pypi)

## SO auto-corrects [basemap] to [matplotlib-basemap] => combine records
## and [jupyter-notebook] to [ipython-notebook]
## also, NA tags = 0 tags
sumx <- . %>% sum(na.rm = TRUE)

so %<>%
    mutate(package=replace(package,
                           package=="matplotlib-basemap",
                           "basemap")) %>%
    mutate(package=replace(package,
                           package=="ipython-notebook",
                           "jupyter-notebook")) %>%
    group_by(package) %>%
    summarise(so_tag_counts=sumx(so_tag_counts),
              so_question_count=sumx(so_question_count))


## ============================================================================
## check data
## ============================================================================
get_unique <- . %>% unique %>% length

## so$package %>% get_unique
## github$package %>% get_unique
## pypi$package %>% get_unique

## check dups
expect_equal(1, so %>% count(package) %>% .$n %>% unique)
expect_equal(1, github %>% count(package) %>% .$n %>% unique)
expect_equal(1, pypi %>% count(package) %>% .$n %>% unique)
expect_false("ggplot" %in% so$package)
expect_false("ggplot" %in% github$package)

## ============================================================================
## make data
## ============================================================================
## combine plotly.py and plotly
## combine ggplot downloads with ggpy results from SO and Github
full_wide <- so %>%
    full_join(., github, by="package") %>%
    full_join(., pypi, by="package") %>%
    select(-full_name) %>%
    filter(package != "sqlite3") %>%
    arrange(package)

plotly_py_forks <- full_wide[full_wide$package=="plotly.py",]$forks
plotly_py_stars <- full_wide[full_wide$package=="plotly.py",]$stars
ggplot_downloads <- full_wide[full_wide$package=="ggplot",]$downloads

## FINAL DATA HERE
full_wide %<>%
    mutate(forks=replace(forks,
                         package=="plotly",
                         plotly_py_forks)) %>%
    mutate(stars=replace(stars,
                         package=="plotly",
                         plotly_py_stars)) %>%
    mutate(downloads=replace(downloads,
                             package=="ggpy",
                             ggplot_downloads)) %>%
    filter(!(package %in% c("ggplot", "plotly.py")))
                             
write_csv(full_wide, "../output/python-data-wide.csv")


## ============================================================================
## Analysis
## ============================================================================
scaled <- full_wide %>%
    gather(type, value, -package) %>%
    filter(!is.na(value)) %>%
    group_by(type) %>%
    mutate(scaled = scale(value) %>% round(2)) %>%
    select(-value) %>%
    spread(type, scaled) %>%
    rename(Package=package, Downloads=downloads)


## function to make ranks
make_ranks <- . %>%
    rowwise() %>%
    mutate(Github=mean(c(forks, stars)) %>% round(2),
           Stack=mean(c(so_question_count, so_tag_counts)) %>% round(2),
           Overall=mean(c(Github, Stack, Downloads)) %>% round(2)) %>%
    arrange(desc(Overall)) %>%
    ungroup() %>%
    mutate(Rank=dense_rank(desc(Overall))) %>%
    select(Package, Rank, Overall, Github, Stack, Downloads,
           forks, stars, starts_with("so"))

## make ranks
rank_with_na <- scaled %>% make_ranks()

write_csv(rank_with_na, "../output/python-ranks-with-na.csv")
