import os

root_path = os.getcwd()

if os.path.exists('slic3r2aerotech'):
    os.chdir('slic3r2aerotech')
    os.system('git pull')
    os.chdir('..')
else:
    os.system('git clone https://github.com/rtellez700/slic3r2aerotech.git')

# if 'slic3r-to-aerotech-examples' not in os.popen('conda env list').read():
#     os.system('conda create -n slic3r-to-aerotech-examples -y')

# os.system('conda activate slic3r-to-aerotech-examples')
# os.system('conda install pip -y')
# os.system('pip install -r requirements.txt -y')
os.chdir('slic3r2aerotech/src/main/python/')
os.system('python main.py')
os.chdir(root_path)