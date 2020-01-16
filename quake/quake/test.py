import datetime



#local_date_time = datetime.datetime.strptime('1970-01-01' + ' 0:0:0.0',"%Y-%m-%d %H:%M:%S.%f")
#local_date_time = local_date_time + datetime.timedelta(milliseconds=1578959660779)
#print(local_date_time)


#coordinates = [56.14,65.15,5.2]

#print(coordinates[1])



import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(BASE_DIR + "\quake\quakemap")