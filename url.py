#!/usr/bin/env python3
import requests
import time

urls = [one_line.strip()
	for one_line in open('urls.txt')]
  
length = {}
start_time = time.time()

for one_url in urls:
	response = requests.get(one_url)
	length[one_url] = len(response.content)
  
for key, value in length.items():
	print("{0:30}: {1:8,}".format(key, value))
  
end_time = time.time()
total_time = end_time - start_time
print("\nTiempo total: {0:.3} segundos".format(total_time))
