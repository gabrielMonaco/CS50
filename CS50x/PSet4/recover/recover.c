#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>



int main(int argc, char *argv[])
{
    //If user didn't call the progrm 2 items
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open memory card
    FILE *memCard = fopen("card.raw", "r");
    if (memCard == NULL)
    {
        printf("could not open %s ", "card.raw");
        return 1;
    }

    FILE *outptr = NULL;

    //create BYTE type
    typedef uint8_t BYTE;
    BYTE byteBlock[512]; //blocks of 512 bytes

    // create an array to store the header while checking
    BYTE header[4];
    // create an ideal array to compare with header
    BYTE jpgsig[4] = {0xff, 0xd8, 0xff, 0xe0};

    int jpgNumber = 0;
    char jpgFilename[8];


    // in a loop, look for beginning of a JPEG, untill the end of memory card
    while (fread(byteBlock, sizeof(byteBlock), 1, memCard) > 0) // greatter than 0. the EOF point
    {
        // iterar nos 4 primeiros bytes, armazenando no array header
        for (int i = 0; i < 4; i++)
        {
            header[i] = byteBlock[i];
        }

        // zerar os quatro ultimos bits do quarto byte
        header[3] = (header[3] >> 4) << 4;

        // comparar header e jpgsig. if equal, is a new jpg file
        if (memcmp(header, jpgsig, sizeof(jpgsig)) == 0)
        {
            // if is the first file
            if (outptr == NULL)
            {
                sprintf(jpgFilename, "%03d.jpg", jpgNumber); // create and give a name
                outptr = fopen(jpgFilename, "a"); // opened it
                fwrite(&byteBlock, sizeof(byteBlock), 1, outptr); // write in it
            }
            else // open a new file that is not the first file
            {
                fclose(outptr); // close the file
                jpgNumber++; // actualizing the name
                sprintf(jpgFilename, "%03d.jpg", jpgNumber); // create and give the new name
                outptr = fopen(jpgFilename, "a"); // opened it
                fwrite(&byteBlock, sizeof(byteBlock), 1, outptr); // write in it


            }
        }
        else if (outptr != NULL) //if is not a new jpg file. just a byteblock
        {
            fwrite(&byteBlock, sizeof(byteBlock), 1, outptr); // write in it
        }

    }
    // fechar arquivos abertos
    fclose(memCard);
    fclose(outptr);
    return 0;
}