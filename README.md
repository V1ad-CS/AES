### **1. User Input and Mode Selection**

- **Prompt:** The program first asks the user whether they want to "encrypt" or "decrypt".  
- **Branching:** Based on the user’s input, the program will either execute the encryption section or the decryption section of the code.


### **2. Encryption Process**

#### **Reading and Preparing the File**

- **File Selection:** The user is prompted to choose a file. The file is then opened in binary mode (`'rb'`), and its contents are read into memory.
  
#### **Key Generation**

- **Random Keys:** Two random keys of 16 bytes (128 bits) each are generated:
  - **AES Key:** Used for the AES encryption.
  - **HMAC Key:** Used to generate the message authentication code.
  
#### **AES Encryption in CTR Mode**

- **Cipher Initialization:**  
  - The AES cipher is created with the randomly generated AES key.
  - It uses CTR mode, which operates by encrypting a counter (or nonce) that is incremented for every block—a common approach for turning a block cipher into a stream cipher.
- **Encryption:**  
  - The file's plaintext is encrypted with this cipher, producing the ciphertext.
  - A nonce is generated and stored as part of the cipher’s state. The nonce is critical in CTR mode since it ensures that the same key produces a different key stream for each encryption session.  
- **Nonce Length:**  
  - The length of the nonce is calculated to ensure it can be properly reconstructed during decryption.

#### **HMAC Tag Calculation**

- **Data Integrity:**  
  - An HMAC (Hash-based Message Authentication Code) is computed using SHA256.  
  - The HMAC object is updated with the concatenation of the nonce and the ciphertext.  
  - The resulting tag will later be used to verify that neither the ciphertext nor the nonce has been tampered with.

#### **Writing the Encrypted File**

- **Output File Construction:**  
  - The path is manipulated (by splitting it on the "\\" character) to create a new file name with an ".encrypted.bin" extension.
- **File Contents:**  
  The output file is built in a structured way to store all necessary components for decryption:
  1. **AES Key (16 bytes)**
  2. **HMAC Key (16 bytes)**
  3. **Nonce Length:** Stored in 4 bytes (big-endian format).
  4. **Nonce:** The value used during AES encryption.
  5. **Ciphertext Length:** Stored in 8 bytes (big-endian format).
  6. **Ciphertext:** The encrypted file data.
  7. **HMAC Tag:** A 32-byte tag generated using SHA256.
- **Notification:**  
  - The program prints a message indicating that the file has been encrypted and saved.

### **3. Decryption Process**

#### **Reading the Encrypted File**

- **Key and Metadata Extraction:**  
  - The file is opened in binary read mode.
  - The program reads the AES key (first 16 bytes) and the HMAC key (next 16 bytes).
  - It then reads 4 bytes to determine the length of the nonce, followed by reading the nonce itself.
  - Next, it reads 8 bytes to determine the length of the ciphertext and then reads the ciphertext.
  - Lastly, it reads the final 32 bytes which represent the HMAC tag.

#### **HMAC Verification**

- **Integrity Check:**  
  - Before attempting decryption, the program re-computes the HMAC (using the stored HMAC key) over the concatenation of the nonce and ciphertext.
  - It then verifies that this computed tag matches the stored tag.
  - **Outcome:**  
    - If the tags match, it indicates that the file has not been tampered with.
    - If the verification fails, the program prints an error message and exits, thus protecting against modifications or corruption.

#### **AES Decryption**

- **Cipher Reconstruction:**  
  - An AES cipher is reconstructed with the retrieved AES key, using the same CTR mode and the same nonce that was stored during encryption.
- **Decryption:**  
  - The ciphertext is decrypted back into plaintext using this cipher.

#### **Writing the Decrypted File**

- **Output Filename Generation:**  
  - The program constructs a new file name, typically prefixed with "decrypted_file.", preserving some part of the original naming convention.
- **Final Output:**  
  - The decrypted plaintext is written to the new output file.
  - A success message is printed to notify the user that decryption was successful.

---

### **4. How the Encryption Model Works**

- **AES in CTR Mode:**  
  - **Mode of Operation:** CTR mode turns a block cipher into a stream cipher by encrypting successive values of a nonce/counter. This mode does not require padding and allows encryption of data of any size.
  - **Security Implication:** The nonce must be unique for every encryption with the same key to prevent key stream reuse, which is properly managed here by generating a random nonce every time.

- **HMAC (Encrypt-then-MAC Paradigm):**  
  - **Purpose:** After encryption, HMAC ensures that any changes to the ciphertext or nonce can be detected. This is known as the Encrypt-then-MAC method.
  - **Process:**  
    - The HMAC is produced using a combination of the nonce and ciphertext.
    - During decryption, the same HMAC process is repeated, and if the resulting MAC does not match, decryption is aborted.
  - **Benefits:**  
    - This ensures both confidentiality (via AES) and integrity/authenticity (via HMAC).
