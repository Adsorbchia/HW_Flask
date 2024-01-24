import time
from multiprocessing import Process
import os
import requests
from task_4_1 import  urls

def download_pr(url):
    folder = 'data_processes'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for index, url in enumerate(urls):
        responce = requests.get(url)
        url = url.split('?')
        url = url[0].split('/')
        url = url[-1]
        filename = os.path.join(folder, f'{url}')
        with open(filename, 'wb') as f:
            f.write(responce.content)
        print(f'Скачивание {index+1}-ого изображения выполнено за {time.time() - start_time:2f} секунд')


processes = []
start_time = time.time()


if __name__ == '__main__':
    for url in urls:
        process = Process(target=download_pr, args=[url])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'Общее время работы процессов = {time.time() - start_time:2f} секунд') 