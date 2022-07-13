import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_pages = pages[-2].get_text(strip=True)
    return int(last_pages)


def extract_job(html):
    company = html.find("h2", {"class": "mb4"})
    location_business = html.find("div", {"class": "fs-body1"})
    if location_business is not None:
        location, business = location_business.find_all("div", recursive=False)
        location = location.get_text(strip=True)
        business = business.get_text(strip=True)
    if company is not None:
        company_Name = company.find("a", {"class": "s-link"}).string
        return{'title': business,
               'company': company_Name,
               'location': location,
               'link': f"https://stackoverflow.com/jobs/companies/{company_Name}"}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "fl1"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs/companies?tl={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
