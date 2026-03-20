import scrapy
import pandas as pd
from scrapy_project.items import JobItem

class JobSpider(scrapy.Spider):
    name = "job_spider"
    
    # Custom settings to look more human and not get blocked by NJP
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'ROBOTSTXT_OBEY': False, # NJP may block bots via robots.txt
        'DOWNLOAD_DELAY': 1.5    # Being polite
    }

    def start_requests(self):
        # Note: I changed 'url' to 'url' because your CSV column is lowercase
        df = pd.read_csv("../data/raw/job_links.csv")
        for index, row in df.iterrows():
            yield scrapy.Request(
                url=row['url'], 
                callback=self.parse, 
                meta={'company_from_csv': row['company']}
            )

    def parse(self, response):
        item = JobItem()
        url = response.url
        item['job_url'] = url
        item['company_name'] = response.meta.get('company_from_csv')

        if "greenhouse.io" in url:
            # SELECTORS FOR GREENHOUSE
            item['job_title'] = response.css('h1.app-title::text').get(default='').strip() or \
                               response.css('.header-container h1::text').get(default='').strip()
            
            item['location'] = response.css('div.location::text').get(default='Remote').strip()
            
            # Get description
            desc_list = response.css('#content ::text').getall()
            description = " ".join(desc_list).strip()
            item['job_description'] = description

        elif "njp.gov.pk" in url:
            # SELECTORS FOR NJP (Adjusted for their specific HTML structure)
            item['job_title'] = response.css('h2.job-title::text, h1::text').get(default='NJP Job').strip()
            item['location'] = response.css('.location-class::text, .job-info::text').get(default='Pakistan').strip()
            
            desc_list = response.css('.job-description ::text, .description ::text').getall()
            item['job_description'] = " ".join(desc_list).strip()

        # Skill Extraction Logic
        keywords = ['Python', 'SQL', 'React', 'Management', 'Engineering', 'Teacher', 'PHP']
        desc_text = item.get('job_description', '').lower()
        found_skills = [k for k in keywords if k.lower() in desc_text]
        item['required_skills'] = ", ".join(found_skills)

        # Only yield if we actually found a title (prevents junk rows)
        if item['job_title']:
            yield item