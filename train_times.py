import requests
from bs4 import BeautifulSoup

http = requests.get('https://ojp.nationalrail.co.uk/service/ldbboard/dep/SRA/CHM/To')

soup = BeautifulSoup(http.content, 'html.parser')

departure_table = soup.find_all('div', class_='tbl-cont')


def parse_row(row):
    return [' '.join(data.string.replace('\n', '').strip(' ').split()) for data in row if data.string]


for table in departure_table:
    for tr in table.find_all('tr'):
        train_times = parse_row(tr.find_all('td'))
        print(' - '.join(train_times))
