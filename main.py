import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def scrape_MBRDNA():
    url = 'https://jobs.lever.co/MBRDNA'  
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        job_listings = soup.find_all('div', class_='postings-group')
        job_data = []
        for listing in job_listings:
            job_title = listing.find('h5', attrs={'data-qa': 'posting-name'})
            job_title = job_title.get_text() if job_title else ' '
            location = listing.find('span', class_='location')
            location = location.get_text() if location else ' '
            job_description_link = listing.find('a', class_='posting-title')['href']
            job_type = listing.find('span', class_='commitment')
            job_type = job_type.get_text() if job_type else ' '
            company = 'Mercedes-Benz'

            job_data.append({
                'job_title': job_title,
                'location': location,
                'job_description_link': job_description_link,
                'job_type': job_type,
                'company_name': company
            })

        return job_data
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

def scrape_AIRBNB():
    url = 'https://careers.airbnb.com/university/' 
    s = HTMLSession()

    response = s.get(url)
    response.html.render(sleep=1)

    
    job_listings = response.html.xpath('/html/body/div[2]/div/main/div[8]/div/div/div[2]/div[2]/div', first=True)

    job_data = job_listings.absolute_links
    j=[]
    for listing in job_data:
        r = requests.get(listing)
        soup = BeautifulSoup(r.content, 'html.parser')
        job_title = soup.find('h1', class_='page-header__title').text
        location = soup.find('p', class_='page-header__locations').get_text()
        job_description_link = listing
        job_type = 'Intern'
        company_name = 'AirBNB'
        location.replace('/n','').replace(' ', '')
        j.append({
            'job_title': job_title,
            'location': location,
            'job_description_link': job_description_link,
            'job_type': job_type,
            'company_name': company_name,
        })

    return j



if __name__ == "__main__":
    job_data = scrape_AIRBNB()
    if job_data:
        for job in job_data:
            print(job['job_title'])
