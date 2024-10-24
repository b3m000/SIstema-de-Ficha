import sqlite3
from banco import conectar
from validacao import validar_data, validar_telefone, normalizar_nome
from tabulate import tabulate
import csv

def cadastrar_paciente():
    nome = input("Nome e Sobrenome: ").strip()
    nome = normalizar_nome(nome)

    data_nascimento = input("Data de Nascimento (ddmmaaaa ou dd/mm/aaaa): ").strip()
    data_nascimento = validar_data(data_nascimento)
    if not data_nascimento:
        print("Data inválida! Use o formato ddmmaaaa ou dd/mm/aaaa.")
        return

    telefone = input("Telefone (DDD99XX99XXX ou (XX) XXXXX-XXXX): ").strip()
    telefone = validar_telefone(telefone)
    if not telefone:
        print("Telefone inválido! Use um número válido.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pacientes (nome, data_nascimento, telefone)
            VALUES (?, ?, ?)
        ''', (nome, data_nascimento, telefone))
        conn.commit()
        print("Paciente cadastrado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar paciente: {e}")
    finally:
        conn.close()

def listar_pacientes_por_letra(letra):
    """Lista pacientes com nomes que começam pela letra fornecida."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, data_nascimento, telefone 
            FROM pacientes 
            WHERE nome LIKE ? COLLATE NOCASE 
            ORDER BY nome ASC
        ''', (letra + '%',))
        pacientes = cursor.fetchall()

        if pacientes:
            print(tabulate(pacientes, headers=['ID', 'Nome', 'Data de Nascimento', 'Telefone'], tablefmt='fancy_grid'))
        else:
            print(f"Nenhum paciente encontrado para a letra {letra}.")
    except sqlite3.Error as e:
        print(f"Erro ao listar pacientes: {e}")
    finally:
        conn.close()

def buscar_paciente():
    """Busca pacientes pelo nome ou parte do nome."""
    nome = input("Digite o nome do paciente: ").strip()
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, data_nascimento, telefone 
            FROM pacientes 
            WHERE nome LIKE ? COLLATE NOCASE 
            ORDER BY nome ASC
        ''', ('%' + nome + '%',))
        pacientes = cursor.fetchall()

        if pacientes:
            print(tabulate(pacientes, headers=['ID', 'Nome', 'Data de Nascimento', 'Telefone'], tablefmt='fancy_grid'))
        else:
            print("Paciente não encontrado.")
    except sqlite3.Error as e:
        print(f"Erro ao buscar paciente: {e}")
    finally:
        conn.close()

def editar_paciente():
    """Edita os dados de um paciente existente."""
    listar_pacientes_por_letra(input("Informe a letra inicial do paciente: ").upper())
    paciente_id = input("Digite o ID do paciente que deseja editar: ").strip()

    nome = input("Novo Nome e Sobrenome: ").strip()
    nome = normalizar_nome(nome)

    data_nascimento = input("Nova Data de Nascimento (ddmmaaaa ou dd/mm/aaaa): ").strip()
    data_nascimento = validar_data(data_nascimento)

    telefone = input("Novo Telefone (27999913109 ou (XX) XXXXX-XXXX): ").strip()
    telefone = validar_telefone(telefone)
    if not telefone:
        print("Telefone inválido! Use um número válido.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pacientes
            SET nome = ?, data_nascimento = ?, telefone = ?
            WHERE id = ?
        ''', (nome, data_nascimento, telefone, paciente_id))
        conn.commit()

        if cursor.rowcount > 0:
            print("Paciente editado com sucesso!")
        else:
            print("Paciente não encontrado.")
    except sqlite3.Error as e:
        print(f"Erro ao editar paciente: {e}")
    finally:
        conn.close()

def excluir_paciente():
    """Exclui um paciente pelo ID."""
    listar_pacientes_por_letra(input("Informe a letra inicial do paciente: ").upper())
    paciente_id = input("Digite o ID do paciente a ser excluído: ").strip()

    confirmacao = input(f"Tem certeza que deseja excluir o paciente com ID {paciente_id}? (s/n): ").lower()
    if confirmacao != 's':
        print("Operação cancelada.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Paciente excluído com sucesso!")
        else:
            print("Paciente não encontrado.")
    except sqlite3.Error as e:
        print(f"Erro ao excluir paciente: {e}")
    finally:
        conn.close()

def exportar_para_csv():
    """Exporta pacientes para arquivos CSV separados por letras iniciais."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes ORDER BY nome ASC")
        pacientes = cursor.fetchall()

        if not pacientes:
            print("Nenhum paciente para exportar.")
            return

        # Agrupar pacientes por letras iniciais
        grupos = {}
        for paciente in pacientes:
            inicial = paciente[1][0].upper()
            if inicial not in grupos:
                grupos[inicial] = []
            grupos[inicial].append(paciente)

        # Exportar cada grupo para um arquivo separado
        for letra, grupo in grupos.items():
            nome_arquivo = f'pacientes_{letra}.csv'
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(['ID', 'Nome', 'Data de Nascimento', 'Telefone'])
                escritor.writerows(grupo)

        print("Pacientes exportados com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao exportar para CSV: {e}")
    finally:
        conn.close()
