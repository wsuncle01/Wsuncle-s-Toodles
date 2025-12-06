import os
import argparse as parse
import re
from tqdm import tqdm
from PyPDF2 import PdfReader,PdfWriter

# print(os.getcwd())
img_ext = ['.webp','.bmp','.jpeg','.jpg','.png']
args = list()
OUTFILE_PATH = "./output"
if not os.path.exists(OUTFILE_PATH):
    os.mkdir(OUTFILE_PATH)
for root,dirs,files in os.walk(os.getcwd(),topdown=True):
    files.sort()
    print(f'{root}')
    pbar_files = tqdm(files)
    input_file_names = ""
    for file in pbar_files:
        file_ext = os.path.splitext(file)[1]
        if file_ext not in img_ext:
            #print("Not Image!")
            continue
        pbar_files.set_description('Processing '+file)
        file_name = f"\"{root}/{file}\""
        os.system(f"magick {file_name} -background white -alpha remove -alpha off {file_name}")
        input_file_names += f"\"{root}/{file}\" "
    if input_file_names == "":
        continue
    output_name = root.split('/')[-1]
    output_name_file = f'\"{OUTFILE_PATH}/{output_name}.pdf\"'
    args.append((input_file_names,output_name_file,output_name))

print("parsing args end.")
print("starting convert img2pdf!!!")
pbar_args = tqdm(args)
for (input_file_names,output_name_file,output_name) in pbar_args:
    pbar_args.set_description('Processing '+output_name)
    os.system(f"img2pdf {input_file_names} -o {output_name_file}")

print("dump to pdf end.")
print("starting set meta info!!!")
pbar_meta_data = tqdm(args)
for (input_file_names,output_name_file,output_name) in pbar_meta_data:
    pbar_args.set_description('Processing '+output_name)
    try:
        Author = re.match(r'^\[(.*?)\]',output_name).groups()[0]
    except:
        Author = "Unknown"
    try:
        Title = re.match(r'^\[(.*?)\](.*)$',output_name).groups()[1]
    except:
        Title = "Unknown"
    reader = PdfReader(f"{os.getcwd()}/{OUTFILE_PATH}/{output_name}.pdf")
    writer = PdfWriter()
    metadata = {
        "/Author": f"{Author}",
        "/Title": f"{Title}",
        "/Creator": "wsuncle",
    }
    writer.add_metadata(metadata)
    writer.append_pages_from_reader(reader)
    with open(f"{os.getcwd()}/{OUTFILE_PATH}/{output_name}.pdf", "wb") as output_file:
        writer.write(output_file)