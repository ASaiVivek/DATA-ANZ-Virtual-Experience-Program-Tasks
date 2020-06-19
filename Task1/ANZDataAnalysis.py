import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

df=pd.read_excel(r'ANZ synthesised transaction dataset.xlsx')
#print(df)

#finding the average amount of transactiona and rounding it
print("Average Transaction Amount: {:.0f} ".format(df["amount"].mean()))
#print(df["amount"].mean())

#converting date column into a date-time type column
df["date"]=pd.to_datetime(df["date"])
#print(df["date"])

#total number of transactions per month
print("Total number of transactions by month:")
print(df["date"].groupby(df.date.dt.to_period("M")).agg('count'))

months=[]
for date in df["date"]:
    if date.month==8:
        months.append("August")
    elif date.month==9:
        months.append("September")
    elif date.month==10:
        months.append("October")

df["Months"]=months

months_data=df["Months"].unique()
#print(months_data)
count_month=df["date"].groupby(df.date.dt.to_period("M")).agg('count')
#print(count_month[])
trans_month=[]
for i in range(0,3):
    trans_month.append(count_month[i])

#print(trans_month)
fig=plt.figure()
plt.bar(months_data,trans_month)
plt.title("Number of Transactions per month by ANZ customers")
plt.xlabel("Months")
plt.ylabel("Transactions")
for index,value in enumerate(trans_month):
    plt.text(index,value,str(value))
fig.savefig("num_trans_month.png")
#print(df["Months"].head())

#Balance in August by Age
df_cus_aug=df[df["Months"]=="August"].groupby("customer_id").mean()
n_points=len(df_cus_aug["age"])
fig=plt.figure()
plt.scatter(df_cus_aug["age"],df_cus_aug["balance"],c="green",label="Balance")
plt.title("ANZ Customer Balance v/s Age for August")
plt.xlabel("Age(years)")
plt.ylabel("Balance AUD($)")
plt.legend()
plt.tight_layout()
#plt.show()
fig.savefig('bal_aug_age.png')

#Balance in September by Age
df_cus_aug=df[df["Months"]=="September"].groupby("customer_id").mean()
n_points=len(df_cus_aug["age"])
fig=plt.figure()
plt.scatter(df_cus_aug["age"],df_cus_aug["balance"],c="green",label="Balance")
plt.title("ANZ Customer Balance v/s Age for September")
plt.xlabel("Age(years)")
plt.ylabel("Balance AUD($)")
plt.legend()
plt.tight_layout()
#plt.show()
fig.savefig('bal_sep_age.png')

#Balance in October by Age
df_cus_aug=df[df["Months"]=="October"].groupby("customer_id").mean()
n_points=len(df_cus_aug["age"])
fig=plt.figure()
plt.scatter(df_cus_aug["age"],df_cus_aug["balance"],c="green",label="Balance")
plt.title("ANZ Customer Balance v/s Age for October")
plt.xlabel("Age(years)")
plt.ylabel("Balance AUD($)")
plt.legend()
plt.tight_layout()
#plt.show()
fig.savefig('bal_oct_age.png')


#Number of Customers by Age
#n_age=df.groupby('age')['customer_id'].agg('sum')
#print(n_age)
fig=plt.figure()
plt.scatter(df['age'].unique(),df['age'].value_counts(),c="red",label="Number of Customers")
plt.title("ANZ Customers by Age")
plt.xlabel("Age(years)")
plt.ylabel("Number of Customers")
plt.legend()
plt.tight_layout()
fig.savefig('tot_cus_age.png')
#plt.show()
#Total Amount Transacted by Age
df_amount_age=df.groupby('age')['amount'].agg('sum')
fig=plt.figure()
plt.scatter(df['age'].unique(),df_amount_age,c="red",label="Amount Transacted")
plt.title("Amount Transacted by ANZ Customers by Age")
plt.xlabel("Age(years)")
plt.ylabel("Amount AUD($)")
plt.legend()
plt.tight_layout()
fig.savefig('tot_amount_trans_age.png')
#print(df_amount_age)
#n_points=len(df_amount_age["age"])
#print(df['txn_description'].value_counts())
#Number of transactions of differnet kind
fig=plt.figure()
plt.scatter(df['txn_description'].unique(),df['txn_description'].value_counts(),c="red",label="Number of Transactions")
plt.title("Number of Transactions of Different types by ANZ Customers")
plt.xlabel("Transaction Description")
plt.ylabel("Number of Transactions")
plt.legend()
plt.tight_layout()
fig.savefig('trans_desc_count.png')

weekday=[]
for date in df["date"]:
    if date.dayofweek==0:
        weekday.append("Monday")
    elif date.dayofweek==1:
        weekday.append("Tuesday")
    elif date.dayofweek==2:
        weekday.append("Wednesday")
    elif date.dayofweek==3:
        weekday.append("Thursday")
    elif date.dayofweek==4:
        weekday.append("Friday")
    elif date.dayofweek==5:
        weekday.append("Saturday")
    elif date.dayofweek==6:
        weekday.append("Sunday")

df["Weekday"]=weekday
#print(df["Weekday"].value_counts())
#Transactions done by day of the week
fig=plt.figure()
plt.plot(df["Weekday"].unique(),df["Weekday"].value_counts())
plt.title("Number of Transactions done each day of the week by ANZ Customers")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Transactions done")
fig.savefig('trans_weekday.png')

#Transactions by States
df_states=df["merchant_state"].unique()
df_states_str=[]
for i in range(0,len(df_states)):
    if i==2:
        continue
    else:
        df_states_str.append(df_states[i])

#print(df_states_str)
fig=plt.figure()
plt.plot(df_states_str,df["merchant_state"].value_counts())
plt.title("Number of Transactions in each state by ANZ Customers")
plt.xlabel("States")
plt.ylabel("Number of Transactions done")
fig.savefig('m_state_trans.png')

#challenge
#plotting areas of transactions done
df_merchant_long_lat=df["merchant_long_lat"].str.split(" ",n=1,expand=True)
df["Longitude"]=df_merchant_long_lat[0]
df["Latitude"]=df_merchant_long_lat[1]

m_lat=df["Latitude"].tolist()
m_long=df["Longitude"].tolist()

m_lat=[float(i) for i in m_lat]
m_long=[float(i) for i in m_long]

fig=plt.figure(num=None,figsize=(12,8))
map=Basemap(width=6000000,height=4500000,resolution='i',projection='aea',lon_0=135,lat_0=-27)
#map=Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,resolution='c')
map.drawcoastlines()
map.drawcountries()
map.drawstates()
map.drawrivers(linewidth=0.5)
map.drawlsmask(land_color='lightgreen',ocean_color='aqua',lakes=True)
map.scatter(m_long,m_lat,latlon=True,s=25,c='red',marker='o',alpha=1,edgecolor='k',linewidth=1,zorder=2)
plt.title("POS and SALES-POS Transactions of ANZ Customers across Australia")
fig.savefig("merchant_tran.png")

#print(df["Longitude"])
#print(df["Latitude"])

#Customer locations of ANZ

#df_cus=df.groupby('customer_id')
#df_cus_loc=df_cus_loc.unique()
df_unq_loc=df['long_lat'].unique()

cus_long=[]
cus_lat=[]
for data in df_unq_loc:
    data_sep=data.split()
    cus_long.append(data_sep[0])
    cus_lat.append(data_sep[1])


cus_long=[float(i) for i in cus_long]
cus_lat=[float(i) for i in cus_lat]

fig=plt.figure(num=None,figsize=(12,8))
map=Basemap(width=6000000,height=4500000,resolution='i',projection='aea',lon_0=135,lat_0=-27)
#map=Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,resolution='c')
map.drawcoastlines()
map.drawcountries()
map.drawstates()
map.drawrivers(linewidth=0.5)
map.drawlsmask(land_color='lightgreen',ocean_color='aqua',lakes=True)
map.scatter(cus_long,cus_lat,latlon=True,s=75,c='red',marker='o',alpha=1,edgecolor='k',linewidth=1,zorder=2)
plt.title("ANZ customers in Australia")
fig.savefig("cus_loc.png")
