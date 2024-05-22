from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


jobTitles = ["software engineer", "software developer", "web developer", 
             "full-stack engineer", "full stack engineer", 
             "full-stack developer", "full stack developer", 
             "frontend engineer", "front-end engineer"
             "frontend developer", "front-end developer"
             "backend engineer", "back-end engineer"
             "backend developer", "back-end developer"
             ""]

keywords = ["software", "developer", "web"
            "frontend", "front-end", "front end",
            "fullstack", "full-stack", "full stack",
            "backend", "back-end", "back end"]



def search_linkedin(driver):
    jobs_found = []
    linkedinURL = "https://www.linkedin.com/jobs/search?keywords=Software%20Developer&location=Utah%2C%20United%20States&geoId=104102239&f_E=1%2C2%2C3&f_TPR=r604800&position=1&pageNum=0"
    try:
        # navigate to linkedin filtered URL
        driver.get(linkedinURL)

        # Find listings
        css_listings_selector = '.base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0.z-\[2\]'
        listings = driver.find_elements(By.CSS_SELECTOR, css_listings_selector)
            
        # for each job listing do the follwoing
        #   1. click on job listing
        #   2. find title, URL, and company name
        #   3. put the above in an object and add it to jobs_found list
        #   4. 
        for listing in listings:
            driver.execute_script("arguments[0].click();", listing)  # Using JavaScript to click to avoid issues with hidden elements or overlays.
            try:
                jobURL = listing.get_attribute('href')
                
                jobTitle = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".top-card-layout__title.font-sans.text-lg.papabear\\:text-xl.font-bold.leading-open.text-color-text.mb-0.topcard__title"))
                ).text
                
                companyName = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".topcard__org-name-link.topcard__flavor--black-link"))
                ).text

                jobLocation = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".topcard__flavor.topcard__flavor--bullet"))
                ).text

                jobLevel = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".description__job-criteria-text.description__job-criteria-text--criteria"))
                ).text

                print(jobTitle, companyName, jobLocation, jobLevel)
                print(jobURL, "\n")

                if contains_keyword(jobTitle) and ("utah" in jobLocation.lower() or "ut" in jobLocation.lower()): 
                    jobs_found.append({
                        "companyName": companyName,
                        "jobTitle": jobTitle,
                        "jobURL": jobURL,
                    })
            except Exception as e:
                print(f"Error processing a listing: {e}")

    except Exception as error:
        print(f"Error processing Linkedin: {error}")
    return jobs_found


def contains_keyword(jobTitle):
    jobTitle = jobTitle.lower()
    for keyword in keywords:
        if keyword in jobTitle:
            return True
    return False