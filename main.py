#main.py>
# Use pd.to_datetime(1599822000000, unit='ms') to convert TDA timestamp.
#Imports
import sys
import requests
import json
import os
import shutil
import time
import pandas as pd
from datetime import datetime

#StartUp class that deals with the main loop implementation.
####################Start#########################
class StartUp:
	def __init__(self):
		scriptDir = os.path.dirname(os.path.realpath(__file__))
		self.consumer_key = ""
		self.base_url = 'https://api.tdameritrade.com/v1/marketdata/chains'
		self.quote_url = 'https://api.tdameritrade.com/v1/marketdata/quotes'
		self.historical_data_general = 'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
		self.historical_data_day_period = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
		self.SPY_historical_URL = self.historical_data_general.format(symbol='SPY')
		self.SPY_historical_day_period_URL = self.historical_data_day_period.format(stock_ticker='SPY',periodType='year',period=1,frequencyType='daily',frequency=1)
		self.ticker = ''
		self.JSONObjectList = []

	def main_loop(self):
		#while not self.done:
		self.analysis()

	def make_requests(self):
		self.file = "SPY"

		 #try:
		 #	time.sleep(1.5)
		 #	#self.page = requests.get(url = self.base_url, params = {'apikey' : self.consumer_key,'symbol' : 'SPY','contractType' : 'ALL'})
		 #	self.page = requests.get(url= self.SPY_historical_URL, params={'apikey' : self.consumer_key})
		 #except:
		 #	time.sleep(10)
		 #	self.count = self.count - 1

		try:
			time.sleep(1.5)
			#self.page = requests.get(url = self.base_url, params = {'apikey' : self.consumer_key,'symbol' : 'SPY','contractType' : 'ALL'})
			self.page = requests.get(url= self.SPY_historical_day_period_URL, params={'apikey' : self.consumer_key})
		except:
			time.sleep(10)
			self.count = self.count - 1
			print('Didnt work...')

		#Parse the returned JSON.
		#Load the JSON and prepare to print the infromation.
		self.content = json.loads(self.page.content)

		#Get a list of dates call and put dates will be the same.		
		for i in self.content['candles']:			
			self.JSONObjectList.append(JSONObject(pd.to_datetime(i['datetime'], unit='ms'), i['high'], i['low'],i['open'], i['close'], i['volume']))

		#print(self.content);
		with open(scriptDir + os.path.sep + 'data/SPY/' + 'SPY_Data_Daily_Period_OneYear.json', 'w') as self.json_file:
			self.json_file_string = json.dumps(self.content, indent=4)
			self.json_file.write(self.json_file_string)

	    #Print some nice processed data to a file.
		with open(scriptDir + os.path.sep + 'data/SPY/' + 'SPY_Data_Daily_Period_OneYear_Processed.json', 'w') as self.json_file:
			for i in self.JSONObjectList:
				self.json_file.write("Date: {}\n".format(str(i.date)))
				if(datetime.weekday(i.date) == 0):
					self.json_file.write("Weekday: {}\n".format('Monday'))
				if(datetime.weekday(i.date) == 1):
					self.json_file.write("Weekday: {}\n".format('Tuesday'))
				if(datetime.weekday(i.date) == 2):
					self.json_file.write("Weekday: {}\n".format('Wednesday'))
				if(datetime.weekday(i.date) == 3):
					self.json_file.write("Weekday: {}\n".format('Thursday'))
				if(datetime.weekday(i.date) == 4):
					self.json_file.write("Weekday: {}\n".format('Friday'))
				if(datetime.weekday(i.date) == 5):
					self.json_file.write("Weekday: {}\n".format('Saturday'))
				if(datetime.weekday(i.date) == 6):
					self.json_file.write("Weekday: {}\n".format('Sunday'))

				self.json_file.write("High: {}\n".format(i.high))
				self.json_file.write("Low: {}\n".format(i.low))
				self.json_file.write("Low: {}\n".format(i.open))
				self.json_file.write("Close: {}\n".format(i.close))
				self.json_file.write("Volume: {}\n\n".format(i.volume))


	def analysis(self):
		with open(scriptDir + os.path.sep + 'data/SPY/' + 'SPY_Data_Results.json', 'w') as self.json_file:
			#Create variables.
			self.thursdayHigh =0
			self.fridayHigh = 0
			self.mondayHigh = 0

			self.inccount = 0
			self.deccount = 0
			self.eqcount = 0

			self.incper = 0.0
			self.decper = 0.0
			self.eqper = 0.0

			self.thursInc = 0
			self.thursDec = 0
			self.thursEq = 0

			self.thursIncPer = 0.0
			self.thursDecPer = 0.0
			self.thursEqPer = 0.0
			self.thursGreaterThan50CentH = 0
			self.thursGreaterThan50CentHPer = 0.0
			self.thursGreaterThan50CentL = 0
			self.thursGreaterThan50CentLPer = 0.0

			self.thursLInc = 0
			self.thursLDec = 0
			self.thursLEq = 0

			self.thursLIncPer = 0.0
			self.thursLDecPer = 0.0
			self.thursLEqPer = 0.0

			self.totalDayCount = 0
			self.totalThursCount = 0
			self.totalThursCountLower = 0

			self.json_file.write('Results File:\n')
			#Loop over all the data and find the Fridays and the Mondays.
			for i in self.JSONObjectList:
				#Total Trading Days counter.
				self.totalDayCount += 1

				#Total count of trading days where thursday high is higher than friday high.
				if(self.thursdayHigh > self.fridayHigh or self.thursdayHigh == self.fridayHigh):
					self.totalThursCount = self.totalThursCount + 1

				#Total count of trading days where thursday high is lower than friday high.
				if(self.thursdayHigh < self.fridayHigh or self.thursdayHigh == self.fridayHigh):
					self.totalThursCountLower = self.totalThursCountLower + 1

				#This will be a Thursday if true.
				if(datetime.weekday(i.date) == 3):
					self.thursdayHigh = i.high

				#This will be a Friday if true.
				if(datetime.weekday(i.date) == 4):
					self.fridayHigh = i.high

				#This will be a Monday if true.
				if(datetime.weekday(i.date) == 0):
					self.mondayHigh = i.high

				#SPY increased over the weekend.
				if(self.mondayHigh > self.fridayHigh):
					self.inccount = self.inccount + 1;

				#SPY decreased over the weekend.
				if(self.mondayHigh < self.fridayHigh):
					self.deccount = self.deccount + 1;

				#SPY didnt change price.
				if(self.mondayHigh == self.fridayHigh):
					self.eqcount = self.eqcount + 1;

				#SPY increased if Friday failed to beat Thursday highs.
				if((self.thursdayHigh > self.fridayHigh) and (self.mondayHigh > self.fridayHigh)):
					self.thursInc = self.thursInc + 1
					if(self.mondayHigh - self.fridayHigh > 0.50):
						self.thursGreaterThan50CentH = self.thursGreaterThan50CentH + 1

				#SPY decreased if Friday failed to beat Thursday highs.
				if((self.thursdayHigh > self.fridayHigh) and (self.mondayHigh < self.fridayHigh)):
					self.thursDec = self.thursDec + 1
					if(self.mondayHigh - self.fridayHigh < 0.50):
						self.thursGreaterThan50CentL = self.thursGreaterThan50CentL + 1

				#SPY didnt change if Friday failed to beat Thursday highs.
				if((self.thursdayHigh > self.fridayHigh) and (self.mondayHigh == self.fridayHigh)):
					self.thursEq = self.thursEq + 1

				#SPY increased if Friday was higher than Thursday highs.
				if((self.thursdayHigh < self.fridayHigh) and (self.mondayHigh > self.fridayHigh)):
					self.thursLInc = self.thursLInc + 1

				#SPY decreased if Friday was higher than Thursday highs.
				if((self.thursdayHigh < self.fridayHigh) and (self.mondayHigh < self.fridayHigh)):
					self.thursLDec = self.thursLDec + 1

				#SPY diidnt change if Friday was higehr than Thursday highs.
				if((self.thursdayHigh < self.fridayHigh) and (self.mondayHigh == self.fridayHigh)):
					self.thursLEq = self.thursLEq + 1

			#Calculate the results.
			if(self.inccount and self.deccount > 0):
				self.incper = ((self.inccount / (self.inccount + self.deccount + self.eqcount)) * 100)
				self.decper = ((self.deccount / (self.inccount + self.deccount + self.eqcount)) * 100)
				self.eqper = ((self.eqcount / (self.inccount + self.deccount + self.eqcount)) * 100)

			if(self.thursInc and self.thursDec > 0):
				self.thursIncPer = ((self.thursInc / self.totalThursCount) * 100)
				self.thursDecPer = ((self.thursDec / self.totalThursCount) * 100)
				self.thursEqPer = ((self.thursEq / self.totalThursCount) * 100)

			if(self.thursLInc and self.thursLDec > 0):
				self.thursLIncPer = ((self.thursLInc / self.totalThursCountLower) * 100)
				self.thursLDecPer = ((self.thursLDec / self.totalThursCountLower) * 100)
				self.thursLEqPer = ((self.thursLEq / self.totalThursCountLower) * 100)

			if(self.thursGreaterThan50CentH and self.thursGreaterThan50CentL > 0):
				self.thursGreaterThan50CentHPer = ((self.thursGreaterThan50CentH / (self.thursGreaterThan50CentH + self.thursGreaterThan50CentL)) * 100)
				self.thursGreaterThan50CentLPer = ((self.thursGreaterThan50CentL / (self.thursGreaterThan50CentH + self.thursGreaterThan50CentL)) * 100)

			#Print the results.
			self.json_file.write('Total Count of Trading Days: {}\n\n'.format(self.totalDayCount))
			self.json_file.write('The amount of days SPY increased on Monday in the last year: {}\n'.format(self.inccount))
			self.json_file.write('The amount of days SPY decreased on Monday in the last year: {}\n'.format(self.deccount))
			self.json_file.write('The amount of days SPY didnt change on Monday in the last year: {}\n'.format(self.eqcount))
			self.json_file.write('The percentage of days SPY increased on Monday in the last year: {:.2f}%\n'.format(self.incper))
			self.json_file.write('The percentage of days SPY decreased on Monday in the last year: {:.2f}%\n'.format(self.decper))
			self.json_file.write('The percentage of days SPY didnt change on Monday in the last year: {:.2f}%\n'.format(self.eqper))

			self.json_file.write('\n')

			self.json_file.write('Total Count of Trading Days where Thurday High was higher than Fridays High: {}\n\n'.format(self.totalThursCount))
			self.json_file.write('The amount of days where SPY increased on Monday if Friday failed to break Thursdays highs?: {}\n'.format(self.thursInc))
			self.json_file.write('The amount of days where SPY decreased on Monday if Friday failed to break Thursdays highs?: {}\n'.format(self.thursDec))
			self.json_file.write('The amount of days where SPY didnt change on Monday if Friday failed to break Thursdays highs?: {}\n'.format(self.thursEq))
			self.json_file.write('The percentage of days where SPY increased on Monday if Friday failed to break Thursdays highs?: {:.2f}%\n'.format(self.thursIncPer))
			self.json_file.write('The percentage of days where SPY decreased on Monday if Friday failed to break Thursdays highs?: {:.2f}%\n'.format(self.thursDecPer))
			self.json_file.write('The percentage of days where SPY didnt change on Monday if Friday failed to break Thursdays highs?: {:.2f}%\n'.format(self.thursEqPer))

			self.json_file.write('The amount of days where SPY had a greater than 50 cent increase on Monday if Friday failed to break Thursdays highs?: {}\n'.format(self.thursGreaterThan50CentH))
			self.json_file.write('The percentage of days where SPY a greater than 50 cent increase on Monday if Friday failed to break Thursdays highs?: {:.2f}%\n'.format(self.thursGreaterThan50CentHPer))
			self.json_file.write('The amount of days where SPY had a greater than 50 cent decrease on Monday if Friday failed to break Thursdays highs?: {}\n'.format(self.thursGreaterThan50CentL))
			self.json_file.write('The percentage of days where SPY a greater than 50 cent decrease on Monday if Friday failed to break Thursdays highs?: {:.2f}%\n'.format(self.thursGreaterThan50CentLPer))

			self.json_file.write('\n')

			self.json_file.write('Total Count of Trading Days where Thurday High was lower than Fridays High: {}\n\n'.format(self.totalThursCountLower))
			self.json_file.write('The amount of days where SPY increased on Monday if Friday was higher than Thursdays highs?: {}\n'.format(self.thursLInc))
			self.json_file.write('The amount of days where SPY decreased on Monday if Friday was higher than Thursdays highs?: {}\n'.format(self.thursLDec))
			self.json_file.write('The amount of days where SPY didnt change on Monday if Friday was higher than Thursdays highs?: {}\n'.format(self.thursLEq))
			self.json_file.write('The percentage of days where SPY increased on Monday if Friday was higher Thursdays highs?: {:.2f}%\n'.format(self.thursLIncPer))
			self.json_file.write('The percentage of days where SPY decreased on Monday if Friday was higher than Thursdays highs?: {:.2f}%\n'.format(self.thursLDecPer))
			self.json_file.write('The percentage of days where SPY didnt change on Monday if Friday was higher than Thursdays highs?: {:.2f}%\n'.format(self.thursLEqPer))
#################END CLASS###########################

################JSON OBJECT##########################

class JSONObject:
	def __init__(self, date, high, low, openp, close, volume):
		self.date = date
		self.high = high
		self.low = low
		self.open = openp
		self.close = close
		self.volume = volume
		

################END CLASS############################
#Entry point.
if __name__ == '__main__':
	scriptDir = os.path.dirname(os.path.realpath(__file__))

	#Program Info.
	print("Historical Data Collector for SPY.");

	#Create needed directories if they do not already exist.
	if not os.path.exists("data/SPY/"):
			os.makedirs(scriptDir + os.path.sep + "data/SPY/")

	dataprocesser = StartUp()

	#Start the loop.
	dataprocesser.make_requests()
	dataprocesser.main_loop()