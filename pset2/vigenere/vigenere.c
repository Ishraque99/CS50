#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include<string.h>

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Error 1a: This program only accepts 1 command line argument\n");
        return 1;
    }
    string key = argv[1];
    int key_length = strlen(key);
    char vig_shift_array[key_length];
    for(int j = 0, vig_mod = 0; j < key_length; j++)
    {
        char key_number = key[j];
        if(isalpha(key_number) && isupper(key_number))
        {
            vig_shift_array[vig_mod] = key_number - 65;
            vig_mod++;
        }
        else if(isalpha(key_number) && islower(key_number))
        {
            vig_shift_array[vig_mod] = key_number - 97;
            vig_mod++;
        }
        else
        {
            printf("Error 1b: Keyword must contain only alphabets\n");
            return 1;
        }
    }
    printf("plaintext: ");
    string p = get_string();
    printf("ciphertext: ");
    for(int i = 0, n = strlen(p), a = 0; i < n; i++)
    {
        char c = p[i];
        if(isalpha(c) && isupper(c))
        {
            char d = ((c - 65) + vig_shift_array[a%key_length])%26 + 65;
            printf("%c", d);
            a++;
        }
        else if(isalpha(c) && islower(c))
        {
            char e = ((c - 97) + vig_shift_array[a%key_length])%26 + 97;
            printf("%c", e);
            a++;
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");    

}