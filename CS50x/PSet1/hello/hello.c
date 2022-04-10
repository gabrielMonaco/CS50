#include <stdio.h>
#include <cs50.h>


int main(void)
{
    // asking who is there
    string name = get_string("what is your name? \n");
    // printing the messege
    printf("hello, %s\n", name);
}