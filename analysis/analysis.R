setwd("/Users/whitesi/Documents/Programming/Python/toronto-housing")

source("Postgres.R")
library(ggplot2)
source("helper.R")
library(data.table)
library(dtplyr)
library(dplyr)
library(scales)
library(zoo)
library(RColorBrewer)
library(plyr)

number_ticks <- function(n) {function(limits) pretty(limits, n)}
##display.brewer.all() ##view all palettes with this
palette <- brewer.pal("YlGnBu", n=9)
###########################################
############  DATA LOADING ################
###########################################

conn = getPSconn('postgres')
strSQL = ""

data = dbGetQuery(conn, strSQL) %>% setDT
#data = dbReadTable(conn, 'all_fsa_meta')

#######################################
############  PLOTTING ################
#######################################


ggplot(data[!(month %in% c('2017-02')) & property_type != 'Other',],
       aes(x=month, y=avg_list_price, label=count, fill=property_type)) +
  geom_bar(stat='identity', position="dodge") +  theme_dlin() +
  geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Listings', y='Median Listing Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = dollar,breaks=number_ticks(10)) +
  scale_fill_manual("Property Type",
                    values = c("Condo" = "#004977", "Detached" = "#D03027","Semi-Detached"="#018BBB", "Townhouse" = "#0EA218"))



ggplot(data[month != '2017-02' & property_type != 'Other',],
       aes(x=month, y=med_sale_price, label=count, fill=property_type)) +
  geom_bar(stat='identity', position="dodge") +  theme_dlin() +
  geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Sales', y='Median Sale Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = dollar,breaks=number_ticks(10)) +
  scale_fill_manual("Property Type",
                    values = c("Condo" = "#004977", "Detached" = "#D03027","Semi-Detached"="#018BBB", "Townhouse" = "#0EA218"))


sales = dbGetQuery(conn, "SELECT * FROM sale_records") %>% setDT
listings = dbGetQuery(conn, "SELECT * FROM list_records") %>% setDT

sales[, location:=NULL]
listings[, location:=NULL]
