from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


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

blockedCompanies = ["epic", "synergisticit", "dice"]

levels = ["entry level", "internship", "associate"]


def search_utah_linkedin(driver):
    utah_jobs_url = "https://www.linkedin.com/jobs/search?keywords=Software%20Developer&location=Utah%2C%20United%20States&geoId=104102239&f_E=1%2C2%2C3&f_TPR=r604800&position=1&pageNum=0";
    utah_jobs = search_url_linkedin(utah_jobs_url, driver)
    return utah_jobs

def search_usa_linkedin(driver):
    usa_jobs_url = "https://www.linkedin.com/jobs/search?keywords=Software%20Developer&location=United%20States&geoId=103644278&f_TPR=r604800&f_E=1%2C2%2C3&position=1&pageNum=0";
    usa_jobs = search_url_linkedin(usa_jobs_url, driver)
    return usa_jobs

def search_url_linkedin(linkedinURL, driver):
    jobs_found = []
    driver.get(linkedinURL)
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # Find listings
    css_listings_selector = '.base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0.z-\[2\]'
    listings = driver.find_elements(By.CSS_SELECTOR, css_listings_selector)
    listings_num = len(listings)

    while listings_num <= 150:
        # Scroll down to bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(3)

        # Try to find and click the 'See more jobs' button if it's visible and clickable
        try:
            more_jobs_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more jobs']")
            if more_jobs_button.is_displayed():
                driver.execute_script("arguments[0].click();", more_jobs_button)
                # print("Clicked 'See more jobs' button.")
                time.sleep(3)  
        except Exception as e:
            print(f"No 'See more jobs' button or not clickable. {e}")

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page")
            break
        last_height = new_height

        # Find listings
        css_listings_selector = '.base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0.z-\[2\]'
        listings = driver.find_elements(By.CSS_SELECTOR, css_listings_selector)
        listings_num = len(listings)

    print("Listings Number ----------------------------------------------------------- ", len(listings))
    try:
        # for each job listing do the follwoing
        # click on job listing, find info, put an object, and add it to jobs_found list
        while len(listings) > 0:
            for listing in listings:
                try:
                    scrapeListing(listing, driver, jobs_found)
                    listings.remove(listing)
                except Exception as e:
                    print(f"Error processing a listing: {e}")
        print("Skipped elements: ", len(listings))
    except Exception as error:
        print(f"Error processing Linkedin: {error}")
    return jobs_found


def scrapeListing(listing, driver, jobs_found): 
    driver.execute_script("arguments[0].scrollIntoView(true);", listing)
    driver.execute_script("arguments[0].click();", listing)

    jobURL = listing.get_attribute('href')
                
    jobTitle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".top-card-layout__title.font-sans.text-lg.papabear\\:text-xl.font-bold.leading-open.text-color-text.mb-0.topcard__title"))
    ).text
    
    companyName = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".topcard__org-name-link.topcard__flavor--black-link"))
    ).text

    jobLocation = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".topcard__flavor.topcard__flavor--bullet"))
    ).text

    jobLevel = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".description__job-criteria-text.description__job-criteria-text--criteria"))
    ).text

    showMoreBtn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="i18n_show_more"]'))
    )
    driver.execute_script("arguments[0].click();", showMoreBtn)

    jobDesc = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".show-more-less-html__markup.relative.overflow-hidden"))
    ).text
    
    postTime = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".posted-time-ago__text.topcard__flavor--metadata"))
    ).text

    experience = findExperience(jobDesc)
    
    if (contains_keyword(jobTitle) and int(experience) < 3 and
        jobLevel.lower() in levels and
        (companyName.lower() not in blockedCompanies)): 
        jobs_found.append({
            "companyName": companyName,
            "jobTitle": jobTitle,
            "jobURL": jobURL,
            "jobLocation": jobLocation,
            "jobLevel": jobLevel,
            "experience": experience,
            "postTime": postTime,
        })

# Filtering ----------------------------
def contains_keyword(jobTitle):
    jobTitle = jobTitle.lower()
    for keyword in keywords:
        if keyword in jobTitle:
            return True
    return False

def findExperience(jobDesc):
    # Extended regex pattern to match different formats including "2+"
    pattern = re.compile(r'(\d+\+?|\d+-\d+)\s+years\'?\s+of\s+(\w+\s+)?experience', re.IGNORECASE)

    # Search the job description for this pattern
    matches = pattern.findall(jobDesc)

    # Print the results
    if matches:
        for match in matches:
            years_spec = match[0]
            # context = match[1].strip() if match[1] else "general"
            
            if '+' in years_spec:
                years = years_spec[:-1]  # remove the "+" and take the number before it
            elif '-' in years_spec:
                years = years_spec.split('-')[0]  # take the lower range in "2-5" format
            else:
                years = years_spec  # direct number like "2"
            
            # print(f"Years of experience required: {years}, Context: {context}")
            return years
    else:
        # print("No specific years of experience requirement found.")
        return 0
    

