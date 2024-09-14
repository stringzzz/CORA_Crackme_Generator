password1 = "" #Enter the final password from the comparison here
password2 = bytearray.fromhex(password1).decode()
password3 = ""
for n in range(0, len(password2)):
	password3 += chr(ord(password2[n]) ^ XOR) #Replace 'XOR' with the byte being XOR'd by
	
print(password3)
