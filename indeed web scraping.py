from operator import le
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    url = f'https://uk.indeed.com/jobs?q&l=Middlesbrough%20TS1&radius=5&sort=date&start={page}&vjk=4a0649e5513c3856'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('a').text
        company = item.find('span', class_ ='companyName').text
        location = item.find('div', class_ = 'companyLocation').text
        try:
            salary = item.find('div', class_ = 'attribute_snippet').text
        except:
            salary = ''
        summary = item.find('table', class_ = ['jobCardShelfContainer']).text.replace('\n', '')
        

        job = {
            'title' : title,
            'company' : company,
            'location' : location,
            'salary' : salary,
            'summary' : summary
        }
        joblist.append(job)
    return


joblist =[]


for i in range(0,100,10):
    print(f'Getting page, {i}')
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')