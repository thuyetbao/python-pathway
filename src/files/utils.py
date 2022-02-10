import os
import glob

def dir_ls(path, pattern: list = None):
    if not os.path.isfile(path):
        raise FileNotFoundError
    
    ls = []
    for pat in pattern:
        fi = glob.glob(f"{path}/{pat}", recursive = True)
        ls.extend(fi)

    return ls
