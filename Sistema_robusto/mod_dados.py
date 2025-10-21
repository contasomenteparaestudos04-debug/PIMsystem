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
    "Lê os arquivos .txt e popula a lista 'alunos_cadastrados' com os dados existentes."
    print("Carregando dados...")
    time.sleep(1)
    temp_alunos = {} # dicionário com RA para evitar duplicatas

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
                    f.write("") 
        except IOError as e:
            print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

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
    "Pede e valida o nome do aluno, garantindo que não tenha números e não seja vazio."
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

def adicionar_dados_teste():
    "Adiciona dois alunos de exemplo para testes iniciais."
    print("Populando o sistema com dados de teste iniciais...")
    aluno1 = { 'nome': 'Carlos Silva', 'ra': 'R8564S7', 'turma': 'DS1Q18', 'disciplinas': { d: 7.5 + (i*0.2) for i, d in enumerate(DISCIPLINAS) } }
    aluno2 = { 'nome': 'Ana Carolina de Albuquerque Pereira', 'ra': 'Q6789P0', 'turma': 'DS2Q18', 'disciplinas': { d: 8.0 - (i*0.3) for i, d in enumerate(DISCIPLINAS) } }
    alunos_cadastrados.extend([aluno1, aluno2])
    print("Dados de teste carregados na memória.")
    salvar_dados_para_c()
    print("Arquivos de relatório iniciais gerados.")

def exibir_dados_aluno(aluno):
    "Função auxiliar para mostrar os dados de um aluno de forma organizada."
    print(f"\nNome: {aluno['nome']}")
    print(f"R.A.: {aluno['ra']}")
    print(f"Turma: {aluno['turma']}")
    print(" Médias por Disciplina ")
    for disciplina, media in aluno['disciplinas'].items():
        status = "Aprovado" if media >= 7.0 else "Reprovado"
        print(f"  - {disciplina:<40} | Média: {media:<5.2f} | Status: {status}")
    print("="*40)