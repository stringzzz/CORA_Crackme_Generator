#ifndef stringzzz_crackme_library_h

/*

    For use in building your own crackme challenges.
    By stringzzz, Ghostwarez Co. 2024

*/

void genBox(int out_box[], int box_size, int shuffles) {
    //Setup out_box to initial values in order from 0 to box_size
    //Suggested not to use in the actual crackme, as it will change evey time the program is ran
    //Meant for setting up the boxes to use in the crackme with the other functions
    //Such as sBox, pBox, etc.
    //shuffles should be greater for greater box_size, actual amount is up to the user
    for(int i = 0; i < box_size; i++) {
        out_box[i] = i;
    }

    //Shuffle the box by int shuffles amount of times
    //Uses rand() to choose from beginning (left) or end (right) to grab from
    for(int shuffle_count = 0; shuffle_count < shuffles; shuffle_count++) {
        int temp_box[box_size];
        //Copy out_box to temp_box
        for(int i = 0; i < box_size; i++) {
            temp_box[i] = out_box[i];
        }
        int left = 0, right = box_size - 1;
        for(int i = 0; i < box_size; i++) {
            if (rand() % 2 == 0) {
                out_box[i] = temp_box[left];
                left++;
            } else {
                out_box[i] = temp_box[right];
                right--;
            }
        } 
    }
}

void genInvertedBox(int inv_box[], int box[], int box_size) {
    //Create the inverted S-Box, P-Box, etc. using the initial box
    for(int n = 0; n < box_size; n++) {
        inv_box[box[n]] = n;
    }
}

void genBytes(int bytes[], int byte_array_size, int max_value) {
    //For generating an array of int values
    //Suggested not to use in the actual crackme, as it will change evey time the program is ran
    //Meant for the values used in xorBytes, addBytes, addNybbles, etc.
    for(int i = 0; i < byte_array_size; i++) {
        bytes[i] = rand() % (max_value + 1);
    }
}

void sBox(char string[], int string_len, int sbox[]) {
    //Run string through S-Box
    //Call with inverted S-Box to reverse the process
        for(int i = 0; i < string_len; i++) {
		string[i] = sbox[string[i]];
	}
}

void pBox(char new_string[], char old_string[], int string_len, int pbox[]) {
    //Run old_string through P-Box
    //Call with inverted P-Box to reverse the process
    //P-Box must be same size as string_len!
    for(int i = 0; i < string_len; i++) {
        new_string[pbox[i]] = old_string[i];
    }
}

void stringReversal(char new_string[], char old_string[], int string_len) {
    //Get reverse of string
    //Inverse is itself
	for (int i = string_len - 1, i2 = 0; i >= 0; i--, i2++) {
		new_string[i2] = old_string[i];
	}
	new_string[string_len] = '\0';
}

void rotateNybbles(char string[], int string_len) {
    //Rotate the left and right nybbles of each byte of string
    //Inverse is itself
    for (int i = 0; i < string_len; i++) {
		string[i] = ((unsigned char)(string[i] & 15) << 4) ^ ((unsigned char)string[i] >> 4);
	}
}

void bitReversal(char string[], int string_len) {
    //Get reverse of the bits of the string
    //Inverse is itself
    for(int i = 0; i < string_len; i++) {
		string[i] = ((string[i] & 1) << 7) ^ ((string[i] & 2) << 5) ^ ((string[i] & 4) << 3) ^ ((string[i] & 8) << 1) ^ ((string[i] & 16) >> 1) ^ ((string[i] & 32) >> 3) ^ ((string[i] & 64) >> 5) ^ ((string[i] & 128) >> 7);
	} 
}

void bytesToNybbles(char string[], int string_len, int nybbles[]) {
    //Convert string to array of nybbles
    //nybbles must be size string_len * 2!
    int n = 0;
    for(int i = 0; i < string_len; i++) {
        nybbles[n] = string[i] >> 4; //Left nybble
        n++;
        nybbles[n] = string[i] & 15; //Right nybble
        n++;
    }
}

void nybblesToBytes(char string[], int string_len, int nybbles[]) {
    //Reassemble array of nybbles into bytes as a string
    //nybbles must be size string_len * 2!
    int n = 0;
    for(int i = 0; i < string_len; i++) {
        string[i] = ((unsigned char)nybbles[n] << 4) ^ (nybbles[n+1]);
        n += 2;
    }
}

void bytesToBits(char string[], int string_len, int bits[]) {
    //Convert string to array of bits
    //bits must be size string_len * 8!
    int i = 0;
    for (unsigned int n = 0; n < string_len; n++) {
        for (int n2 = 1; n2 <= 8; n2++) {
            bits[i] = ((unsigned char)string[n] >> (8 - n2)) & 1;
            i++;
        }
    }
}

void bitsToBytes(char string[], int string_len, int bits[]) {
    //Reassemble array of bits into bytes as a string
    //bits must be size string_len * 8!
    for (int n = 0, m = 0; n < string_len; n++) {
        string[n] = ((unsigned char)string[n]) ^ bits[m];
        for(int n2 = 0; n2 < 8; n2++, m++) {
            string[n] = ((unsigned char)string[n] << 1) ^ bits[m];
        }
    } 
}

void addBytes(char string[], int string_len, int bytes[], int mod) {
    //+ bytes mod n
    //bytes must be same size as string_len!
    //mod is highest value in desired range + 1
    for(int i = 0; i < string_len; i++) {
        string[i] = (string[i] + bytes[i]) % mod;
    }
}

void subBytes(char string[], int string_len, int bytes[], int mod) {
    //- bytes mod n
    //bytes must be same size as string_len!
    //mod is highest value in desired range + 1
    for(int i = 0; i < string_len; i++) {
        string[i] = (unsigned char)(string[i] - bytes[i]) % mod;
    }
}

void addNybbles(char string[], int string_len, int nybbles[]) {
    //+ nybbles mod 16
    //nybbles must be same size as string_len * 2!
    for(int i = 0, n = 0; i < string_len; i++, n += 2) {
        string[i] = ((((string[i] >> 4) + nybbles[n]) % 16) << 4) ^ ((((string[i] & 15) + nybbles[n+1]) % 16));
    }
}

void subNybbles(char string[], int string_len, int nybbles[]) {
    //- nybbles mod 16
    //nybbles must be same size as string_len * 2!
    for(int i = 0, n = 0; i < string_len; i++, n += 2) {
        string[i] = (((unsigned char)((string[i] >> 4) - nybbles[n]) % 16) << 4) ^ (((unsigned char)((string[i] & 15) - nybbles[n+1]) % 16));
    }
}

void xorBytes(char string[], int string_len, int bytes[]) {
    //XOR the string with the xor_bytes
    //xor_bytes must be same length as string!
    //Inverse is itself
    for(int i = 0; i < string_len; i++) {
        string[i] ^= bytes[i];
    }
}

void toHexString(char new_string[], char old_string[], int string_len) {
    //Convert string into string of hex digits
    //Typically used to convert final password to string that can be stored directly in code and compared to
    //new_string length must be string_len * 2!
    char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };
	int i2 = 0;
	for (int i = 0; i < string_len; i++) {
		new_string[i2] = hexes[old_string[i] >> 4];
		i2++;
		new_string[i2] = hexes[old_string[i] & 15];
		i2++;
	}
    new_string[string_len * 2] = '\0';
}

void toBinaryString(char new_string[], char old_string[], int string_len) {
    //Convert string into string of binary digits
    //new_string length must be string_len * 8!
    int i = 0;
    for (int n = 0; n < string_len; n++) {
        for (int n2 = 1; n2 <= 8; n2++) {
            new_string[i] = (((unsigned char)old_string[n] >> (8 - n2)) & 1) + 48; //char(0 + 48) = '0', char(1 + 48) = '1'
            i++;
        }
    }
    new_string[string_len * 8] = '\0';
}

int string_length(char string[]) {
    //Get string length without strlen function
    //May throw off crackme challenger by using this instead of call to strlen
    int len = 0;
    for(int i = 0; string[i] != '\0'; i++) {
        len++;
    }
    return len;
}

int string_compare(char string1[], char string2[]) {
    //See if two strings match exactly
    //Can use instead of strcmp function
    //May throw off crackme challenger by not making call to strcmp at end
    int i = 0;
    while(string1[i] != '\0' && string2[i] != '\0') {
        if (string1[i] != string2[i]) {
            return 0;
        } else {
            i++;
        }
    }
    if (string1[i] == '\0' && string2[i] == '\0') {
        return 1;
    } else {
        return 0;
    }
}

#define stringzzz_crackme_library_h
#endif
