# CORA: Crackme Originator Randomizing Automator
# By stringzzz, Ghostwarez Co. :3
#
# Uses prng and input difficulty level to generate a crackme challenge executable
# Doesn't remove the resulting c source code file by default, see end of code for uncommenting this
#
# Start Date: 09-04-2024
# Levels 0-5 Complete Date: 09-05-2024

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
		printf(\"SUCCESS! GOOD JOB!\\n\");\n\
	} else {\n\
		printf(\"FAILURE! TRY AGAIN!\\n\");\n\
	}\n\
	\n\
	return 0;\n\
}\
"	

c_source_final = ""
	
executable_name = input("Enter the name of the executable: ")
difficulty_level = int(input("Enter the difficulty level (0-9): "))

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
	\n\
	for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= {{XOR_BYTE}};\n\
	}\n\
	\n\
	char hex_guess[len * 2 + 1];\n\
	\n\
	for(int i = 0; i < len; i++) {\n\
		sprintf(hex_guess + i*2, \"%02x\", password_guess[i]);\n\
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
	\n\
	int xor_bytes[] = { {{XOR_BYTES}} };\n\
	for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= xor_bytes[i];\n\
	}\n\
	\n\
	char hex_guess[len * 2 + 1];\n\
	\n\
	for(int i = 0; i < len; i++) {\n\
		sprintf(hex_guess + i*2, \"%02x\", password_guess[i]);\n\
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
	\n\
	int xor_bytes[] = { {{XOR_BYTES}} };\n\
	int add_bytes[] = { {{ADD_BYTES}} };\n\
	for(int i = 0; i < len; i++) {\n\
		password_guess[i] ^= xor_bytes[i];\n\
		password_guess[i] = (password_guess[i] + add_bytes[i]) % 128;\n\
	}\n\
	\n\
	char hex_guess[len * 2 + 1];\n\
	\n\
	for(int i = 0; i < len; i++) {\n\
		sprintf(hex_guess + i*2, \"%02x\", password_guess[i]);\n\
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
	char password_guess2[len * 2 + 1];\n\
	\n\
	for(int i = 0; i < len; i++) {\n\
		sprintf(password_guess2 + i*2, \"%02x\", password_guess[i]);\n\
	}\n\
	char password_guess3[len * 8 + 1];\n\
	\n\
	int i = 0;\n\
	for(unsigned int n = 0; n < len * 2; n++) {\n\
		sprintf(password_guess3 + i, \"%d\", password_guess2[n] >> 7);\n\
		i++;\n\
		for (int n2 = 2; n2 <= 8; n2++) {\n\
			sprintf(password_guess3 + i, \"%d\", (password_guess2[n] >> (8 - n2)) & 1);\n\
			i++;\n\
		}\n\
	}\n\
	char password_guess4[len * 8 + 1];\n\
	for(int i = 0; i < (len * 8 + 1); i++) {\n\
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
	char password_guess2[len * 2 + 1];\n\
	\n\
	for(int i = 0; i < len; i++) {\n\
		sprintf(password_guess2 + i*2, \"%02x\", password_guess[i]);\n\
	}\n\
	char password_guess3[len * 8 + 1];\n\
	\n\
	int i = 0;\n\
	for(unsigned int n = 0; n < len * 2; n++) {\n\
		sprintf(password_guess3 + i, \"%d\", password_guess2[n] >> 7);\n\
		i++;\n\
		for (int n2 = 2; n2 <= 8; n2++) {\n\
			sprintf(password_guess3 + i, \"%d\", (password_guess2[n] >> (8 - n2)) & 1);\n\
			i++;\n\
		}\n\
	}\n\
	char password_guess4[len * 8 + 1];\n\
	for(int i = 0; i < (len * 8 + 1); i++) {\n\
		if (password_guess3[i] == '1') {\n\
			password_guess4[i] = 'a';\n\
		} else if (password_guess3[i] == '0') {\n\
			password_guess4[i] = 'b';\n\
		}\n\
	}\n\
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
	c_source_final = c_source_final.replace("return 0;\n}", "return 0;\n}\n\
char* abCompress(char s1[], char detect_char, char replace_char1, char replace_char2, char replace_char3) {\n\
	\n\
	char s2[strlen(s1) + 1];\n\
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
	")
	
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
