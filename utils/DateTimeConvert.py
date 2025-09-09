from datetime import datetime

def convet_datetime(data_str:str, hora_str:str):
    data_hora_str = f"{data_str} {hora_str}"
    data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
    return data_hora
