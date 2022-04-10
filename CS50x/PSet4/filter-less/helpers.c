#include "helpers.h"

#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float rgbGray;
    // for each pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // mean value = grey scale
            rgbGray = round(round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue)) / 3);
            if (rgbGray > 255)
            {
                rgbGray = 255;
            }
            image[i][j].rgbtRed = rgbGray;
            image[i][j].rgbtGreen = rgbGray;
            image[i][j].rgbtBlue = rgbGray;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed, sepiaGreen, sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaRed = round((0.393 * image[i][j].rgbtRed) + (0.769 * image[i][j].rgbtGreen) + (0.189 * image[i][j].rgbtBlue));
            sepiaGreen = round((0.349 * image[i][j].rgbtRed) + (0.686 * image[i][j].rgbtGreen) + (0.168 * image[i][j].rgbtBlue));
            sepiaBlue = round((0.272 * image[i][j].rgbtRed) + (0.534 * image[i][j].rgbtGreen) + (0.131 * image[i][j].rgbtBlue));

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }


            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    //
    int temp[3];
    // for each pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            temp[0] = image[i][j].rgbtRed;
            temp[1] = image[i][j].rgbtGreen;
            temp[2] = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - (j + 1)].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - (j + 1)].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - (j + 1)].rgbtBlue;

            image[i][width - (j + 1)].rgbtRed = temp[0];
            image[i][width - (j + 1)].rgbtGreen = temp[1];
            image[i][width - (j + 1)].rgbtBlue = temp[2];

        }
    }
    return;
}




// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE imageBlur[height][width];
    // for each pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // number of pixels (for mean value)
            float numPixels = 0;

            // the neighborhood mean
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;

            for (int k = i - 1; k < i + 2; k++) //for each line of neighborhood
            {
                for (int l = j - 1; l < j + 2; l++) //for each element of neighborhood
                {
                    if (k < 0 || l < 0 || k >= height || l >= width) // if has no data, continue
                    {
                        continue;
                    }
                    else
                    {
                        numPixels += 1; // one more pixel (to the mean)
                        //sum of neighborhood's collor
                        sumRed += image[k][l].rgbtRed;
                        sumGreen += image[k][l].rgbtGreen;
                        sumBlue += image[k][l].rgbtBlue;
                    }
                }
            }
            // get the copied pixels value
            imageBlur[i][j].rgbtRed = round(sumRed / numPixels);
            imageBlur[i][j].rgbtGreen = round(sumGreen / numPixels);
            imageBlur[i][j].rgbtBlue = round(sumBlue / numPixels);

            // if bigger than 255
            if (imageBlur[i][j].rgbtRed > 255)
            {
                imageBlur[i][j].rgbtRed = 255;
            }
            if (imageBlur[i][j].rgbtGreen > 255)
            {
                imageBlur[i][j].rgbtGreen = 255;
            }
            if (imageBlur[i][j].rgbtBlue > 255)
            {
                imageBlur[i][j].rgbtBlue = 255;
            }

        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // revalue the original image
            image[i][j].rgbtRed = imageBlur[i][j].rgbtRed;
            image[i][j].rgbtGreen = imageBlur[i][j].rgbtGreen;
            image[i][j].rgbtBlue = imageBlur[i][j].rgbtBlue;
        }
    }
    return;
}
