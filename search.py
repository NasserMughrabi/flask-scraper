from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def common_search(driver, company):
    """Perform a job search for a specified company."""
    jobs_found = []
    companyURL = company['FilteredURL']
    try:
        driver.get(companyURL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, company['className'])))
        titles = driver.find_elements(By.CLASS_NAME, company['className'])

        for title in titles:
            title_text = title.text
            titleURL = title.get_attribute('href')
            if title_text.lower() == company['jobTitle'].lower():
                jobs_found.append({"companyName": company['companyName'], "jobTitle": title_text, "jobURL": titleURL})
        if not jobs_found:
            jobs_found.append({"companyName": company['companyName'], "jobTitle": "None Available", "jobURL": companyURL})
    except Exception as e:
        print(f"Error processing {company['companyName']}: {str(e)}")
    return jobs_found

def search_qualtrics(driver):
    jobs_found = []
    qualtricsURL = "https://www.qualtrics.com/careers/us/en/search-results?m=3&keywords=software%20engineer"
    try:
        driver.get(qualtricsURL)
        titles = driver.find_elements(By.CLASS_NAME, 'job-title')
        locations = driver.find_elements(By.CLASS_NAME, 'job-location')
        
        for title, location in zip(titles, locations):
            title_text = title.text
            location_text = location.text
            if title_text.lower() == 'software engineer i' and 'utah' in location_text.lower():
                jobs_found.append({"companyName": "Qualtrics", "jobTitle": title_text, "jobURL": qualtricsURL})
        if not jobs_found:
            jobs_found.append({"companyName": "Qualtrics", "jobTitle": "None Available", "jobURL": qualtricsURL})        
    except Exception as error:
        print(f"Error processing Qualtrics: {error}")
    return jobs_found

def search_domo(driver):
    jobs_found = []
    domoURL = "https://www.domo.com/company/careers/all"
    try:
        driver.get(domoURL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
        titles = driver.find_elements(By.TAG_NAME, 'tr')
        for title in titles:
            title_text = title.text
            if 'software' in title_text.lower() and 'utah' in title_text.lower():
                jobs_found.append({"companyName": "Domo", "jobTitle": title_text, "jobURL": domoURL})
        if not jobs_found:
            jobs_found.append({"companyName": "Domo", "jobTitle": "None Available", "jobURL": domoURL})        
    except Exception as error:
        print(f"Error processing Domo: {error}")
    return jobs_found

def search_fusion(driver):
    jobs_found = []
    fusionURL = "https://fusion360agency.com/careers/"
    try:
        driver.get(fusionURL)
        titles = driver.find_elements(By.CSS_SELECTOR, "div > div > div > h3 > a")
        for title in titles:
            title_text = title.text
            titleURL = title.get_attribute('href')
            if 'developer' in title_text.lower():
                jobs_found.append({"companyName": "Fusion", "jobTitle": title_text, "jobURL": titleURL})
        if not jobs_found:
            jobs_found.append({"companyName": "Fusion", "jobTitle": "None Available", "jobURL": fusionURL})        
    except Exception as error:
        print(f"Error processing Fusion: {error}")
    return jobs_found
    

def search_bamboohr(driver):
    jobs_found = []
    bamboohrURL = "https://www.bamboohr.com/careers/#explore-all-bamboohr-jobs"
    try:
        driver.get(bamboohrURL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div > ul > div:nth-child(3) > div > div > div > h4 > a")))
        titles = driver.find_elements(By.CSS_SELECTOR, "div > ul > div:nth-child(3) > div > div > div > h4 > a")
        
        for title in titles:
            title_text = title.text
            titleURL = title.get_attribute('href')
            if 'developer' in title_text.lower():
                jobs_found.append({"companyName": "BambooHR", "jobTitle": title_text, "jobURL": titleURL})
        if not jobs_found:
            jobs_found.append({"companyName": "BambooHR", "jobTitle": "None Available", "jobURL": bamboohrURL})     
    except Exception as error:
        print(f"Error processing BambooHR: {error}")
    return jobs_found
    