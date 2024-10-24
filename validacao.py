import re
from datetime import datetime

def validar_data(data):
    """Permite inserir a data no formato ddmmyyyy ou dd/mm/yyyy."""
    if re.match(r'^\d{6}$', data):
        dia, mes, ano = data[:2], data[2:4], '19' + data[4:]
        data_formatada = f"{dia}/{mes}/{ano}"
    elif re.match(r'^\d{8}$', data):
        dia, mes, ano = data[:2], data[2:4], data[4:]
        data_formatada = f"{dia}/{mes}/{ano}"
    else:
        data_formatada = data

    try:
        datetime.strptime(data_formatada, "%d/%m/%Y")
        return data_formatada
    except ValueError:
        return None

def validar_telefone(telefone):
    """Aceita números com ou sem formatação e retorna no formato (XX) XXXXX-XXXX."""
    telefone = re.sub(r'\D', '', telefone)  # Remove todos os não numéricos

    if len(telefone) == 11:  # Verifica se tem DDD + número válido
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    else:
        return None

def normalizar_nome(nome):
    return ' '.join([palavra.capitalize() for palavra in nome.split()]).strip()
