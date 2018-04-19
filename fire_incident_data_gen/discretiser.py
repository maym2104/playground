# This file discretises the time and longitude-tatitude 

import pandas as pd 
import numbers
import calendar, time


NO_OF_ROWS=13
NO_OF_COLUMNS=13
TIME_FRAMES=100000

incident_data = r'fd_incidents_past_12_mo_datasd.csv'
conversion_data= r'zip_codes_states.csv'

i_d = pd.read_csv(incident_data)
c_d = pd.read_csv(conversion_data)


#making pin to latitude-longitude dictionatry
max_latitude=c_d['latitude'].max()
min_latitude=c_d['latitude'].min()
max_longitude=c_d['longitude'].max()
min_longitude=c_d['longitude'].min()
pin_latlong={}
for i in range(0,len(c_d)):
	pin_latlong[ str(c_d['zip_code'][i])]=(c_d['latitude'][i],c_d['longitude'][i])



#time discretisation preprocessing
temp=[]
for i in range(0,len(i_d)): 
	t = time.strptime(  i_d['response_date'][i] , "%Y-%m-%dT%H:%M:%S")
	temp.append(calendar.timegm(time.struct_time(t)))

i_d['response_machinetime']=temp
max_time=max(temp)
min_time=min(temp)


#dropping bad columns
# dropcol=[]
# for i in range(0,len(i_d)):
# 	if (not isinstance(i_d['zip'][i], float)) or (isinstance(i_d['zip'][i]!=isinstance(i_d['zip'][i]))):  
# 		dropcol.append(i)

# i_d=i_d.drop(i_d.index[dropcol])


#adding x y and t
lati_to_x=[]
longi_to_y=[]
machinetime_to_discretetime=[]

row_width=((max_latitude-min_latitude)/NO_OF_ROWS)
col_width=((max_longitude-min_longitude)/(NO_OF_COLUMNS-1))
time_width=((max_time-min_time)/TIME_FRAMES)

for i in range(0,len(i_d)):
	#print i
	x=int((pin_latlong[str(int(i_d['zip'][i]))][0]-min_latitude)//row_width)
	y=int((pin_latlong[str(int(i_d['zip'][i]))][1]-min_longitude)//col_width)
	t=int((i_d['response_machinetime'][i]-min_time)//time_width)
	lati_to_x.append(x)
	longi_to_y.append(y)
	machinetime_to_discretetime.append(t)

i_d['x']=lati_to_x
i_d['y']=longi_to_y
i_d['t']=machinetime_to_discretetime
# for i in range(0,len(i_d)):
# 	if isinstance(i_d['zip'][i], numbers.Integral):
# 		lati.append(pin_latlong[str(int(i_d['zip'][i]))][0])
# 		longi.append(pin_latlong[str(int(i_d['zip'][i]))][1])
# 	else:
# 		lati.append("")
# 		longi.append("")

i_d=i_d.sort_values(by=['response_machinetime'])
i_d.to_csv('out.csv')
