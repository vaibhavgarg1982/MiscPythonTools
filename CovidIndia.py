import requests
import matplotlib.pyplot as plt 
import pandas as pd 


r = requests.get("https://api.covid19india.org/data.json").json()
fig, ((ax_total, ax_daily), (ax_tested, ax_state)) = plt.subplots(nrows=2, ncols=2)


daily_df =  pd.DataFrame(r['cases_time_series'])
daily_df[['dailyconfirmed', 'totalconfirmed', "dailydeceased" , "dailyrecovered"  , "totalrecovered"]] = (daily_df[['dailyconfirmed', 'totalconfirmed', "dailydeceased" , "dailyrecovered"  , "totalrecovered"]]).apply(pd.to_numeric)
daily_df['date'] = pd.to_datetime(daily_df['date']+"2020", format = "%d %B %Y")


ax_total.set_title("Total cases")
ax_total.set_yscale("log")
ax_total.grid(which='both')
ax_total.plot(daily_df['date'], daily_df[[ 'totalconfirmed']])

ax_daily.set_title("Daily cases")
ax_daily.plot(daily_df['date'], daily_df[[ 'dailyconfirmed']])

#plt.show()

test_df = pd.DataFrame(r['tested'])
try:
    test_df['updatetimestamp'] = pd.to_datetime(test_df['updatetimestamp'],infer_datetime_format=True, dayfirst = True)
except:
    test_df['updatetimestamp'] = pd.to_datetime(test_df['updatetimestamp'],format = "%d/%m/%Y %I:%M: %p")

ax_tested.plot(test_df['updatetimestamp'], pd.to_numeric(test_df['totalsamplestested']))
ax_tested.set_title("Total Samples Tested")

state_df = pd.DataFrame(r['statewise'])
ax_state.bar(state_df['state'].iloc[1:11], pd.to_numeric(state_df['active'].iloc[1:11]))
ax_state.set_title("Top ten states # by cases")
#ax_state.legend(state_df['active'].iloc[1:11])

plt.setp(ax_total.xaxis.get_majorticklabels(), rotation=30)
plt.setp(ax_daily.xaxis.get_majorticklabels(), rotation=30)
plt.setp(ax_tested.xaxis.get_majorticklabels(), rotation=30)
plt.setp(ax_state.xaxis.get_majorticklabels(), rotation=30)
plt.tight_layout()
plt.show()


districts = requests.get("https://api.covid19india.org/state_district_wise.json").json()

distnames=[]
distconfirmed = []

for dist in districts['Rajasthan']['districtData']:
    distconfirmed.append(districts['Rajasthan']['districtData'][dist]['confirmed'])
    distnames.append(dist)

dist_df = pd.DataFrame({"districts":distnames, "confirmed":distconfirmed}) 
dist_df.sort_values(by="confirmed", ascending = False, inplace = True)
plt.xticks(rotation=90)
plt.bar(dist_df['districts'],dist_df['confirmed'])

plt.show()
pass