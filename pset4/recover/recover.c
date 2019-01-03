#include<stdio.h>
#include<stdlib.h>

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if(file == NULL)
    {
        fclose(file);
        fprintf(stderr, "Unable to open file %s\n", argv[1]);
        return 2;
    }
    unsigned char buffer[512];
    fread(buffer, 512, 1, file);
    FILE* output;
    int jpeg = 0;
    while(fread(buffer, 512, 1, file) == 1)
    {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            char name[8];
            sprintf(name, "%03d.jpg", jpeg);
            output = fopen(name, "w");
            fwrite(buffer, 512, 1, output);
            jpeg++;
        }
        else
        {
            fwrite(buffer, 512, 1, output);
        }
    }
    fclose(output);
    fclose(file);
    return 0;
}