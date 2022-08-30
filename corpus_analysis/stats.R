library(tidyverse)

stats_for_order_color_corr <- function() {
  color_df <- read.csv(file='~/Documents/word-ordering/wals/number_non_derived_color_categories.tsv', sep='\t', header=TRUE, stringsAsFactors=FALSE)
  order_df <- read.csv(file='~/Documents/word-ordering/wals/order_adj_noun.tsv', sep='\t', header=TRUE, stringsAsFactors=FALSE)
  joint_df <- merge(order_df, color_df, by='wals.code')
  joint_df <- joint_df[joint_df['description.x'] != 'Only internally-headed relative clauses', ]
  noun_adj_idx <- joint_df['description.x'] == 'Noun-Adjective'
  no_dom_order_idx <- joint_df['description.x'] == 'No dominant order'
  joint_df['value.x'][noun_adj_idx] = 3
  joint_df['value.x'][no_dom_order_idx] = 2
  
  industrialized_languages = list(
    'English',
    'French',
    'German',
    'Japanese',
    'Korean',
    'Mandarin',
    'Russian',
    'Spanish'
  )
  
  unindustrialized_joint_df <- joint_df[!(joint_df$name.x %in% industrialized_languages), ]
  
  ggplot(data=unindustrialized_joint_df) +
    geom_violin(mapping = aes(x = description.x, y = description.y)) +
    ggtitle('unindustrialized languages')
  
  relation <- lm(unindustrialized_joint_df$description.y~unindustrialized_joint_df$value.x)
  return(summary(relation))
}
  

# kinbank data
languages_df <- read.csv(file='~/Documents/word-ordering/kinbank/languages.csv')
languages_df <- rename(languages_df, Language_ID=ID)
forms_df <- read.csv(file='~/Documents/word-ordering/kinbank/forms.csv')
num_forms_df <- forms_df %>%
  group_by(Language_ID) %>%
  summarise(n_distinct(Value))

languages_and_num_forms_df <- merge(languages_df, num_forms_df, by='Language_ID')

# wals data
order_df <- read.csv(file='~/Documents/word-ordering/wals/order_adj_noun.tsv', sep='\t', header=TRUE, stringsAsFactors=FALSE)
language_codes_df <- read.csv(file='~/Documents/word-ordering/wals/languages.csv')
WALS_iso_df <- merge(order_df, language_codes_df, by.x='wals.code', by.y='ID')

# merge kinbank and wals
joint_df <- merge(WALS_iso_df, languages_and_num_forms_df, by='ISO639P3code')

# get ride of dupes
joint_df <- joint_df[!duplicated(joint_df$ISO639P3code),]

# get rid of this random category
joint_df <- joint_df[joint_df['description'] != 'Only internally-headed relative clauses', ]

# recode from 1-3
noun_adj_idx <- joint_df['description'] == 'Noun-Adjective'
no_dom_order_idx <- joint_df['description'] == 'No dominant order'
joint_df['value'][noun_adj_idx] = 3
joint_df['value'][no_dom_order_idx] = 2
joint_df <- rename(joint_df, num_unique_kin_terms='n_distinct(Value)')

ggplot(data=joint_df) +
  geom_violin(mapping = aes(x = description, y = num_unique_kin_terms)) +
  ggtitle('all languages')

relation <- lm(joint_df$value~joint_df$num_unique_kin_terms)

order_color_relation <- stats_for_order_color_corr()
#print('stats for order/color relationship')
#print(order_color_relation)
