#Montgomery County Public Schools' management of the ongoing pandemic hasn't gone smoothly.
#In January, the county pledged to update reported COVID-19 case totals by school daily.
#But two days later, the county stopped updating data.
#Below, I've designed a script that would automatically scrape data on when the county releases data.
#When we think of COVID-19 data, we often think of the numbers themselves. But in MCPS, just the times of the updates alone have proved newsworthy -- cases aside.
#This script could be the foundation for a Twitter bot, or a newsroom tool to inform reporters when the new data is available.
#On the other hand, a public Twitter bot could hold MCPS accountable.

#Here is the script:

#I began by importing packages.
import csv
import pandas as pd
from datetime import date
import requests
from bs4 import BeautifulSoup

#Here's the URL I used where the data sits.
url = 'https://www.montgomeryschoolsmd.org/coronavirus/dashboard/'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
html = response.content

#Next, I prepped BeautifulSoup to find the data I wanted on the page.
soup = BeautifulSoup(html, features="html.parser")
div = soup.find('div',{'class':'col-md-4'})
content = str(div)

#Here, I've identified the chunk of code that I'm going to be mining.
list_item = div.find('li')

#This variable zeroes in on the stated data. This is the one that was most recently added to the page.
latest_date = list_item.text

#Here, I'm pulling the ends of these internal links. These links lead to pdfs of all of the data by schools available for the school.
suffix = list_item.find('a')['href']
pdf_link = "https://www.montgomeryschoolsmd.org/coronavirus/dashboard" + suffix

#Let's also collect the time, so we can show any delays in the data.
today=date.today()
date_fmt = today.strftime("%B %d, %Y")
print(date_fmt)

#This prints when the data was last reported and the associated link.This could be the text in a Twitter bot, or just a commit message in GitHub.
print( "Today is " + date_fmt + ". " + "MCPS data was last updated on " + latest_date + "." + " You can see the latest data here:" + pdf_link)

#This program is certainly not infallible or ready to publish, but it lays the groundwork for a newsworthy automated tool.
#For one, there are errors in the date sometimes. For Feb. 2, it says the year is 2002. In addition, there are spaces in the pdf URL that would need to be cleaned so that the links would actually work.
#You would have to insert specific string replacements since it's not always the same insertions in the URL.

#This could also be useful as csv. I could create a list of lists with columns of "date_reported," "date_updated" and the link to  the pdf.

#For example, it could look something like  this:
#(But a better version of this would probably use a for loop)
cell_list = []

cell_list.append(date_fmt)
cell_list.append(latest_date)
cell_list.append(pdf_link)
#print(cell_list)

#You'd end up returning something that would like this:

#cells_for_csv = [date_fmt, latest_date, pdf_link]

#This would give a simple list, and I might ultimately want to convert that into a list of lists to collect more data. A list of lists could allow us to see it in csv.

#Here is one of my attemps I made at pushing it to a csv. There were others, but this one might be the closest I could get, but it's still a bit far from where we want.

outfile = open("./covid.csv", "w", newline="")
writer = csv.writer(outfile)
writer.writerows(cell_list)

#
