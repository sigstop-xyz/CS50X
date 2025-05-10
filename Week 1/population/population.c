#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int n;
    do
    {
        n = get_int("Start size: ");
    }
    while (n < 9);

    // TODO: Prompt for end size

    int m;
    do
    {
        m = get_int("End size: ");
    }
    while (m < n);

    // TODO: Calculate number of years until we reach threshold
    int e = 0;
    if (m > n)
    {
        do
        {
            n = n + n / 3 - n / 4;
            e++;
        }
        while (n < m);
    }
    // TODO: Print number of years
    printf("Years: %i\n", e);
}
