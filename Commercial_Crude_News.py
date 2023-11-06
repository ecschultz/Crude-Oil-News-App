#!/usr/bin/env python
# coding: utf-8

                                                    ### Commercial Crude News Aggregator ###

import streamlit as st
from PIL import Image
import feedparser
import requests
import pandas as pd
from io import BytesIO
import datetime as dt
from datetime import datetime, timedelta
#from IPython.display import HTML

### Words of interest, pls add as the team sees fit
Words_of_interest = ['energy', 'oil', 'crude', 'natural gas', 'power', 'Shell', 'Chevron', 'commodity', 'Vitol', 'SLB',\
                    'Halliburton', 'drillers', 'TC Energy', 'Columbia', 'natural gas', 'gasoline', 'naphtha', 'pipeline',\
                    'maintenance', 'North Sea','emissions', 'economy', 'propane', 'butane', 'Henry Hub', 'inventories',\
                    'MMBtu', 'EIA', 'barrel', 'tanker', 'Nigeria','petroleum', 'midstream','refinery', 'refining', 'Brent',\
                    'West Texas Intermediate', 'Strategic Petroleum Reserve', 'Alaska', 'maritime','Russia', 'Russian',\
                    'Saudi Arabia', 'UAE', 'OPEC', 'Permian', 'Bakken', 'Eagle Ford', 'Delaware', 'Phillips 66', \
                    'Pioneer Natural Resources', 'petrochemical', 'offshore', 'rig', 'IMF', 'GDP', 'shale', 'Oil and Gas']

### ConocoPhillips Header
cop_image = 'https://raw.githubusercontent.com/ecschultz/Conoco/main/COP.jpg'

### Collect RSS News feed links -> feel free to add feeds to this list
rawrss = [
    'https://www.cnbc.com/id/19836768/device/rss',
    'https://www.opec.org/opec_web/en/pressreleases.rss',
    'https://www.spglobal.com/commodityinsights/en/rss-feed/oil#',
    'https://www.spglobal.com/commodityinsights/en/rss-feed/petrochemicals',
    'https://www.spglobal.com/commodityinsights/en/rss-feed/shipping',
    'https://www.rigzone.com/news/rss/rigzone_finance.aspx',
    'https://www.rigzone.com/news/rss/rigzone_production.aspx',
    'https://www.energyintel.com/rss-feed',
    'https://www.eia.gov/petroleum/weekly/includes/week_in_petroleum_rss.xml',
    'http://purl.org/rss',
    'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'https://feeds.bloomberg.com/markets/news.rss',
    'https://oilprice.com/rss/main',
    'https://oilandgas.einnews.com/rss/81qK6_Vu9bAkFhbP',
    'https://energy.einnews.com/rss/hnbgM_dmoXbIESYV',
    'https://oilandgas.einnews.com/rss/uQDUGy2gjuMBapAb',
    'https://oilandgas.einnews.com/rss/qYXAS5NnVzQxdOq_',
    'https://energy.einnews.com/rss/YtuHxCVlIq3H0L3W',
    'https://energy.einnews.com/rss/RvPOsHiergpb7rzB',
    'http://search.yahoo.com/mrss/',
    'https://www.reutersagency.com/feed/?best-sectors=commodities-energy&#038;post_type=best" rel="self" type="application/rss+xml',

    'https://www.spglobal.com/commodityinsights/en/rss-feed/oil',
    'https://www.spglobal.com/commodityinsights/en/rss-feed/blogs',
    'https://www.cer-rec.gc.ca/rss/rssfd.aspx?l=e&c=catNR',
    'https://www.cer-rec.gc.ca/rss/rssfd.aspx?l=e&c=catER',
    'https://www.eia.gov/rss/todayinenergy.xml',
    'https://www.eia.gov/petroleum/weekly/includes/week_in_petroleum_rss.xml',
    'https://www.eia.gov/rss/press_rss.xml',
    
    ]  

feeds = [] # list of feed objects
for url in rawrss:
    feeds.append(feedparser.parse(url))

posts = [] # list of posts [(title1, link1, summary1), (title2, link2, summary2) ... ]
for feed in feeds:
    for post in feed.entries:
        posts.append((post.title, post.link, post.summary, post.published))

df = pd.DataFrame(posts, columns=['Title', 'Link', 'Summary','Date']) # pass data to init

df['HyperLink'] = df['Link']

### Source Column
df["Source"] = df["HyperLink"].str.split(".").str[1]

### Rearrange the column order and add HyperLink column
df = df[['Date', 'Source','Title', 'Summary', 'Link']]

# ### Sort the articles by the most recent at the top
# df.sort_values(by='Date', ascending=False)

# ### Setting Character Limit on Summary Column
# df["Summary"] = df["Summary"].str[:100]


Day = dt.datetime.today().strftime("%d") # if the column is not in datetime format
Month = dt.datetime.today().strftime("%b")

df['Date'] = df['Date'].astype('string')   # Find all dates w/ month and date of today
df = df[df['Date'].str.contains(Day) & df['Date'].str.contains(Month)]

df = df.loc[df['Title'].apply(lambda x: any(w in x for w in Words_of_interest))]    # Filter df for only words of interest

### create the column clickable_url based on the url column
def make_clickable(val):
    return '<a href="{}">{}</a>'.format(val,'Link to article')

df.style.format({'Link': make_clickable})
df['Link'] = df['Link'].apply(make_clickable)
# df = df.to_html(escape=False)



    ### Streamlit Web app deployment ###

### Header
st.write("""
# COP Crude News 
Crude News app *NEWS*
""", use_container_width = True)

### COP Image
st.image(cop_image, caption='News Updated Daily')

### Add RSS Feed Dataframe to the app
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
####################st.write(df, unsafe_allow_html=True, use_container_width = True) 

# Line to run script in command prompt -> python -m streamlit run 





