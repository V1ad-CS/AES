from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

choose = input("encrypt/decrypt: ")

if choose == "encrypt":
    file = input('Choose your file: ')  
    with open(file, 'rb') as open_file:
        file_data = open_file.read() 

    n = 16
    aes_key = get_random_bytes(n)  
    hmac_key = get_random_bytes(n)  

    cipher = AES.new(aes_key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(file_data)
    nonce = cipher.nonce  
    nonce_length = len(nonce)

    hmac_obj = HMAC.new(hmac_key, digestmod=SHA256)
    hmac_obj.update(nonce + ciphertext)
    tag = hmac_obj.digest()

    path_parts = file.split("\\")[:-1] 
    file_format = file.split('.')[-1]
    outfile = "\\".join(path_parts) + "\\" + file_format + ".encrypted.bin"

    with open(outfile, "wb") as f:
        f.write(aes_key)
        f.write(hmac_key)
        f.write(nonce_length.to_bytes(4, 'big'))
        f.write(nonce)
        f.write(len(ciphertext).to_bytes(8, 'big'))  
        f.write(ciphertext)
        f.write(tag)

    print(f"File encrypted and saved as: {outfile}")

elif choose == 'decrypt':
    file = input('Choose your encrypted file: ') 
    with open(file, 'rb') as open_file:
        aes_key = open_file.read(16)   
        hmac_key = open_file.read(16)  

        nonce_length = int.from_bytes(open_file.read(4), 'big') 
        nonce = open_file.read(nonce_length)

        ciphertext_length = int.from_bytes(open_file.read(8), 'big')
        ciphertext = open_file.read(ciphertext_length)

        tag = open_file.read(32)  

    hmac_obj = HMAC.new(hmac_key, digestmod=SHA256)
    hmac_obj.update(nonce + ciphertext)
    try:
        hmac_obj.verify(tag)
        print("HMAC tag verification successful!")
    except ValueError:
        print("HMAC tag verification failed!")
        exit()

    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    path_parts = file.split("\\")[:-1]
    file_format = file.split('\\').pop(-1)
    outfile = "\\".join(path_parts) + "\\decrypted_file." + file_format.split('.').pop(0)
    with open(outfile, 'wb') as f:
        f.write(plaintext)

    print(f"File successfully decrypted and saved to: {outfile}")

else:
    print("Incorrect, try again!")
