#Imports
import requests as req
from bs4 import BeautifulSoup as bs
import csv

#Start url and base processes
url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
page = req.get(url)
bspage = bs(page.text, "html.parser")

#Shortlisting the table
table = bspage.find_all('table')[0]

#Preparing headers and neccessary lists
headers = ['v_mag', 'name', 'bayer_designation', 'distance', 'spectral_class', 'mass', 'radius', 'luminosity']
stellar_data = []

#Looping through all data and storing it
#tr - entire row
for tr_tag in table.find_all('tbody')[0].find_all('tr'):
    row_data = []
    #td - each cell in row
    for index, td_tag in enumerate(tr_tag.find_all('td')):
        #checking for anchor tags
        if len(td_tag.find_all('a')) > 0:
            #removing superscript/subscript elements
            if '[' in td_tag.find_all('a')[0].contents[0]:
                #Lopping through all contents in the omission exception
                for part in td_tag.contents:
                    #Looking for an item which isn't a tag
                    if '<' not in str(part):
                        row_data.append(part)
                        row_data.append("Error")
            else:
                row_data.append(td_tag.find_all('a')[0].contents[0])
        else:
            row_data.append(td_tag.contents[len(td_tag.contents)-1])

    #Post-processing such as removing \n and non-breaking spaces
    for index,data in enumerate(row_data):
        data_str = str(data)
        if '\n' in data_str:
            data_str = data_str.replace('\n', '')
        if '\xa0' in data_str:
            data_str = data_str.replace('\xa0', '')
        row_data[index] = data_str
    #Deleting additional items from list
    for index, data in enumerate(row_data):
        if data == 'Error':
            del row_data[index+2]
            del row_data[index+1]
            del row_data[index]

    #Appending row_data to main list
    if not len(row_data) == 0:
        stellar_data.append(row_data)

#Writing data to csv file
with open('stellar_data.csv', 'w', encoding="utf-8") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(stellar_data)