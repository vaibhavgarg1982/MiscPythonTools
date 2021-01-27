import requests
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from datetime import datetime, timedelta

def test(x, a, b): 
    return a * np.exp(b * x)

fig, axes = plt.subplots(ncols=3, nrows=1)
plt.tight_layout()
plt.rcParams["figure.figsize"] = (20,10)
#plt.style.use('seaborn')
countries = ['india', 'us', 'south-korea', 'iran', 'italy', 'germany']
for country in countries:
    print(f"getting data for {country}")
    data = requests.get("https://www.worldometers.info/coronavirus/country/"+ country)
    data = data.text
    tot = data[data.find("data: [", data.find("name: \'Cases\'"))+len("data: ["):data.find("]", data.find("data: [", data.find("name: \'Cases\'"))+len("data: ["))]
    #data[data.find("data: [")+len("data: ["):data.find("]", data.find("data: [")+len("data: ["))]
    tot = [int(i) for i in tot.split(',')]
    dates = data [data.find("categories: [")+len("categories: [") : data.find("]" , data.find("categories: [")+len("categories: ["))]
    dates = [date for date in dates.split(",")]
    axes[0].plot(dates, tot ,  label = country)

axes[0].legend()
axes[0].grid(which = "both")
axes[0].set_yscale("log")
#axes[0,0].xticks(rotation=90)
axes[0].set_xticklabels([str(x) for x in dates],rotation=90)
#axes[0,0].show()

#plt.show()

#plt.rcParams["figure.figsize"] = (20,10)
countries = ['india']
for country in countries:
    print(f"getting data for {country}")

    data = requests.get("https://www.worldometers.info/coronavirus/country/"+ country)
    data = data.text
    #active = data[data.find("data: [")+len("data: ["):data.find("]", data.find("data: [")+len("data: ["))]
    tot = data[data.find("data: [", data.find("name: \'Cases\'"))+len("data: ["):data.find("]", data.find("data: [", data.find("name: \'Cases\'"))+len("data: ["))]

    #active = [int(i) for i in active.split(',')]
    tot = [int(i) for i in tot.split(',')]
    #print(active)
    print(tot)

    dates = data [data.find("categories: [")+len("categories: [") : data.find("]" , data.find("categories: [")+len("categories: ["))]
    dates = [date for date in dates.split(",")]

    print(len(tot))

    #use only the exponential part to fit the curve, not the whole data
    finish = 42
    start = 0
    span = finish-start
    param, param_cov = curve_fit(test, np.linspace(0, span-1, span) , tot[start:finish])
    print(param)
    #param, param_cov = curve_fit(test, np.linspace(0, len(tot)-5, len(tot)-4) , tot[:-4])
    clean_dates = [datetime.strptime(str(date) + " 2020", '\"%b %d\" %Y') for date in dates]
    axes[1].plot(clean_dates, tot ,  label = country.upper() +" Total \n" + clean_dates[-1].strftime('%Y-%m-%d') + ":" + str(tot[-1]))
    #plt.plot(clean_dates, active ,  label = country.upper() +" Active" )
    lobf = []
    cleandates_lobf = []

    for i in range(len(tot)+11):
        lobf.append(test(i, param[0], param[1]))
        cleandates_lobf.append(min(clean_dates)+ timedelta(days = i))

    print(lobf)
    axes[1].plot(cleandates_lobf, lobf, label = country.upper() + " exp curve fit on totals projected 1 week \n " + str(param[0]) + " , " + str(param[1]))

#for xy in zip(dates, tot):                                       
#    plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') 

axes[1].legend()
axes[1].grid(which = "both")
axes[1].set_yscale("log")

axes[1].set_xticks(cleandates_lobf)
axes[1].set_xticklabels([str(datetime.date(x)) for x in cleandates_lobf], rotation=90, fontsize=7)
plt.gcf().subplots_adjust(bottom=0.15)
plt.show()



def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0)))+b
    return (y)

plt.rcParams["figure.figsize"] = (20,10)
countries = ['china']
for country in countries:
    data = requests.get("https://www.worldometers.info/coronavirus/country/"+ country)
    data = data.text
    active = data[data.find("data: [")+len("data: ["):data.find("]", data.find("data: [")+len("data: ["))]
    tot = data[data.find("data: [", data.find("name: \'Cases\'"))+len("data: ["):data.find("]", data.find("data: [", data.find("name: \'Cases\'"))+len("data: ["))]

    active = [int(i) for i in active.split(',')]
    tot = [int(i) for i in tot.split(',')]
    print(active)
    print(tot)

    dates = data [data.find("categories: [")+len("categories: [") : data.find("]" , data.find("categories: [")+len("categories: ["))]
    dates = [date for date in dates.split(",")]

    print(len(tot))

    #use only the exponential part to fit the curve, not the whole data
    finish = 40
    start = 0
    span = finish-start
    p0 = [max(tot[start:finish]), np.median(np.linspace(0, span-1, span)),1,min(tot[start:finish])]
    param, param_cov = curve_fit(sigmoid, np.linspace(0, span-1, span) , tot[start:finish], p0, method='dogbox')
    print(param)
    #param, param_cov = curve_fit(test, np.linspace(0, len(tot)-5, len(tot)-4) , tot[:-4])
    clean_dates = [datetime.strptime(str(date) + " 2020", '\"%b %d\" %Y') for date in dates]
    plt.plot(clean_dates, tot ,  label = country.upper() +" Total \n" + clean_dates[-1].strftime('%Y-%m-%d') + ":" + str(tot[-1]))
    plt.plot(clean_dates, active ,  label = country.upper() +" Active" )
    lobf = []
    cleandates_lobf = []

    for i in range(len(tot)+5):
        lobf.append(sigmoid(i, param[0], param[1], param[2], param[3]))
        cleandates_lobf.append(min(clean_dates)+ timedelta(days = i))

    print(lobf)
    plt.plot(cleandates_lobf, lobf, label = country.upper() + " Sigmoid curve fit on totals projected 1 week \n " + str(param))

#for xy in zip(dates, tot):                                       
#    plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') 

plt.legend()
plt.grid(which = "both")
#plt.yscale("log")
plt.xticks(rotation=90)
plt.xticks(cleandates_lobf)
plt.show()
