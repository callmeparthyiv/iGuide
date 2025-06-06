from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_apple_compare():
    
    base_url = "https://www.gsmarena.com/"
    devices = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(f'{base_url}apple-phones-f-48-0-p3.php')
        page.wait_for_selector('.makers')
        
        
        html = page.content()
        soup = BeautifulSoup(html,'html.parser')
        

        for li in soup.select('.makers li'):
            device_url =base_url + li.a['href']
            device_name = li.a.text.strip()
            image_url = li.img['src']
            
            device_data = scrape_device_details(context, device_url, device_name, image_url)
            
            
            if device_data:
                devices.append(device_data)
                print(f"Scraped : {device_name}")
        
            # next_page_btn = page.query_selector('a.prevnextbutton')
            # if(next_page_btn):
            #     next_page_btn.click()
            #     page.wait_for_selector('.makers')        
            #     time.sleep(2)

            

        browser.close()
    return pd.DataFrame(devices)
                
                
def scrape_device_details(context, device_url, device_name, image_url):
    page = context.new_page()
    try:
        
        page.goto(device_url)
        page.wait_for_selector('#specs-list')
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        

        specs = {"Device": device_name, "Image_url": image_url, "Source_url": device_url}
        
        for table in soup.select('#specs-list table'):
            
            header = table.find('th').text.strip()
            
                
                     
            for row in table.select('tr'): 
                if(row.find("td") == None):
                    continue 
                key = row.find("td", "ttl").text.strip()
                
                value = row.find("td", "nfo").text.strip()
                specs[f"{header} - {key}"] = value
        

        
        return specs
        
    except Exception as e:
        print(f"Error while scraping {device_url}: {str(e)}")
        return None
    finally:
        page.close()

df = scrape_apple_compare()
print(df.head())
df.to_csv('gsm_dataset_3.csv', index=False)
df.to_json('gsm_dataset_3.json', orient='records',indent=2)
print(f"\nScraping complete! Saved {len(df)} devices.")
