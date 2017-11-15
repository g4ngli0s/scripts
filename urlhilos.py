#!/usr/bin/env python3
import requests
import time
import threading
from queue import Queue

urls = [one_line.strip()
	for one_line in open('urls.txt')]

length = {}
queue = Queue()
start_time = time.time()
threads = [ ]

def get_length(one_url):
	response = requests.get(one_url)
	queue.put((one_url, len(response.content)))

#Lanza la funcion en el thread
print("Lanzando")
for one_url in urls:
	t = threading.Thread(target=get_length, args=(one_url,))
	threads.append(t)
	t.start()

#Uniendo los threads
print("Uniendo")
for one_thread in threads:
	one_thread.join()


#Recupera y muestra la info
print("Recuperando y mostrando")
while not queue.empty():
	one_url,length = queue.get()
	print("{0:30}: {1:8,}".format(one_url, length))

end_time = time.time()
total_time = end_time - start_time
print("\nTiempo total: {0:.3} segundos".format(total_time))
