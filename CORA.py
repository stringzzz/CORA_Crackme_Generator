# CORA: Crackme Originator Randomizing Automator
# By stringzzz, Ghostwarez Co. :3
#
# Uses prng and input difficulty level to generate a crackme challenge executable
# Doesn't remove the resulting c source code file by default, see end of code for uncommenting this
#
# Start Date: 09-04-2024
# Levels 0-5 Complete Date: 09-05-2024
# Levels 6-8 Complate Date: 09-09-2024
# Major overhaul to fix several different problems Complete Date: 09-10-2024
# Level 9 Complete Date: 09-11-2024
# Added level 10: 09-13-2024

import os
import random

def password_gen():
	chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@$%&?"
	pass1 = ""
	length = random.randint(8, 24)
	for n in range(0, length):
		pass1 += random.choice(chars)
	return pass1
	
c_source_template = "\
#include <stdio.h>\n\
#include <string.h>\n\
#include <stdbool.h>\n\
\n\
int main() {\n\
	bool authenticated = 0;\n\
	\n\
	char password_guess[64];\n\
	printf(\"Enter the password: \");\n\
	scanf(\"%[^\\n]%*c\", password_guess);\n\
	{{AUTHENTICATION}}\n\
	if (authenticated) {\n\
		printf(\"\\nSUCCESS! GOOD JOB!\\n\\n\");\n\
	} else {\n\
		printf(\"\\nFAILURE! TRY AGAIN!\\n\\n\");\n\
	}\n\
	\n\
	return 0;\n\
}\
"	

ab_compress = "\
return 0;\n}\n\
char* abCompress(char s1[], char detect_char, char replace_char1, char replace_char2, char replace_char3) {\n\
	\n\
	char s2[strlen(s1) + 1];\n\
	memset(s2, 0, (strlen(s1) + 1)*sizeof(char));\n\
	int i = 0;\n\
	int chars_left = 0;\n\
	for (int n4 = 0; (n4 + 3) < strlen(s1); i++) {\n\
		if (s1[n4] == detect_char && s1[n4+1] == detect_char && s1[n4+2] == detect_char && s1[n4+3] == detect_char) {\n\
			s2[i] = replace_char1;\n\
			n4 += 4;\n\
		} else {\n\
			s2[i] = s1[n4];\n\
			n4++;\n\
		}\n\
		if ((n4 + 3) >= strlen(s1)) {\n\
			chars_left = strlen(s1) - n4;\n\
		}\n\
	}\n\
	while (chars_left != 0) {\n\
		s2[i] = s1[strlen(s1) - chars_left];\n\
		chars_left--;\n\
		i++;\n\
	}\n\
	s2[i] = '\\0';\n\
	\n\
	char s3[strlen(s2) + 1];\n\
	memset(s3, 0, (strlen(s2) + 1)*sizeof(char));\n\
	i = 0;\n\
	chars_left = 0;\n\
	for (int n3 = 0; (n3 + 2) < strlen(s2); i++) {\n\
		if (s2[n3] == detect_char && s2[n3+1] == detect_char && s2[n3+2] == detect_char) {\n\
			s3[i] = replace_char2;\n\
			n3 += 3;\n\
		} else {\n\
			s3[i] = s2[n3];\n\
			n3++;\n\
		}\n\
		if ((n3 + 2) >= strlen(s2)) {\n\
			chars_left = strlen(s2) - n3;\n\
		}\n\
	}\n\
	while (chars_left != 0) {\n\
		s3[i] = s2[strlen(s2) - chars_left];\n\
		chars_left--;\n\
		i++;\n\
	}\n\
	s3[i] = '\\0';\n\
	\n\
	char *s4 = malloc((strlen(s3) + 1) * sizeof(char));\n\
	memset(s4, 0, (strlen(s3) + 1)*sizeof(char));\n\
	i = 0;\n\
	chars_left = 0;\n\
	for (int n2 = 0; (n2 + 1) < strlen(s3); i++) {\n\
		if (s3[n2] == detect_char && s3[n2+1] == detect_char) {\n\
			s4[i] = replace_char3;\n\
			n2 += 2;\n\
		} else {\n\
			s4[i] = s3[n2];\n\
			n2++;\n\
		}\n\
		if ((n2 + 1) >= strlen(s3)) {\n\
			chars_left = strlen(s3) - n2;\n\
		}\n\
	}\n\
	while (chars_left != 0) {\n\
		s4[i] = s3[strlen(s3) - chars_left];\n\
		chars_left--;\n\
		i++;\n\
	}\n\
	s4[i] = '\\0';\n\
	\n\
	return s4;\n\
\n\
}\n\
"

c_source_final = ""
	
executable_name = input("Enter the name of the executable: ")
difficulty_level = int(input("Enter the difficulty level (0-10): "))

print("\nGenerating source code...")

if (difficulty_level == 0):
	authentication_template0 = "\
if (strcmp(password_guess, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	"
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password_gen() + "\"")
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	
elif (difficulty_level == 1):
	authentication_template0 = "\
char reversed_guess[strlen(password_guess) + 1];\n\
	\n\
	for (int i = strlen(password_guess) - 1, i2 = 0; i >= 0; i--, i2++) {\n\
		reversed_guess[i2] = password_guess[i];\n\
	}\n\
	reversed_guess[strlen(password_guess)] = '\\0';\n\
	if (strcmp(reversed_guess, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	"
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + (password_gen())[::-1] + "\"")
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	
elif (difficulty_level == 2):
	authentication_template0 = "\
int len = strlen(password_guess);\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= {{XOR_BYTE}};\n\
	}\n\
	\n\
	char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	\n\
    char hex_guess[len * 2 + 1];\n\
    memset(hex_guess, 0, (len * 2 + 1)*sizeof(char));\n\
    int i2 = 0;\n\
    for (int i = 0; i < len; i++) {\n\
        hex_guess[i2] = hexes[password_guess[i] >> 4];\n\
        i2++;\n\
        hex_guess[i2] = hexes[password_guess[i] & 15];\n\
        i2++;\n\
    }\n\
	\n\
	if (strcmp(hex_guess, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	xor_byte = random.randint(0, 127)
	for n in range(0, len(password1)):
		password2 += format((ord(password1[n]) ^ xor_byte), "02x")
	
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password2 + "\"")
	authentication_final0 = authentication_final0.replace("{{XOR_BYTE}}", str(xor_byte))
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	
elif (difficulty_level == 3):
	authentication_template0 = "\
int len = strlen(password_guess);\n\
    int xor_bytes[] = { {{XOR_BYTES}} };\n\
	for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= xor_bytes[i];\n\
	}\n\
	\n\
	char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	\n\
    char hex_guess[len * 2 + 1];\n\
    memset(hex_guess, 0, (len * 2 + 1)*sizeof(char));\n\
    int i2 = 0;\n\
    for (int i = 0; i < len; i++) {\n\
        hex_guess[i2] = hexes[password_guess[i] >> 4];\n\
        i2++;\n\
        hex_guess[i2] = hexes[password_guess[i] & 15];\n\
        i2++;\n\
    }\n\
	\n\
	if (strcmp(hex_guess, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	xor_bytes = []
	for n in range(0, len(password1)):
		xor_bytes.append(random.randint(0, 127))
	for n in range(0, len(password1)):
		password2 += format((ord(password1[n]) ^ xor_bytes[n]), "02x")
	for n in range(0, len(password1)):
		xor_bytes[n] = str(xor_bytes[n])

	xor_bytes_array = ", ".join(xor_bytes)
	
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password2 + "\"")
	authentication_final0 = authentication_final0.replace("{{XOR_BYTES}}", xor_bytes_array)
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	
elif (difficulty_level == 4):
	authentication_template0 = "\
int len = strlen(password_guess);\n\
    int xor_bytes[] = { {{XOR_BYTES}} };\n\
	int add_bytes[] = { {{ADD_BYTES}} };\n\
	for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= xor_bytes[i];\n\
		password_guess[i] = (password_guess[i] + add_bytes[i]) % 128;\n\
	}\n\
	\n\
	char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	\n\
    char hex_guess[len * 2 + 1];\n\
    memset(hex_guess, 0, (len * 2 + 1)*sizeof(char));\n\
    int i2 = 0;\n\
    for (int i = 0; i < len; i++) {\n\
        hex_guess[i2] = hexes[password_guess[i] >> 4];\n\
        i2++;\n\
        hex_guess[i2] = hexes[password_guess[i] & 15];\n\
        i2++;\n\
    }\n\
	\n\
	if (strcmp(hex_guess, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	xor_bytes = []
	add_bytes = []
	for n in range(0, len(password1)):
		xor_bytes.append(random.randint(0, 127))
	for n in range(0, len(password1)):
		add_bytes.append(random.randint(0, 127))
	for n in range(0, len(password1)):
		password2 += format((((ord(password1[n]) ^ xor_bytes[n]) + add_bytes[n]) % 128), "02x")
	for n in range(0, len(password1)):
		xor_bytes[n] = str(xor_bytes[n])
	for n in range(0, len(password1)):
		add_bytes[n] = str(add_bytes[n])	

	xor_bytes_array = ", ".join(xor_bytes)
	add_bytes_array = ", ".join(add_bytes)
	
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password2 + "\"")
	authentication_final0 = authentication_final0.replace("{{XOR_BYTES}}", xor_bytes_array)
	authentication_final0 = authentication_final0.replace("{{ADD_BYTES}}", add_bytes_array)
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	
elif (difficulty_level == 5):
	authentication_template0 = "\
int len = strlen(password_guess);\n\
    char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	\n\
    char password_guess2[len * 2 + 1];\n\
    memset(password_guess2, 0, (len * 2 + 1)*sizeof(char));\n\
    int i2 = 0;\n\
    for (int i = 0; i < len; i++) {\n\
        password_guess2[i2] = hexes[password_guess[i] >> 4];\n\
        i2++;\n\
        password_guess2[i2] = hexes[password_guess[i] & 15];\n\
        i2++;\n\
    }\n\
    \n\
    int len2 = strlen(password_guess2);\n\
	char password_guess3[len2 * 8 + 1];\n\
    memset(password_guess3, 0, (len2 * 8 + 1)*sizeof(char));\n\
    \n\
    int i = 0;\n\
    for (int n = 0; n < len2; n++) {\n\
        password_guess3[i] = (password_guess2[n] >> 7) + 48;\n\
        i++;\n\
        \n\
        for (int n2 = 2; n2 <= 8; n2++) {\n\
            password_guess3[i] = ((password_guess2[n] >> (8 - n2)) & 1) + 48;\n\
            i++;\n\
        }\n\
    }\n\
    \n\
	char password_guess4[strlen(password_guess3) + 1];\n\
	memset(password_guess4, 0, (strlen(password_guess3) + 1)*sizeof(char));\n\
	for(int i = 0; i < (strlen(password_guess3)); i++) {\n\
		if (password_guess3[i] == '1') {\n\
			password_guess4[i] = 'a';\n\
		} else if (password_guess3[i] == '0') {\n\
			password_guess4[i] = 'b';\n\
		}\n\
	}\n\
	\n\
	if (strcmp(password_guess4, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	
	for n in range(0, len(password1)):
		password2 += format(ord(password1[n]), "02x")
			
	password3 = ""
	for n in range(0, len(password2)):
		password3 += format(ord(password2[n]), '008b')
			
	password4 = password3.replace("1", "a")
	password4 = password4.replace("0", "b")
	
	
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password4 + "\"")
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	
elif (difficulty_level == 6):
	authentication_template0 = "\
int len = strlen(password_guess);\n\
    char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	\n\
    char password_guess2[len * 2 + 1];\n\
    memset(password_guess2, 0, (len * 2 + 1)*sizeof(char));\n\
    int i2 = 0;\n\
    for (int i = 0; i < len; i++) {\n\
        password_guess2[i2] = hexes[password_guess[i] >> 4];\n\
        i2++;\n\
        password_guess2[i2] = hexes[password_guess[i] & 15];\n\
        i2++;\n\
    }\n\
    \n\
	char password_guess3[strlen(password_guess2) * 8 + 1];\n\
    memset(password_guess3, 0, (strlen(password_guess2) * 8 + 1)*sizeof(char));\n\
    \n\
    int i = 0;\n\
    for (int n = 0; n < strlen(password_guess2); n++) {\n\
        password_guess3[i] = (password_guess2[n] >> 7) + 48;\n\
        i++;\n\
        \n\
        for (int n2 = 2; n2 <= 8; n2++) {\n\
            password_guess3[i] = ((password_guess2[n] >> (8 - n2)) & 1) + 48;\n\
            i++;\n\
        }\n\
    }\n\
    \n\
	char password_guess4[strlen(password_guess3) + 1];\n\
	memset(password_guess4, 0, (strlen(password_guess3) + 1)*sizeof(char));\n\
	for(int i = 0; i < (strlen(password_guess3)); i++) {\n\
		if (password_guess3[i] == '1') {\n\
			password_guess4[i] = 'a';\n\
		} else if (password_guess3[i] == '0') {\n\
			password_guess4[i] = 'b';\n\
		}\n\
	}\n\
    \n\
	char *password_guess5 = abCompress(password_guess4, 'b', 'c', 'd', 'e');\n\
	char *password_guess6 = abCompress(password_guess5, 'a', 'f', 'g', 'h');\n\
	\n\
	if (strcmp(password_guess6, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	free(password_guess5);\n\
	free(password_guess6);\n\
	"
	
	password1 = password_gen()
	password2 = ""
	
	for n in range(0, len(password1)):
		password2 += format(ord(password1[n]), "02x")
			
	password3 = ""
	for n in range(0, len(password2)):
		password3 += format(ord(password2[n]), '008b')
			
	password4 = password3.replace("1", "a")
	password4 = password4.replace("0", "b")
	password4 = password4.replace("bbbb", "c")
	password4 = password4.replace("bbb", "d")
	password4 = password4.replace("bb", "e")
	password4 = password4.replace("aaaa", "f")
	password4 = password4.replace("aaa", "g")
	password4 = password4.replace("aa", "h")
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password4 + "\"")
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	c_source_final = c_source_final.replace("#include <stdbool.h>\n", "#include <stdbool.h>\n#include <stdlib.h>\n\nchar* abCompress(char s1[], char detect_char, char replace_char1, char replace_char2, char replace_char3);\n\n")
	c_source_final = c_source_final.replace("return 0;\n}", ab_compress)
	
elif (difficulty_level == 7):
	authentication_template0 = "\
int len = strlen(password_guess);\n\
for(int i = 0; i < len; i++) {\n\
		if (password_guess[i] < 25) {\n\
			if (password_guess[i] < 15) {\n\
				password_guess[i] ^= 10;\n\
			} else if (password_guess[i] < 20) {\n\
				password_guess[i] = (password_guess[i] + 150) % 128;\n\
			} else {\n\
				password_guess[i] ^= 22;\n\
			}\n\
		} else if (password_guess[i] < 50) {\n\
			if (password_guess[i] < 30) {\n\
				password_guess[i] = (password_guess[i] + 122) % 128;\n\
			} else if (password_guess[i] < 40) {\n\
				password_guess[i] ^= 120;\n\
			} else {\n\
				password_guess[i] = (password_guess[i] + 155) % 128;\n\
			}\n\
		} else if (password_guess[i] < 75) {\n\
			if (password_guess[i] < 55) {\n\
				password_guess[i] ^= 90;\n\
			} else if (password_guess[i] < 65) {\n\
				password_guess[i] = (password_guess[i] + 140) % 128;\n\
			} else {\n\
				password_guess[i] = (password_guess[i] + 165) % 128;\n\
			}\n\
		} else if (password_guess[i] < 100) {\n\
			if (password_guess[i] < 80) {\n\
				password_guess[i] ^= 77;\n\
			} else if (password_guess[i] < 90) {\n\
				password_guess[i] = (password_guess[i] + 129) % 128;\n\
				} else {\n\
				password_guess[i] ^= 27;\n\
			}\n\
		} else if (password_guess[i] < 125) {\n\
			if (password_guess[i] < 110) {\n\
				password_guess[i] ^= 30;\n\
			} else if (password_guess[i] < 118) {\n\
				password_guess[i] ^= 40;\n\
			} else {\n\
				password_guess[i] ^= 50;\n\
			}\n\
		} else {\n\
			password_guess[i] = ((password_guess[i] ^ 66) + 195) % 128;\n\
		}\n\
	}\n\
	\n\
	char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	\n\
    char hex_guess[len * 2 + 1];\n\
    memset(hex_guess, 0, (len * 2 + 1)*sizeof(char));\n\
    int i2 = 0;\n\
    for (int i = 0; i < len; i++) {\n\
        hex_guess[i2] = hexes[password_guess[i] >> 4];\n\
        i2++;\n\
        hex_guess[i2] = hexes[password_guess[i] & 15];\n\
        i2++;\n\
    }\n\
	\n\
	if (strcmp(hex_guess, {{PASSWORD}}) == 0) {\n\
		authenticated = 1;\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	
	pass_bytes = []
	for n in range(0, len(password1)):
		pass_bytes.append(ord(password1[n]))

	for i in range(0, len(pass_bytes)):
		if (pass_bytes[i] < 25):
			if (pass_bytes[i] < 15):
				pass_bytes[i] ^= 10;
			elif (pass_bytes[i] < 20):
				pass_bytes[i] = (pass_bytes[i] + 150) % 128;
			else:
				pass_bytes[i] ^= 22;
			
		elif (pass_bytes[i] < 50):
			if (pass_bytes[i] < 30):
				pass_bytes[i] = (pass_bytes[i] + 122) % 128;
			elif (pass_bytes[i] < 40):
				pass_bytes[i] ^= 120;
			else:
				pass_bytes[i] = (pass_bytes[i] + 155) % 128;
			
		elif (pass_bytes[i] < 75):
			if (pass_bytes[i] < 55):
				pass_bytes[i] ^= 90;
			elif (pass_bytes[i] < 65):
				pass_bytes[i] = (pass_bytes[i] + 140) % 128;
			else:
				pass_bytes[i] = (pass_bytes[i] + 165) % 128;
			
		elif (pass_bytes[i] < 100):
			if (pass_bytes[i] < 80):
				pass_bytes[i] ^= 77;
			elif (pass_bytes[i] < 90):
				pass_bytes[i] = (pass_bytes[i] + 129) % 128;	
			else:
				pass_bytes[i] ^= 27;
			
		elif (pass_bytes[i] < 125):
			if (pass_bytes[i] < 110):
				pass_bytes[i] ^= 30;
			elif (pass_bytes[i] < 118):
				pass_bytes[i] ^= 40;
			else:
				pass_bytes[i] ^= 50;
			
		else:
			pass_bytes[i] = ((pass_bytes[i] ^ 66) + 195) % 128;

	password2 = ""
	for n in range(0, len(pass_bytes)):
		password2 += format(pass_bytes[n], "02x")
	
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password2 + "\"")
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	
elif (difficulty_level == 8):
	authentication_template0 = "\
int len = strlen(password_guess);\n\
    char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	\n\
    char hex_guess1[len * 2 + 1];\n\
    memset(hex_guess1, 0, (len * 2 + 1)*sizeof(char));\n\
    int i2 = 0;\n\
    for (int i = 0; i < len; i++) {\n\
        hex_guess1[i2] = hexes[password_guess[i] >> 4];\n\
        i2++;\n\
        hex_guess1[i2] = hexes[password_guess[i] & 15];\n\
        i2++;\n\
    }\n\
	\n\
	if (strcmp(hex_guess1, {{PASSWORD1}}) == 0) {\n\
		\n\
		int server_fd, new_socket;\n\
		ssize_t valread;\n\
		struct sockaddr_in address;\n\
		int opt = 1;\n\
		socklen_t addrlen = sizeof(address);\n\
		char password_guess2[64] = { 0 };\n\
		\n\
		if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {\n\
			perror(\"socket failed\");\n\
			exit(EXIT_FAILURE);\n\
		}\n\
		\n\
		if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {\n\
			perror(\"setsockopt\");\n\
			exit(EXIT_FAILURE);\n\
		}\n\
		address.sin_family = AF_INET;\n\
		address.sin_addr.s_addr = INADDR_ANY;\n\
		address.sin_port = htons(25535);\n\
		\n\
		if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {\n\
			perror(\"bind failed\");\n\
			exit(EXIT_FAILURE);\n\
		}\n\
		\n\
		printf(\"I'm listening...\\n\");\n\
		if (listen(server_fd, 3) < 0) {\n\
			perror(\"listen\");\n\
			exit(EXIT_FAILURE);\n\
		}\n\
		\n\
		if ((new_socket = accept(server_fd, (struct sockaddr*)&address, &addrlen)) < 0) {\n\
			perror(\"accept\");\n\
			exit(EXIT_FAILURE);\n\
		}\n\
		\n\
		valread = read(new_socket, password_guess2, 64 - 1);\n\
		\n\
		close(new_socket);\n\
		close(server_fd);\n\
		\n\
		int len = strlen(password_guess);\n\
		int len2 = strlen(password_guess2);\n\
		\n\
		for(int i = 0, i2 = 0; (i < len) && (i2 < len2); i++, i2++) {\n\
			password_guess2[i2] ^= password_guess[i];\n\
		}\n\
		\n\
		char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	    \n\
        char hex_guess2[strlen(password_guess2) * 2 + 1];\n\
        memset(hex_guess2, 0, (strlen(password_guess2) * 2 + 1)*sizeof(char));\n\
        int i2 = 0;\n\
        for (int i = 0; i < strlen(password_guess2); i++) {\n\
            hex_guess2[i2] = hexes[password_guess2[i] >> 4];\n\
            i2++;\n\
            hex_guess2[i2] = hexes[password_guess2[i] & 15];\n\
            i2++;\n\
        }\n\
		\n\
		if (strcmp(hex_guess2, {{PASSWORD2}}) == 0) {\n\
			authenticated = 1;\n\
		}\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	for n in range(0, len(password1)):
		password2 += format(ord(password1[n]), "02x")
		
	password1_2 = password_gen()
	password2_2 = ""
	i = 0
	i2 = 0
	while (i < len(password1) and i2 < len(password1_2)):
		password2_2 += chr(ord(password1_2[i2]) ^ ord(password1[i]))
		i += 1
		i2 += 1
	password3_2 = ""
	for n in range(0, len(password2_2)):
		password3_2 += format(ord(password2_2[n]), "02x")
	
	authentication_final0 = authentication_template0.replace("{{PASSWORD1}}", "\"" + password2 + "\"")
	authentication_final0 = authentication_final0.replace("{{PASSWORD2}}", "\"" + password3_2 + "\"")
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	c_source_final = c_source_final.replace("#include <stdbool.h>\n", "#include <stdbool.h>\n#include <stdlib.h>\n#include <netinet/in.h>\n#include <sys/socket.h>\n#include <unistd.h>\n\n")

elif (difficulty_level == 9):
	authentication_template0 = "\
int len = 0;\n\
	for(int i = 0; password_guess[i] != '\\0'; i++) {\n\
		len++;\n\
	}\n\
	\n\
    int s_box[] = { {{S_BOX}} };\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] = s_box[password_guess[i]];\n\
	}\n\
	\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] = ((password_guess[i] & 1) << 7) ^ ((password_guess[i] & 2) << 5) ^ ((password_guess[i] & 4) << 3) ^ ((password_guess[i] & 8) << 1) ^ ((password_guess[i] & 16) >> 1) ^ ((password_guess[i] & 32) >> 3) ^ ((password_guess[i] & 64) >> 5) ^ ((password_guess[i] & 128) >> 7);\n\
	}\n\
	\n\
	int xor_bytes[] = { {{XOR_BYTES}} };\n\
	for(int i = 0, i2 = len - 1; i < len; i++, i2--) {\n\
		password_guess[i] ^= xor_bytes[i2];\n\
	}\n\
	\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= xor_bytes[i];\n\
	}\n\
	\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] = ((password_guess[i] & 1) << 7) ^ ((password_guess[i] & 2) << 5) ^ ((password_guess[i] & 4) << 3) ^ ((password_guess[i] & 8) << 1) ^ ((password_guess[i] & 16) >> 1) ^ ((password_guess[i] & 32) >> 3) ^ ((password_guess[i] & 64) >> 5) ^ ((password_guess[i] & 128) >> 7);\n\
	}\n\
	\n\
	int len2 = len * 2;\n\
	char hex_guess[len2 + 1];\n\
	memset(hex_guess, 0, (len2 + 1)*sizeof(char));\n\
    char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	int i2 = 0;\n\
	for (int i = 0; i < len; i++) {\n\
		hex_guess[i2] = hexes[(unsigned char)password_guess[i] >> 4];\n\
		i2++;\n\
		hex_guess[i2] = hexes[(unsigned char)password_guess[i] & 15];\n\
		i2++;\n\
	}\n\
	\n\
    for (int i = 0; i < len2; i++) {\n\
        if (hex_guess[i] == '0') {\n\
            hex_guess[i] = 'f';\n\
        } else if (hex_guess[i] == '1') {\n\
            hex_guess[i] = 'e';\n\
        } else if (hex_guess[i] == '2') {\n\
            hex_guess[i] = 'd';\n\
        } else if (hex_guess[i] == '3') {\n\
            hex_guess[i] = 'c';\n\
        } else if (hex_guess[i] == '4') {\n\
            hex_guess[i] = 'b';\n\
        } else if (hex_guess[i] == '5') {\n\
            hex_guess[i] = 'a';\n\
        } else if (hex_guess[i] == '6') {\n\
            hex_guess[i] = '9';\n\
        } else if (hex_guess[i] == '7') {\n\
            hex_guess[i] = '8';\n\
        } else if (hex_guess[i] == '8') {\n\
            hex_guess[i] = '7';\n\
        } else if (hex_guess[i] == '9') {\n\
            hex_guess[i] = '6';\n\
        } else if (hex_guess[i] == 'a') {\n\
            hex_guess[i] = '5';\n\
        } else if (hex_guess[i] == 'b') {\n\
            hex_guess[i] = '4';\n\
        } else if (hex_guess[i] == 'c') {\n\
            hex_guess[i] = '3';\n\
        } else if (hex_guess[i] == 'd') {\n\
            hex_guess[i] = '2';\n\
        } else if (hex_guess[i] == 'e') {\n\
            hex_guess[i] = '1';\n\
        } else if (hex_guess[i] == 'f') {\n\
            hex_guess[i] = '0';\n\
        }\n\
    }\n\
	\n\
	int i = 0;\n\
	char password[] = {{PASSWORD}};\n\
	while(hex_guess[i] != '\\0' && password[i] != '\\0') {\n\
		if (hex_guess[i] != password[i]) {\n\
			break;\n\
		}\n\
		i++;\n\
	}\n\
	if (hex_guess[i] == '\\0' && password[i] == '\\0') {\n\
		authenticated = 1;\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	s_box = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
          17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
            32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 
            46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 
            60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 
            74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 
            88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 
            102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
              114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127 ]
	random.shuffle(s_box)
	s_box2 = s_box[:]
	for n in range(0, len(s_box)):
			s_box2[n] = str(s_box[n])
	s_box_out = ", ".join(s_box2)

	for c in password1:
		password2 += chr(s_box[ord(c)])

	password3 = ""
	for c in password2:
		password3 += chr(((ord(c) & 1) << 7) ^ ((ord(c) & 2) << 5) ^ ((ord(c) & 4) << 3) ^ ((ord(c) & 8) << 1) ^ ((ord(c) & 16) >> 1) ^ ((ord(c) & 32) >> 3) ^ ((ord(c) & 64) >> 5) ^ ((ord(c) & 128) >> 7))

	xor_bytes = []
	for n in range(0, len(password3)):
		xor_bytes.append(random.randint(0, 127))  
	xor_bytes2 = xor_bytes[:]
	for n in range(0, len(xor_bytes)):
			xor_bytes2[n] = str(xor_bytes[n])
	xor_bytes_out = ", ".join(xor_bytes2)

	xor_bytes = xor_bytes[::-1]
	password4 = ""
	for n in range(0, len(password3)):
		password4 += chr(ord(password3[n]) ^ xor_bytes[n])

	xor_bytes = xor_bytes[::-1]
	password5 = ""
	for n in range(0, len(password4)):
		password5 += chr(ord(password4[n]) ^ xor_bytes[n])

	password6 = ""
	for c in password5:
		password6 += chr(((ord(c) & 1) << 7) ^ ((ord(c) & 2) << 5) ^ ((ord(c) & 4) << 3) ^ ((ord(c) & 8) << 1) ^ ((ord(c) & 16) >> 1) ^ ((ord(c) & 32) >> 3) ^ ((ord(c) & 64) >> 5) ^ ((ord(c) & 128) >> 7))

	password7 = ""
	for n in range(0, len(password6)):
			password7 += format((ord(password6[n])), "02x")

	hex_flip = { '0': 'f', '1': 'e', '2': 'd', '3': 'c', '4': 'b', '5': 'a', '6': '9', '7': '8', '8': '7', '9': '6', 'a': '5', 'b': '4', 'c': '3', 'd': '2', 'e': '1', 'f': '0' }
	password8 = ""
	for c in password7:
		password8 += hex_flip[c]
	
	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password8 + "\"")
	authentication_final0 = authentication_final0.replace("{{XOR_BYTES}}", xor_bytes_out)
	authentication_final0 = authentication_final0.replace("{{S_BOX}}", s_box_out)	
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	

elif (difficulty_level == 10):
	authentication_template0 = "\
int len = 0;\n\
	for(int i = 0; password_guess[i] != '\\0'; i++) {\n\
		len++;\n\
	}\n\
	\n\
    int s_box[] = { {{S_BOX}} };\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] = s_box[password_guess[i]];\n\
	}\n\
	\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] = ((password_guess[i] & 1) << 7) ^ ((password_guess[i] & 2) << 5) ^ ((password_guess[i] & 4) << 3) ^ ((password_guess[i] & 8) << 1) ^ ((password_guess[i] & 16) >> 1) ^ ((password_guess[i] & 32) >> 3) ^ ((password_guess[i] & 64) >> 5) ^ ((password_guess[i] & 128) >> 7);\n\
	}\n\
	\n\
	int xor_bytes[] = { {{XOR_BYTES}} };\n\
	for(int i = 0, i2 = len - 1; i < len; i++, i2--) {\n\
		password_guess[i] ^= xor_bytes[i2];\n\
	}\n\
	for (int i = 0; i < len; i++) {\n\
		password_guess[i] = (((unsigned char)password_guess[i] & 15) << 4) ^ ((unsigned char)password_guess[i] >> 4);\n\
	}\n\
	\n\
	int add_nybbles[] = { {{ADD_NYBBLES}} };\n\
    for (int i = 0, n = 0; i < len; i++, n += 2) {\n\
		password_guess[i] = (((((unsigned char)password_guess[i] >> 4) + add_nybbles[n]) % 16) << 4) ^ (((((unsigned char)password_guess[i] & 15) + add_nybbles[n+1]) % 16));\n\
	}\n\
	\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= xor_bytes[i];\n\
	}\n\
	\n\
    for(int i = 0; i < len; i++) {\n\
		password_guess[i] = ((password_guess[i] & 1) << 7) ^ ((password_guess[i] & 2) << 5) ^ ((password_guess[i] & 4) << 3) ^ ((password_guess[i] & 8) << 1) ^ ((password_guess[i] & 16) >> 1) ^ ((password_guess[i] & 32) >> 3) ^ ((password_guess[i] & 64) >> 5) ^ ((password_guess[i] & 128) >> 7);\n\
	}\n\
	\n\
	int len2 = len * 2;\n\
	char hex_guess[len2 + 1];\n\
	memset(hex_guess, 0, (len2 + 1)*sizeof(char));\n\
    char hexes[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };\n\
	int i2 = 0;\n\
	for (int i = 0; i < len; i++) {\n\
		hex_guess[i2] = hexes[(unsigned char)password_guess[i] >> 4];\n\
		i2++;\n\
		hex_guess[i2] = hexes[(unsigned char)password_guess[i] & 15];\n\
		i2++;\n\
	}\n\
	\n\
    for (int i = 0; i < len2; i++) {\n\
        if (hex_guess[i] == '0') {\n\
            hex_guess[i] = 'f';\n\
        } else if (hex_guess[i] == '1') {\n\
            hex_guess[i] = 'e';\n\
        } else if (hex_guess[i] == '2') {\n\
            hex_guess[i] = 'd';\n\
        } else if (hex_guess[i] == '3') {\n\
            hex_guess[i] = 'c';\n\
        } else if (hex_guess[i] == '4') {\n\
            hex_guess[i] = 'b';\n\
        } else if (hex_guess[i] == '5') {\n\
            hex_guess[i] = 'a';\n\
        } else if (hex_guess[i] == '6') {\n\
            hex_guess[i] = '9';\n\
        } else if (hex_guess[i] == '7') {\n\
            hex_guess[i] = '8';\n\
        } else if (hex_guess[i] == '8') {\n\
            hex_guess[i] = '7';\n\
        } else if (hex_guess[i] == '9') {\n\
            hex_guess[i] = '6';\n\
        } else if (hex_guess[i] == 'a') {\n\
            hex_guess[i] = '5';\n\
        } else if (hex_guess[i] == 'b') {\n\
            hex_guess[i] = '4';\n\
        } else if (hex_guess[i] == 'c') {\n\
            hex_guess[i] = '3';\n\
        } else if (hex_guess[i] == 'd') {\n\
            hex_guess[i] = '2';\n\
        } else if (hex_guess[i] == 'e') {\n\
            hex_guess[i] = '1';\n\
        } else if (hex_guess[i] == 'f') {\n\
            hex_guess[i] = '0';\n\
        }\n\
    }\n\
	\n\
	char password_guess3[strlen(hex_guess) * 8 + 1];\n\
    memset(password_guess3, 0, (strlen(hex_guess) * 8 + 1)*sizeof(char));\n\
    \n\
    int i = 0;\n\
    for (int n = 0; n < strlen(hex_guess); n++) {\n\
        password_guess3[i] = (hex_guess[n] >> 7) + 48;\n\
        i++;\n\
        \n\
        for (int n2 = 2; n2 <= 8; n2++) {\n\
            password_guess3[i] = ((hex_guess[n] >> (8 - n2)) & 1) + 48;\n\
            i++;\n\
        }\n\
    }\n\
	\n\
	char password_guess4[strlen(password_guess3) + 1];\n\
	memset(password_guess4, 0, (strlen(password_guess3) + 1)*sizeof(char));\n\
	for(int i = 0; i < (strlen(password_guess3)); i++) {\n\
		if (password_guess3[i] == '1') {\n\
			password_guess4[i] = 'a';\n\
		} else if (password_guess3[i] == '0') {\n\
			password_guess4[i] = 'b';\n\
		}\n\
	}\n\
    \n\
	char *password_guess5 = abCompress(password_guess4, 'b', 'c', 'd', 'e');\n\
	char *password_guess6 = abCompress(password_guess5, 'a', 'f', 'g', 'h');\n\
	\n\
	i = 0;\n\
	char password[] = {{PASSWORD}};\n\
	while(password_guess6[i] != '\\0' && password[i] != '\\0') {\n\
		if (password_guess6[i] != password[i]) {\n\
			break;\n\
		}\n\
		i++;\n\
	}\n\
	if (password_guess6[i] == '\\0' && password[i] == '\\0') {\n\
		authenticated = 1;\n\
	}\n\
	"
	
	password1 = password_gen()
	password2 = ""
	s_box = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
          17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
            32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 
            46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 
            60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 
            74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 
            88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 
            102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
              114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127 ]
	random.shuffle(s_box)
	s_box2 = s_box[:]
	for n in range(0, len(s_box)):
			s_box2[n] = str(s_box[n])
	s_box_out = ", ".join(s_box2)

	for c in password1:
		password2 += chr(s_box[ord(c)])

	password3 = ""
	for c in password2:
		password3 += chr(((ord(c) & 1) << 7) ^ ((ord(c) & 2) << 5) ^ ((ord(c) & 4) << 3) ^ ((ord(c) & 8) << 1) ^ ((ord(c) & 16) >> 1) ^ ((ord(c) & 32) >> 3) ^ ((ord(c) & 64) >> 5) ^ ((ord(c) & 128) >> 7))

	xor_bytes = []
	for n in range(0, len(password3)):
		xor_bytes.append(random.randint(0, 127))  
	xor_bytes2 = xor_bytes[:]
	for n in range(0, len(xor_bytes)):
			xor_bytes2[n] = str(xor_bytes[n])
	xor_bytes_out = ", ".join(xor_bytes2)

	xor_bytes = xor_bytes[::-1]
	password4 = ""
	for n in range(0, len(password3)):
		password4 += chr(ord(password3[n]) ^ xor_bytes[n])

	password5 = ""
	for c in password4:
		password5 += chr((((ord(c) & 15) << 4) ^ (ord(c) >> 4)))

	add_nybbles = []
	for n in range(0, len(password5) * 2):
		add_nybbles.append(random.randint(0, 15))  
	add_nybbles2 = add_nybbles[:]
	for n in range(0, len(add_nybbles)):
		add_nybbles2[n] = str(add_nybbles[n])
	add_nybbles_out = ", ".join(add_nybbles2)

	n = 0
	password6 = ""
	for c in password5:
		password6 += chr(((((ord(c) >> 4) + add_nybbles[n]) % 16) << 4) ^ (((ord(c) & 15) + add_nybbles[n+1]) % 16))
		n += 2

	xor_bytes = xor_bytes[::-1]
	password7 = ""
	for n in range(0, len(password6)):
		password7 += chr(ord(password6[n]) ^ xor_bytes[n])

	password8 = ""
	for c in password7:
		password8 += chr(((ord(c) & 1) << 7) ^ ((ord(c) & 2) << 5) ^ ((ord(c) & 4) << 3) ^ ((ord(c) & 8) << 1) ^ ((ord(c) & 16) >> 1) ^ ((ord(c) & 32) >> 3) ^ ((ord(c) & 64) >> 5) ^ ((ord(c) & 128) >> 7))

	password9 = ""
	for n in range(0, len(password8)):
			password9 += format((ord(password8[n])), "02x")

	hex_flip = { '0': 'f', '1': 'e', '2': 'd', '3': 'c', '4': 'b', '5': 'a', '6': '9', '7': '8', '8': '7', '9': '6', 'a': '5', 'b': '4', 'c': '3', 'd': '2', 'e': '1', 'f': '0' }
	password10 = ""
	for c in password9:
		password10 += hex_flip[c]
	
	password11 = ""
	for n in range(0, len(password10)):
		password11 += format(ord(password10[n]), '008b')

	password12 = password11.replace("1", "a")
	password12 = password12.replace("0", "b")
	password12 = password12.replace("bbbb", "c")
	password12 = password12.replace("bbb", "d")
	password12 = password12.replace("bb", "e")
	password12 = password12.replace("aaaa", "f")
	password12 = password12.replace("aaa", "g")
	password12 = password12.replace("aa", "h")

	authentication_final0 = authentication_template0.replace("{{PASSWORD}}", "\"" + password12 + "\"")
	authentication_final0 = authentication_final0.replace("{{XOR_BYTES}}", xor_bytes_out)
	authentication_final0 = authentication_final0.replace("{{ADD_NYBBLES}}", add_nybbles_out)
	authentication_final0 = authentication_final0.replace("{{S_BOX}}", s_box_out)	
	c_source_final = c_source_template.replace("{{AUTHENTICATION}}", authentication_final0)
	c_source_final = c_source_final.replace("#include <stdbool.h>\n", "#include <stdbool.h>\n#include <stdlib.h>\n\nchar* abCompress(char s1[], char detect_char, char replace_char1, char replace_char2, char replace_char3);\n\n")
	c_source_final = c_source_final.replace("return 0;\n}", ab_compress)

else:
	print("This level hasn't been made yet!\n")
	exit()

print("Outputting source code...")
source_file = open(executable_name + ".c", 'w')
source_file.write(c_source_final)
source_file.close()

print("Compiling source code...")
os.system("gcc " + executable_name + ".c -o " + executable_name) #Replace this with the command line C compiler of your choice

#These can be uncommented if the user wishes to avoid temptation of peeking at the C source code files
#Uncommenting them will prompt user before removing the file
#####################################################################
#print("Removing source code file...")
#os.system("rm -i " + executable_name + ".c")
#####################################################################

print("Process complete. Happy cracking! -stringzzz :3")
