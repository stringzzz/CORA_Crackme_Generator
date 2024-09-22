#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "stringzzz_crackme_library.h"

/*

    Demonstration of the different stringzzz_crackme_library functions
    Note that due to the different odd characters output after each operation, 
    the output may end up 'garbled up' and the rest may not display properly.
    This is just for example purposes, chances are you will not be displaying the strings
    in the actual crackme anyway.

    By stringzzz, Ghostwarez Co. 2024

*/

int main() {
    srand(time(NULL)); //For genBox() function

    //genBox
    int box[16]; //Must declare the box to pass to genBox
    genBox(box, 16, 30); //genBox(int out_box[], int box_size, int shuffles)

    //Output the box in format for initializing the actual box in the crackme
    printf("box output: { ");
    for(int i = 0; i < 16; i++) {
        printf("%i", box[i]);
        if (i < 15) { printf(", "); }
    }
    printf(" };\n\n");

    //genBytes
    int bytes[16]; //Must declare the bytes to pass to genBytes
    genBytes(bytes, 16, 127); //genBytes(int bytes, int byte_array_size, int max_value)

    //Output the bytes in format for initializing the actual bytes in the crackme
    printf("bytes output: { ");
    for(int i = 0; i < 16; i++) {
        printf("%i", bytes[i]);
        if (i < 15) { printf(", "); }
    }
    printf(" };\n\n");

    //sBox
    char test_string[] = "testing one two three";
    printf("Before S-Box: %s\n", test_string);
    int sbox[128]; //Must declare the box to pass to genBox
    genBox(sbox, 128, 100); //genBox(int out_box[], int box_size, int shuffles)
    sBox(test_string, string_length(test_string), sbox); //sBox(char string, int string_len, int sbox[])
    printf("After S-Box: %s\n", test_string);
    //Inverted sBox
    int inv_sbox[128];
    genInvertedBox(inv_sbox, sbox, 128); //genInvertedBox(int inv_box[], int box[], int box_size)
    sBox(test_string, string_length(test_string), inv_sbox); //sBox(char string, int string_len, int sbox[])
    printf("After Inverted S-Box: %s\n\n", test_string);

    //pBox
    char test_string2[] = "testing one two three";
    printf("Before P-Box: %s\n", test_string2);
    int len1 = string_length(test_string2);
    int pbox[len1]; //Must declare the box to pass to genBox
    genBox(pbox, len1, 30); //genBox(int out_box[], int box_size, int shuffles)
    char test_string3[len1 + 1];
    pBox(test_string3, test_string2, len1, pbox); //pBox(char new_string[], char old_string[], int string_len, int pbox[])
    printf("After P-Box: %s\n", test_string3);
    //Inverted pBox
    int inv_pbox[len1];
    genInvertedBox(inv_pbox, pbox, len1); //genInvertedBox(int inv_box[], int box[], int box_size)
    char test_string4[len1 + 1];
    pBox(test_string4, test_string3, len1, inv_pbox); //pBox(char new_string[], char old_string[], int string_len, int pbox[])
    printf("After Inverted P-Box: %s\n\n", test_string4);

    //addBytes
    char add_string[] = "testing one two three";
    printf("Before Add Bytes: %s\n", add_string);
    int add_bytes[len1];
    genBytes(add_bytes, len1, 127); //genBytes(int bytes[], int byte_array_size, int max_value)
    addBytes(add_string, len1, add_bytes, 128); //addBytes(char string[], int string_len, int bytes[], int mod)
    printf("After Add Bytes: %s\n", add_string);
    //subBytes
    subBytes(add_string, len1, add_bytes, 128); //subBytes(char string[], int string_len, int bytes[], int mod)
    printf("After Sub Bytes: %s\n\n", add_string);

    //addNybbles
    char nybble_string[] = "testing one two three";
    printf("Before Add Nybbles: %s\n", nybble_string);
    int add_nybbles[len1 * 2];
    genBytes(add_nybbles, len1 * 2, 15); //genBytes(int bytes[], int byte_array_size, int max_value)
    addNybbles(nybble_string, len1, add_nybbles); //addNybbles(char string[], int string_len, int bytes[])
    printf("After Add Nybbles: %s\n", nybble_string);
    //subNybbles
    subNybbles(nybble_string, len1, add_nybbles); //subNybbles(char string[], int string_len, int bytes[])
    printf("After Sub Nybbles: %s\n\n", nybble_string);

    //xorBytes
    char xor_string[] = "testing one two three";
    printf("Before xor bytes: %s\n", xor_string);
    int xor_bytes[len1];
    genBytes(xor_bytes, len1, 127); //genBytes(int bytes[], int byte_array_size, int max_value)
    xorBytes(xor_string, len1, xor_bytes); //xorBytes(char string[], int string_len, int bytes[])
    printf("After xor bytes: %s\n", xor_string);
    xorBytes(xor_string, len1, xor_bytes); //xorBytes(char string[], int string_len, int bytes[])
    printf("After xor bytes again: %s\n\n", xor_string);

    //stringReversal
    char original_string[] = "this is a test";
    printf("String before reverse: %s\n", original_string);
    int rev_len = string_length(original_string);
    char reversed_string[rev_len + 1];
    stringReversal(reversed_string, original_string, rev_len); //stringReversal(char new_string[], char old_string[], int string_len)
    printf("String after reverse: %s\n", reversed_string);
    char reversed_string2[rev_len + 1];
    stringReversal(reversed_string2, reversed_string, rev_len); //stringReversal(char new_string[], char old_string[], int string_len)
    printf("String after reverse again: %s\n\n", reversed_string2);

    //rotateNybbles
    char nybble_string3[] = "this is a test";
    printf("String before nybble rotation: %s\n", nybble_string3);
    int nybble_len = string_length(nybble_string3);
    rotateNybbles(nybble_string3, nybble_len); //rotateNybbles(char string[], int string_len)
    printf("String after nybble rotation: %s\n", nybble_string3);
    rotateNybbles(nybble_string3, nybble_len); //rotateNybbles(char string[], int string_len)
    printf("String after nybble rotation again: %s\n\n", nybble_string3);

    //bitReversal
    char original_string2[] = "testing";
    printf("String before bit reverse: %s\n", original_string2);
    int rev_bit_len = string_length(original_string2);
    bitReversal(original_string2, rev_bit_len); //bitReversal(char string[], int string_len)
    printf("String after bit reverse: %s\n", original_string2);
    bitReversal(original_string2, rev_bit_len); //bitReversal(char string[], int string_len)
    printf("String after bit reverse again: %s\n\n", original_string2);

    //bytesToNybbles
    //The main purpose of this (not shown) is to generate a P-Box the same size as nybbles_array
    // and run the nybble_array through it, permuting all the nybbles of the string.
    // They could then be reassembled
    char nybble_string1[] = "testing one two";
    printf("Original string: %s\n", nybble_string1);
    int len3 = string_length(nybble_string1);
    int nybble_array[len3 * 2];
    bytesToNybbles(nybble_string1, len3, nybble_array); //bytesToNybbles(char string[], int string_len, int nybbles[])
    printf("String as array of nybbles: ");
    for(int i = 0; i < len3 * 2; i++) {
        printf("%i ", nybble_array[i]);
    }
    printf("\n");
    //nybblesToBytes
    //Reassemble the nybbles back into a string
    char nybble_string2[len3 + 1];
    nybblesToBytes(nybble_string2, len3, nybble_array); //nybblesToBytes(char string[], int string_len, int nybbles[])
    printf("After reassemble back into string: %s\n\n", nybble_string2);

    //bytesToBits
    //The main purpose of this (not shown) is to generate a P-Box the same size as bit_array
    // and run the bit_array through it, permuting all the bits of the string.
    // They could then be reassembled
    char test_string5[] = "testing";
    printf("Original string: %s\n", test_string5);
    int len2 = string_length(test_string5);
    int bit_array[len2 * 8];
    bytesToBits(test_string5, len2, bit_array); //bytesToBits(char string[], int string_len, int bits[])
    printf("String as array of bits: ");
    for(int i = 0; i < len2 * 8; i++) {
        printf("%i ", bit_array[i]);
    }
    printf("\n");
    //bitsToBytes
    //Reassemble the bits back into a string
    char test_string6[len2 + 1];
    bitsToBytes(test_string6, len2, bit_array); //bitsToBytes(char string[], int string_len, int bits[])
    printf("After reassemble back into string: %s\n\n", test_string6);

    //Convert string to string of hex digits
    char test_string7[] = "testing one two three";
    printf("String as normal: %s\n", test_string7);
    int len4 = string_length(test_string7);
    char hex_string[len4 * 2 + 1];
    toHexString(hex_string, test_string7, len4); //toHexString(char new_string[], char old_string[], int string_len)
    printf("String as hex digits: %s\n", hex_string);
    //Convert same string to string of binary digits
    char bin_string[len4 * 8 + 1];
    toBinaryString(bin_string, test_string7, len4); //toBinaryString(char new_string[], char old_string[], int string_len)
    printf("String as binary digits: %s\n\n", bin_string);

    return 0;
}