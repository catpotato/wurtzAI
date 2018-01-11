from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import os, re, csv, urllib


data_loc = "raw_data"

raw_years = [2017,2016]
raw_months = [i+1 for i in range(12)]

years = [str(yr) for yr in raw_years]
months = [str(month).zfill(2) for month in raw_months]

def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_csv(year, month, csv_dict):


    # if data folder does not exist, create it
    data_path = os.path.abspath(data_loc)

    make_path(data_path)

    # if year path does not exist, create it
    directory = os.path.join(data_path + "/" + year)
    make_path(directory)



    # actually write the darned data
    file = os.path.join(directory + "/" + month + ".csv")
    with open(file, 'wt') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['question', 'answer'])
        for key, value in csv_dict.items():
            writer.writerow([key, value])

    print("saved " + file)

def format_txt(a, answer=False):
    try:
        if len(a):
            # remove junk
            a = a.replace(u'\xa0','')
            a = a.replace(u'\n', '')
            a = a.replace('"', '')
            a = a.replace('"', '')
            a = a.strip()

            # all these operations require indexing so i shrouding them with a len thing
            if len(a):
                # get rid of quotes
                if a[0] == "'" or a[0] == '"':
                    a = a[1:-1]
                    # add period at the end

                last_char = a[-1]

                if last_char != "?" and last_char != "." and last_char != "!":
                    if answer:
                        a = a + '.'
                    else:
                        a = a + '?'
                else:
                    if answer:
                        a[-1] = '.'
                    else:
                        a[-1] = '?'

    except TypeError:
        if answer:
            return '.'
        else:
            return '?'

    return a

def save_questions(url, year, month):
    print("downloading " + url)

    soup = BeautifulSoup(urlopen(url), 'html.parser')

    print("finding q & a's")

    if year == "2017" and int(month) >= 4:
        questions = soup.find_all('qco')

    else:
        questions = soup.find_all('font', {'color': '#B387FF'})


    final_qs = [format_txt(q.get_text()) for q in questions]
    final_as = [format_txt(q.parent.next_sibling, answer=True) for q in questions]



    print("q's': " + str(len(final_qs)))
    print("a's: " + str(len(final_as)))

    q_and_a = dict(zip(final_qs, final_as))

    make_csv(year, month, q_and_a)

def attempt_save(year, month):
    url = 'http://www.billwurtz.com/questions/questions-' + year + "-" + month + '.html'

    try:
        save_questions(url, year, month)
    except urllib.error.HTTPError:
        pass


if __name__ == '__main__':
    for year in years:
        for month in months:
            attempt_save(year, month)

    print("done.")
