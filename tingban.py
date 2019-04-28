import requests
import json
import os
import sys

global url
url = 'http://www.tingban.cn/webapi/audios/list?id=1100000000316&pagesize=1&pagenum=1&sorttype=-1&_=1556425026680'

class ProgressBar(object):

    def __init__(self, file_name, total):
        super().__init__()
        self.file_name = file_name
        self.count = 0
        self.prev_count = 0
        self.total = total
        self.end_str = '\r'

    def __get_info(self):
        return 'Progress: {:6.2f}%, {:8.2f}MB, [{:.100}]'\
            .format(self.count/self.total*100, self.total/1024/1024, self.file_name)

    def refresh(self, count):
        self.count += count
          # Update progress if down size > 10k
        if (self.count - self.prev_count) > 10240:
            self.prev_count = self.count
            print(self.__get_info(), end=self.end_str)
          # Finish downloading
        if self.count >= self.total:
            self.end_str = '\n'
            print(self.__get_info(), end=self.end_str)

def TingBan():
    #global url
    '''
    response = requests.get(url=url, stream=True).text
    response = json.loads(response)
    count = response['result']['count']
    res = response['result']['dataList'][0]
    file_url = res['mp3PlayUrl']
    file_name = res['audioName'] + '.mp3'
    print('1')
    print(file_name)
    r = download_file(file_url, file_name)
    if r:
        print('Mp3 file already download:', file_name)
    '''
    for i in range(int(sys.argv[1]), int(sys.argv[1])+1):
        url = 'http://www.tingban.cn/webapi/audios/list?id=1100000000316&pagesize=1&pagenum={}&sorttype=-1&_=1556425026680'.format(i)
        response = requests.get(url=url, stream=True).text
        response = json.loads(response)
        res = response['result']['dataList'][0]
        file_url = res['mp3PlayUrl']
        file_name = res['audioName'] + '.mp3'
        print(i)
        print(file_name)
        r = download_file(file_url, file_name)
        if r:
            print('Mp3 file already download:', file_name)

def download_file(file_url, file_name):
    response = requests.get(url=file_url, stream=True)
    length = int(response.headers.get('Content-Length'))
    file_path = os.path.join('song', file_name)
    if os.path.exists(file_path) and os.path.getsize(file_path) == length:
        return True
    else:
        progress = ProgressBar(file_path, length)
        with open(file_path, 'wb') as f:
            for check in response.iter_content(1024):
                f.write(check)
                progress.refresh(len(check))
        return False

if __name__ == '__main__':
    TingBan()

