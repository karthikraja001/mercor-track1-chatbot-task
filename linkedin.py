import requests
from bs4 import BeautifulSoup

def getJobs(company="", experience=[], role="", location=""):
    print("FETCH")
    exp_code = {
        'internship' : 1,
        'entry level' : 2,
        'associate' : 3,
        'mid senior' : 4,
        'director' : 5
    }
    exps = ''
    print("FETCH")
    try:
        for i in experience:
            exps += str(exp_code[i]) + ","
    except:
        pass
    searchurl = "https://linkedin.com/jobs/search"
    searchurl = searchurl + "?keywords="+ role + "&location=" + location + "&f_E=" + exps
    print(searchurl)
    try:
        pg = requests.get(searchurl)
        soup = BeautifulSoup(pg.content)

        jobs = []

        for i in soup.findAll("main"):
            for j in i.findAll("ul", {"class" : "jobs-search__results-list"}):
                for k in j.findAll("li"):
                    temp = {}
                    for link in k.findAll("a") : temp['url'] = link['href'].split("?ref")[0] if 'url' not in temp.keys() else link['href']
                    for l in k.findAll("div", {"class" : "base-search-card__info"}):
                        for jobRole in l.findAll("h3") : temp['Role'] = jobRole.get_text().strip()
                        for company in l.findAll("h4") : temp['Company'] = company.get_text().strip()
                        for location in l.findAll("span", {"class" : "job-search-card__location"}) : temp['location'] = location.get_text().strip()
                    jobs.append(temp)
        print(jobs)
        return {"message" : jobs, "code" : 200}
    except:
        return {"message" : "server_problem", "code" : 500}

def getCompanyDetails(companyName="google"):
    companyUrl = f"https://www.crunchbase.com/organization/{companyName.lower()}"
    headers = {
        'Upgrade-Insecure-Requests': '5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    desc = ''
    worksOn = ''
    try:
        response = requests.get(companyUrl, headers=headers)
        soup = BeautifulSoup(response.content)
        for i in soup.findAll('mat-card', {'class':'mat-mdc-card mdc-card'}):
            for j in i.findAll('div', {'class' : 'section-content-wrapper'}):
                for k in j.findAll('description-card'): desc = k.get_text()
            for l in i.findAll('div', {'class' : 'section-content-wrapper'}):
                for m in l.findAll('field-formatter'):
                    for n in m.findAll('chips-container'):
                        for t in n.findAll('a'): worksOn += t.get_text() + ", "
        return {'description' : desc, 'worksOn' : worksOn, 'code': 200}
    except:
        return {'message' : 'server_error', 'code' : 200}