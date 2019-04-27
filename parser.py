import requests
import csv
import os
from bs4 import BeautifulSoup as bs


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

base_url2 = 'https://hh.ru/search/vacancy?text=python&clusters=true&area=1&enable_snippets=true&search_period=3'
base_url = 'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&search' \
           '_period=1&experience=noExperience&from=cluster_experience'


def hh_parse(base_url, headers):
    urls = [base_url]
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pages_count = int(soup.find_all('a', attrs={'data-qa': 'pager-page'})[-1].text)
            for i in range(1, pages_count):
                url = base_url + f'&page={i}'
                urls.append(url)
        except:
            pass

    for i in range(len(urls)):
        request = session.get(urls[i], headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            for div in divs:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
                responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                salary = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                salary = 'Не указано' if salary is None else salary.text
                company = 'Не указано' if company is None else company.text
                jobs.append({'title': title,
                             'company': company,
                             'responsibility': responsibility,
                             'requirement': requirement,
                             'salary': salary,
                             'href': href})
        else:
            print(request.status_code)
        print('Парсинг страницы: ' + str(int(i / len(urls) * 100)) + '%')
    return jobs


def save_jobs_to_csv(jobs, path):
    print("Сохранение файла...")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8') as file:
        pen = csv.writer(file)
        pen.writerow(('Вакансия', 'Компания', 'Обязанности', 'Требования', 'Зар. плата', 'URL'))
        for job in jobs:
            pen.writerow((job['title'], job['company'], job['responsibility'],
                          job['requirement'], job['salary'], job['href']))
    print('Файл успешно сохранен!')


jobs = hh_parse(base_url, headers)
save_jobs_to_csv(jobs, 'csv/test_csv.csv')
