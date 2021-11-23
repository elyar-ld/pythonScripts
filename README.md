# pythonScripts

## csvToSQL
Python script that converts comma-separated values to INSERT statements in SQL. The first argument received is the route and name of the .csv file; the second is the name that the table and .sql file will have (is optional).

## steganography
My implementation of [steganography](https://towardsdatascience.com/steganography-hiding-an-image-inside-another-77ca66b2acb1) in images technique.

**encodeImage:** This script hides the binary of any file into an image. Takes every bit of the file to be encoded, and puts it in the least significant bit of RGB values of a random pixel in the image. A password that generates a seed for the random positions is required. The use of the script is `python encodeImage.py wrapperImage.ext fileToEncode.ext password`. The result is a `resultEncoded.png` file.

**decodeImage:** This decodes the file encoded by `encodeImage.py`. Visits the random image pixels, takes the least significant bit of its RGB values, and recomposes the binary file. The use of the script is `python decodeImage.py resultEncoded.png password`. The result is a `resultDecoded` file. The extension must be added manually.

**showLastBit:** Script that creates an image made with the least significant bit of another. This can be used for observing if the least bit of images has been manipulated. The use of the script is `python showLastBit.py image.ext`