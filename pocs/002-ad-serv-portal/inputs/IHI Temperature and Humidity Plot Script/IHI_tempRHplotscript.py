# Author: Paul Giessner, Borrego
# Date last modified: 10/13/2022
# Purpose: Plot IHI commissioning test results data, including capacity,
# ramp rate (charge and discharge), and output transition control tests

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md

# ----- Import data -----
# Data sent 2022-07-28
# f1 = "2022-04-21_299FARMTOMARKET_container1_Data.xlsx"
# f2 = "2022-04-28_77FARMTOMARKET_container1_Data.xlsx"
# f3 = "2022-04-27_71CHARLOTTEFURNACE_container1_Data.xlsx"
# f4 = "2022-04-30_160TIHONET_container1_Data.xlsx"
# f5 = "2022-04-30_160TIHONET_container2_Data.xlsx"
# f6 = "2022-04-30_196TREMONT_container1_Data.xlsx"
# f7 = "2022-04-30_196TREMONT_container2_Data.xlsx"
# f8 = "2022-04-27_0HAMMOND1_container1_Data.xlsx"
# f9 = "2022-04-27_0HAMMOND1_container2_Data.xlsx"

# Data sent 2022-09-02
f1 = "299farmtomarket temp data.xlsx"
f2 = "77 farmtomarket.xlsx"
f3 = "71charlottefurnace temp data.xlsx"
f4 = "160 tihonet temp data.xlsx"
f5 = "196 tremont temp data.xlsx"
f6 = "ohammond1and2tempdata.xlsx"
f7 = "59 federal 2 temp data.xlsx"
f8 = "276 federal  temp data.xlsx"

# File import parameters
# sheet_offset = 0 # accounts for different spreadsheet configs IHI may use; 0 is default
# header_row = 1 # number of rows before data columns start in Excel file

# Read data from Excel/CSV file(s)
header_row = 1 # could be 0 or 1; look at files
idx_col = 1 # could be 0 or 1; look for "local timestamp" in files

# Data sent 2022-07-28
# data_299FTM = pd.read_excel(f1,index_col=0,skiprows=header_row)
# data_77FTM = pd.read_excel(f2,index_col=0,skiprows=header_row)
# data_71CFR = pd.read_excel(f3,index_col=0,skiprows=header_row)
# data_160TIH1 = pd.read_excel(f4,index_col=0,skiprows=header_row)
# data_160TIH2 = pd.read_excel(f5,index_col=0,skiprows=header_row)
# data_196TRE1 = pd.read_excel(f6,index_col=0,skiprows=header_row)
# data_196TRE2 = pd.read_excel(f7,index_col=0,skiprows=header_row)
# data_0HAM1 = pd.read_excel(f8,index_col=0,skiprows=header_row)
# data_0HAM2 = pd.read_excel(f9,index_col=0,skiprows=header_row)

# Data sent 2022-09-02
data_299FTM = pd.read_excel(f1,index_col=idx_col,skiprows=header_row)
data_77FTM = pd.read_excel(f2,index_col=idx_col,skiprows=header_row)
data_71CFR = pd.read_excel(f3,index_col=idx_col,skiprows=header_row)
data_160TIH = pd.read_excel(f4,index_col=idx_col,skiprows=header_row)
data_196TRE = pd.read_excel(f5,index_col=idx_col,skiprows=header_row)
data_0HAM = pd.read_excel(f6,index_col=idx_col,skiprows=header_row)
data_59FED2 = pd.read_excel(f7,index_col=idx_col,skiprows=header_row)
data_276FED = pd.read_excel(f8,index_col=idx_col,skiprows=header_row)

# Acceptance Criteria
max_temp = 30;
max_humidity = 80;

# Put all capacity test results in an array to make it easier to plot
# Data sent 2022-07-28
# containers = [data_299FTM,data_77FTM,data_71CFR,data_160TIH1,data_160TIH2,\
# data_196TRE1,data_196TRE2,data_0HAM1,data_0HAM2] 
# titles = ["299 FTM", "77 FTM", "71 CFR", "160 TIH #1", "160 TIH #2",\
# "196 TRE #1", "196 TRE #2","0 HAM #1", "0 HAM #2"]
# Data sent 2022-09-02
containers = [data_299FTM,data_77FTM,data_71CFR,data_160TIH,data_196TRE,\
data_0HAM,data_59FED2,data_276FED] 
titles = ["299 FTM", "77 FTM", "71 CFR", "160 TIH", "196 TRE",\
"0 HAM", "59 FED #2", "276 FED"]

# ----- Plots -----
# if 'file_name2' in locals(): # print the names of the files being plotted
    # print("Plots for:", file_name, "and", file_name2)
# else:
    # print("Plots for:", file_name)

# Plots
for idx, i in enumerate(containers): # loop through each site's container and plot results
    i = i.drop('t_stamp', axis=1) # remove the non-local timestamp column, if needed

    plt.figure(figsize=(10,5)) # make plot figure
        
    # top plot for humidity
    plt.subplot(211)
    for x in range(0,i.shape[1],4):
        plt.plot(i.iloc[:,x],label=i.columns[x])
        # plot text
        plt.text(i.index[0], 10*(x/4+1), i.columns[x] + ': % of points over 80% = '\
+ "{:.2f}".format(100*(i.iloc[:,x]>80).sum()/len(i.iloc[:,x]),4) + '% (' + str(len(i.iloc[:,x]))\
+ " data points)", fontsize = 12)
    
    plt.legend()
    plt.axhline(y=max_humidity,linestyle='--') # plot acceptance criteria line
    plt.gca().set_ylim(0, 100)
    plt.ylabel("Relative Humidity (%)")
    plt.title(titles[idx] + " Container Conditions")
    plt.grid(which='major',axis='both')
    plt.gca().xaxis.set_minor_locator(md.DayLocator(interval = 1))
    plt.gca().xaxis.set_major_locator(md.DayLocator(interval = 7))
    plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation = 45)

    # bottom plot for temperature
    plt.subplot(212)
    for y in range(0,i.shape[1],4):
        plt.plot(i.iloc[:,y+1],label=i.columns[y+1]) 
        try:
            plt.plot(i.iloc[:,y+2],label=i.columns[y+2])
        except:
            print("Missing column")
        try:
            plt.plot(i.iloc[:,y+3],label=i.columns[y+3])
        except:
            print("Missing column")
            
    plt.legend()
    plt.axhline(y=max_temp,color='r',linestyle='--') # plot acceptance criteria line
    plt.ylabel("Container Temperature (C)")
    plt.grid(which='major',axis='both')
    plt.gca().xaxis.set_minor_locator(md.DayLocator(interval = 1))
    plt.gca().xaxis.set_major_locator(md.DayLocator(interval = 7))
    plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation = 45)

plt.show() # plots will not show up until this point
