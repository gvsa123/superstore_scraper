from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import numpy as np
import csv
import os


url = "https://www.realcanadiansuperstore.ca/Shop-by-Category/c/017377000000"
ROOT = "https://www.realcanadiansuperstore.ca/"
WAIT_TIME = 10
driver = webdriver.Chrome('/home/girard/Scripts/Python/WebScraping/WebDriver/chromedriver')
webpage = driver.get(url)

time.sleep(WAIT_TIME)

# Insert test.py here...

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

"""
#Product Class
<div class="product-tile__details"><div class="product-tile__details__info"><h3 class="product-tile__details__info__name"><a class="product-tile__details__info__name__link" href="/Food/Pantry/Baking-Ingredients/Extracts-%26-Colouring/Artificial-Vanilla-Extract/p/20430551_EA"><span class="product-name product-name--product-tile"><span class="product-name__item product-name__item--brand">No Name</span><span class="product-name__item product-name__item--name" title="Artificial Vanilla Extract">Artificial Vanilla Extract</span><span class="product-name__item product-name__item--package-size">250 mL</span></span></a></h3><div class="product-tile__details__info__text-badge"></div></div><div class="product-prices product-prices--product-tile product-prices--product-tile"><ul class="selling-price-list selling-price-list--product-tile,product-tile"><li class="selling-price-list__item"><span class="price selling-price-list__item__price selling-price-list__item__price--now-price"><span class="price__value selling-price-list__item__price selling-price-list__item__price--now-price__value">$3.48</span><span class="price__unit selling-price-list__item__price selling-price-list__item__price--now-price__unit">ea</span></span></li></ul><ul class="comparison-price-list comparison-price-list--product-tile comparison-price-list--product-tile"><li class="comparison-price-list__item"><span class="price comparison-price-list__item__price"><span class="price__value comparison-price-list__item__price__value">$1.39</span><span class="price__unit comparison-price-list__item__price__unit">/ 100mL</span></span></li></ul></div><div class="product-fulfillment-pickup-header product-fulfillment-pickup-header--product-tile"><span>Pickup only</span></div><div class="product-button-group product-button-group--product-tile product-button-group--add-to-list-button product-button-group--inactive"><button class="quantity-selector quantity-selector--update quantity-selector--horizontal quantity-selector--product-tile quantity-selector--add-to-cart quantity-selector--add-to-list-button" data-track="productAddToCartLocalize" data-track-product-quantity="1" data-track-link-name="add-to-cart-open" data-track-products-array="[{&quot;productSKU&quot;:&quot;20430551_EA&quot;,&quot;productName&quot;:&quot;Artificial Vanilla Extract&quot;,&quot;productBrand&quot;:&quot;No Name&quot;,&quot;productCatalog&quot;:&quot;grocery&quot;,&quot;productVendor&quot;:null,&quot;productPrice&quot;:&quot;3.48&quot;,&quot;productQuantity&quot;:1,&quot;dealBadge&quot;:null,&quot;loyaltyBadge&quot;:&quot;false&quot;,&quot;textBadge&quot;:null,&quot;productPosition&quot;:null,&quot;productOrderId&quot;:null,&quot;productVariant&quot;:null}]"><span>Add</span></button><div class="add-to-list add-to-list--product-tile"><div class="add-to-list__flyout add-to-list__flyout--product-tile"><div class="add-to-list__flyout__scroll-bar-container"><ul class="shopping-list-list shopping-list-list--product-tile"><li class="shopping-list-list__item"><button class="shopping-list-list__create-list" tabindex="-1"><span>Create a new list</span></button></li></ul></div></div></div></div></div>


#Product Item
<span class="product-name__item product-name__item--package-size">500 g</span>


#Product name
<a class="product-tile__details__info__name__link" 
href="/Food/Meat-%26-Seafood/Pork/Bacon/Maple-Flavoured-Naturally-Smoked-Bacon/p/20117351_EA">
<span class="product-name product-name--product-tile"><span class="product-name__item product-name__item--brand">President's Choice</span><span class="product-name__item product-name__item--name" title="Maple Flavoured Naturally Smoked Bacon">Maple Flavoured Naturally Smoked Bacon</span><span class="product-name__item product-name__item--package-size">500 g</span></span></a>

<span class="product-name__item product-name__item--name" title="Maple Flavoured Naturally Smoked Bacon">Maple Flavoured Naturally Smoked Bacon</span>


#Price
<span class="price__value selling-price-list__item__price selling-price-list__item__price--now-price__value">$3.48</span>
<ul class="selling-price-list selling-price-list--product-tile,product-tile"><li class="selling-price-list__item"><span class="price selling-price-list__item__price selling-price-list__item__price--now-price"><span class="price__value selling-price-list__item__price selling-price-list__item__price--now-price__value">$3.48</span><span class="price__unit selling-price-list__item__price selling-price-list__item__price--now-price__unit">ea</span></span></li></ul>

# Region Selector
//*[@id="site-layout"]/div[5]/div[2]/div/div/ul/li[1]/button

"""

# Get list of grocery aisles.
AISLE = []
for a in soup.find_all('a', class_="browse-by-aisle__list__item"):
	AISLE.append((a['href']))

# Print AISLE
print("Scraping the following aisles: ")
for i in AISLE:
	print(i)

# Get product name and price; create dataframe
ITEM = []
PRICE = []

# Iterate over aisles
print("\nProcessing...\n")
for aisle in AISLE:
	webpage = driver.get(ROOT+aisle)
	time.sleep(WAIT_TIME)
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	print(str(ROOT+aisle))
	
	for item in soup.find_all('div', class_='product-tile__details'):
		name = item.find('a', class_='product-tile__details__info__name__link')
		ITEM.append(name.findChild().text)
		val = item.find('ul', class_='selling-price-list')
		PRICE.append(val.findChild().text[:-2])

# Processing prices
PRICE_CLEAN = []
for i in PRICE:
	if i[-1] == ')':
		PRICE_CLEAN.append(i[:-6])
	elif i[-2] == '/':
		PRICE_CLEAN.append(i[:-2])
	elif i[-3] == '/':
		PRICE_CLEAN.append(i[:-3])
	elif i[-4] == '/':
		PRICE_CLEAN.append(i[:-4])
	else:
		PRICE_CLEAN.append(i)

# Create DataFrame
df = pd.DataFrame(list(zip(ITEM, PRICE_CLEAN)), columns = ['Item', 'Price'])
print("Dataframe created...")

# Increment filename
def filename():
	i = 0
	global FILENAME
	
	while os.path.exists("cart%s.csv" % i):
		i += 1

	print("New file created: cart%s.csv" % i)
	FILENAME = ("cart%s.csv" % i)

filename()

df.to_csv(FILENAME)
print("Done. Go and change the world!")


























