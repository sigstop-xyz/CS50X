#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    BYTE buffer[BLOCK_SIZE];
    if (argc != 2)
{
    printf("Usage: ./recover image\n");
    return 1;
}

FILE *file = fopen(argv[1], "r");

if (file == NULL)
{
    printf("Could not open file.\n");
    return 1;
}
    int file_number = -1;
    FILE *filefound;
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {


        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            file_number++;
            if (filefound != NULL)
        {
            fclose(filefound);
        }
            char filename[8];
        sprintf(filename, "%03i.jpg", file_number);
        filefound = fopen(filename, "w");

            fwrite(buffer, sizeof(char), BLOCK_SIZE, filefound);
        if (filefound == NULL)
        {
            return 1;
        }

        }
        else if (filefound != NULL)
        {
            fwrite(buffer, sizeof(char), BLOCK_SIZE, filefound);
        }


    }
      if (filefound != NULL)
        {
            fclose(filefound);
        }
 fclose(file);
    return 0;
}
