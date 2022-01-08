# Question 1: How many cases were there each day in different cities in Ontario for a given month?

# This program will create a graph of the COVID cases in a given month for the cities in Ontario with the most cases. 

# The first command line argument is the amount of months since the start of COVID
# For example, "3" would be March 2020 and "15" would be March 2021

# The second command line argument is the number of cities you want to appear in the graph. 
# This is optional and if a second argument isn't given, then 5 cities will be shown on the graph

import sys
import csv
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# This function is called when the user runs the program incorrectly
def usage():
  print("\nUsage: python Q1.py <Months> (<Number of cities>)")
  print("<Months> should be a value between 1 and 15")
  print("<Number of cities> is optional and should be a value between 1 and 20")
  sys.exit(1)

def main(argv):

  # Making sure the right number of cmd line args is given
  # And giving the option for either 2 or 3 cmd line args
  if len(argv) != 3 :
    if len(argv) != 2:
      print("\nError: Incorrect number of arguments provided")
      usage()
    else: num_cities_in_graph = 5; # default num_cities is 5
  
  else: # If there are 3 cmd line args
  # Making sure num cities is an int
    try:
      num_cities_in_graph = int(argv[2]);
    except ValueError:
      print("\nError: <Number of cities> was entered incorrectly")
      usage()
  
  # Making sure months is an int
  try:
    months_input = int(argv[1])
  except ValueError:
    print("\nError: <Months> was entered incorrectly")
    usage()

  if num_cities_in_graph < 1:
    num_cities_in_graph = 1

  # Formatting the date based on the months given
  year = 2020 + ((months_input - 1) // 12)
  month = ((months_input - 1) % 12) + 1
  formatted_date = str(year) + "-" + str(month).zfill(2)

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
    days_in_month = 28
  
  print("Opening data file...")
  # Opening covid cases data file
  try:
    fh = open("conposcovidloc.csv", encoding="utf-8-sig")

  except IOError as err:
    print("Unable to open file '{}' : {}"
    .format("conposcovidloc.csv", err), file=sys.stderr)
    sys.exit(1)


  reader = csv.reader(fh)
  raw_data = []
  city_list = []
  data_list = []
  grand_list = []
  pandas_list = []
  dates = []
  current_city = ""
  first = True

  print("Reading data...")
  # Trying to store all the needed data of the given month into an array
  # Needed data: Episode_Date: row[1], Reporting_PHU_City: row[13]
  for row in reader:
    if formatted_date in row[1]:
      raw_data.append([row[1],row[13]])
  
  # Closing file
  fh.close()
  
  # Making sure there was at least 1 case that month
  if (len(raw_data) < 1):
    print("\nNo data found in the month of " + formatted_date)
    sys.exit(1)

  # Making a list of all the cities that have any cases
  # and the number of cases in each city
  for x in raw_data:
    if not(x[1] in city_list):
      city_list.append(x[1])
      data_list.append([x[1], 1])
    else:
      for city in data_list:
        if x[1] in city[0]:
          city[1] += 1

  print("Sorting data...")
  # Sorting the list by num of cases total in the month
  data_list.sort(reverse = True, key = lambda x: x[1])

  # Making sure that numcities isn't higher than the amount of cities in the data
  if len(data_list) < num_cities_in_graph:
    num_cities_in_graph = len(data_list)
 

  # This goes through the cities with the most cases
  # and adds the data to "grand_list"
  for city_rank in range(num_cities_in_graph):

    current_city = data_list[city_rank][0]
    
    #Checking for data on each day
    for day in range(days_in_month):
      for row in raw_data:
        if current_city in row[1]:
          if(formatted_date + "-" + str(day+1).zfill(2) in row[0]):
            if(first):
              dates.append([row[0], 1])
              first = False
            else:
              dates[day][1] += 1

      if (first == True):
        dates.append([formatted_date + "-" + str(day+1).zfill(2) , 0])
      first = True
    
    grand_list.append([current_city , dates])
    dates = []


  # Arranging data in a format that can be plotted
  for days in range(days_in_month):
    for city in range(len(grand_list)):
      pandas_list.append(
        {
          "Date":int(grand_list[city][1][days][0][-2:]),
          "City":grand_list[city][0],
          "Count":grand_list[city][1][days][1]
        }
      )
  
  print("Plotting data on a graph...")
  
  # Plotting The graph using pandas and seaborn
  fig = plt.figure()

  sns.lineplot(x = "Date", y = "Count", hue="City",data=pd.DataFrame(pandas_list))
  plt.title("COVID cases per day in " + formatted_date )

  # Moving legend outside of graph
  plt.legend(bbox_to_anchor=(1.01, 1.0),loc='upper left')
  
  plt.tight_layout()
  fig.savefig("Q1Plot.pdf", bbox_inches="tight")

  print("Graph plotted, check Q1Plot.pdf to see it!")

# Calling main function
main(sys.argv)