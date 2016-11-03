''' this code is to calculate the match winner based on regression and machine learning over time'''
'''this can e used in the analysis of the player and the output of the match based on the venue'''
''' this code gets data from the archives of yahoo cricket'''

							######################################
							###                                ###
							###   @@Author:Lakshmana Deepesh   ###
							###                                ###
							######################################


from bs4 import BeautifulSoup
import requests as re
import pandas as pd

url = "https://cricket.yahoo.com/matches/archive/page_"
iterator = 0

sno = []
time =[]
team_name = []
venue = []
result = []

for i in xrange(2,15):
	headers = {'User-agent': 'Mozilla/5.0'}
	_html_text = re.get(url+str(i),headers=headers)

	soup = BeautifulSoup(_html_text.text,"html.parser")
	_main_html = soup.find_all('table',{"id":"ycric-series-schedule-past-table"})

	for x in _main_html:
		for row in x.find_all('tr')[1:]:

			col = row.find_all('td')

			#This is for Serial Number
			sno.append(str(col[0].contents))

			#this is for time and date of the match
			time.append(col[1].find('span').contents)

			#this is for the team name
			try:
				team_name.append(str(col[2].find('a').contents).strip())
			except Exception as e:
				team_name.append(str(col[2].contents).strip())
			
			
			# This is for the ground
			venue.append(str(col[3].find('a').contents).strip())

			#this is for the Matchresult
			try:
				result.append(str(col[4].find('a').contents).strip())
			except Exception as e:
				
				result.append(str(col[4].contents).strip())


dictionary = {'sno':sno,'time':time,'team_name':team_name,'venue':venue,'Match_result':result}

df = pd.DataFrame(dictionary)
# print df.head()




#writing it to a file ##

# df = pd.DataFrame(_main_html)		
# print df.head(1)
df.to_csv('c:\Users\Deepesh\Desktop\cricket_results.csv')

# f = open('c:\Users\Deepesh\Desktop\cricket_results.txt','w')
# f.write(str(_main_html[0]))
# f.close()

