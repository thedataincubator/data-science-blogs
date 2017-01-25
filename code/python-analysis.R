library(tidyverse)
library(magrittr)
library(stringr)

df <- read_csv("../data/python-data.csv")

rank <- df %>%
    gather(type, count, -package) %>%
    group_by(type) %>%
    mutate(scaled = scale(count) %>% round(., 2)) %>%
    select(-count) %>%
    spread(type, scaled) %>%
    rowwise() %>%
    mutate(Github=mean(c(forks, stars)) %>% round(2),
           Stack=mean(c(so_question_count, so_tag_counts)) %>% round(2),
           Overall=mean(c(Github, Stack)) %>% round(2)) %>%
    arrange(desc(Overall)) %>%
    select(package, Overall, Github, Stack)


write.csv(rank, "../python-ranks.csv", )
