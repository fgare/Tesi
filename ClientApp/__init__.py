import requests, time

BASE = "http://127.0.0.1:5000/"
MAX = 100

if __name__ == "__main__":
    values = []

    for n in range(1,MAX):
        start = time.time()*1000 #inizio
        response = requests.get(BASE + "productsList")
        end = time.time()*1000 #fine
        values.append(end - start)

    print("Tempo medio per richiesta > %f ms}" % (sum(values)/len(values)))