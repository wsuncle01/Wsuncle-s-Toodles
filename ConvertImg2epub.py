import os
import re
import argparse as parse
from tqdm import tqdm
import shutil
import uuid
from datetime import datetime
from PIL import Image

# print(os.getcwd())
img_ext:list = ['.webp','.bmp','.jpeg','.jpg','.png']
quality:int = 50

#path
OUTFILE_PATH = "./output"
CSS_PATH = "/Users/huangzhe/Documents/Python/style.css"
EPUB_FMT_PATH = __file__.rsplit('/',1)[0] + "/epub_format/"
VOL_OPF = EPUB_FMT_PATH + "vol.opf"
VOL_NCX = EPUB_FMT_PATH + "vol.ncx"
STYLE_CSS = EPUB_FMT_PATH + "style.css"
SGC_NAV_CSS = EPUB_FMT_PATH + "sgc-nav.css"
COVER_HTML = EPUB_FMT_PATH + "cover.html"
MAIN_HTML = EPUB_FMT_PATH + "MAIN.html"
NAV_HTML = EPUB_FMT_PATH + "nav.xhtml"

#fmt
manifest_page_main_fmt:str = '    <item id="Page_{count}" '\
                            'href="html/page-{count}.html" '\
                            'media-type="application/xhtml+xml"/>\n'
manifest_page_img_fmt:str = '    <item id="img_{count}" '\
                            'href="image/img_{count}.{file_ext}" '\
                            'media-type="image/{file_ext}"/>\n'
manifest_page_cover_main_fmt:str = '    <item id="Page_cover" '\
                                   'href="html/cover.html" '\
                                    'media-type="application/xhtml+xml"/>\n'
manifest_page_cover_img_fmt:str = '    <item id="cover_img" href="image/cover.{file_ext}" '\
                                  'media-type="image/{file_ext}" '\
                                  'properties="cover-image"/>\n'
spine_page_cov_fmt:str = '    <itemref idref="Page_cover"/>\n'
spine_page_main_fmt:str = '    <itemref idref="Page_{count}"/>\n'
navMap_main_fmt:str = \
'    <navPoint class="other" id="Page_{count}" playOrder="{count}">\n'\
'      <navLabel><text>第{count}页</text></navLabel>\n'\
'      <content src="../html/page-{count}.html"/>\n'\
'    </navPoint> \n'


#info
VOL_OPF_INFO = {
"KSBN_ID":"",
"Title":"",
"author":"",
"publisher":"",
"date":"",
"rights":"",
"series":"",
"number":"",
"manifest_page_main":"",
"manifest_page_img":"",
"spine_page_main":"",
}

VOL_NCX_INFO = {
"uuid":"",
"Page_Num":"",
"Title":"",
"Author":"",
"navMap_main":"",
}

def reset_info() -> None:
    for Name in ("VOL_OPF_INFO",
                 "VOL_NCX_INFO",):
        for key in globals()[Name].keys():
            globals()[Name][key] = ""

def output_dir(output_name:str) -> str:
    output_name_file = f'{OUTFILE_PATH}/{output_name}'
    if os.path.exists(output_name_file):
        shutil.rmtree(output_name_file)
    os.mkdir(output_name_file)
    return output_name_file

def get_meta_data(output_name:str) -> dict:
    metaInfo=dict()
    try:
        Author = re.match(r'^\[(.*?)\]',output_name).groups()[0]
    except:
        Author = "Unknown"
    try:
        Title = re.match(r'^\[(.*?)\](.*)$',output_name).groups()[1]
    except:
        Title = "Unknown"
    
    metaInfo["Author"] = Author
    metaInfo["Title"] = Title
    metaInfo["publisher"] = "wsuncle"
    metaInfo["date"] = datetime.now().year
    metaInfo["rights"] = "wsuncle"
    metaInfo["series"] = Title
    metaInfo["number"] = 0
    return metaInfo

def dump_vol_opf(output_name_file:str,
                 metaInfo:dict,
                 manifest_page_main:str,
                 manifest_page_img:str,
                 spine_page_main:str,
                 file_ext:str) -> None:
    VOL_OPF_INFO["KSBN_ID"] = str(uuid.uuid4())
    VOL_OPF_INFO["author"] = metaInfo["Author"]
    VOL_OPF_INFO["Title"] = metaInfo["Title"]
    VOL_OPF_INFO["publisher"] = metaInfo["publisher"]
    VOL_OPF_INFO["date"] = metaInfo["date"]
    VOL_OPF_INFO["rights"] = metaInfo["rights"]
    VOL_OPF_INFO["series"] = metaInfo["series"]
    VOL_OPF_INFO["number"] = metaInfo["number"]
    VOL_OPF_INFO["manifest_page_main"] = manifest_page_main
    VOL_OPF_INFO["manifest_page_img"] = manifest_page_img
    VOL_OPF_INFO["spine_page_main"] = spine_page_main
    VOL_OPF_INFO["file_ext"] = file_ext
    open(output_name_file+"/vol.opf","w").write(
        open(VOL_OPF,"r").read().format(**VOL_OPF_INFO)
    )

def dump_css(css_path:str) -> None:
    if not os.path.exists(css_path):
        os.mkdir(css_path)
    open(css_path+"/sgc-nav.css","w").write(
        open(SGC_NAV_CSS,"r").read()
    )
    open(css_path+"/style.css","w").write(
        open(STYLE_CSS,"r").read()
    )

def dump_ncx(ncx_path:str,
             metaInfo:dict,
             page_count:int,
             navMap_main:str) -> None:
    if not os.path.exists(ncx_path):
        os.mkdir(ncx_path)
    VOL_NCX_INFO["uuid"] = str(uuid.uuid4())
    VOL_NCX_INFO["Title"] = metaInfo["Title"]
    VOL_NCX_INFO["Author"] = metaInfo["Author"]
    VOL_NCX_INFO["Page_Num"] = page_count
    VOL_NCX_INFO["navMap_main"] = navMap_main
    open(ncx_path+"/vol.ncx","w").write(
        open(VOL_NCX,"r").read().format(**VOL_NCX_INFO)
    )

def dump_main_cov(main_path:str,
                  file_ext:str) -> None:
    if not os.path.exists(main_path):
        os.mkdir(main_path)
    open(main_path + "/cover.html","w").write(
        open(COVER_HTML,"r").read().format(file_ext=file_ext)
    )

def dump_main(main_path:str,
              page_count:int,
              file_ext:str) -> None:
    if not os.path.exists(main_path):
        os.mkdir(main_path)
    open(main_path + f"/page-{page_count}.html","w").write(
        open(MAIN_HTML,"r").read().format(count=page_count,file_ext=file_ext)
    )

def dump_nav(main_path:str) -> None:
    if not os.path.exists(main_path):
        os.mkdir(main_path)
    open(main_path + f"/nav.xhtml","w").write(
        open(NAV_HTML,"r").read()
    )


def dump_img_cov(img_path:str,
                 input_path:str,
                 file_ext:str) -> None:
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    img = Image.open(input_path)
    img = img.convert('RGB')
    img.save(img_path + f"/cover.{file_ext}", quality=quality)

def dump_img(img_path:str,
             input_path:str,
             page_count:int,
             file_ext:str) -> None:
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    size:int = os.path.getsize(input_path)
    img = Image.open(input_path)
    img = img.convert('RGB')
    img.save(img_path + f"/img_{page_count}.{file_ext}", quality=quality)

if not os.path.exists(OUTFILE_PATH):
    os.mkdir(OUTFILE_PATH)
for root,dirs,files in os.walk(os.getcwd(),topdown=True):
    if root.startswith(os.getcwd()+"/output") or root == os.getcwd():
        continue
    print(root)
    files.sort()
    none_img:bool = True
    
    page_count:int = 1
    input_file_list:list = list()
    manifest_page_main:str = ""
    manifest_page_img:str = ""
    spine_page_main:str = ""
    navMap_main:str = ""

    output_name = root.split('/')[-1]
    output_name_file = output_dir(output_name)

    pbar_files = tqdm(files)
    for file in pbar_files:
        file_ext = os.path.splitext(file)[1]
        if file_ext not in img_ext:
            continue
        # file_ext = file_ext.replace(".","")
        file_ext = "jpg"
        pbar_files.set_description('Processing '+file)
        input_file_names = f"{root}/{file}"
        input_file_list.append(input_file_names)
        if page_count == 1:
            manifest_page_main += manifest_page_cover_main_fmt
            manifest_page_img += manifest_page_cover_img_fmt.format(file_ext=file_ext)
            spine_page_main += spine_page_cov_fmt
            dump_main_cov(output_name_file+"/html",
                          file_ext)
            dump_img_cov(output_name_file+"/image",
                         input_file_names,
                         file_ext)
        
        manifest_page_main += manifest_page_main_fmt.format(count=page_count)
        manifest_page_img += manifest_page_img_fmt.format(count=page_count,file_ext=file_ext)
        spine_page_main += spine_page_main_fmt.format(count=page_count)
        navMap_main += navMap_main_fmt.format(count=page_count)
        dump_main(output_name_file+"/html",
                  page_count,
                  file_ext)
        dump_img(output_name_file+"/image",
                 input_file_names,
                 page_count,
                 file_ext)
        none_img = False
        page_count += 1

    manifest_page_main = manifest_page_main[:-1]
    manifest_page_img = manifest_page_img[:-1]
    spine_page_main = spine_page_main[:-1]
    navMap_main = navMap_main[:-1]
    page_count -= 1

    if none_img :
        continue

    print("starting set meta info!!!")
    metaInfo:dict = get_meta_data(output_name)
    
    print("dump epub data")
    dump_vol_opf(output_name_file,
                 metaInfo,
                 manifest_page_main,
                 manifest_page_img,
                 spine_page_main,
                 file_ext)
    dump_nav(output_name_file + "/html")
    dump_css(output_name_file + "/css")
    dump_ncx(output_name_file + "/xml",
             metaInfo,
             page_count,
             navMap_main)
    if os.path.exists(output_name_file + ".epub"):
        os.remove(output_name_file + ".epub")
    shutil.make_archive(output_name_file, 'zip', root_dir=output_name_file)
    os.rename(output_name_file + ".zip",output_name_file + ".epub")
    if os.path.exists(output_name_file):
        shutil.rmtree(output_name_file)
    reset_info()
