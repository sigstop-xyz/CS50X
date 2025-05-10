#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char rotate(char c, int r);
bool only_digits(string s);

int main(int argc, string argv[])
{
    // Exit
    if (argc == 1 || argc > 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        // Check für nur Zahlen
        if (only_digits(argv[1]) == false)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        else if (only_digits(argv[1]) == true)
        {
            // String als input nehmen
            string text = get_string("plaintext: ");

            // key bilden
            int r = atoi(argv[1]);

            // Länge ermitteln
            int length = strlen(text);

            // Cipher bilden
            printf("ciphertext: ");
            for (int i = 0; i < length; i++)
            {
                if (text[i] >= 65 && text[i] <= 90)
                {
                    printf("%c", rotate(text[i], r));
                }
                else if (text[i] >= 97 && text[i] <= 122)
                {
                    printf("%c", rotate(text[i], r));
                }
                else
                {
                    printf("%c", text[i]);
                }
            }
            printf("\n");

            return 0;
        }
    }
}

// Funktion die den Text verschlüsselt
char rotate(char c, int r)
{
    char new_c;
    if (islower(c) == 0)
    {
        new_c = ((c - 'A' + r) % 26) + 'A';
    }
    else
    {
        new_c = ((c - 'a' + r) % 26) + 'a';
    }
    return new_c;
}

// Funktion die checkt ob der Input string nur digits ist.
bool only_digits(string s)
{
    int length = strlen(s);
    int check = 0;
    for (int i = 0; i < length; i++)
    {
        if (isdigit(s[i]) == 0)
        {
            check++;
        }
        else
        {
            check += 0;
        }
    }
    if (check == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
