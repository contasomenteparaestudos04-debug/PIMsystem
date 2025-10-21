import os
import re
import time

DISCIPLINAS = [
    'ENGENHARIA DE SOFTWARE AGIL',
    'ALGORIT E ESTRUT DE PYTHON',
    'PROGRAMAÇAO ESTRUTURADA EM C',
    'ANALISE E PROJETO DE SISTEMAS',
    'PESQUISA, TECNOLOG E INOVAÇÃO',
    'EDUCAÇAO AMBIENTAL',
    'REDES COMP E SIST DESTRIBUIDOS',
    'INTELIGENCIA ARTIFICIAL'
]

alunos_cadastrados = []

def sanitizar_nome_arquivo(nome_disciplina):
    "Remove caracteres especiais e substitui espaços por underscores."
    nome_disciplina = nome_disciplina.replace('Ç', 'C').replace('Ã', 'A')
    nome_disciplina = nome_disciplina.replace(' ', '_')
    return re.sub(r'\W+', '', nome_disciplina) + ".txt"

# dados dos arquivos já existentes
def carregar_dados_existentes():
    "Le os arquivos .txt"
    print("Carregando dados...")
    time.sleep(1)
    temp_alunos = {} # dicionario com RA para evitar duplicatas

    for disciplina in DISCIPLINAS:
        nome_arquivo = sanitizar_nome_arquivo(disciplina)
        if os.path.exists(nome_arquivo):
            try:
                with open(nome_arquivo, 'r', encoding='utf-8') as f:
                    for linha in f:
                        partes = linha.strip().split(';')
                        if len(partes) == 5:
                            nome, ra, turma, _, media_str = partes
                            if ra not in temp_alunos:
                                temp_alunos[ra] = {
                                    'nome': nome, 'ra': ra, 'turma': turma, 'disciplinas': {}
                                }
                            try:
                                temp_alunos[ra]['disciplinas'][disciplina] = float(media_str)
                            except ValueError:
                                continue
            except IOError as e: #erro de leitura
                print(f"Aviso: Nao foi possivel ler o arquivo {nome_arquivo}: {e}")

    if temp_alunos:
        global alunos_cadastrados
        alunos_cadastrados = list(temp_alunos.values())
        print(f"{len(alunos_cadastrados)} aluno(s) carregado(s) com sucesso.")
    else:
        print("Nenhum dado anterior encontrado.")


def salvar_dados_para_c():
    "Salva os dados de todos os alunos da memoria em arquivos .txt "
    dados_por_disciplina = {disciplina: [] for disciplina in DISCIPLINAS}
    for aluno in alunos_cadastrados:
        for disciplina, media in aluno['disciplinas'].items():
            linha = f"{aluno['nome']};{aluno['ra']};{aluno['turma']};N/A;{media:.2f}\n"
            if disciplina in dados_por_disciplina:
                dados_por_disciplina[disciplina].append(linha)
    for disciplina, linhas in dados_por_disciplina.items():
        nome_arquivo = sanitizar_nome_arquivo(disciplina)
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                if linhas:
                    f.writelines(linhas)
                else:
                    # Caso nao tenha alunos para cada disciplina, garante que o arquivo fique vazio
                    f.write("")
        except IOError as e: #erro de leitura
            print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

def mostrar_menu():
    """Exibe o menu principal de opções para o usuário."""
    print("\n" + "="*40)
    print("   SISTEMA DE CADASTRO DE ALUNOS E NOTAS")
    print("="*40)
    print("1. Cadastrar novo aluno")
    print("2. Listar alunos cadastrados")
    print("3. Buscar aluno por R.A.")
    print("4. Excluir aluno") 
    print("5. Sair")       
    print("="*40)

def validar_nota(texto_usuario):
    "garante que seja um valor numérico entre 0 e 10."
    while True:
        try:
            nota_str = input(f"  Digite a nota {texto_usuario} (0-10): ")
            nota = float(nota_str)
            if 0 <= nota <= 10:
                return nota
            else:
                print("Erro: A nota deve ser um valor entre 0 e 10.")
        except ValueError:
            print("Erro: Por favor, digite um número válido.")

def validar_nome():
    "Valida o nome do aluno"
    while True:
        nome = input("Nome completo do aluno: ").strip()
        if not nome:
            print("Erro: O nome não pode ficar em branco. Por favor, tente novamente.")
            continue
        if any(char.isdigit() for char in nome):
            print("Erro: O nome não deve conter números. Por favor, tente novamente.")
            continue
        if len(nome) < 3:
            print("Erro: O nome parece curto demais. Por favor, insira o nome completo.")
            continue
        return nome.title()

def cadastrar_aluno():
    print("\n=== Cadastro de Novo Aluno ===")
    
    nome = validar_nome()
    
    for aluno in alunos_cadastrados:
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
    for disciplina in DISCIPLINAS:
        print(f"\n-> Lançando notas para: {disciplina}")
        np1 = validar_nota("NP1")
        np2 = validar_nota("NP2")
        pin = validar_nota("PIN")
        media = ((np1 * 4) + (np2 * 4) + (pin * 2)) / 10
        medias_disciplinas[disciplina] = media
        status = "Aprovado" if media >= 7.0 else "Reprovado"
        print(f"   Média em {disciplina}: {media:.2f} - Status: {status}")

    novo_aluno = { 'nome': nome, 'ra': ra, 'turma': turma, 'disciplinas': medias_disciplinas }
    alunos_cadastrados.append(novo_aluno)
    print(f"\nAluno '{nome}' cadastrado com sucesso!")
    
    salvar_dados_para_c()
    print("Arquivos atualizados.")

def exibir_dados_aluno(aluno):
    " mostra os dados de um aluno de forma organizada"
    print(f"\nNome: {aluno['nome']}")
    print(f"R.A.: {aluno['ra']}")
    print(f"Turma: {aluno['turma']}")
    print(" Médias por Disciplina ")
    for disciplina, media in aluno['disciplinas'].items():
        status = "Aprovado" if media >= 7.0 else "Reprovado"
        print(f"  - {disciplina:<40} | Média: {media:<5.2f} | Status: {status}")
    print("="*40)

def listar_alunos():
    "Exibe todos os alunos cadastrados no sistema."
    print("\n Lista de Alunos Cadastrados ")
    if not alunos_cadastrados:
        print("Nenhum aluno cadastrado no sistema.")
        return
    for aluno in alunos_cadastrados:
        exibir_dados_aluno(aluno)

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
        exibir_dados_aluno(aluno_encontrado)
    else:
        print(f"\nNenhum aluno encontrado com o R.A. '{ra_busca}'.")

def excluir_aluno():
    """Remove um aluno do sistema pelo R.A."""
    print("\n=== Excluir aluno ===")
    if not alunos_cadastrados:
        print("Nenhum aluno cadastrado para excluir.")
        return
    
    ra_busca = input("Digite o R.A. do aluno que deseja excluir: ")
    aluno_a_excluir = None
    
    for aluno in alunos_cadastrados:
        if aluno['ra'] == ra_busca:
            aluno_a_excluir = aluno
            break
            
    if aluno_a_excluir:
        print("\n--- Aluno a ser excluído ---")
        exibir_dados_aluno(aluno_a_excluir)
        
        confirmacao = input("Tem certeza que deseja excluir este aluno? (s/n): ").lower()
        if confirmacao == 's':
            alunos_cadastrados.remove(aluno_a_excluir)
            salvar_dados_para_c()
            print(f"\nAluno '{aluno_a_excluir['nome']}' foi excluído com sucesso.")
            print("Arquivos de relatório atualizados.")
        else:
            print("\nExclusão cancelada pelo usuário.")
    else:
        print(f"\nNenhum aluno encontrado com o R.A. '{ra_busca}'.")


def adicionar_dados_teste():
    "Adiciona dois alunos de exemplo para testes iniciais."
    print("Populando o sistema com dados de teste iniciais...")
    aluno1 = { 'nome': 'Carlos Silva', 'ra': 'R8564S7', 'turma': 'DS1Q18', 'disciplinas': { d: 7.5 + (i*0.2) for i, d in enumerate(DISCIPLINAS) } }
    aluno2 = { 'nome': 'Ana Carolina de Albuquerque Pereira', 'ra': 'Q6789P0', 'turma': 'DS2Q18', 'disciplinas': { d: 8.0 - (i*0.3) for i, d in enumerate(DISCIPLINAS) } }
    alunos_cadastrados.extend([aluno1, aluno2])
    print("Dados de teste carregados na memória.")
    salvar_dados_para_c()

def main():
    "menu"
    carregar_dados_existentes()
    if not alunos_cadastrados:
        adicionar_dados_teste()
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção (1-5): ") 
        if opcao == '1':
            cadastrar_aluno()
        elif opcao == '2':
            listar_alunos()
        elif opcao == '3':
            buscar_aluno()
        elif opcao == '4':
            excluir_aluno()
        elif opcao == '5': 
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\nOpção inválida! Por favor, escolha um número de 1 a 5.") 

main()