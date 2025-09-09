import time
import random

def gerar_numero_unico():
    timestamp = int(time.time() * 1000000)  
    parte_tempo = str(timestamp)[-3:]       
    parte_random = str(random.randint(0, 99)).zfill(2)
    return parte_tempo + parte_random