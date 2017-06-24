setwd("/Users/whitesi/Documents/Programming/Python/toronto-housing/analysis")

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


sold = dbGetQuery(conn, "SELECT * FROM sale_records") %>% setDT
notify('sold load complete')
list = dbGetQuery(conn, "SELECT * FROM list_records") %>% setDT
notify('list load complete')
#data = dbReadTable(conn, 'all_fsa_meta')


############################################
############  DATA CLEANING ################
############################################
sold[, location := NULL]
list[, location := NULL]

# days on market
sold[, dom := as.integer(solddate-inputdate)]

sold[, region := city]
sold[substr(city,1,7) == 'Toronto', region := 'Toronto']

sold[, yymm := substr(solddate,1,7)]

#######################################
############  PLOTTING ################
#######################################

main_types = c('Detached', 'Condo Apt', 'Semi-Detached', 'Att/Row/Twnhouse','Condo Townhouse')


ggplot(sold[region=='Toronto' & type %in% main_types, 
            .(med_sale_price=as.integer(median(soldprice)), count=.N) ,by=.(yymm,type)],
       aes(x=yymm, y=med_sale_price, label=count, fill=type)) +
  geom_bar(stat='identity', position="dodge") +  theme_dlin() +
  geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Sales', y='Median Sale Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = dollar,breaks=number_ticks(10))

ggplot(sold[region=='Toronto' & type %in% main_types, 
            .(med_sale_price=mean(soldprice), count=.N, dom = mean(dom)) ,by=.(yymm,type)],
       aes(x=yymm, y=dom, label=count, fill=type)) +
  geom_bar(stat='identity', position="dodge") +  theme_dlin() +
  # geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Sales', y='Average Days on the Market', x='Date', fill='Property Type') +
  scale_y_continuous(labels = comma, breaks=number_ticks(10))






##PLOTTING TO DO:

##SOLD


##LIST
# track number of price changes