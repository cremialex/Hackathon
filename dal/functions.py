import pandas as pd

def getPrices(list_of_tickers):
	df = pd.read_csv('data_new_list_wikipedia.csv', header=[0,1], index_col=0, dayfirst= True, parse_dates=True)
	df = df[list_of_tickers]

	return df.iloc[:,::2]

def getVolumes(list_of_tickers):
	df = pd.read_csv('data_new_list_wikipedia.csv', header=[0,1], index_col=0, dayfirst= True, parse_dates=True)
	df = df[list_of_tickers]

	return df.iloc[:,1::2]

def getVolatilities(list_of_tickers, feature):
	df = pd.read_csv('data_new_list_wikipedia.csv', header=[0,1], index_col=0, dayfirst= True, parse_dates=True)
	df = df[list_of_tickers]
	if lower(feature) == 'price':
		df = df.iloc[:,::2]
	elif lower(feature) == 'volume':
		df = df.iloc[:,1::2]
	else:
		print("Please insert either 'price' or 'volume' as feature")
		return


	return 
