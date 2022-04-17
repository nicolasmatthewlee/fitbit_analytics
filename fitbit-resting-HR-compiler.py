import os
import json

# get folder
folder=input('What is the address to your MyFitbitData physical activity folder?\nex) xxx/MyFitbitData/JohnSmith/Physical Activity\n')

# get list of filenames of Heart Rate Variability Details
filenames=os.listdir(folder)
rhr_file=""

# find resting_heart_rate file
for f in filenames:
    if 'resting_heart_rate' in f:
        rhr_file=f
if rhr_file == "":
    print('Could not find any "resting_heart_rate" files.')
    os._exit(1)

# open file and load data
file=open(os.path.join(folder,rhr_file))
data=json.load(file)

# compile rhr data
csv_text="date,rhr,error\n"
for d in data:
    if d['value']['value'] != 0:
        csv_text+=d['dateTime']+','+str(d['value']['value'])+','+str(d['value']['error'])+'\n'

# save data
path=os.path.join(folder,'rhr_compiled.csv')
csv=open(path,'w')
csv.write(csv_text)
csv.close()
print(f'Data saved to: {path}')