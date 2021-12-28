import requests
from bs4 import BeautifulSoup

#LIMIT = 50

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    #max_page = pages[-1] + 2
    max_page = pages[-1]
    return max_page

# for n in range(max_page):
    # print(f"start={n*50}")

def extrat_job(html):
        #title = html.find("h2", {"class": "jobTitle"}).find("span").string
        title = html.find("h2", {"class": "jobTitle"}).find("span", recursive=False).string
        company = html.find("span", {"class": "companyName"}) 
        company_anchor = company.find("a")
        if company:
            if company_anchor is not None:
                company = str(company_anchor.string)
            else: 
                company = str(company.string)
            company = company.strip()
        else: 
            company = None

        location = html.select_one("pre > div").text
        job_id = html.parent["data-jk"]
        return {
            'title': title, 
            'company': company, 
            'location': location, 
            "link": f"https://ca.indeed.com/jobs?jk={job_id}"
        }

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed : page {page}")
        result = requests.get(f"{url}&start={page}")
        #result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "slider_container"})
        for result in results:
            job = extrat_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://ca.indeed.com/jobs?q={word}&l=Canada&fromage=14" 
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs