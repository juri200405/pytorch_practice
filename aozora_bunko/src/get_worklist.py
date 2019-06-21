import zipfile
import urllib.request
from pathlib import Path
import csv

def get_zip_file(dpath):
    urllib.request.urlretrieve("https://www.aozora.gr.jp/index_pages/list_person_all_extended_utf8.zip", str(data_path / "list_person_all_extended_utf8.zip"))

def unzip(dpath):
    with zipfile.ZipFile(str(data_path / "list_person_all_extended_utf8.zip")) as existing_zip:
        existing_zip.extractall(str(data_path))

def get_worklist(dpath):
    worklist = []
    with open(str(dpath / "list_person_all_extended_utf8.csv"), newline='', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if(row["分類番号"] == "NDC 913" and row["文字遣い種別"] == "新字新仮名" and row["作品著作権フラグ"] == "なし"):
                worklist.append(row)
    return worklist

if __name__ == "__main__":
    data_path = Path("./aozora_bunko/datas")
    #get_zip_file(data_path)
    #unzip(data_path)
    worklist = get_worklist(data_path)
    for item in worklist:
        print(','.join([item["作品名"], item["分類番号"], item["文字遣い種別"], item["作品著作権フラグ"]]))