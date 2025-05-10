#include <cs50.h>
#include <stdio.h>

int get_input(void);
void print_grid(int size);

int main(void)
{
    // get input from user
    int n = get_input();

    // print bricks
    print_grid(n);
}

int get_input(void)
{

    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n >= 9 || n < 1);
    return n;
}

void print_grid(int size)
{
    int anzahl = size;

    for (int i = 0; i < size; i++, anzahl--)
    {
        for (int h = 0; h < anzahl - 1; h++)
        {
            printf(" ");
        }
        for (int j = 0; j < size - (anzahl - 1); j++)
        {
            printf("#");
        }

        printf("  ");

        for (int j = 0; j < size - (anzahl - 1); j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
