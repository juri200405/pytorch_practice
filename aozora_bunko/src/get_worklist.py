import zipfile
import urllib.request
from pathlib import Path
import csv
import re

def get_zip_file(dpath):
    urllib.request.urlretrieve("https://www.aozora.gr.jp/index_pages/list_person_all_extended_utf8.zip", str(dpath / "list_person_all_extended_utf8.zip"))

def unzip(dpath):
    with zipfile.ZipFile(str(dpath / "list_person_all_extended_utf8.zip")) as existing_zip:
        existing_zip.extractall(str(dpath))

def get_worklist(dpath):
    worklist = []
    with open(str(dpath / "list_person_all_extended_utf8.csv"), newline='', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if(row["分類番号"] == "NDC 913" and row["文字遣い種別"] == "新字新仮名" and row["作品著作権フラグ"] == "なし"):
                worklist.append(row)
    return worklist

def get_work(dpath, worklist):
    for item in worklist:
        zip_path = dpath / "zips"
        text_path = dpath / "texts"

        work_url = item["テキストファイルURL"]
        zip_name = re.sub(r".*/", "", work_url)
        urllib.request.urlretrieve(work_url, str(zip_path / zip_name))

        file_name = re.sub(r"\.zip", "", zip_name)
        with zipfile.ZipFile(str(zip_path / zip_name)) as existing_zip:
            existing_zip.extractall(str(text_path / file_name))


if __name__ == "__main__":
    data_path = Path("./aozora_bunko/datas")
    get_zip_file(data_path)
    unzip(data_path)
    worklist = get_worklist(data_path)
    get_work(data_path, worklist)