#Indeed.com Data Science Webscraper
#Drew Fingerhut 3/6/2022

#importing the necessary libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

#establishing necessary lists outside the for loop to be populated
titles = []
companies = []
salaries = []
pp = []
this = []
num = 0
compare = []

for i in range(100):   
    start = 'start='+str(num)        
    
    if i == 0:
        url = 'https://www.indeed.com/jobs?q=data%20scientist&l=Remote'
        req = requests.get(url)
        #print(url)
    if i != 0:
        url = 'https://www.indeed.com/jobs?q=data%20scientist&l=Remote'
        url_new = url+'&'+start+'&'+str(pp[-1])
        req = requests.get(url_new)
        #print(url_new)
    
    compare.append(i) 
    num += 10
    
    soup = BeautifulSoup(req.content, "html.parser")
    results = soup.find(id="resultsBodyContent")
    job_elements = results.find_all("div", class_="job_seen_beacon")
    
    for job_element in job_elements:
        title_element = job_element.find("h2", class_="jobTitle")
        company_element = job_element.find("a", class_ ="turnstileLink companyOverviewLink")
        salary_element = job_element.find("div", class_ = "attribute_snippet")
        if title_element != None:    
             titles.append(title_element.text)
        elif title_element == None:
            titles.append(0)
        if company_element != None:    
            companies.append(company_element.text)
        elif company_element == None:
             companies.append(0)
        if salary_element != None:
            salaries.append(salary_element.text)
        elif salary_element == None:
            salaries.append(0)
            
    df = pd.DataFrame ({
                    "Title": titles,
                    "Company": companies,
                    "Salary": salaries
                        })
            
    link = soup.find("ul", class_ = "pagination-list")
    for links in link:
        label = links.find('a')
        if label != None and label!=-1:
            if str(label["aria-label"]) !=  'Previous' and str(label["aria-label"]) != str(i) and str(label["aria-label"]) != str(i-1):
                #print(str(label["aria-label"]))
                #print(str(i+1))
                pp.append(label["data-pp"])
df

df.to_csv('Indeed_Data_Science_New.csv')
