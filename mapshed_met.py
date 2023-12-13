# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 14:31:17 2023

@author: Mehmet.kalfazade
"""


#importing necessary libraries
import os
os.system('cls')
import pandas as pd


#Daily min, max temperature and precipitation filenames
T_MIN_FILENAME 		= '1234_T_MIN.xlsx';	
T_MAX_FILENAME 		= '1234_T_MAX.xlsx';	
PRCP_FILENAME 		= '1234_PRCP.xlsx';	    


#Read and transform daily maximum temperature data
T_MAX_DATA          =  pd.read_excel(T_MAX_FILENAME)
#celsius to fahreneit conversion
T_MAX_DATA.iloc[:, 5] = (T_MAX_DATA.iloc[:, 5] * 1.8) + 32
YEARS               = T_MAX_DATA['YIL'].unique()
YEARS               = YEARS.astype(int)
FIRST_YEAR          = min(YEARS)
LAST_YEAR           = max(YEARS)
MONTHS              = T_MAX_DATA['AY'].unique()
MET_DATA_T_MAX_ROW  = (len(YEARS)*12)
MET_DATA_MONTHS 	= ['JAN','FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

MET_DATA_T_MAX      = pd.DataFrame(index=range(MET_DATA_T_MAX_ROW), columns=range(35))
#Filling NaN cells with -999999
MET_DATA_T_MAX      = MET_DATA_T_MAX.fillna(-999999)
STATION_NO 			= T_MAX_DATA.iloc[0,0]
MET_DATA_T_MAX.iloc[:, 0] 	= STATION_NO
MET_DATA_T_MAX.iloc[:, 1] 	= 'Tmax'

#Transforming long type data to wide data (days on columns months and years on rows)
for j in range(FIRST_YEAR, LAST_YEAR+1):
    T_MAX_YEAR = T_MAX_DATA[T_MAX_DATA.iloc[:,2]==j]
    T_MAX_YEAR = T_MAX_YEAR.iloc[:, [3, 5]]
    for i in range(1, 13):
        T_MAX_MONTHLY_DATA = T_MAX_YEAR[T_MAX_YEAR.iloc[:, 0]==i]
        T_MAX_MONTHLY_DATA = T_MAX_MONTHLY_DATA.iloc[:, 1]
        MET_DATA_T_MAX.iloc[(i-1)+((j-FIRST_YEAR)*12), 4:((len(T_MAX_MONTHLY_DATA)+4))]	= T_MAX_MONTHLY_DATA.T
        MET_DATA_T_MAX.iloc[((i-1)+((j-FIRST_YEAR)*12), 2)] = j
    MET_DATA_T_MAX.iloc[((i-1)+((j-FIRST_YEAR)*12)-11):((i+(j-FIRST_YEAR)*12)), 3] = MET_DATA_MONTHS

#---------------------------------------------------------------------------------------------#
#Repeating the process above for daily minimum temperature data

T_MIN_DATA          =  pd.read_excel(T_MIN_FILENAME)
T_MIN_DATA.iloc[:, 5] = (T_MIN_DATA.iloc[:, 5] * 1.8) + 32
YEARS               = T_MIN_DATA['YIL'].unique()
MONTHS              = T_MIN_DATA['AY'].unique()
MET_DATA_T_MIN_ROW  = (len(YEARS)*12)

MET_DATA_T_MIN      = pd.DataFrame(index=range(MET_DATA_T_MIN_ROW), columns=range(35))
MET_DATA_T_MIN      = MET_DATA_T_MIN.fillna(-999999)
STATION_NO 			= T_MIN_DATA.iloc[0,0]
MET_DATA_T_MIN.iloc[:, 0] 	= STATION_NO
MET_DATA_T_MIN.iloc[:, 1] 	= 'Tmin'

for j in range(FIRST_YEAR, LAST_YEAR+1):
    T_MIN_YEAR = T_MIN_DATA[T_MIN_DATA.iloc[:,2]==j]
    T_MIN_YEAR = T_MIN_YEAR.iloc[:, [3, 5]]
    for i in range(1, 13):
        T_MIN_MONTHLY_DATA = T_MIN_YEAR[T_MIN_YEAR.iloc[:, 0]==i]
        T_MIN_MONTHLY_DATA = T_MIN_MONTHLY_DATA.iloc[:, 1]
        MET_DATA_T_MIN.iloc[(i-1)+((j-FIRST_YEAR)*12), 4:((len(T_MIN_MONTHLY_DATA)+4))]	= T_MIN_MONTHLY_DATA.T
        MET_DATA_T_MIN.iloc[((i-1)+((j-FIRST_YEAR)*12), 2)] = j
    MET_DATA_T_MIN.iloc[((i-1)+((j-FIRST_YEAR)*12)-11):((i+(j-FIRST_YEAR)*12)), 3] = MET_DATA_MONTHS
    
#---------------------------------------------------------------------------------------------#
#Repeating the process above for daily precipitation data

PRCP_DATA          =  pd.read_excel(PRCP_FILENAME)
#mm to inch conversion
PRCP_DATA.iloc[:, 5] = (PRCP_DATA.iloc[:, 5] / 25.4)
PRCP_DATA.round({'TOPLAM_YAGIS_mm' : 4})
YEARS               = PRCP_DATA['YIL'].unique()
MONTHS              = PRCP_DATA['AY'].unique()
MET_DATA_PRCP_ROW  = (len(YEARS)*12)

MET_DATA_PRCP      = pd.DataFrame(index=range(MET_DATA_PRCP_ROW), columns=range(35))
MET_DATA_PRCP      = MET_DATA_PRCP.fillna(-999999)
STATION_NO 			= PRCP_DATA.iloc[0,0]
MET_DATA_PRCP.iloc[:, 0] 	= STATION_NO
MET_DATA_PRCP.iloc[:, 1] 	= 'Prcp'

for j in range(FIRST_YEAR, LAST_YEAR+1):
    PRCP_YEAR = PRCP_DATA[PRCP_DATA.iloc[:,2]==j]
    PRCP_YEAR = PRCP_YEAR.iloc[:, [3, 5]]
    for i in range(1, 13):
        PRCP_MONTHLY_DATA = PRCP_YEAR[PRCP_YEAR.iloc[:, 0]==i]
        PRCP_MONTHLY_DATA = PRCP_MONTHLY_DATA.iloc[:, 1]
        MET_DATA_PRCP.iloc[(i-1)+((j-FIRST_YEAR)*12), 4:((len(PRCP_MONTHLY_DATA)+4))]	= PRCP_MONTHLY_DATA.T
        MET_DATA_PRCP.iloc[((i-1)+((j-FIRST_YEAR)*12), 2)] = j
    MET_DATA_PRCP.iloc[((i-1)+((j-FIRST_YEAR)*12)-11):((i+(j-FIRST_YEAR)*12)), 3] = MET_DATA_MONTHS


#merging 3 final dataframe
MET_DATA = pd.concat([MET_DATA_T_MAX, MET_DATA_T_MIN, MET_DATA_PRCP])

#saving output as comma seperated value file as model input
MET_DATA.to_csv('C:/Users/mehmet.kalfazade/.spyder-py3/SCRIPTS_PY/MAPSHED_MET/Sta1234.csv', header=False, index=False)
