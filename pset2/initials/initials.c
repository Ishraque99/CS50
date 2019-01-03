#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>

int main(void)
{
    string s = get_string();
    if(s[0] >= 'A' && s[0] <= 'z')
    {
        printf("%c", toupper(s[0]));
    }
    for(int i = 0, n = strlen(s); i < n; i++)
    {
        char d = s[i];
        char e = s[i+1];
        if (d == ' ' && e >= 'A' && e <= 'z')
        {
            printf("%c", toupper(e));
        }
    }
    printf("\n");
}