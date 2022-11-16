
from lib.PythonSetup import *

def refresh_selSolutions(datapath, selSolutions):
    temp=selSolutions.value
    selSolutions.options = listFilesInDirectory(datapath)
    selSolutions.value=temp

def unusedfname(datapath, fnamebase):
    notavailable=True
    i=0
    while notavailable and i<100:
        i=i+1
        notavailable=os.path.exists(f'{datapath}/{fnamebase}{i}')
    return (fnamebase+str(i))

def listFilesInDirectory(datapath):
    mylist=[]
    mytimes=[]
    files = [f for f in os.listdir(datapath) if os.path.isfile(os.path.join(datapath,f))]
    for strfile in files:
        if strfile != '.ipynb_checkpoints':
            mylist.append(strfile)    
            mytimes.append(os.path.getmtime(f'{datapath}/{strfile}'))
    mylist=pd.Series(data=mylist, dtype='object', index=mytimes).sort_index(ascending=False).tolist()
    return mylist 

def Clear(datapath):
    for folder, subfolders, files in os.walk(datapath):
        send2trash.send2trash(folder)
