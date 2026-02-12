# Author: Paul Giessner, Borrego
# Date last modified: 6/24/2022
# Purpose: Plot IHI commissioning test results data, including capacity,
# ramp rate (charge and discharge), and output transition control tests

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md

# ----- Import data -----
# Name of file to import

# file_name = "IHI Results_Maple St. 05022022.xlsx"
# file_name = "IHI Preliminary Results_77F2M 05192022b.xlsx"
file_name = "IHI Results_299 Farm preliminary_Kc_PG 10122022.xlsx"
# file_name = "IHI Preliminary Results_160TIH 05192022b.xlsx"
# file_name = "IHI Results_71CFR 10122022.xlsx"
# file_name = "IHI Preliminary Results_0HAM1 05192022b.xlsx"
# file_name = "IHI Preliminary Results_0HAM2 05192022b.xlsx"
# file_name = "IHI Preliminary Results_59FED1 05192022b.xlsx"
# file_name = "IHI Preliminary Results_59FED2 05192022b.xlsx"
# file_name = "IHI Preliminary Results_196TRE 05192022b.xlsx"
# file_name = "IHI Preliminary Results_276FED 05192022b.xlsx"
# file_name = "IHI Preliminary Results_Faunce 05192022b.xlsx"
# file_name = "IHI Preliminary Results_Ventura 05192022b.xlsx"
# file_name = "IHI Preliminary Results_RearSomers 05192022b.xlsx"

# OPTIONAL - Use only if IHI splits results into two files (otherwise, comment out)
# file_name2 = "IHI Results_71CFR 06222022 (2 of 2).xlsx"

# File import parameters
sheet_offset = 0 # accounts for different spreadsheet configs IHI may use; 0 is default
header_row = 13 # number of rows before data columns start in Excel file

# Read data from Excel file(s)
chrg_1 = pd.read_excel(file_name,1+sheet_offset,skiprows=header_row,index_col=1)
dchg_1 = pd.read_excel(file_name,2+sheet_offset,skiprows=header_row,index_col=1)
chrg_2 = pd.read_excel(file_name,3+sheet_offset,skiprows=header_row,index_col=1)
dchg_2 = pd.read_excel(file_name,4+sheet_offset,skiprows=header_row,index_col=1)
chrg_3 = pd.read_excel(file_name,5+sheet_offset,skiprows=header_row,index_col=1)
dchg_3 = pd.read_excel(file_name,6+sheet_offset,skiprows=header_row,index_col=1,)

if 'file_name2' in locals(): # if files are split into two, use 2nd file
    crr = pd.read_excel(file_name2,0,index_col=1)
    drr = pd.read_excel(file_name2,1,index_col=1)
    otc = pd.read_excel(file_name2,2,index_col=1)
else: # otherwise, use same file to read CRR, DRR, and OTC test results
    crr = pd.read_excel(file_name,7+sheet_offset,index_col=1) 
    drr = pd.read_excel(file_name,8+sheet_offset,index_col=1) 
    otc = pd.read_excel(file_name,9+sheet_offset,index_col=1)

# Put all capacity test results in an array to make it easier to plot
cap_tests = [chrg_1, dchg_1, chrg_2, dchg_2, chrg_3, dchg_3] 
titles = ["Capacity Test #1 - Charge Cycle", "Capacity Test #1 - Discharge Cycle",\
"Capacity Test #2 - Charge Cycle", "Capacity Test #2 - Discharge Cycle",\
"Capacity Test #3 - Charge Cycle", "Capacity Test #3 - Discharge Cycle"]

# ----- Plots -----
if 'file_name2' in locals(): # print the names of the files being plotted
    print("Plots for:", file_name, "and", file_name2)
else:
    print("Plots for:", file_name)

# Capacity Tests
for idx, i in enumerate(cap_tests): # loop through each capacity test and plot results
    plt.figure(figsize=(10,5))
    plt.subplot(211)
    plt.plot(i.iloc[:,1])
    plt.ylabel("SOC (%)")
    plt.title(titles[idx])
    plt.grid(which='major',axis='both')
    plt.gca().xaxis.set_major_locator(md.HourLocator(interval = 1))
    plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
    plt.xticks(rotation = 45)
    
    plt.subplot(212)
    plt.plot(i.iloc[:,2],label=i.columns[2])
    plt.plot(i.iloc[:,3],label=i.columns[3])
    plt.plot(i.iloc[:,4],label=i.columns[4])
    plt.ylabel("Power (kW)")
    plt.legend()
    plt.grid(which='both',axis='both')
    plt.gca().xaxis.set_major_locator(md.HourLocator(interval = 1))
    plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
    plt.xticks(rotation = 45)

# Charge Ramp Rate (CRR) Test
crr_len = 300 # set how much data (maximum) of the CRR test to plot; 300 plots first 5 minutes

plt.figure(figsize=(10,5))
plt.subplot(211)
plt.plot(crr.iloc[0:crr_len,1]) 
plt.ylabel("SOC (%)")
plt.title("Charge Ramp Rate Test")
plt.grid(which='major',axis='both')
plt.gca().xaxis.set_major_locator(md.SecondLocator(interval = 5))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.xticks(rotation = 45)

plt.subplot(212)
plt.plot(crr.iloc[0:crr_len,2],label=crr.columns[2])
plt.plot(crr.iloc[0:crr_len,3],label=crr.columns[3])
plt.plot(crr.iloc[0:crr_len,4],label=crr.columns[4])
plt.ylabel("Power (kW)")
plt.legend()
plt.grid(which='both',axis='both')
plt.gca().xaxis.set_major_locator(md.SecondLocator(interval = 5))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.xticks(rotation = 45)

# Discharge Ramp Rate (DRR) Test
drr_len = crr_len # set how much data (maximum) of the DRR test to plot; 300 plots first 5 minutes

plt.figure(figsize=(10,5))
plt.subplot(211)
plt.plot(drr.iloc[0:drr_len,1])
plt.ylabel("SOC (%)")
plt.title("Discharge Ramp Rate Test")
plt.grid(which='major',axis='both')
plt.gca().xaxis.set_major_locator(md.SecondLocator(interval = 5))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.xticks(rotation = 45)

plt.subplot(212)
plt.plot(drr.iloc[0:drr_len,2],label=drr.columns[2])
plt.plot(drr.iloc[0:drr_len,3],label=drr.columns[3])
plt.plot(drr.iloc[0:drr_len,4],label=drr.columns[4])
plt.ylabel("Power (kW)")
plt.legend()
plt.grid(which='both',axis='both')
plt.gca().xaxis.set_major_locator(md.SecondLocator(interval = 5))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.xticks(rotation = 45)

# Output Transition Control (OTC or OTT) Test
plt.figure(figsize=(10,5))
plt.subplot(211)
plt.plot(otc.iloc[:,1])
plt.ylabel("SOC (%)")
plt.title("Output Transition Control Test")
plt.grid(which='major',axis='both')
plt.gca().xaxis.set_major_locator(md.HourLocator(interval = 1))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
plt.xticks(rotation = 45)

plt.subplot(212)
plt.plot(otc.iloc[:,2],label=otc.columns[2])
plt.plot(otc.iloc[:,3],label=otc.columns[3])
plt.plot(otc.iloc[:,4],label=otc.columns[4])
plt.ylabel("Power (kW)")
plt.legend()
plt.grid(which='both',axis='both')
plt.gca().xaxis.set_major_locator(md.HourLocator(interval = 1))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
plt.xticks(rotation = 45)

plt.show() # plots will not show up until this point
