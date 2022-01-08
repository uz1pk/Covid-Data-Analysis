import sys
import csv
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plot

#Defining the index map for the data set I will be using
INDEX_MAP = {
        "report_date" :  0,
        "previous_day_doses_administered" :  1,
        "total_doses_administered" :  2,
        "total_doses_in_fully_vaccinated_individuals" :  3,
        "total_individuals_fully_vaccinated" :  4 }

def main(argv):

  #checks to make sure the correct amount of arguments are provided
  #the arguments being, this python script, filename, and given month
  if len(argv) < 3 :
      
      print("Usage: vaccines_per_month.py <FILE> <Month>")
      print("<Month> should be a number with 2 digit spaces through 01 - 12")
      sys.exit(1)

  #storing each of the arguments into variables and declaring a list
  filename = argv[1]
  month = argv[2] 
  data = []

  #creating a formatted date for each year
  formatted_date_2020 = "2020-" + str(month)
  formatted_date_2021 = "2021-" + str(month)

  #integer form of the month to be used in conditionals later
  int_month = int(month)

  #check if the file name given even exists, if it does open it
  try:
    fh = open(filename, encoding="utf-8-sig")

  except IOError as err:
      print("Unable to open file '{}' : {}".format(filename, err), file=sys.stderr)
      sys.exit(1)

  #csv file reader to go through the csv file
  data_reader = csv.reader(fh)

  #looping through and appending the appropriate data elements to the data list
  #using the index map. 
  for row in data_reader:

    #this compares the user given date and compares it to the current row
    #to see if they are the same. When the year/month are the same it will append
    #the elements (report date and previous doses) to the data list.
    #there is no need for a sort function either since the data set comes pre-sorted
    #by date which in this case exactly what I need.
    if formatted_date_2020 in row[0]:
      data.append([row[ INDEX_MAP["report_date"] ], row[ INDEX_MAP["previous_day_doses_administered"] ] ])

    if formatted_date_2021 in row[0]:
      data.append([row[ INDEX_MAP["report_date"] ], row[ INDEX_MAP["previous_day_doses_administered"] ] ])

  #removing all commas in the numbers so that the csv reader for the txt file
  #that will be used to create the graph will not mistake it for a third element
  for i in range(len(data)):
    if "," in data[i][1]:
      data[i][1] = data[i][1].replace(",", "")

  #writing all the data to the data text file that will be reopened for the graph
  with open("Q3Data.txt", "w") as file:
    file.write("Day_Of_Month,Doses_Administered\n")
    for i in range(len(data)):
      tempDate = data[i][0]
      tempDoses = data[i][1]
      if int_month == 12:
        file.write("%s,%s\n"% (tempDate, tempDoses))
      else:
        file.write("%s,%s\n"% (tempDate[-2:], tempDoses))

  #here it checks to make sure the file was successfully printed/created
  try:
    csv_read_data = pd.read_csv("Q3Data.txt")

  except IOError as err:
    print("Unable to open data file", "Q3Data.txt",
      ": {}".format(err), file=sys.stderr)
    sys.exit(1)

  #from here we are simply graphing the lien graph with the names/parameters given
  #on lines 90-94 I am adding the given date the user wanted into the title.
  graph = plot.figure()

  sns.lineplot(x = "Day_Of_Month", y = "Doses_Administered", data = csv_read_data)

  if int_month < 12:
    plot.title("Doses Given Per Day on " + formatted_date_2021)

  else:
    plot.title("Doses Given Per Day on " + formatted_date_2020)
    
  graph.savefig("Q3Graph4.pdf", bbox_inches="tight")

#end of script
main(sys.argv)