from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from search import common_search, search_qualtrics, search_domo, search_fusion, search_bamboohr

# List of companies and their respective URLs and job search parameters
UtahCompanies = [
    {"companyName": "Sorenson", "FilteredURL": "https://recruiting2.ultipro.com/SOR1001SORE/JobBoard/1fe5e40e-4e0c-4b11-86e3-9a8e1f396263/?q=&o=postedDateDesc&f5=xIKn0bPiEku4pQdds-6CmQ+aqi5uoXa-kWy23u2oiGC-A+yJ9c9kLIjUqZ_nEk7RAAkA+wjOrzqEsFk6uoZC_VDMj2A", "className": "opportunity-link", "jobTitle": "Software Engineer"},
    {"companyName": "Cox", "FilteredURL": "https://jobs.coxenterprises.com/en/jobs/?search=&req=software+engineer&location=Utah%2C+USA&type=&posted=3&pagesize=20&locname=Utah&lat=39.3209801&lng=-111.0937311#results", "className": "stretched-link", "jobTitle": "Software Engineer I"},
    {"companyName": "Pluralsight", "FilteredURL": "https://pluralsight.wd1.myworkdayjobs.com/en-US/Careers/?q=software%20engineer&locationCountry=bc33aa3152ec42d4995f4791a106ed09", "className": "css-19uc56f", "jobTitle": "Software Engineer"},
    {"companyName": "Vivint", "FilteredURL": "https://vivint.wd5.myworkdayjobs.com/vivintjobs?q=software%20engineer&locations=f70e457a468e1084450fed99703b1deb", "className": "css-19uc56f", "jobTitle": "Software Engineer"},
]

def setup_webdriver():
    """Set up and return a Selenium WebDriver."""
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)

def find_utah_jobs():
    """Search for jobs across multiple companies using a single WebDriver instance."""
    driver = setup_webdriver()
    all_jobs = []
    try:
        print(f"\nSearching jobs for Qualtrics")
        qulatrics_jobs = search_qualtrics(driver)
        domo_jobs = search_domo(driver)
        fusion_jobs = search_fusion(driver)
        bamboohr_jobs = search_bamboohr(driver)
        all_jobs.extend(qulatrics_jobs)
        all_jobs.extend(domo_jobs)
        all_jobs.extend(fusion_jobs)
        all_jobs.extend(bamboohr_jobs)
        for company in UtahCompanies:
            print(f"\nSearching jobs for {company['companyName']}")
            jobs = common_search(driver, company)
            all_jobs.extend(jobs)
    finally:
        time.sleep(5)
        driver.quit()
    return all_jobs
