import zipfile
import urllib.request
from pathlib import Path

if __name__ == "__main__":
    data_path = Path("./aozora_bunko/datas")
    urllib.request.urlretrieve("https://www.aozora.gr.jp/index_pages/list_person_all_extended_utf8.zip", str(data_path / "list_person_all_extended_utf8.zip"))