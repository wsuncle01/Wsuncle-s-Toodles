import os
import re
import ebooklib
from ebooklib import epub
import argparse as parse
from tqdm import tqdm

# print(os.getcwd())
img_ext = ['.webp','.bmp','.jpeg','.jpg','.png']
OUTFILE_PATH = "./output"
CSS_PATH = "/Users/huangzhe/Documents/Python/style.css"
if not os.path.exists(OUTFILE_PATH):
    os.mkdir(OUTFILE_PATH)
for root,dirs,files in os.walk(os.getcwd(),topdown=True):
    files.sort()
    print(f'{root}')
    pbar_files = tqdm(files)

    none_img = True
    
    book = epub.EpubBook()
    page_count = 0
    spine = []
    toc = ()
    nav_css = epub.EpubItem(
        uid="style",
        file_name="style/style.css",
        media_type="text/css",
        content=open(CSS_PATH,"r").read(),
    )
    for file in pbar_files:
        file_ext = os.path.splitext(file)[1]
        if file_ext not in img_ext:
            continue
        pbar_files.set_description('Processing '+file)
        input_file_names = f"{root}/{file}"
        if page_count == 0:
            book.set_cover(f"cover.{file_ext}",open(input_file_names, "rb").read())
        c1 = epub.EpubHtml(title=f"第{page_count}页", file_name=f"{'%05d' % page_count}.xhtml", lang="ch")
        c1.content = (
            f'<p><img alt="{'%05d' % page_count}" src="Images/{file}"/></p>'
        )
        book.add_item(c1)
        c1.add_item(nav_css)
        spine.append(c1)
        img = epub.EpubImage(
            uid=f"image_{'%05d' % page_count}",
            file_name=f"Images/{file}",
            media_type=f"image/{file_ext}",
            content=open(input_file_names, "rb").read(),
        )
        book.add_item(img)
        none_img = False
        page_count += 1
    
    if none_img :
        continue
    
    output_name = root.split('/')[-1]
    output_name_file = f'{OUTFILE_PATH}/{output_name}.epub'
    print("starting set meta info!!!")
    try:
        Author = re.match(r'^\[(.*?)\]',output_name).groups()[0]
    except:
        Author = "Unknown"
    try:
        Title = re.match(r'^\[(.*?)\](.*)$',output_name).groups()[1]
    except:
        Title = "Unknown"
    print(f"Author:{Author}\nTitle:{Title}")
    book.toc = (
        epub.Link("cover.xhtml", "cover", "cover"),
        (epub.Section("Languages"), tuple(spine)),
    )
    book.spine = spine
    book.set_title(Title)
    book.add_item(nav_css)
    book.add_author(Author)
    book.set_language("zh")
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(output_name_file, book)
