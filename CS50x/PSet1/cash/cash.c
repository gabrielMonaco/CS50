#include <cs50.h>
#include <stdio.h>


int main(void)
{
    //creating cents variable
    int cents;
    // asking its value...
    do
    {
        cents = get_int("Total cents i own you? ");
    }
    // ... while negative value
    while (cents < 0);


    //count the number of coins
    int counter = 0;
    // array with types of coins
    int coinsType[4] = {25, 10, 5, 1};
    // for each type
    for (int i = 0; i < 4; i++)
    {
        // debug test printf("*");
        // while is grater than the array type
        while (cents >= coinsType[i])
        {
            // discount the value type
            cents = cents - coinsType[i];
            // add a coin to the counter
            counter = counter + 1;
            // debug test printf("&");
        }
    }
    // print the messege
    printf("%i coins\n", counter);
}
