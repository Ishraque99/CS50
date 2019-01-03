#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main(void)
{
    printf("O hai! ");
    float x;
    do
    {
        printf("How much change is owed?\n");
        x = get_float();
    }
    while (x < 0.0);
    
    int monies = round(x * 100);
    
    int count = 0;
    
    while(monies >= 25)
    {
        monies = monies - 25;
        count++;
    }
    while(monies >= 10)
    {
        monies = monies - 10;
        count++;
    }
    while(monies >= 5)
    {
        monies = monies - 5;
        count++;
    }
    while(monies >= 1)
    {
        monies = monies - 1;
        count++;
    }
    
    printf("%i\n", count);
}