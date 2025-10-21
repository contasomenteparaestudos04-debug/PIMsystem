#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 256
#define MIN_NAME_WIDTH 20

int main(int argc, char *argv[]) {

    if (argc != 2) {
        printf("Erro de uso: O programa espera o nome de um arquivo como argumento.\n");
        printf("Exemplo: ./relatorio NOME_DO_ARQUIVO.txt\n");
        return 1; // Retorna um código de erro
    }

    char *filename = argv[1]; // Pega o nome do arquivo do argumento

    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Arquivo '%s' nao encontrado.\n", filename);
        return 1;
    }

    int max_name_width = MIN_NAME_WIDTH;
    char temp_line[MAX_LINE];
    while (fgets(temp_line, sizeof(temp_line), file) != NULL) {
       
        char line_copy[MAX_LINE];
        strcpy(line_copy, temp_line);
        char* name = strtok(line_copy, ";");
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
    
    char *dot = strrchr(disciplina_titulo, '.');
    if (dot) *dot = '\0';

    printf("\n--- Relatorio da disciplina %s ---\n", disciplina_titulo);

    // Imprime o cabeçalho da tabela usando a largura dinâmica
    printf("\n%-*s | %-10s | %-8s | %-5s | %s\n", max_name_width, "Nome", "RA", "Turma", "Notas", "Media");
    for (int i = 0; i < max_name_width + 38; i++) { printf("-"); }
    printf("\n");

    char line[MAX_LINE];
    int count = 0;
    // 2. Segunda passada: Imprimir os dados com a formatação correta
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
    return 0; // Sucesso
}