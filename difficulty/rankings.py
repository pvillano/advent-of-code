import csv
import datetime

import requests
from lxml import etree
from tqdm import tqdm

selectors = {
    'css selector': 'div.leaderboard-entry:nth-child(102) > span:nth-child(2)',
    # 'css path': 'html.yjdsmpi.idc0_343 body.vsc-initialized main div.leaderboard-entry span.leaderboard-time',
    'xpath': '/html/body/main/div[100]/span[2]'
}

def get_rankings():
    last_year = datetime.datetime.now().year - 1
    rankings = []
    for year in tqdm(range(2015, last_year + 1)):
        for day in range(1,26):
            url = f'https://adventofcode.com/{year}/leaderboard/day/{day}'
            response = requests.get(url)
            response.raise_for_status()
            month, day_str, time = etree.HTML(response.content).xpath(selectors['xpath'])[0].text.split()
            assert month == 'Dec' and int(day_str) == day
            hours, minutes, seconds = map(int, time.split(':'))
            time = hours * 60 * 60 + minutes * 60 + seconds
            link = f'https://adventofcode.com/{year}/day/{day}'
            yield time, year, day, link


def main():
    # with open('rankings.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(
    #         ('Time', 'Year', 'Day', 'Link')
    #     )
    #     for row in get_rankings():
    #         print(*row, sep='\t')
    #         writer.writerow(row)
    with open('rankings.csv', newline='') as csvfile:
        rows = list(csv.reader(csvfile))
        print(sorted(rows))



if __name__ == '__main__':
    main()