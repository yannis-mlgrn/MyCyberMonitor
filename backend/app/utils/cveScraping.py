"""
author : @yannis_mlgrn
Scraping tool to extract CVE links from the Vulmon website.
This script uses Selenium to automate the process of navigating
and gather information about trending CVEs.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from app.models.cve import CVE
import json


def get_cve_list(n: int = 5):
    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Step 1: Aller sur la page d'accueil
    url = "https://vulmon.com/trends"
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr"))
    )

    # Step 2: Récupérer la liste des CVE (id + link)
    rows = driver.find_elements(By.XPATH, "//tr")
    cve_links = []

    for row in rows[:n]:
        try:
            cve_link_elem = row.find_element(By.XPATH, ".//td[1]/a")
            cve_id = cve_link_elem.text.strip()
            cve_link = "https://vulmon.com/vulnerabilitydetails?qid=" + cve_id
            cve_links.append((cve_id, cve_link))
        except Exception:
            continue

    cve_list = []

    # Step 3: Pour chaque CVE, ouvrir la page détail
    for cve_id, cve_link in cve_links:
        driver.get(cve_link)
        time.sleep(2)  # Remplacer plus tard par WebDriverWait propre

        try:
            # Get CVSS score
            cvss_elem = driver.find_element(
                By.XPATH,
                (
                    "/html/body/div[3]/div/div[1]/div[1]/div/div/a/div/div/"
                    "div[1]"
                )
            )
            cvss_score = cvss_elem.text.strip()
            # Get the short description
            desc_elem = driver.find_element(
                By.CSS_SELECTOR, "p.jsdescription1.content_overview"
            )
            desc_html = desc_elem.get_attribute("innerHTML")
            short_description = desc_html.split('<br>')[0].strip()
        except Exception:
            cvss_score = None
            short_description = "No description available"

        cve_list.append(CVE(
            id=cve_id,
            cvss=(
                float(cvss_score)
                if cvss_score and cvss_score != 'NA'
                else None
            ),
            description=short_description,
            link=cve_link
        ))

    driver.quit()

    # Save the CVE list to a JSON file
    json_object = json.dumps([cve.model_dump() for cve in cve_list], indent=4)
    with open('app/data/cve.json', "w") as outfile:
        outfile.write(json_object)
