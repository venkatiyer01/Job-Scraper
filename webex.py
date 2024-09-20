from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

print("Put some skill you're familiar with: ")
familiar_skill = input('>') #Taking input regarding the skill.
print(f'Filtering out {familiar_skill}')

def find_jobs():
   #Send the GET request to the timejobs website and get html content.
    html_text = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml') #Parsing the html content using beautifulsoup and lxml parser.
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx') #Finding all job postings using this class and tag.

    job_list = []
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text #Get the date when the job is posted.
        if 'few' in published_date: #checks the date if the job was posted a few days ago.
            company_name = job.find('h3', class_='joblist-comp-name').text.strip() #Extracting thr company name
            skills = job.find('span', class_='srp-skills').text.strip() #Extracting the skills info in that job posting.
            more_info = job.header.h2.a['href'] #Gets the link to more information about the job.

            # Check if familiar skill is in the job's required skills
            if familiar_skill.lower() in skills.lower():
                job_details = {
                    'Company name': company_name,
                    'Skills': skills,
                    'More info': more_info,
                    'Published date': published_date
                }
                job_list.append(job_details)

    # Converts the list of job details to the Pandas dataframe.
    df = pd.DataFrame(job_list)

    # Save DataFrame to an Excel file
    df.to_excel('job_data.xlsx', index=False)

    # Print the number of jobs saved
    print(f'{len(job_list)} jobs saved to job_data.xlsx')

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10  # time to wait between scraping cycles in minutes
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)