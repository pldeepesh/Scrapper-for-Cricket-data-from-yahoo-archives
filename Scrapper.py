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
from sklearn import tree

url = "https://cricket.yahoo.com/matches/archive/page_"
iterator = 0

sno = []
time =[]
team_name = []
venue = []
result = []
city = []
first_batting=[]
winner=[]
team1 = []
team2 = []
_passing_list = []

for i in xrange(2,15):
	headers = {'User-agent': 'Mozilla/5.0'}
	_html_text = re.get(url+str(i),headers=headers)

	soup = BeautifulSoup(_html_text.text,"html.parser")
	_main_html = soup.find_all('table',{"id":"ycric-series-schedule-past-table"})

	for x in _main_html:
		for row in x.find_all('tr')[1:]:

			col = row.find_all('td')

			#This is for Serial Number
			sno.append(str(col[0].text))

			#this is for time and date of the match
			time.append(col[1].find('span').text)

			#this is for the team name
			try:
				team_name.append(str(col[2].find('a').text).strip())
			except Exception as e:
				team_name.append(str(col[2].text).strip())
			
			
			# This is for the ground
			venue.append(str(col[3].find('a').text).strip())

			#this is for the Matchresult
			try:
				result.append(str(col[4].find('a').text).strip())
			except Exception as e:
				
				result.append(str(col[4].text).strip())

dictionary = {'sno':sno,'time':time,'team_name':team_name,'venue':venue,'Match_result':result}
df = pd.DataFrame(dictionary)
# print df.head()

#Preping Data for Data Analytics

#Adding Venue to the data
for i in df['venue']:
	_city = i.split(',')
	_city = [_city[len(_city)-1]]
	_city = ''.join(_city)
	city.append(str(_city))

df['city']=city

#Finding out the first batting

for i in df['Match_result']:
	_first_batting = i.split(' ')
	if _first_batting[len(_first_batting)-1] == 'wickets' or _first_batting[len(_first_batting)-1] == 'wicket':
		first_batting.append('0')
	elif _first_batting[len(_first_batting)-1] == 'runs' or _first_batting[len(_first_batting)-1] == 'run':
		first_batting.append('1')
	else:
		first_batting.append('NA')

df['first batting'] = first_batting

#Figuring out the winning team

for i in df['Match_result']:
	_winner = i.partition(' won ')
	_winner = _winner[0]
	winner.append(_winner)

df['winner'] = winner

#seggregating the team names

for i in df['team_name']:
	_team = i.split(' vs ')
	team1.append(_team[0])
	team2.append(_team[1])
	
df['Team 1'] = team1
df['Team 2'] = team2

#using SCIKIT--Learn we are trying to predict the match winner
#
#
## machine learning code comes here ##

#Taking input form the user

count=1
print 'Select first team'
_unique_team1 = df['Team 1'].unique()
for i in _unique_team1:
	print str(count)+'.'+i
	count=count+1
a=int(raw_input('Enter your choice number: '))
_passing_list.append(_unique_team1[a-1])


count = 1
print 'Select seccond team'
_unique_team2 = df['Team 2'].unique()
for i in _unique_team2:
	print str(count)+'.'+i
	count = count+1
a=int(raw_input('Enter your choice number: '))
_passing_list.append(_unique_team2[a-1])


count = 1
print 'Select country'
_unique_city = df['city'].unique()
for i in _unique_city:
	print str(count)+'.'+i
	count = count+1
a=int(raw_input('Enter your choice number: '))
_passing_list.append(_unique_city[a-1])

#writing it to a file ##

df.to_csv('c:\Users\Deepesh\Desktop\cricket_results.csv')
