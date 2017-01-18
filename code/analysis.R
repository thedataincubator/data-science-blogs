library(tidyverse)
library(jsonlite)
library(forcats)

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
so_tags <- fromJSON("../data/so_tags.json") %>% tbl_df %>%
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

## GITHUB data
github <- read_csv("../data/github_stars.csv") %>%
    separate(X1, c("package_author", "package_name"), "/") %>%
    select(package_name, package_author, starts_with("string")) %>%
    arrange(package_name, package_author, desc(string))



## ============================================================================
## data checks
## ============================================================================
write.csv(github, "../tmp_github.csv")

github %>% group_by(package_name) %>%
    filter(n()>1) %>%
    write.csv("../tmp_dups.csv")



## ============================================================================
## analysis
## ============================================================================




df <- bind_rows(cran, so_tags, so_body, so_body_r) %>%
    select(-count)


top10_packs <- df %>%
    filter(kind=="SO body + [R]", rank<11) %>%
    .$package %>% u

df$kind %>% factor %>% levels

fix <- . %>% factor(levels=c("CRAN", "SO body + [R]", "SO body", "SO tag"))



ggplot(df %>% filter(package %in% top10_packs),
       aes(x=kind %>% fix, y=rank, group=package, colour=package)) +
    coord_cartesian(ylim = c(1, 20)) +
    scale_y_reverse(breaks = 1:20) +
    scale_x_discrete() +
    geom_line() +
    labs(x="source")


