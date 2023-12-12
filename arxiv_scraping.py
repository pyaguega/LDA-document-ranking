# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:31:31 2023

@author: pyagu

----------------------------------
Query format:
    run [file_directory.py] [space separated keywords] --time='YYYY-MM-DD'
"""


import pandas as pd

import urllib
import urllib.request

import argparse
import PyPDF2
import requests
import io

parser = argparse.ArgumentParser(description='Scrape arxiv papers')
parser.add_argument('keywords', nargs='+',
                   help='a list of keywords')
parser.add_argument('--time', help='a list of keywords')

baseurl = 'http://export.arxiv.org/api/query?search_query='

args = parser.parse_args()

keyword_list = args.keywords



date = pd.Timestamp(str(args.time), tz='US/Pacific')


i = 0
for keyword in keyword_list:
    if i ==0:
        url = baseurl + 'abs:' + keyword
        i = i + 1
                    
    else:
        url = url + '+AND+' + 'abs:' + keyword

url = url+ '&max_results=10000'        

try:        
    # API GET request (arguments already included in the URL)
    # Query returns bytes
    arxiv_page = urllib.request.urlopen(url).read()

    # Typecast bytes into str
    arxiv_page = str(arxiv_page)    

    # Marks the index where the nth pdf result starts
    begin=[]
    # Marks the index end of where the nth pdf result ends
    end = []
    # Same operation but with timestamp for the corresponding pdf results
    begin_time=[]
    end_time = []
    # Same operation but for abstract/summary of the article
    begin_summary=[]
    end_summary=[]
    start = 0
    while True:
        # Find index of all pdf-type results (AKA find the constant expression that precedes href links)
        # Starting from index start
        start = arxiv_page.find('<link title="pdf" href=',start)
        if start==-1:
            break
        # Add index to a begin array
        begin.append(start)
        # href = destination of the hyperlink. AKA the url of the document.
        # Appends to the array the index of where the link starts
        start = start + len('<link title="pdf" href=')    

    start = 0
    while True:
        # Find the expression always posterior to the href link, starting from index start
        start = arxiv_page.find('rel="related" type="application/pdf"/>',start)
        if start==-1:
            break
        # Append index to array end
        end.append(start)
        start = start + len('rel="related" type="application/pdf"/>')    


    start = 0
    # Same as last two loops, but for timestamps.
    while True:
        
        start = arxiv_page.find('<published>',start)
        if start==-1:
            break
        begin_time.append(start)
        
        start = start + len('<published>')    

    start = 0
    while True:
        
        start = arxiv_page.find('</published>',start)
        if start==-1:
            break
        end_time.append(start)
        start = start + len('</published>')    

    start = 0
    while True:
        
        start = arxiv_page.find('<summary>',start)
        if start==-1:
            break
        begin_summary.append(start)
        start = start + len('<summary>')
    
    start = 0
    while True:
        
        start = arxiv_page.find('</summary>',start)
        if start==-1:
            break
        end_summary.append(start)
        start = start + len('</summary>')

    # Declaring what each row in the CSV file will be
    rows = []
    fileName = ''.join([str(item) for item in keyword_list])
    for i in range(len(begin)):  

       
        # Gets links for all papers
        paper_link = arxiv_page[begin[i]+24:end[i]-2]
        #paper_timestamp = arxiv_page[begin_time[i]+11:end_time[i]]
        paper_summary = arxiv_page[begin_summary[i]+11:end_summary[i]-2]
        # Only prints papers with timestamps greater than specified date
        
        #if pd.to_datetime(paper_timestamp) > date:
        print(i)
        #print(paper_summary)
        #rows.append([paper_link])
        
        
        ### Process to get text from PDF link
        response = requests.get(paper_link)
        f = io.BytesIO(response.content)
        reader = PyPDF2.PdfReader(f)
        pages = reader.pages
        #get all pages data
        text = "".join([page.extract_text() for page in pages])
        currFile = open(fileName+str(i)+".txt", "w+")
        currFile.write(text)
        currFile.close()
    
    """
    import csv
    with open('arxiv.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    """


except:
    pass