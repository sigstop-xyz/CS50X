#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text, int length);
int count_words(string text, int length);
int count_sentences(string text, int length);

int main(void)
{
    // Input nehmen in form von string
    string text = get_string("Text: ");

    // Länge feststellen
    int length = strlen(text);

    // Funktionen ausführen
    int count_l = count_letters(text, length);
    int count_w = count_words(text, length);
    int count_s = count_sentences(text, length);

    // Rechnung durchführen
    float count_lf = count_l;
    float count_wf = count_w;
    float count_sf = count_s;
    float L = count_lf / count_wf * 100;
    float S = count_sf / count_wf * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);
    int final = index;

    // Ergebnis drucken
    if (final >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (final < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", final);
    }
}

// Funktion mit der die Anzahl an Buchstaben gezählt wird.
int count_letters(string text, int length)
{
    int count = 0;
    for (int i = 0; i < length; i++)
    {
        if (text[i] > 64 && text[i] < 91)
        {
            count++;
        }
        else if (text[i] > 96 && text[i] < 123)
        {
            count++;
        }
        else
        {
            count += 0;
        }
    }
    return count;
}

// Funktion mit der die Anzahl an Wörtern gezählt wird.
int count_words(string text, int length)
{
    int count = 1;
    for (int i = 0; i < length; i++)
    {
        if (text[i] == 32)
        {
            count++;
        }
        else
        {
            count += 0;
        }
    }
    return count;
}

// Funktion mit der die Anzahl der Sätze gezählt wird.
int count_sentences(string text, int length)
{
    int count = 0;
    for (int i = 0; i < length; i++)
    {
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            count++;
        }
        else
        {
            count += 0;
        }
    }
    return count;
}
