import os
import argparse as parse
import re
from tqdm import tqdm

zip_ext = ['.zip']
args = list()
OUTFILE_PATH = "./output"
if not os.path.exists(OUTFILE_PATH):
    os.mkdir(OUTFILE_PATH)
for root,dirs,files in os.walk(os.getcwd(),topdown=True):
    files.sort()
    print(f'{root}')
    for file in files:
        file_ext = os.path.splitext(file)[1]
        file_rm_ext = os.path.splitext(file)[0]
        if file_ext not in zip_ext:
            continue
        file_name = f"\"{root}/{file}\""
        file_name = file_name.replace(" ","\ ").replace("(","\(").replace(")","\)")
        os.system(f"unzip \"{file_name}\" -d \"{file_rm_ext}\"")
