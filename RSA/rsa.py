"""
This Python script demonstrates the use of asymmetric encryption and digital signatures for secure communication between two users, Alice and Bob. The script leverages the `cryptography` library to implement RSA-based encryption, decryption, message signing, and signature verification.

Class:
1. **User**:
   - Represents a user in the network with their own RSA key pair.
   - Manages public key distribution through a shared database (`db`).
   - Provides methods for:
     - Signing messages with their private key.
     - Verifying message signatures using the sender's public key.
     - Encrypting messages with the recipient's public key.
     - Decrypting messages using their own private key.

Workflow:
1. **Key Generation**:
   - Each user generates an RSA key pair (private and public keys) during initialization.
   - Users exchange their public keys and save them in their local database (`db`).

2. **Secure Communication**:
   - **Step 1**: Alice encrypts a plaintext message with Bob's public key to ensure confidentiality.
   - **Step 2**: Alice signs the encrypted message with her private key to provide authentication and integrity.
   - **Step 3**: Alice sends both the signed message and the encrypted message to Bob.

3. **Message Verification and Decryption**:
   - **Step 1**: Bob verifies the signature on the encrypted message using Alice's public key. This step ensures that the message was indeed sent by Alice and was not tampered with.
   - **Step 2**: If the signature is valid, Bob decrypts the encrypted message using his private key to retrieve the original plaintext.

Key Methods:
- **User**:
  - `get_pbk()`: Retrieves the public key of the user.
  - `save_pbk(usr_pbk: dict)`: Saves a public key from another user into the database.
  - `sign_mex(message)`: Signs a message using the user's private key.
  - `verify_mex(signature, message, user)`: Verifies a message signature using the sender's public key.
  - `encrypt_mex(sent_mex_to, message)`: Encrypts a message using the recipient's public key.
  - `decrypt_mex(ciphertext)`: Decrypts a ciphertext using the user's private key.

Example Usage:
1. **Public Key Exchange**:
   - Alice and Bob exchange public keys to enable encrypted communication.

2. **Message Sending**:
   - Alice encrypts the message for Bob using Bob's public key and signs the encrypted message with her private key.

3. **Message Receiving**:
   - Bob verifies Alice's signature and decrypts the message using his private key.

Security Features:
- **Confidentiality**: Ensured by encrypting messages with the recipient's public key.
- **Authentication**: Achieved through digital signatures.
- **Integrity**: Verified by ensuring the message signature matches the sender's private key.

Example Output:
- Demonstrates the encryption of a plaintext message, signing it, and verifying the signature before decrypting the message.

Important Notes:
- This script is designed for educational purposes and demonstrates the principles of public-key cryptography.
- In production environments, additional safeguards like secure key distribution mechanisms and protection against replay attacks are essential.

"""


from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class User:
    def __init__(self, username):
        self._public_exponent = 65537
        self._key_size = 2048
        self.name = username
        self.private_key = rsa.generate_private_key(
            public_exponent=self._public_exponent,
            key_size=self._key_size
        )
        self.public_key = self.private_key.public_key()
        self.db = {username: self.public_key}

    def get_pbk(self):
        return {self.name: self.public_key}

    def save_pbk(self, usr_pbk: dict):
        self.db.update(usr_pbk)

    def sign_mex(self, message):
        # SIGN MEX FOR AUTHENTICATION WITH MY PRIVATE KEY
        return self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify_mex(self, signature, message, user):
        # VERIFY THE AUTHENTICATION OF MY SIGNATURE ON A MEX WITH MY PUBLIC KEY
        # EVERY USER CAN DO THIS
        try:
            return self.db[user].verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except Exception as e:
            # if the signature is not corret
            print(f"\nInvalid Signature\n")
            raise e

    def encrypt_mex(self, sent_mex_to: str, message):
        # ENCRYPT MEX TO SENT IT TO A SPECIFIC USER
        # FOR RESERVATION WITH THE USER PUBLIC KEY
        return self.db[sent_mex_to].encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )


    def decrypt_mex(self, ciphertext):
        # DECRYPT MEX WITH MY PRIVATE KEY
        return self.private_key.decrypt(
            ciphertext=ciphertext,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

# Users in the network
Alice = User('Alice')
Bob = User('Bob')

# Tips:
# 1. Alice sends his public key to Bob, and Bob does the same
# 2. Alice encrypt the message with Bob's public key and
# encrypts the obtained ciphertext with its private key.
# 3. Bob first verify the signature using Alice's public key and
# then decrypt the message through its private key

# Sharing public keys
Alice.save_pbk(Bob.get_pbk())
Bob.save_pbk(Alice.get_pbk())
# Message
message_plaintext = b'this is my message'
print('Message to sent:\n%s\n' % message_plaintext)
# Alice sent the message
# Encrypt with bob public key
encrypted_m = Alice.encrypt_mex(sent_mex_to='Bob', message=message_plaintext)
print('Message encrypted by Alice for Bob with Bob PBK:\n%s\n' % encrypted_m)
# sign the encrypted mex with her private key
signed_m = Alice.sign_mex(encrypted_m)
print('Message signed by Alice:\n %s \n' % signed_m)

print('\n\t...Alice is sending the ecrypted mex and the signed mex to Bob...\n')

# Bob take the message
# Verify the signature of Alice
# if is not correct the signature the except must be throws
# if is correct now decrypt
try:
    Bob.verify_mex(signature=signed_m, message=encrypted_m, user='Alice')
    print('Signature verified by Bob\n')
    decryped_m = Bob.decrypt_mex(encrypted_m)
    print('Message decrypted by Bob:\n%s\n' % decryped_m)
except Exception as e:
    print('\nProtocol not completed!\n\n%s' % e)