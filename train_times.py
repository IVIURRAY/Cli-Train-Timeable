import os
import time

import requests
from bs4 import BeautifulSoup
from pyfiglet import Figlet
from colorama import Fore
from subprocess import call


def parse_data(data):
    if data.string:
        return data.string
    else:
        try:
            mins = list(data.find_all('span')[0])[0]
            if mins.startswith('for the'):
                return ''
            else:
                return f'{mins} mins '
        except Exception as e:
            # print(f'Unable to parse {data} - {e}')
            pass

    return ''


def parse_row(row):
    return [' '.join(parse_data(data).replace('\n', '').strip(' ').split()) for data in row][:4]


def read_website():
    trains = []
    http = requests.get('https://ojp.nationalrail.co.uk/service/ldbboard/dep/SRA/CHM/To')
    soup = BeautifulSoup(http.content, 'html.parser')
    departure_table = soup.find_all('div', class_='tbl-cont')

    for table in departure_table:
        for tr in table.find_all('tr'):
            train_times = parse_row(tr.find_all('td'))
            if train_times:
                trains.append(train_times)

    return trains


def clear():
    # check and make call for specific operating system
    _ = call('clear' if os.name =='posix' else 'cls', shell=True)


def display_logo():
    f = Figlet(font='slant')
    print(Fore.BLUE + f.renderText('Train Delays'))


def display_train_times():
    display_logo()
    print('%0s %17s %16s %5s' % ('Due', 'Dest', 'Status', 'Plat'))
    train_data = read_website()
    for train in train_data:
        print('%0s %0s %0s %0s' % tuple(x.center(0 if i in [0, 2, 3] else 25) for i, x in enumerate(train)))


if __name__ == '__main__':
    while True:
        clear()
        display_train_times()
        time.sleep(1)
