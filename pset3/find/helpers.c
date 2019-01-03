/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    int start = 0, end = n - 1;
    int confirm = 0;
    while(start <= end)
    {
        int check = (start + end)/2;
        if(values[check] == value)
        {
            confirm++;
            return true;
        }
        else if(value > values[check])
        {
            start = check + 1;
        }
        else if(value < values[check])
        {
            end = check - 1;
        }

    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    int swap = -1;
    do
    {
        swap = 0;
        int j = 0;
        for(int i = 0; i < (n - 1 - j); i++)
        {
            if(values[i] > values[i+1])
            {
                int p = values[i+1];
                values [i+1] = values[i];
                values[i] = p;
                swap++;
            }
        }
        j++;
    }
    while(swap != 0);
}
