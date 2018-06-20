import pandas as pd

"""
This preprocessing workflow is the same as in preprocess.ipynb. For a more in-depth explanation of each step of the
preprocessing, refer to that notebook.
"""

print "Loading dataframe"
df = pd.read_csv('flights.csv', low_memory=False)

for i in ['YEAR', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']:
    print "Discarding column", i
    df.pop(i)

for i in df:
    print "Filtering out rows with NaNs at", i
    df = df[pd.isnull(df[i]) == False]

print "Adding PREVIOUS_ARRIVAL_DELAY and PREVIOUS_DEPARTURE_DELAY"
prev = {i:{'arrival':0, 'departure':0} for i in df['TAIL_NUMBER'].unique()}
prev_arr = []
prev_dep = []
for i in df[['TAIL_NUMBER', 'ARRIVAL_DELAY', 'DEPARTURE_DELAY']].values:
    prev_arr.append(prev[i[0]]['arrival'])
    prev_dep.append(prev[i[0]]['departure'])
    prev[i[0]]['arrival'] = i[1]
    prev[i[0]]['departure'] = i[2]
df['PREVIOUS_ARRIVAL_DELAY'] = prev_arr
df['PREVIOUS_DEPARTURE_DELAY'] = prev_dep

for i in ['FLIGHT_NUMBER', 'TAIL_NUMBER', 'DEPARTURE_TIME', 'ARRIVAL_TIME']:
    print "Discarding column", i
    df.pop(i)

for col in ['SCHEDULED_DEPARTURE', 'SCHEDULED_ARRIVAL', 'WHEELS_OFF', 'WHEELS_ON']:
    df[col] = df[col].map(lambda x : 60*(x/100) + (x % 100))

df.pop('DIVERTED')
df.pop('CANCELLED')

dums = ['MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE']

for i in dums:
    print "Dummifying column", i
    p = df.pop(i)
    dummies = pd.get_dummies(p, prefix=i)
    df = pd.concat([df, dummies[dummies.columns[1:]]], axis=1)

print "Converting BTS IDs to IATA codes"
bts_df = pd.read_csv('L_AIRPORT_ID.csv_')
iata_df = pd.read_csv('L_AIRPORT.csv_')
bts_dict = {str(i[0]):i[1] for i in zip(bts_df['Code'], bts_df['Description'])}
iata_dict = {i[1]:i[0] for i in zip(iata_df['Code'], iata_df['Description'])}

airports = pd.read_csv('airports.csv')
airport_dict = {i[0]:{'latitude':i[1], 'longitude':i[2]} for i in airports[['IATA_CODE', 'LATITUDE', 'LONGITUDE']].values}
airport_dict['ECP'] = {'latitude':30.358333, 'longitude':-85.795556}
airport_dict['UST'] = {'latitude':29.95925, 'longitude':-81.339722}
airport_dict['PBG'] = {'latitude':44.650833, 'longitude':-73.468056}

print "Converting ORIGIN_AIRPORT and DESTINATION_AIRPORT to latitudes and longitudes"
origin_airport = df.pop('ORIGIN_AIRPORT')
destination_airport = df.pop('DESTINATION_AIRPORT')

iata_dict[bts_dict['10423']] = 'AUS'

origin_airport = origin_airport.map(lambda x : x if x in airport_dict else iata_dict[bts_dict[str(x)]])
destination_airport = destination_airport.map(lambda x : x if x in airport_dict else iata_dict[bts_dict[str(x)]])
df['ORIGIN_LATITUDE'] = origin_airport.map(lambda x : airport_dict[x]['latitude'])
df['ORIGIN_LONGITUDE'] = origin_airport.map(lambda x : airport_dict[x]['longitude'])
df['DESTINATION_LATITUDE'] = destination_airport.map(lambda x : airport_dict[x]['latitude'])
df['DESTINATION_LONGITUDE'] = destination_airport.map(lambda x : airport_dict[x]['longitude'])

print "Saving to CSV"
df.to_csv('finaldf.csv')