import os
import argparse as parse
import re
from tqdm import tqdm
import pdb

zip_ext = ['.zip']
args = list()
OUTFILE_PATH = "output"
if not os.path.exists(OUTFILE_PATH):
    os.mkdir(OUTFILE_PATH)
for dir in os.listdir(os.getcwd()):
    if not os.path.isdir(dir):
        continue
    if dir == OUTFILE_PATH:
        continue
    files = os.listdir(dir)
    src_files = [f'./{dir}/{file}' for file in files]
    dst_files = [f'./{OUTFILE_PATH}/{dir}_{file}' for file in files]
    for i in range(len(files)):
        os.system(f"cp {src_files[i]} {dst_files[i]}")
    # pdb.set_trace()