from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


import time
import pandas as pd
import numpy as np
import csv
import os

# SET ENV TO RUN ON PI ~ Thanks Disavowed!
# python3 -m venv .env && source .env/bin/activate && pip install -r requirements.txt

"""
Created to capture a snapshot of the prices from the local superstore during the COVID pandemic to be later run on data analytic tools.
# HTML ELEMENTS:
#Product Class
<div class="product-tile__details"><div class="product-tile__details__info"><h3 class="product-tile__details__info__name"><a class="product-tile__details__info__name__link" href="/Food/Pantry/Baking-Ingredients/Extracts-%26-Colouring/Artificial-Vanilla-Extract/p/20430551_EA"><span class="product-name product-name--product-tile"><span class="product-name__item product-name__item--brand">No Name</span><span class="product-name__item product-name__item--name" title="Artificial Vanilla Extract">Artificial Vanilla Extract</span><span class="product-name__item product-name__item--package-size">250 mL</span></span></a></h3><div class="product-tile__details__info__text-badge"></div></div><div class="product-prices product-prices--product-tile product-prices--product-tile"><ul class="selling-price-list selling-price-list--product-tile,product-tile"><li class="selling-price-list__item"><span class="price selling-price-list__item__price selling-price-list__item__price--now-price"><span class="price__value selling-price-list__item__price selling-price-list__item__price--now-price__value">$3.48</span><span class="price__unit selling-price-list__item__price selling-price-list__item__price--now-price__unit">ea</span></span></li></ul><ul class="comparison-price-list comparison-price-list--product-tile comparison-price-list--product-tile"><li class="comparison-price-list__item"><span class="price comparison-price-list__item__price"><span class="price__value comparison-price-list__item__price__value">$1.39</span><span class="price__unit comparison-price-list__item__price__unit">/ 100mL</span></span></li></ul></div><div class="product-fulfillment-pickup-header product-fulfillment-pickup-header--product-tile"><span>Pickup only</span></div><div class="product-button-group product-button-group--product-tile product-button-group--add-to-list-button product-button-group--inactive"><button class="quantity-selector quantity-selector--update quantity-selector--horizontal quantity-selector--product-tile quantity-selector--add-to-cart quantity-selector--add-to-list-button" data-track="productAddToCartLocalize" data-track-product-quantity="1" data-track-link-name="add-to-cart-open" data-track-products-array="[{&quot;productSKU&quot;:&quot;20430551_EA&quot;,&quot;productName&quot;:&quot;Artificial Vanilla Extract&quot;,&quot;productBrand&quot;:&quot;No Name&quot;,&quot;productCatalog&quot;:&quot;grocery&quot;,&quot;productVendor&quot;:null,&quot;productPrice&quot;:&quot;3.48&quot;,&quot;productQuantity&quot;:1,&quot;dealBadge&quot;:null,&quot;loyaltyBadge&quot;:&quot;false&quot;,&quot;textBadge&quot;:null,&quot;productPosition&quot;:null,&quot;productOrderId&quot;:null,&quot;productVariant&quot;:null}]"><span>Add</span></button><div class="add-to-list add-to-list--product-tile"><div class="add-to-list__flyout add-to-list__flyout--product-tile"><div class="add-to-list__flyout__scroll-bar-container"><ul class="shopping-list-list shopping-list-list--product-tile"><li class="shopping-list-list__item"><button class="shopping-list-list__create-list" tabindex="-1"><span>Create a new list</span></button></li></ul></div></div></div></div></div>
#Product Item
<span class="product-name__item product-name__item--package-size">500 g</span>
#Product name
<a class="product-tile__details__info__name__link"href="/Food/Meat-%26-Seafood/Pork/Bacon/Maple-Flavoured-Naturally-Smoked-Bacon/p/20117351_EA"><span class="product-name product-name--product-tile"><span class="product-name__item product-name__item--brand">President's Choice</span><span class="product-name__item product-name__item--name" title="Maple Flavoured Naturally Smoked Bacon">Maple Flavoured Naturally Smoked Bacon</span><span class="product-name__item product-name__item--package-size">500 g</span></span></a><span class="product-name__item product-name__item--name" title="Maple Flavoured Naturally Smoked Bacon">Maple Flavoured Naturally Smoked Bacon</span>
#Price
<span class="price__value selling-price-list__item__price selling-price-list__item__price--now-price__value">$3.48</span><ul class="selling-price-list selling-price-list--product-tile,product-tile"><li class="selling-price-list__item"><span class="price selling-price-list__item__price selling-price-list__item__price--now-price"><span class="price__value selling-price-list__item__price selling-price-list__item__price--now-price__value">$3.48</span><span class="price__unit selling-price-list__item__price selling-price-list__item__price--now-price__unit">ea</span></span></li></ul>
# Region Selector
//*[@id="site-layout"]/div[5]/div[2]/div/div/ul/li[1]/button
"""

url1 = "https://www.realcanadiansuperstore.ca/Shop-by-Category/c/017377000000"
url0 = "https://www.realcanadiansuperstore.ca/"

ITEM = []
PRICE = []
PRICE_CLEAN = []


	
if os.getcwd() != '/home/girard/Scripts/Python/WebScraping/superstore_scraper':
	DRIVER_PATH = ''
	WAIT_TIME = 20
else:
	DRIVER_PATH = '/home/girard/Scripts/Python/WebScraping/WebDriver/chromedriver'
	WAIT_TIME = 10
	
print("Setting webdriver path to: " + DRIVER_PATH)
print("Setting WAIT_TIME to " + str(WAIT_TIME))


driver = webdriver.Chrome(DRIVER_PATH)

webpage = driver.get(url1)
wait = WebDriverWait(driver,10,2)
scroll = driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


# Create bs4 instance
time.sleep(WAIT_TIME)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Get list of grocery aisles.
AISLE = []
for a in soup.find_all('a', class_="browse-by-aisle__list__item"):
	AISLE.append((a['href']))

# Print AISLE
print("Scraping the following aisles: ")
for i in AISLE:
	print(i)

def Click_Event():
	
	"""Initial waiting for clickable elements ; Scroll to bottom and wait for element_to_be_clickable"""
	
	while True:
		try:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more-button')))
			
		except TimeoutException:
			print("Loading...")
			time.sleep(WAIT_TIME)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more-button')))
		
		except NoSuchElementException as err:
			print(err)
			continue
		
		else:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			BUTTON = driver.find_elements_by_tag_name('button')
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			BUTTON[-4].click()
			print("...")
		
		finally:
			break

def Max_Load():
	
	"""Extracts maximum number of times to loop over Click_Event() based on NUM of RESULTS """
		
	NUM = []
	
	for i in RESULTS.text:
		NUM.append(i)
		
	STR = "".join(NUM) # Creates str from list
	
	for i in STR.split():
		if i.isdigit():
			return i

def Load_Count():
	
	"""Tracks number of times to loop over Click_Event() based on NUM of RESULTS """
	
	NUM = []
	LIST = []
	TEMP_NUM = []	
	
	for i in RESULTS.text:
		NUM.append(i)
		
	STR = "".join(NUM) # Creates str from list
	
	for x in STR.split(" "):
		LIST.append(x)
	
	TEMP_NUM.append(LIST[0].split("-"))
	
	return TEMP_NUM[0][1]

def Count_Load():
	
	"""Counter to monitor maximum loaded items """
	
	x = 0
	MAX = int(MAX_LOAD) # Sets option to iterate over ALL items. 
	print(f"Loading items up to {MAX} items... ")
	
	try:
		while x < MAX:
			Click_Event()
			x += int(LOAD_COUNT)
	
	except KeyboardInterrupt:
		pass

def Soup_Extraction(ITEM, PRICE):
	
	print("Soup extraction...")
	time.sleep(WAIT_TIME)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser") # Different soup flavour

	for item in soup.find_all('div', class_='product-tile__details'):
		name = item.find('a', class_='product-tile__details__info__name__link')
		ITEM.append(name.findChild().text)
		val = item.find('ul', class_='selling-price-list')
		PRICE.append(val.findChild().text[:-2])

def Price_Clean(PRICE, PRICE_CLEAN):
	"""Parsing PRICE to PRICE_CLEAN"""
	
	print("Processing prices...")
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
	print(f"Processed {len(PRICE_CLEAN)} items.")

print("\nAISLE[] created. Processing...\n") # Iterate over aisles

def Aisle():
	global RESULTS
	global MAX_LOAD
	global LOAD_COUNT
	
	for aisle in AISLE: # Use [:] for testing		
		webpage = driver.get(url0+aisle)
		print("Loading ---> " + str(url0+aisle) + "\n")
		time.sleep(2)
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		time.sleep(2)
	
		try:
			RESULTS = driver.find_element(By.CLASS_NAME, 'pagination')
			print("RESULTS found.")
			MAX_LOAD = Max_Load()
			LOAD_COUNT = Load_Count()
			Count_Load()
			print("Aisle loaded.")

		except NoSuchElementException as err: # Catch Aisle with different data
			print(err)		
			print("Continue with making soup anyway...")	
		
		finally:
			Soup_Extraction(ITEM, PRICE)
			print("Downloaded " + str(url0+aisle) + "\n")
			print(f"{len(ITEM)} items in ITEM with {len(PRICE)} matching PRICES.")

Aisle()

def filename(ITEM, PRICE, PRICE_CLEAN):
	"""Database function"""
	
	i = 0
	global FILENAME
	
	Price_Clean(PRICE, PRICE_CLEAN) # Parse PRICE into PRICE_CLEAN
	df = pd.DataFrame(list(zip(ITEM, PRICE_CLEAN)), columns = ['Item', 'Price']) # Create DataFrame
	print("Dataframe created...")
	
	while os.path.exists("cart%s.csv" % i): # Increment filename
		i += 1

	print("New file created: cart%s.csv" % i)
	FILENAME = ("cart%s.csv" % i)
	df.to_csv(FILENAME)

filename(ITEM, PRICE, PRICE_CLEAN)
print("Done. Go and change the world!")


























