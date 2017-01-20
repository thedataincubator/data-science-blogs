library(tidyverse)
library(jsonlite)
library(forcats)
library(magrittr)
library(testthat)

json_dict_to_tbl <- function(file, cols=2, names=c("package", "count")) {
    return(fromJSON(file) %>%
           map_df(~as.data.frame(., stringsAsFactors=FALSE), .id="x") %>%
           setNames(names) %>%
           arrange(desc(count)) %>%
           tbl_df
           )
}



## TODO: check date range
cran <- fromJSON("../data/cran_metadata.json") %>% tbl_df %>%
    select(package, downloads) %>%
    rename(count=downloads) %>%
    arrange(desc(count)) %>%
    mutate(kind="CRAN",
           rank=dense_rank(desc(count)))

packages <- cran$package %>% u %>% tolower

## filter this one for packages
so_tags <- fromJSON("../data/so_tags.json") %>% tbl_df %>%
    filter(name %in% packages) %>% 
    select(name, count) %>%
    rename(package=name) %>%
    mutate(kind="SO tag",
           rank=dense_rank(desc(count)))
so_body <- json_dict_to_tbl("../data/body_counts.json") %>%
    mutate(kind="SO body",
           rank=dense_rank(desc(count)))
so_body_r <- json_dict_to_tbl("../data/body_counts_r.json") %>%
    mutate(kind="SO body + [R]",
           rank=dense_rank(desc(count)))
github <- json_dict_to_tbl("../data/github_stars.json") %>%
    mutate(kind="github star",
           rank=dense_rank(desc(count)))

## ============================================================================
## check data
## ============================================================================
checks <- function(df){
    namez <- c("package", "count", "kind", "rank")
    expect_equal(df %>% names %>% length, 4)
    expect_equal(namez %in% names(df) %>% sum, 4)
}
cran %>% checks
so_tags %>% checks
github %>% checks


## ============================================================================
## analysis
## ============================================================================
df <- bind_rows(cran, so_tags, github) 

top10any <- df %>%
    filter(rank<11) %>%
    .$package %>% unique

top10_rank <- df %>%
    group_by(package) %>%
    summarise(mean_rank=mean(rank)) %>%
    top_n(10, desc(mean_rank)) 

top10 <- top10_rank %>% .$package %>% unique


df$kind %>% factor %>% levels
fix <- . %>% factor(levels=c("CRAN", "SO tag", "github star"))

dft <- df %>% filter(package %in% top10)


ggplot(dft,
       aes(x=kind %>% fix, y=rank, group=package, colour=package)) +
    coord_cartesian(ylim = c(1, 20)) +
    scale_y_reverse(breaks = 1:20) +
    scale_x_discrete() +
    scale_color_brewer(type='qual') +
    geom_line() +
    labs(x="source")


