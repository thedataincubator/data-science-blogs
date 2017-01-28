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


cran <- fromJSON("../data/cran_downloads.json") %>% tbl_df %>%
    select(package, downloads) %>%
    rename(count=downloads) %>%
    arrange(desc(count)) %>%
    mutate(kind="CRAN",
           rank=dense_rank(desc(count)))

packages <- cran$package %>% u %>% tolower

## filter this one for packages
so_tags <- fromJSON("../data/so_tag_counts.json") %>% tbl_df %>%
    filter(name %in% packages) %>% 
    select(name, count) %>%
    rename(package=name) %>%
    mutate(kind="SO_tag",
           rank=dense_rank(desc(count)))
so_body <- json_dict_to_tbl("../data/so_body_counts.json") %>%
    mutate(kind="SO_body",
           rank=dense_rank(desc(count)))
so_body_r <- json_dict_to_tbl("../data/so_body_counts_r.json") %>%
    mutate(kind="SO_body_r_tag",
           rank=dense_rank(desc(count)))
github <- json_dict_to_tbl("../data/github_stars.json") %>%
    mutate(kind="Github_star",
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
df <- bind_rows(cran, so_body_r, github)

df_wide <- df %>% select(-rank) %>% spread(kind, count)

write_csv(df_wide, "../output/r-data-wide.csv")

## main ranking (excludes github due to some missing data)
ranks1 <- df %>% filter(kind != "Github_star") %>% group_by(package) %>%
    summarise(mean_rank1=round(mean(rank), 1), lists1=n()) %>%
    arrange(mean_rank1) %>%
    rownames_to_column(var="ranking1")

# ranks1$lists %>% unique

## ranking which includes github data, if any
ranks2 <- df %>% group_by(package) %>%
    summarise(mean_rank2=round(mean(rank), 1), lists2=n()) %>%
    arrange(mean_rank2) %>%
    rownames_to_column(var="ranking2")


## COMBINE ranks
ranking <- df %>% select(package, kind, rank) %>%
    spread(kind, rank) %>%
    left_join(ranks1 %>% select(-lists1, -ranking1), ., on="package") %>%
    arrange(mean_rank1) %>%
    select(package, CRAN, SO_body_r_tag, Github_star)
names(ranking) <- c("Package", "CRAN", "Stack Overflow", "GitHub")

write.csv(ranking, "../ranking.csv")
