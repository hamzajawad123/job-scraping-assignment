from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

# 4 APPROVED SOURCES (Point 3)
sources = [
    {"name": "Vectara", "url": "https://job-boards.greenhouse.io/vectara", "role": "Software Engineer"},
    {"name": "Careem", "url": "https://job-boards.greenhouse.io/careem", "role": "Software Engineer"},
    {"name": "ByteDance", "url": "https://jobs.lever.co/bytedance", "role": "Software Engineer"},
    {"name": "NJP", "url": "https://www.njp.gov.pk", "role": "Software Engineer"}
]

all_links = []

for source in sources:
    print(f"🔄 Processing {source['name']}...")
    
    # 4.1 Open real browser session
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Remove # for headless
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
    
    # 4.2 Open careers page
    driver.get(source['url'])
    time.sleep(3)
    
    # 4.3 SEARCH target role
    try:
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='search'], .search-input, #search")))
        search_box.clear()
        search_box.send_keys(source['role'])
        search_box.send_keys(Keys.RETURN)
        print(f"✅ Searched '{source['role']}' on {source['name']}")
        time.sleep(4)
    except Exception as e:
        print(f"⚠️ No search box on {source['name']}, listing all")
    
    # 4.4 APPLY FILTERS (location Pakistan)
    try:
        # Common filter selectors
        filters = driver.find_elements(By.XPATH, "//*[contains(text(),'Pakistan') or contains(text(),'Lahore') or contains(text(),'Remote')]")
        if filters:
            filters[0].click()
            print(f"✅ Applied Pakistan filter")
            time.sleep(3)
    except:
        pass
    
    # 4.5 Scroll + Load More + Paginate
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0
    while scroll_count < 5:
        # CLICK Load More buttons
        try:
            load_more = driver.find_element(By.XPATH, "//button[contains(text(),'Load More') or contains(text(),'Show More') or contains(@class,'load-more')]")
            if load_more.is_enabled():
                driver.execute_script("arguments[0].click();", load_more)
                print("✅ Clicked Load More")
                time.sleep(3)
        except:
            pass
        
        # SCROLL JS listings
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_count += 1
    
    # 4.6 Collect URLs after fully loaded
    job_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/jobs/'], a[data-qa-job-link], .job-title a, .posting a")
    for link in job_links:
        url = link.get_attribute('href')
        if url and '/jobs/' in url:
            all_links.append({'company': source['name'], 'url': url})
    
    driver.quit()
    time.sleep(2)  # Polite delay (Point 12)

print(f"📄 Saved {len(all_links)} job links")

# Save intermediate output (Point 6.4, 10)
os.makedirs('data/raw', exist_ok=True)
with open('data/raw/job_links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['company', 'url'])
    writer.writeheader()
    writer.writerows(all_links[:50])  # Reasonable limit

print("✅ job_links.csv created in data/raw/")
