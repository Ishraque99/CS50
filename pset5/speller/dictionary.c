/**
 * Implements a dictionary's functionality.
 */

#include<stdbool.h>
#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include<string.h>
#include<math.h>
#include<strings.h>
#include "dictionary.h"

#define HASHCAP 50


typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

node *hashtable[HASHCAP] = {NULL};


int hash(char *x);

int dicsize = 0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // TODO
    int l = strlen(word);
    char strcheck[l + 1];
    for(int i = 0; i < l; i++)
    {
        strcheck[i] = tolower(word[i]);
    }
    strcheck[l] = '\0';
    
    //int table_check = hash(check);
    
    node *cursor = hashtable[hash(strcheck)];
    
    while(cursor != NULL)
    {
        if (strcasecmp(cursor->word, strcheck) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // TODO
    FILE *dic = fopen(dictionary, "r");
    if (dic == NULL)
    {
        printf("Could not open %s\n", dictionary);
        return false;
    }
    
    char word[LENGTH + 1];
    
    while(fscanf(dic, "%s", word) !=EOF)
    {
        node *newn = malloc(sizeof(node));
        memset(newn, 0, sizeof(node));
        if (newn == NULL)
        {
            unload();
            return false;
        }
        strcpy(newn->word, word);
        int table_number = hash(newn->word);
        //inserting into hashtable
        if(hashtable[table_number] == NULL)
        {
            hashtable[table_number] = newn;
        }
        else if (hashtable[table_number] != NULL)
        {
            newn->next = hashtable[table_number];
            hashtable[table_number] = newn;
        }
        dicsize++;
    }
    fclose(dic);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    return dicsize;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // TODO
    for(int i = 0; i < HASHCAP; i++)
    {
        node *point = hashtable[i];
        while (point != NULL)
        {
            node *temp = point;
            point = point->next;
            free(temp);
        }
    }
    return true;
}

//hashfunction
int hash(char *x)
{
    int y = strlen(x);
    int sum = 0;
    for (int i = 0; i < y; i++)
    {
        int a = atoi(&x[i]);
        sum += a;
    }
    int hesh = sum % HASHCAP;
    return hesh;
}