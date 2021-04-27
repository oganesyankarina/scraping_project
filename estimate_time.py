import time
import requests

url = "https://lipetsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python"
start = time.time()

_ = requests.get(url, headers={"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})

end = time.time()
delta = end - start
result = delta * 50 * 40
# минуты + кол-во потоков
print(f"{result // 60 // 32} m")
print(f"{result // 32} sec")
