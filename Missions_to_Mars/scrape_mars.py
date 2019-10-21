#!/usr/bin/env python
# coding: utf-8

#import dependencies
from splinter import Browser
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time




def init_browser(headless=False, exec_path="/usr/local/bin/chromedriver"):
    """
    initializes and returns a a splinter Browser.
    """
    executable_path = {"executable_path": exec_path, "headless": headless}
    return Browser("chrome", **executable_path)

def scrape():
    browser = init_browser(headless=True)
    mars_data_dict = {}
    
    ### Nasa Mars News
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #find recent news article, date and title
    article = soup.find("div", class_="list_text").text
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    news_date = soup.find("div", class_="list_date").text
    
    mars_data_dict['article'] = article
    mars_data_dict['news_title'] = news_title
    mars_data_dict['news_p'] = news_p
    mars_data_dict['news_date'] = news_date
    
    
    ###JPL Mars Space###
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    ##Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a 
    #variable called `featured_image_url`.
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #using beautiful soup to find image
    image_page = soup.select("#full_image")[0]["data-link"]

    full_image_url = "https://jpl.nasa.gov" + image_page

    browser.visit(full_image_url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    full_img_path = soup.select("#page > section.content_page.module > div > article > figure > a > img")[0]['src']
    mars_data_dict['featured_image'] = "https://jpl.nasa.gov" + full_img_path
    
    
    ### Mars Weather ###

    #visit URL 
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    time.sleep(5)

    #scrape the latest Mars weather tweet from the page 
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #find mars weather info
    weather_list_info = []

    for weather_info in soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_list_info.append(weather_info.text)
    
    #create a variable for mars weather info
    mars_weather = weather_list_info[0]

    mars_data_dict["mars_weather"] = mars_weather


    ### Mars Facts ###

    #Visit the Mars Facts webpage
    mars_fact_url = "https://space-facts.com/mars/"
    browser.visit(mars_fact_url)

    #create dataframe 
    df_mars_fact = pd.read_html("https://space-facts.com/mars/")

    df_mars_fact = pd.DataFrame(df_mars_fact[0])

    #convert dataframe to html
    mars_data_dict['df_mars_fact'] = df_mars_fact.to_html()


    ### Mars Hemispheres ###
    
    #visit URL 
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)

    #scrape the latest Mars weather tweet from the page 
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    full_image_url = []
    hemisperes_title = []

    image_domain = "https://astrogeology.usgs.gov"

    for img_title in soup.find_all('div',class_="description"):
        hemisperes_title.append(img_title.find('h3').text)

    item_divs = soup.select("#product-section > div.collapsible.results div.item > a > img")

    for item in item_divs:
        full_image_url.append(image_domain + item.get('src'))

        
    hemisphere_image_url = [{"title": hemisperes_title[i], "img_url": full_image_url[i]} for i in range(len(hemisperes_title))]

    
    mars_data_dict['hemisphere_image'] = hemisphere_image_url
    
    return mars_data_dict 

