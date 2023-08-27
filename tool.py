from bs4 import BeautifulSoup
import requests
import csv
import urllib
import bs4 as bs
import re
import sys
import os
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

#THE FOLLOWING LIST OF LISTS ARE REQUIRED TO WRITE TO THE CSV
links = []
texts = [] 

#A LIST OF TOPICS WHERE URL COULD NOT BE FOUND 
Err404 = []

#THE FOLLOWING ARE INDEX VALUES BASED OFF OF THE CSV
topic_column_index = 0
url_column_index = 1

#THE FILE NAME
filename = input("Enter the name of the file (must be placed in same folder as this script): ")

#CHECK IF THE FILE EXISTS
if os.path.exists(filename):
    #READING THE TOPICS AND GETTING LINKS
    print("\n[FILE FOUND!]\n")
    print(f"[BEGINNING TO READ TOPIS FROM CSV {filename}]")
    with open(filename, 'r') as csv_file:
        #GETTING URL
        csv_reader = csv.reader(csv_file)
        url = 'https://www.google.com/search'
        for row in csv_reader:
            search = row[topic_column_index]
            thislink = [search] #first column for each row has to be the search topic
            print("\tRetriving URL for topic: " + search)
            headers = {
                'Accept' : '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
            }
            parameters = {'q': search + "Wikipedia"}

            content = requests.get(url, headers = headers, params = parameters).text
            soup = BeautifulSoup(content, 'html.parser')

            search = soup.find(id = 'search')
            first_link = search.find('a')

            #IF LINK WAS NOT FOUND
            if first_link is None:
                print(f"\t\t[ERROR: Couldn't find link for {row[topic_column_index]}]")
                thiserr = [row[topic_column_index]]
                Err404.append(thiserr)
            #IF LINK WAS FOUND
            else:
                thislink.append(first_link['href']) #second column has to be the link
                links.append(thislink) #Add tuple to the csv

    print("[FINISHED RETRIVING URL FOR ALL TOPICS]")

    #WRITING TO CSV ALL THE FOUND URLS
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(links)

    print(f"\n[FINISHED WRITING ALL URLS TO CSV {filename}]")

    #WRITING TO CSV ALL MISSES, IF ANY
    if len(Err404) > 0:
        print(f"\n[{len(Err404)} URLS COULD NOT BE FOUND. WRITING THEM TO CSV misses.csv]")
        with open('misses.csv', 'w', newline='') as missfile:
            csv_writer = csv.writer(missfile)
            csv_writer.writerows(Err404)

############################################################

    #READING URLS FROM CSV AND EXTRACTING TEXT
    print(f"\n[EXTRACTINNG DATA FROM THE URLS OF CSV {filename}]")
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            #Gettings the data source
            my_url = row[url_column_index]
            thistext = [row[topic_column_index]] #first column has to be topic name
            thistext.append(my_url) #second column has to be the URL
            print("\tRetriving text from URL: " + my_url)
            source = urllib.request.urlopen(my_url).read()

            #Parsing the data/ creating BeautifulSoup object
            soup = bs.BeautifulSoup(source,'lxml')

            #Fetching the text
            text = """"""
            for paragraph in soup.find_all('p'):
                text += paragraph.text

            text = re.sub(r'\[[0-9]*\]',' ',text) #Removing citations

            thistext.append(text)
            texts.append(thistext)
    print("[FINISHED RETRIVING TEXTS FROM ALL URLS]")

    #WRITING EXTRACTED TEXT TO CSV
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(texts)

    print(f"\n[FINISHED WRITING ALL TEXTS TO CSV {filename}]")
else:
    print("\n[ERROR: FILE NOT FOUND]\n")