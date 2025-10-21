import os
import getpass

from mod_dados import *

def login_professor():
    "Verifica as informações do professor no arquivo professores.txt"
    if not os.path.exists("professores.txt"):
        print("Arquivo 'professores.txt' não encontrado. Crie o arquivo com 'usuario;senha'.")
        return False
        
    usuario = input("Usuário do professor: ")
    print("Obs: Sua senha permaneçe oculta por questões de segurança.")
    senha = getpass.getpass("Senha: ")
    
    with open("professores.txt", 'r', encoding='utf-8') as f:
        for line in f:
            user_file, pass_file = line.strip().split(';')
            if user_file == usuario and pass_file == senha:
                print("Login bem-sucedido!")
                return True
    print("Usuário ou senha inválidos.")
    return False

def cadastrar_aluno():
    
    print("\n Cadastro de Novo Aluno ")
    
    nome = validar_nome() # função de mod_dados
    
    for aluno in alunos_cadastrados: # lista de mod_dados
        if aluno['nome'].lower() == nome.lower():
            print(f"\nAtenção: Já existe um aluno cadastrado com o nome '{aluno['nome']}'.")
            confirmacao = input("Deseja continuar com o cadastro mesmo assim? (s/n): ").lower()
            if confirmacao != 's':
                print("Cadastro cancelado pelo usuário.")
                return
            break

    ra = input("Digite o R.A. (Registro Acadêmico): ")
    for aluno in alunos_cadastrados:
        if aluno['ra'] == ra:
            print(f"\nErro: O R.A. '{ra}' já pertence ao aluno {aluno['nome']}.")
            print("Cadastro cancelado.")
            return

    turma = input("Digite a turma: ")
    medias_disciplinas = {}
    print(f"\nSR(A) {nome}, por favor, digite suas notas para cada disciplina:")
    for disciplina in DISCIPLINAS: # Constante importada de mod_dados
        print(f"\n-> Lançando notas para: {disciplina}")
        np1 = validar_nota("NP1") # Função importada de mod_dados
        np2 = validar_nota("NP2")
        pin = validar_nota("PIN")
        media = ((np1 * 4) + (np2 * 4) + (pin * 2)) / 10
        medias_disciplinas[disciplina] = media
        status = "Aprovado" if media >= 7.0 else "Reprovado"
        print(f"   Média em {disciplina}: {media:.2f} - Status: {status}")

    novo_aluno = { 'nome': nome, 'ra': ra, 'turma': turma, 'disciplinas': medias_disciplinas }
    alunos_cadastrados.append(novo_aluno)
    print(f"\nAluno '{nome}' cadastrado com sucesso!")
    
    salvar_dados_para_c() # Funçao importada de mod_dados
    print("Arquivos atualizados.")

def listar_alunos():
    "Exibe todos os alunos cadastrados no sistema."
    print("\n Lista de Alunos Cadastrados ")
    if not alunos_cadastrados:
        print("Nenhum aluno cadastrado no sistema.")
        return
    for aluno in alunos_cadastrados:
        print(f"\nNome: {aluno['nome']} | R.A.: {aluno['ra']} | Turma: {aluno['turma']}")
    print("="*40)
    print("Para ver detalhes de um aluno, use a opção de busca por R.A.")


def buscar_aluno():
    "Procura um aluno específico pelo R.A. e exibe seus dados."
    print("\n Buscar Aluno por R.A. ")
    if not alunos_cadastrados:
        print("Nenhum aluno cadastrado para buscar.")
        return
    ra_busca = input("Digite o R.A. do aluno que deseja buscar: ")
    aluno_encontrado = None
    for aluno in alunos_cadastrados:
        if aluno['ra'] == ra_busca:
            aluno_encontrado = aluno
            break
    if aluno_encontrado:
        print("\n=== Aluno Encontrado ===")
        exibir_dados_aluno(aluno_encontrado) # Função importada de mod_dados
    else:
        print(f"\nNenhum aluno encontrado com o R.A. '{ra_busca}'.")


def visualizar_relatorios():
    """Apresenta um menu de disciplinas e chama o executável em C
    para exibir o relatório correspondente."""
    
    # verifica se o programa C foi compilado
    if not os.path.exists("relatorio") and not os.path.exists("relatorio.exe"):
        print("\nERRO: O programa de relatórios 'relatorio' não foi encontrado.")
        print("Por favor, compile o arquivo 'relatorio.c' primeiro (gcc relatorio.c -o relatorio).")
        return

    while True:
        print("\nMenu de Relatorios de Disciplinas:")
        print("1. ENGENHARIA DE SOFTWARE AGIL")
        print("2. ALGORIT E ESTRUT DE PYTHON")
        print("3. PROGRAMACAO ESTRUTURADA EM C")
        print("4. ANALISE E PROJETO DE SISTEMAS")
        print("5. PESQUISA, TECNOLOG E INOVACAO")
        print("6. EDUCACAO AMBIENTAL")
        print("7. REDES COMP E SIST DESTRIBUIDOS")
        print("8. INTELIGENCIA ARTIFICIAL")
        print("9. Voltar ao Menu do Professor")
        
        choice = input("Escolha uma opcao: ")
        if not choice.isdigit() or not 1 <= int(choice) <= 9:
            print("Entrada invalida! Por favor, digite um numero de 1 a 9.")
            continue
        choice = int(choice)

        if choice == 9:
            break


        disciplina_original = DISCIPLINAS[choice - 1]
        filename = sanitizar_nome_arquivo(disciplina_original)
        
        # comando para chamar o executável C
        command = f"./relatorio {filename}"
        if os.name == 'nt': # Se for Windows o executavel pode ter .exe
            command = f"relatorio.exe {filename}"

        print(f"\nGerando relatório com o programa C para '{filename}'...")
        os.system(command) # executa o comando no terminal
        print("\nRelatório finalizado.")


def menu_professor():
    """Menu de ações disponíveis para o professor."""
    while True:
        print("\n" + "="*40)
        print("   PAINEL DO PROFESSOR")
        print("="*40)
        print("1. Cadastrar novo aluno")
        print("2. Listar alunos cadastrados")
        print("3. Buscar aluno por R.A.")
        print("4. Visualizar Relatórios por Disciplina (via C)")
        print("5. Sair (Voltar ao menu principal)")
        print("="*40)
        
        opcao = input("Escolha uma opção (1-5): ")
        if opcao == '1':
            cadastrar_aluno()
        elif opcao == '2':
            listar_alunos()
        elif opcao == '3':
            buscar_aluno()
        elif opcao == '4':
            visualizar_relatorios()
        elif opcao == '5':
            print("\nVoltando ao menu principal...")
            break
        else:
            print("\nOpção inválida! Por favor, escolha um número de 1 a 5.")