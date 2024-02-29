import subprocess
import os
# subprocess.run('python3 main_v4.py & python3 plate_reader.py', shell=True)
p = Popen([r'/home/pi/Desktop/WRO_code/reciever.py', "ArcView"], shell=True, stid=PIPE, stdout=PIPE)
output= p.communicate()
print(output[0])

p = Popen([r'/home/pi/Desktop/WRO_code/plate_reader.py', "ArcEditor"], shell=True, stid=PIPE, stdout=PIPE)
output= p.communicate()
print(output[0])