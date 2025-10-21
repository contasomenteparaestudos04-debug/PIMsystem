#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 256  // Tamanho maximo de uma linha do arquivo
#define MIN_NAME_WIDTH 20

int main() {
    int choice; // escolha do usuario

    while (1) {
        // MENU
        printf("\n=== Menu de relatorios de disciplinas ===\n");
        printf("1. ENGENHARIA DE SOFTWARE AGIL\n");
        printf("2. ALGORIT E ESTRUT DE PYTHON\n");
        printf("3. PROGRAMACAO ESTRUTURADA EM C\n");
        printf("4. ANALISE E PROJETO DE SISTEMAS\n");
        printf("5. PESQUISA, TECNOLOG E INOVACAO\n");
        printf("6. EDUCACAO AMBIENTAL\n");
        printf("7. REDES COMP E SIST DESTRIBUIDOS\n");
        printf("8. INTELIGENCIA ARTIFICIAL\n");
        printf("9. Sair\n");
        printf("Escolha uma opcao: ");

        if (scanf("%d", &choice) != 1) {
            while (getchar() != '\n'); 
            printf("Entrada invalida! Por favor, digite um numero.\n");
            continue;
        }
        while (getchar() != '\n');

        if (choice == 9) {
            break;
        }

        char filename[100];
        if (choice == 1) strcpy(filename, "ENGENHARIA_DE_SOFTWARE_AGIL.txt");
        else if (choice == 2) strcpy(filename, "ALGORIT_E_ESTRUT_DE_PYTHON.txt");
        else if (choice == 3) strcpy(filename, "PROGRAMACAO_ESTRUTURADA_EM_C.txt");
        else if (choice == 4) strcpy(filename, "ANALISE_E_PROJETO_DE_SISTEMAS.txt");
        else if (choice == 5) strcpy(filename, "PESQUISA_TECNOLOG_E_INOVACAO.txt");
        else if (choice == 6) strcpy(filename, "EDUCACAO_AMBIENTAL.txt");
        else if (choice == 7) strcpy(filename, "REDES_COMP_E_SIST_DESTRIBUIDOS.txt");
        else if (choice == 8) strcpy(filename, "INTELIGENCIA_ARTIFICIAL.txt");
        else {
            printf("Opcao invalida!\n");
            continue;
        }

        FILE *file = fopen(filename, "r");
        if (file == NULL) {
            printf("Arquivo '%s' nao encontrado.\n", filename);
            printf("Dica: Execute o programa Python primeiro para gerar os relatorios.\n");
            continue;
        }

        // tabela dinamica
        int max_name_width = MIN_NAME_WIDTH;
        char temp_line[MAX_LINE];
        while (fgets(temp_line, sizeof(temp_line), file) != NULL) {
            char* name = strtok(temp_line, ";");
            if (name) {
                int name_len = strlen(name);
                if (name_len > max_name_width) {
                    max_name_width = name_len;
                }
            }
        }
        rewind(file);

        char disciplina_titulo[100];
        strcpy(disciplina_titulo, filename);
        *strrchr(disciplina_titulo, '.') = '\0';

        printf("\n--- Relatorio da disciplina %s ---\n", disciplina_titulo);

        printf("\n%-*s | %-10s | %-8s | %-5s | %s\n", max_name_width, "Nome", "RA", "Turma", "Notas", "Media");
        for (int i = 0; i < max_name_width + 38; i++) { printf("-"); }
        printf("\n");

        char line[MAX_LINE];
        int count = 0;
        while (fgets(line, sizeof(line), file) != NULL) {
            line[strcspn(line, "\n")] = 0;

            char *token;
            token = strtok(line, ";");
            if (token) printf("%-*s", max_name_width, token);

            token = strtok(NULL, ";");
            if (token) printf(" | %-10s", token);

            token = strtok(NULL, ";");
            if (token) printf(" | %-8s", token);

            token = strtok(NULL, ";");
            if (token) printf(" | %-5s", token);

            token = strtok(NULL, ";");
            if (token) printf(" | %s", token);

            printf("\n");
            count++;
        }
        
        if (count == 0) {
            printf("Nenhum dado encontrado no relatorio.\n");
        } else {
             for (int i = 0; i < max_name_width + 38; i++) { printf("-"); }
             printf("\n");
        }

        fclose(file);
    }

    printf("Programa finalizado.\n");
    return 0;
}