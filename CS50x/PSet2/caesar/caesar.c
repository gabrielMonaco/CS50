#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

bool is_valid_key(string s);
void encrypt(string plaintext, string ciphertext, int k);


int main(int argc, string argv[]) {
    if (argc != 2 || !is_valid_key(argv[1])) {
        printf("Usage: ./caesar key\n");
        return 1;
    }


    int k = atoi(argv[1]);
    string s = get_string("plaintext: ");
    int n = strlen(s);
    char ciphertext[n + 1];
    encrypt(s, ciphertext, k);
    printf("ciphertext: %s\n", ciphertext);
    return 0;

}


void encrypt(string s, string ciphertext, int k) {
    int i = 0;
    for (i = 0; i < strlen(s); i++) {
        char ch = s[i];

        if (isalpha(ch)) {
            char temp = tolower(ch);
            int pi = temp - 'a';
            char ci = ( (pi + k) % 26) + 'a';
            ciphertext[i] = islower(ch) ? ci : toupper(ci);


        } else {
            ciphertext[i] = ch;
        }
    }
    ciphertext[i] = '\0';

}

bool is_valid_key(string s) {
    for (int i = 0; i < strlen(s); i++) {
        char ch = s[i];
        if (!isdigit(ch)) {
            return false;
        }

    }
    return true;
}


