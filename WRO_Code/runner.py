import subprocess
import os
# subprocess.run('python3 main_v4.py & python3 plate_reader.py', shell=True)
key = 1
while key != 32:
    os.system('main_v4.py')
    os.system('plate_reader.py')
    os.system('reciever.py')