# poetry export --without-hashes --format=requirements.txt > requirements.txt
import asyncio
import argparse
import logging
import platform
from datetime import datetime, timedelta

import aiohttp

"""
  Commands   |                 Description
==============================================================
  {1...10}   | Positional argument. The number of past days 
             | that expected the currency. Default: 1 (Today).
             | it is required.
      -t     | The  flag that help visualize output into the table.
             | It is optional. Default value "False".
      -c     | Choose currency that can be shown. Default: "USD, EUR".
==============================================================
"""


def hypo(string):
    return string.strip(",./?: ")


parser = argparse.ArgumentParser(description='Currency exchange bot (Private Bank)')
parser.add_argument('days', type=int, choices=range(1, 11), help="The number of past days that expected the currency. "
                                                                 "it's "
                                                                 "required.", default=1)
parser.add_argument(
    '-t', action='store_true', help='Visualize currency in table. Default value "False".', default=False)

parser.add_argument('--curr', '-c', help='Choose currency that can be shown. Default value "USD, EUR".', action="extend", nargs="+", type=hypo,
                    default=['USD', 'EUR'])

args = vars(parser.parse_args())

print(args)
DAYS = args.get('days')  # int
TABLE = args.get('t')  # True / False
curr = args.get('curr')  # set{str, }
CURR = set(curr)

HOST = 'https://api.privatbank.ua/p24api/exchange_rates?date='
TODAY = datetime.now().date()

DATE = 'date'  # str '01.01.2023'
EX_RATE = 'exchangeRate'  # list{dict}
B_CURRENCY = 'baseCurrency'  # str 'UAH'
CURRENCY = 'currency'  # str
SR_NB = 'saleRateNB'  # float
PR_NB = 'purchaseRateNB'  # float
SR_P = 'saleRate'  # float
PR_P = 'purchaseRate'  # float

currencies = {"AUD", "AZN", "BYN", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "GEL", "ILS", "KZT", "NOK", "PLN",
              "SEK", "TMT", "UAH", "USD", "UZS", "XAU", "HUF", "JPY", "MDL", "SGD", "TRY"}


def get_urls_list(days: int = 1, host: str = HOST) -> list:
    urls_list = []
    count = 0
    if days <= 0:
        days = 1

    for day in range(days):
        new_date = TODAY - timedelta(days=count)
        urls_list.append(host + new_date.strftime('%d.%m.%Y'))
        count += 1
    urls_list.sort()
    return urls_list


def header_table_maker():
    first_line = ' ' * 29 + '=' * 85 + '\n' + ' ' * 29 + '|{:^41}|{:^41}|\n'.format('National Bank', 'Private Bank') + '=' * 114 + '\n'
    second_line = '|{:^12}|{:^15}|{:^19}|{:^21}|{:^19}|{:^21}|\n'.format('Date', 'Currency', 'Sale rate',
                                                                         'Purchase rate', 'Sale rate',
                                                                         'Purchase rate') + '=' * 114 + '\n'
    return first_line + second_line


def record_table_maker(date: str, exchange_rate_item: dict) -> str:
    row_table = '|{:^12}|{:^15}|{:^19}|{:^21}|{:^19}|{:^21}|\n'.format(date, exchange_rate_item[CURRENCY],
                                                                       exchange_rate_item[SR_NB],
                                                                       exchange_rate_item[PR_NB],
                                                                       exchange_rate_item.get(SR_P, '-'),
                                                                       exchange_rate_item.get(PR_P, '-'))
    return row_table


def footer_table_maker():
    return '=' * 114 + '\n'


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    rer = await response.json()
                    return rer
                logging.error(f'Error status {response.status} for {url}')
        except aiohttp.ClientConnectionError as e:
            logging.error(f'Connection error {url}: {e}')
        return None


async def get_exchange(days: int = DAYS, table: bool = TABLE, currency_list=CURR):
    table_result = ''
    urls = get_urls_list(days)
    json_list = []
    result_list = []

    for url in urls:
        exchange_per_day = await request(url)
        json_list.append(exchange_per_day)

        rows_result = ''
        result_list = []
        for item in json_list:
            date_from_response = item[DATE]
            norm_curr_list = []
            for currency in item[EX_RATE]:
                if currency[CURRENCY] in currency_list:
                    row = record_table_maker(date_from_response, currency)
                    rows_result += row
                    norm_curr_list.append(currency)

            item_dict = {date_from_response: norm_curr_list}

            result_list.append(item_dict)

            rows_result += footer_table_maker()
        table_result = header_table_maker() + rows_result

    if table:
        return table_result
    else:
        return result_list


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    r = asyncio.run(get_exchange())
    print(r)
