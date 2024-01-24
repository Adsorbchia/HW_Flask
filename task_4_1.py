import requests
import threading
import time
from multiprocessing import Process
import os

urls = ['https://img1.fonwall.ru/o/fi/grass-field-meadow-prairie.jpeg?auto=compress&fit=crop&w=1280&h=800',
'https://img1.fonwall.ru/o/ja/landscape-animals-sunset-nature.jpeg?auto=compress&fit=crop&w=1280&h=800',
'https://img3.fonwall.ru/o/tu/tree-nature-horizon-wilderness.jpeg?auto=compress&fit=crop&w=1280&h=800',
'https://img3.fonwall.ru/o/kw/nature-black-and-white-adventure-wildlife-ulfa.jpeg?auto=compress&fit=crop&w=1280&h=800',
'https://img1.fonwall.ru/o/ty/animals-nature-grass-squirrel.jpeg?auto=compress&fit=crop&w=1280&h=800',
'https://img3.fonwall.ru/o/cj/landscape-nature-grass-wildlife.jpeg?auto=compress&fit=crop&w=1280&h=800']

def download_th(url):
    for index, url in enumerate(urls):
        responce = requests.get(url)
        url = url.split('?')
        url = url[0].split('/')
        url = url[-1]
        filename = os.path.join(folder, f'{url}')
        with open(filename, 'wb') as f:
            f.write(responce.content)
        print(f'Скачивание {index+1}-ого изображения выполнено за {time.time() - start_time:2f} секунд')
        




if __name__ == '__main__':
    folder = 'data_threads'
    if not os.path.exists(folder):
        os.mkdir(folder)
    threads = []
    start_time = time.time()

    for url in urls:
        thread = threading.Thread(target=download_th, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    print(f'Общее время работы потоков = {time.time() - start_time:2f} секунд')

