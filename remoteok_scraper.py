import requests
from bs4 import BeautifulSoup
import csv

def scrape_remoteok(keyword):
    url = f'https://remoteok.com/remote-{keyword}-jobs'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job in soup.find_all('tr', class_='job'):
        title = job.find('h2')
        company = job.find('h3')
        tags = job.find_all('div', class_='tag')
        date = job.find('time')
        link = job.get('data-href')

        if title and company:
            jobs.append({
                'Title': title.text.strip(),
                'Company': company.text.strip(),
                'Tags': ', '.join(t.text.strip() for t in tags),
                'Date': date['datetime'] if date else 'N/A',
                'Link': f'https://remoteok.com{link}' if link else 'N/A'
            })

    with open('jobs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)

    print(f"✅ Scraped {len(jobs)} jobs and saved to jobs.csv.")

if __name__ == "__main__":
    keyword = input("Enter job keyword (e.g., python): ").lower()
    scrape_remoteok(keyword)
