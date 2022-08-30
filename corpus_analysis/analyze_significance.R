# script to analyze significance of correlation between word order convention and number of nouns

library(tidyverse)

# load the file
df <- read_csv('processed-corr-data/word_order_noun_count.csv')

# code the word order variable
noun_adj_idx <- df['description'] == 'Noun-Adjective'
no_dom_order_idx <- df['description'] == 'No dominant order'
df['value'][noun_adj_idx] = 3
df['value'][no_dom_order_idx] = 2

# get rid of this category
df <- df[df['description'] != 'Only internally-headed relative clauses', ]

# get rid of languages from industrialized nations


# visualize data
ggplot(data=df) +
  geom_violin(mapping = aes(x = description, y = num_unique_words)) +
  ggtitle('all languages')

# linear model to determine correlation
relation <- lm(df$value ~ df$num_unique_words)

df %>%
  group_by(description) %>%
  summarise_at(vars(num_unique_words), list(name = mean))

df %>%
  group_by(description) %>%
  summarise_at(vars(num_unique_concepts), list(name = mean))

df %>%
  count(description)
