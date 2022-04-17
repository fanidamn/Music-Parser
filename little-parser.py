import requests, lxml.html, os.path, eyed3, sys
from lxml import etree

script = os.path.abspath(os.path.dirname(__file__))

def download_Track(url, name, download_url):
    value = "_n"
    main = requests.get(url)
    tree = lxml.html.document_fromstring(main.text)
    artist = tree.xpath('//*[@id="dle-content"]/div[2]/div/div[1]/div[1]/div[1]/span[2]/a/text()')
    track_name = tree.xpath('//*[@id="dle-content"]/div[2]/div/div[1]/div[1]/div[2]/span[2]/text()')
    path = script + '\\tracks\\' + name.replace(" ", "_") + ".mp3"
    if os.path.isfile(path):
        value = "_e"
    if value != "_e":
        with open(path, 'wb') as f:
            api = requests.get(f"http://{download_url.split('//')[1]}", stream=True)
            total_length = int(api.headers.get('Content-Length'))
            if total_length != None:
                dl = 0
                for data in api.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write(f" Скачивание: {name}" + "\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()
        if value == "_y":
            for i in range(len(artist)):
                d3 = eyed3.load(path)
                d3.tag.artist = artist[i]
                d3.tag.title = track_name[i]
                d3.tag.save()
        else:
            value = "_n"
    return value

def main_Links(url):
    api = requests.get(url)
    tree = lxml.html.document_fromstring(api.text)
    song_name = tree.xpath('//*[@class="table song-item"]/tbody/tr/td[1]/div/a/text()')
    link = tree.xpath('//*[@class="table song-item"]/tbody/tr/td[1]/div/a/@href')
    download_url = tree.xpath('//*[@class="table song-item"]/tbody/tr/td[1]/div/div[1]/@href')
    for i in range(len(link)):
        value = download_Track(f"http://{link[i].split('//')[1]}", song_name[i], download_url[i])
        if value == "_e":
            print("Трек", song_name[i], "уже есть в папке.")

def main():
    main_Links("https://quvonch.com/uzbekskaya-muzyka/")

if __name__ == "__main__":
    main()