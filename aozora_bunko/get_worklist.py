import zipfile
import urllib.request

if __name__ == "__main__":
    #req = urllib.request.Request("https://www.aozora.gr.jp/index_pages/person_all.html")
    req = urllib.request.Request("https://www.aozora.gr.jp/")
    req.set_proxy("proxy.uec.ac.jp:8080", 'https')
    with urllib.request.urlopen(req) as response:
        file_data = response.read()
        print(file_data.decode("utf8"))
        #with open("list_person_all_extended_utf8.zip", 'wb') as f:
            #f.write(file_data)