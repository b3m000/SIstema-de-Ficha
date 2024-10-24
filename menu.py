import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    from operacoes import cadastrar_paciente, listar_pacientes, buscar_paciente, editar_paciente, excluir_paciente, exportar_para_csv
    from banco import criar_tabela

    criar_tabela()

    while True:
        limpar_tela()
        print("\n===== Clínica Médica =====")
        print("1. Cadastrar Novo Paciente")
        print("2. Listar Pacientes por Letra")
        print("3. Buscar Paciente")
        print("4. Editar Paciente")
        print("5. Excluir Paciente")
        print("6. Exportar para CSV")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            cadastrar_paciente()
        elif opcao == '2':
            listar_pacientes()  # Chama a nova função de listagem com paginação
        elif opcao == '3':
            buscar_paciente()
        elif opcao == '4':
            editar_paciente()
        elif opcao == '5':
            excluir_paciente()
        elif opcao == '6':
            exportar_para_csv()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

        input("\nPressione Enter para continuar...")
