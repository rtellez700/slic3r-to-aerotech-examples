import os

root_path = os.getcwd()

if os.path.exists('slic3r2aerotech'):
    os.chdir('slic3r2aerotech')
    os.system('git pull')
    os.chdir('..')
else:
    os.system('git clone https://github.com/rtellez700/slic3r2aerotech.git')

os.chdir('slic3r2aerotech/src/main/python/')
os.system('python main.py')
os.chdir(root_path)