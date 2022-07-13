import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    jobTitle = html.find("h2", {"class": "jobTitle"})
    title = jobTitle.find("span").string
    if title == "new":
        title = jobTitle.find_all("span")[1].string
    company = html.find("span", {"class": "companyName"}).string
    location = html.find("div", {"class": "companyLocation"}).string
    job_id = html.find("a")["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page}")
        result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "fs-unmask"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://kr.indeed.com/취업?q={word}&limit={LIMIT}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
