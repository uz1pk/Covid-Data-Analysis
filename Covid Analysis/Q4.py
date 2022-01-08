import sys
import csv
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
#Defining the index map for the data set I(conposcovidloc.csv) will be using
INDEX_MAP = {
        "Row_ID" :  0,
        "Accurate_Episode_Date" :  1,
        "Case_Reported_Date" :  2,
        "Test_Reported_Date" :  3,
        "Specimen_Date" :  4,
        "Age_Group" :  5,
        "Client_Gender" :  6,
        "Case_AcquisitionInfo" :  7,
        "Outcome1" :  8,
        "Outbreak_Related" :  9,
        "Reporting_PHU_ID" : 10,
        "Reporting_PHU" : 11,
        "Reporting_PHU_Address" : 12,
        "Reporting_PHU_City" : 13,
        "Reporting_PHU_Postal_Code" : 14,
        "Reporting_PHU_Website" : 15,
        "Reporting_PHU_Latitude" : 16,
        "Reporting_PHU_Longitude" : 17 }
#Defining the index map for the data set II(vaccine_doses.csv) will be using
INDEX_MAP_vac = {
        "report_date" :  0,
        "previous_day_doses_administered" :  1,
        "total_doses_administered" :  2,
        "total_doses_in_fully_vaccinated_individuals" :  3,
        "total_individuals_fully_vaccinated" :  4 }

def main(argv):

    if len(argv) != 2:
        print("Usage: Q4.py <Month>")
        
        sys.exit(1)

    
    month_user = int(argv[1])
    data=[]
    data_vac=[]
    test=[]


    # print out the specified index column from our sample data
    #opening the required csv files
    try:
        fh = open("conposcovidloc.csv", encoding="utf-8-sig")

    except IOError as err:
        print("Unable to open file '{}' : {}".format(
                "conposcovidloc.csv", err), file=sys.stderr)
        sys.exit(1)
    try:
        fh2 = open("vaccine_doses.csv", encoding="utf-8-sig")

    except IOError as err:
        print("Unable to open file '{}' : {}".format(
                "vaccine_doses.csv", err), file=sys.stderr)
        sys.exit(1)
  
    #reading csv files
    file_reader = csv.reader(fh)
    vaccine_file_reader = csv.reader(fh2)
    
    #calculating year and month to get formatted_date
    year = 2020 + ((month_user - 1) // 12)
    month = ((int(month_user) - 1) % 12) + 1
    int(month)
    if month < 10:
      formatted_date = str(year) + "-0" + str(month)
    else:    
      formatted_date = str(year) + "-" +str(month)

   
    
    # Checking how many days are in the given month
    days_in_month = 31;
    if month == 4 or month == 6 or month == 9 or month == 11:
      days_in_month = 30;
    elif month == 2:
      if year == 2020:
        days_in_month = 29
      else:
        days_in_month = 28
    elif month == 3 and year == 2021:
      days_in_month = 28 #Update depending on date
    
    row=[]
    day=""
    b=""
    curr_date=""
    count=0

    for row in file_reader:
      day=""
      curr_date=""
      if (row[INDEX_MAP["Case_Reported_Date"]][:-3] == formatted_date):
        
        day=row[INDEX_MAP["Case_Reported_Date"]][-2:]
        
        curr_date=formatted_date + "-" +day
        
        data.append(curr_date)
    fh.close()
    

    vac_admin=""
    row_vac=[]

    for row_vac in vaccine_file_reader:
      vac_admin=""
      if(row_vac[INDEX_MAP_vac["report_date"]][:-3] == formatted_date):
        
        vac_admin=row_vac[INDEX_MAP_vac["previous_day_doses_administered"]]
        day = row_vac[INDEX_MAP_vac["report_date"]][-2:]
        data_vac.append([vac_admin,day])
        
    fh2.close()
    
    
    for i in range(1,days_in_month+1):
      if len(data_vac) >= i:
        data_vac[i-1][0]= str(data_vac[i-1][0])
        data_vac[i-1][0]= data_vac[i-1][0].replace(',','')

      count=0
      if(i<10):
        b=formatted_date + "-0" + str(i)
      
      else:
        b=formatted_date +"-" + str(i)
        
      for row in data:
        if(row in b):
          count=count+1
  
      if len(data_vac) >= i:
        test.append({"Date":i,"Legend":"Vaccines","Count":int(data_vac[i-1][0]) })
      test.append({"Date":i,"Legend":"COVID cases","Count":count })
    
    # Plotting The graph using pandas and seaborn
    fig = plt.figure()

    sns.lineplot(x = "Date", y = "Count", hue="Legend",data=pd.DataFrame(test))
    plt.title("COVID cases and vaccines in " + formatted_date)

    fig.savefig("Q4Plot2.pdf", bbox_inches="tight")


# Calling main function
main(sys.argv)
