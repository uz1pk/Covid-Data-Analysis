import sys
import csv
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

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

def main(argv):
  
  if(len(argv) != 3):
    print("Usage: cases_by_age.py <file name> 'City Name'")
    sys.exit(1)

  filename = argv[1]
  region = argv[2]
  data_list = []
  counter = 0

  # Opening data file
  try:
          fh = open(filename, encoding="utf-8-sig")

  except IOError as err:
        print("Unable to open file '{}' : {}".format(
                filename, err), file=sys.stderr)
        sys.exit(1)

  data_reader = csv.reader(fh)

  # Placing all age groups of positive COVID cases within the requested city into a list
  for row in data_reader:
    Reporting_PHU_City = row[INDEX_MAP["Reporting_PHU_City"]]

    if Reporting_PHU_City.lower() == region.lower(): 
      data_list.append(row[INDEX_MAP["Age_Group"]])

  fh.close()
  data_list.sort()

  # Moving <20 to the front of the data text file
  for x in range(0, len(data_list) - 1):
    if data_list[x] == "<20":
      data_list.insert(0, data_list[x])

  # Check to see if a number is read twice in the data
  alreadyWritten = True

  # Writing the data in the list to a text file
  with open("Q2Plot.txt", "w") as f:
    f.write("Age Group,Total Cases\n")
    for x in range(0, len(data_list) - 1):
      if data_list[x] == data_list[x+1]:
        counter = counter + 1

      else:
        if alreadyWritten or data_list[x] != "<20":
          f.write("%s,%d\n"%(data_list[x], counter))

        #Fixing errors with <20 being written twice when changing the order of the print to the datalist
        if data_list[x] == "<20":
          alreadyWritten = False
        counter = 0

  # Generating Plot Files
  try:
    csv_df = pd.read_csv("Q2Plot.txt")

  except IOError as err:
    print("Unable to open source file", "Q2Plot.txt",
      ": {}".format(err), file=sys.stderr)
    sys.exit(-1)

  fig = plt.figure()

  # Printing plot
  sns.barplot(x = "Age Group", y = "Total Cases", data=csv_df)

  plt.title("COVID cases by age in " + region)
  
  fig.savefig("Guelph.pdf")

main(sys.argv)
