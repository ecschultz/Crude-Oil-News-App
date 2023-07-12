#!/usr/bin/env python
# coding: utf-8

# # Commercial Crude News Aggregator

### Words_of_interest = ['energy', 'oil', 'crude', 'natural gas', 'power', 'Shell']

import streamlit as st
from PIL import Image
import feedparser
import requests
import pandas as pd
from io import BytesIO
#from IPython.display import HTML

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

### create the column clickable_url based on the url column
def make_clickable(val):
    return '<a href="{}">{}</a>'.format(val,'Link to article')

df.style.format({'Link': make_clickable})

##result = df.to_html()



### Streamlit Web app ###

### Header
st.write("""
# COP Crude News 
Crude News app *NEWS*
""")

### COP Image
st.image(cop_image, caption='News Updated every ** Minutes')

### Add RSS Feed Dataframe to the app
#st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)


# Line to run script in command prompt -> python -m streamlit run 





