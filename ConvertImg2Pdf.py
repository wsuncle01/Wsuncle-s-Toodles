import os
import argparse as parse
#print(os.getcwd())
#os.system('pause')
img_ext = ['.webp','.bmp','.jpeg','.jpg','.png']
input_file_names = ""
for root,dirs,files in os.walk(os.getcwd(),topdown=True):
    files.sort()
    for file in files:
        file_ext = os.path.splitext(file)[1]
        if file_ext not in img_ext:
            #print("Not Image!")
            continue
        file_name = f"\"{root}/{file}\""
        os.system(f"magick {file_name} -background white -alpha remove -alpha off {file_name}")
        input_file_names += f"\"{root}/{file}\" "
        print(file)
        #print(input_file_names)

output_name = os.getcwd().split('/')[-1]
print(output_name)

os.system(f"img2pdf {input_file_names} -o \"{output_name}.pdf\"")
