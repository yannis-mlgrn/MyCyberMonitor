"""
author : @yannis_mlgrn
Scraping tool to extract CVE links from the Vulmon website.
This script uses Selenium to automate the process of navigating
and gather informations about trending CVEs.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from app.models.cve import CVE


def get_cve_list(n:int=5) -> list[CVE]:
    """
    Scrape the latest CVEs from the Vulmon website.
    Returns a list of dictionaries containing CVE ID, description, and link.
    """
    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Launch Chrome
    driver = webdriver.Chrome(options=options)

    # Navigate to the page with the latest CVEs
    url = "https://vulmon.com/trends"
    driver.get(url)
    # Small pause to allow JS to load
    time.sleep(3)
    # Retrieve all <tr> elements containing CVEs
    rows = driver.find_elements(By.XPATH, "//tr")

    cve_list = []

    # Parse each row
    for row in rows[:n]:
        try:
            cve_link_elem = row.find_element(By.XPATH, ".//td[1]/a")

            cve_list.append(CVE(
                id=cve_link_elem.text.strip(),
                description=row.find_element(By.XPATH, ".//td[2]")
                .text.strip(),
                link=cve_link_elem.get_attribute("href")
            ))
        except Exception:
            continue

    driver.quit()
    return cve_list
