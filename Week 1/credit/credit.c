#include <cs50.h>
#include <math.h>
#include <stdio.h>

long get_num(void);
int stellen(long number);
void calc(long number, int stellen);

int main(void)
{

    // rechnung
    // calc(n, s);

    int digit;
    long long num;
    long long num2;

    // input bekommen

    num = get_num();

    // Zahlenstellen herausfinden

    int s = stellen(num);

    // rechnung
    long part1 = 0;
    long part2 = 0;

    long reversedNum = 0;
    long reversedNum2 = 0;
    long reversedNumC = 0;
    long reversedNumV = 0;
    while (num > 0)
    {
        reversedNum = reversedNum * 10 + num % 10;
        num /= 10;
    }
    reversedNum2 = reversedNum;
    reversedNumC = reversedNum;
    reversedNumV = reversedNum;

    while (reversedNum > 0)
    {
        digit = reversedNum % 10;
        reversedNum /= 10;
        if (reversedNum > 0)
        {
            reversedNum /= 10;
            digit = digit * 2;
            if (digit > 9)
            {
                int memory = digit;
                digit = memory % 10;
                memory /= 10;
                digit += memory % 10;
            }
        }
        part1 += digit;
    }

    num2 = num;
    reversedNum2 /= 10;
    while (reversedNum2 > 0)
    {

        digit = reversedNum2 % 10;
        reversedNum2 /= 10;
        reversedNum2 /= 10;
        part2 += digit;
    }

    int final = part1 + part2;
    int final_2 = final % 10;
  //   printf("final: %i, reversnum: %ld, part2: %ld, stelle: %i, part1: %ld\n", final_2, reversedNum, part2, s,part1);
int memory2 = 0;
for (int i = 0; i<2 ; i++)
{
    memory2 = memory2 * 10 + reversedNumV % 10;
        reversedNumV /= 10;
}
int memory3 = reversedNumC % 10;


    if (final % 10 == 0)
    {
        if (s == 15)
        {
            if (memory2 == 34 || memory2 == 37)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        if (s == 16)
        {
            if (memory2 >= 51 && memory2 <= 55)
            {
                printf("MASTERCARD\n");
            }
            else if (reversedNumC % 10 == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }

        if (s == 13 || s == 16)
        {
            if (memory2 % 10 == 4)
                printf("VISA\n");
        }
       
    }
   else
    {
        printf("INVALID\n");
    }
}

long get_num(void)
{
    long n;
    n = get_long("Number: ");
    return n;
}

int stellen(long number)
{
    int stellen = 1;
    while (number >= 10)
    {
        stellen += 1;
        number = number / 10;
    }
    return stellen;
}
