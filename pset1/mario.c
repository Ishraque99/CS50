#include<stdio.h>
#include<cs50.h>

int main(void)
{
    int h;
    do
    {
        printf("Height: ");
        h = get_int();
    }
    while (h <0 || h > 23);
    
    for(int i = 1; i <= h; i++)
    {
        for(int j = 0; j <= h; j++)
        {
            if (j < h - i)
            printf(" ");
            else
            printf("#");
        }
        printf("\n");
    }
}