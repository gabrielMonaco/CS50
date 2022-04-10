#include <cs50.h>
#include <stdio.h>


int main(void)
{
    //declaring variable
    int height;
    do
    {
        // asking height...
        height = get_int("Height: ");
    }
    // ...between 1-8
    while (height < 1 || height > 8);

    // for each line...
    for (int i = 0; i < height; i++)
    {
        // ...print spaces
        for (int j = height - i; j > 1; j--)
        {
            printf(" ");
        }
        // ...print hashs
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
