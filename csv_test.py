import csv 

with open('text.csv', 'w') as csvfile:
  w = csv.writer(csvfile)
  w.writerow('haha,uno,dos')