#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// declare functions
int count_letters(string texto);
int count_words(string texto);
int count_sentences(string texto);


int main(void)
{
    // input a text
    string texto = get_string("Text: ");
    // declare variables
    float letras, palavras, frases;
    letras = count_letters(texto);
    palavras = count_words(texto);
    frases = count_sentences(texto);

    // calculating the indeex
    float L, S;
    double index;
    L = (letras / palavras * 100);
    S = (frases / palavras * 100);
    index = round(0.0588 * L - 0.296 * S - 15.8);

    // what to plot
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        if (index <= 0)
        {
            printf("Before Grade 1\n");

        }
        else
        {
            int int_index = (int) index;
            printf("Grade %i\n", int_index);
        }
    }

}
// funtion to sum the number of letters
int count_letters(string texto)
{
    int letras = 0;
    for (int i = 0; i < strlen(texto); i++)
    {
        if (isalpha(texto[i]))
        {
            letras += 1;
        }
    }
    // printf("%i letras\n", letras);
    return letras;
}

// funtion to sum the number of words
int count_words(string texto)
{
    int palavras = 1;
    for (int i = 0; i < strlen(texto); i++)
    {
        if (isspace(texto[i]))
        {
            palavras += 1;
        }
    }
    // printf("%i palavras\n", palavras);
    return palavras;
}

// funtion to sum the number of sentences
int count_sentences(string texto)
{
    int frases = 0;
    for (int i = 0; i < strlen(texto); i++)
    {
        if (texto[i] == '.' || texto[i] == '!' || texto[i] == '?')
        {
            frases += 1;
        }
    }
    // printf("%i frases\n", frases);
    return frases;
}