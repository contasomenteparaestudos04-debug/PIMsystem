# Importa o necessario
from mod_dados import alunos_cadastrados, exibir_dados_aluno

def login_aluno():
    """Pede o R.A. do aluno e, se encontrado, exibe seu boletim."""
    if not alunos_cadastrados:
        print("\nNenhum aluno cadastrado no sistema. Peça para um professor realizar o cadastro.")
        return
        
    ra_busca = input("Digite seu R.A. para ver seu boletim: ")
    aluno_encontrado = None
    for aluno in alunos_cadastrados:
        if aluno['ra'] == ra_busca:
            aluno_encontrado = aluno
            break
            
    if aluno_encontrado:
        # Chama a funçao de exibir dados 
        exibir_dados_aluno(aluno_encontrado)
    else:
        print(f"R.A. '{ra_busca}' não encontrado no sistema.")
    
    input("\nPressione Enter para voltar ao menu principal...")