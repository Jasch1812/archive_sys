import os

for rt, dirs, files in os.walk('/home/johann/Downloads',topdown=False):
  print dirs[0]

# for f in os.listdir('/home/johann/Downloads'):
#   print f