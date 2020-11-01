# superstore_scraper project

This project was intended to create a snapshot of the grocery item prices at the beginning of the 2020 pandemic, in order to be able to test the hypothesis of rising prices during the first few weeks of the COVID-19 outbreak.

## Method

An custom data miner (`superstore_main.py`) was created that scraped the superstore website in order to gather the prices of grocery items, which was to be later used as the baseline for comparing future prices. These prices are then saved to disk and a subsequent scrape was initiated after the baseline prices had been established. The data is then further processed and analysed. See the `data_cleaning.ipynb` file for the actual analysis.