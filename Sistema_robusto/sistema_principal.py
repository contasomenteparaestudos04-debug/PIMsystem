import os


import mod_dados
import mod_professor
import mod_aluno

def main():
    "Função principal que executa o menu de perfis."

    # Verifica se o arquivo dos professores existe
    if not os.path.exists("professores.txt"):
        with open("professores.txt", "w", encoding="utf-8") as f:
            f.write("admin;admin123\n")
        print("Arquivo 'professores.txt' criado com credenciais padrão (admin/admin123). ALTERAR LOGO")

 
    mod_dados.carregar_dados_existentes()
    if not mod_dados.alunos_cadastrados:
        mod_dados.adicionar_dados_teste()

    while True:
        print("\n" + "="*40)
        print("   SISTEMA DE GESTÃO ACADÊMICA")
        print("="*40)
        print("Você é:")
        print("1. Professor")
        print("2. Aluno")
        print("3. Encerrar Programa")
        print("="*40)
        
        perfil = input("Escolha seu perfil (1-3): ")
        
        if perfil == '1':
            if mod_professor.login_professor():
                mod_professor.menu_professor()
        elif perfil == '2':
            
            mod_aluno.login_aluno()
        elif perfil == '3':
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()