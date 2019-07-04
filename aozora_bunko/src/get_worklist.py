import zipfile
import urllib.request
from pathlib import Path
import csv
import re
import tqdm

def get_zip_file(dpath):
    urllib.request.urlretrieve("https://www.aozora.gr.jp/index_pages/list_person_all_extended_utf8.zip", str(dpath / "list_person_all_extended_utf8.zip"))

def unzip(dpath):
    with zipfile.ZipFile(str(dpath / "list_person_all_extended_utf8.zip")) as existing_zip:
        existing_zip.extractall(str(dpath))

def get_worklist(dpath):
    worklist = []
    with open(str(dpath / "list_person_all_extended_utf8.csv"), newline='', encoding='utf_8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if(row["分類番号"] == "NDC 913" and row["文字遣い種別"] == "新字新仮名" and row["作品著作権フラグ"] == "なし" and not row["テキストファイルURL"] == ""):
                worklist.append(row)
    return worklist

def download_text_zip(item, zip_path, if_download=True):
    work_url = item["テキストファイルURL"]
    zip_name = re.sub(r".*/", "", work_url)
    if if_download:
        urllib.request.urlretrieve(work_url, str(zip_path / zip_name))
    return zip_name

def extract_text_zip(zip_path, zip_name, text_path):
    file_name = re.sub(r"\.zip", "", zip_name)
    with zipfile.ZipFile(str(zip_path / zip_name)) as existing_zip:
        existing_zip.extractall(str(text_path / file_name))
    
    return file_name

def get_work(dpath, worklist, download=True):
    zip_path = dpath / "zips"
    text_path = dpath / "texts"

    write_byte_num = 0
    output_file_num = 0
    fout = open(str(dpath / 'text_{:04d}_.txt'.format(output_file_num)), 'wt', encoding='utf_8')

    for item in tqdm.tqdm(worklist):
        zip_name = download_text_zip(item, zip_path, download)
        file_name = extract_text_zip(zip_path, zip_name, text_path)
            
        p_tmp = (text_path / file_name).glob('*.txt')
        for text_file in p_tmp:
            with open(str(text_file), 'rt', encoding='shift_jisx0213') as fstream:
                write_byte_num += fout.write(file_name)
                write_byte_num += fout.write('\n')
                texts = fstream.read(-1)
                    
                #作品名と著者名、及び注を削除
                texts = re.sub(r"^.+-+\s", "", texts, flags=re.DOTALL)
                texts = re.sub(r"^\s*", "", texts)
                    
                #文末の書誌情報の削除
                texts = re.sub(r"\s底本：.*$", "", texts, flags=re.DOTALL)
                    
                #行頭のスペース、改行の削除
                texts = re.sub(r"^\s+", "", texts, flags=re.MULTILINE)
                    
                #文中のルビを削除
                texts = re.sub(r"《.*?》", "", texts)

                #文中の注を削除
                texts = re.sub(r"［＃.*?］", "", texts)

                #文中のルビ用の記号の削除
                texts = re.sub(r"｜", "", texts)

                #かぎかっこを別の行に
                texts = re.sub(r"(?<!\n)「", "\n「", texts)
                texts = re.sub(r"」(?!\n)", "」\n", texts)
                
                #かぎかっこで始まらない行を句点で分割
                text_list = re.split(r"\n+", texts)
                text_list_new = []
                for text_line in text_list:
                    if(not re.match(r"^「", text_line)):
                        text_line = re.sub(r"。(?!\s)", "。\n", text_line)
                    text_list_new.append(text_line)
                texts = "\n".join(text_list_new)

                write_byte_num += fout.write(texts)
                write_byte_num += fout.write("\n\n\n")
        if write_byte_num > 1000000:
            fout.close()
            output_file_num += 1
            write_byte_num = 0
            fout = open(str(dpath / 'text_{:04d}_.txt'.format(output_file_num)), 'wt', encoding='utf_8')
    fout.close()

if __name__ == "__main__":
    use_proxy = True
    #use_prixy = False
    #download = True
    download = False
    data_path = Path("./aozora_bunko/datas")
    if download:
        if use_proxy:
            proxy = urllib.request.ProxyHandler({'https':'http://proxy.uec.ac.jp:8080'})
            urllib.request.install_opener(urllib.request.build_opener(proxy))
        get_zip_file(data_path)
        unzip(data_path)
    worklist = get_worklist(data_path)
    get_work(data_path, worklist, download)