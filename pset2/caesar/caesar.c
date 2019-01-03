#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include<string.h>

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Error 1: This program only accepts 1 command line argument\n");
        return 1;
    }
    int key = atoi(argv[1])%26;
    printf("plaintext:");
    string p = get_string();
    printf("ciphertext:");
    for(int i = 0, n = strlen(p); i < n; i++)
    {
        char c = p[i];
        if(isalpha(c) && isupper(c))
        {
            char d = ((c - 65) + key)%26 + 65;
            printf("%c", d);
        }
        else if(isalpha(c) && islower(c))
        {
            char e = ((c - 97) + key)%26 + 97;
            printf("%c", e);
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
}