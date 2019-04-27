import requests
from bs4 import BeautifulSoup as bs


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

base_url = 'https://hh.ru/search/vacancy?text=python&clusters=true&area=1&enable_snippets=true&search_period=3&page=0'


def hh_parse(base_url, headers):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            salary = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            salary = 'Не указано' if salary is None else salary.text
            jobs.append({'title': title,
                         'company': company,
                         'responsibility': responsibility,
                         'requirement': requirement,
                         'salary': salary,
                         'href': href})
        print(jobs)
    else:
        print(request.status_code)


hh_parse(base_url, headers)
