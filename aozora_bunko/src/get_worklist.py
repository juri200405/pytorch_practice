import zipfile
import urllib.request
from pathlib import Path

def get_zip_file(dpath):
    urllib.request.urlretrieve("https://www.aozora.gr.jp/index_pages/list_person_all_extended_utf8.zip", str(data_path / "list_person_all_extended_utf8.zip"))

def unzip(dpath):
    with zipfile.ZipFile(str(data_path / "list_person_all_extended_utf8.zip")) as existing_zip:
        existing_zip.extractall(str(data_path))

if __name__ == "__main__":
    data_path = Path("./aozora_bunko/datas")
    #get_zip_file(data_path)
    #unzip(data_path)