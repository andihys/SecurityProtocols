"""
This Python script implements a basic Key Distribution Center (KDC) simulation for secure session key exchange and encrypted communication between users. It leverages the `cryptography` library to perform encryption and decryption using Fernet keys.

Classes:
1. **KeyDistributionCenter (KDC)**:
   - Manages users and their private keys.
   - Generates session keys for secure communication between users.
   - Facilitates the secure exchange of session keys by encrypting them with the private keys of the users involved.

2. **User**:
   - Represents an individual user in the system.
   - Manages private keys for communicating securely with the KDC.
   - Handles session keys for encrypted communication with other users.
   - Provides methods for encrypting and decrypting messages using private and session keys.

Workflow:
1. **Initialization**:
   - A `KeyDistributionCenter` instance (KDC) is created.
   - Two `User` instances (`Alice` and `Bob`) are created and registered with the KDC to receive their private keys.

2. **Session Key Exchange**:
   - Alice initiates a secure session with Bob via the KDC.
   - The KDC generates a session key and encrypts it using the private keys of Alice and Bob.
   - Alice decrypts her message from the KDC to extract the session key and a message for Bob.
   - Bob decrypts his message from Alice to retrieve the session key, enabling both users to communicate securely.

3. **Encrypted Communication**:
   - Alice encrypts a secret message using the session key.
   - Bob decrypts the received message using the same session key.

Key Methods:
- **KDC**:
  - `add_user(user_name)`: Registers a user and generates a private key.
  - `gen_session_key()`: Creates a new session key.
  - `start_session(user_a, user_b)`: Facilitates the session key exchange.

- **User**:
  - Properties `private_key` and `session_key`: Handle the user's private and session keys.
  - `encrypt(mex)` and `decrypt(mex)`: Encrypt and decrypt messages using the private key.
  - `encrypt_s(mex)` and `decrypt_s(mex)`: Encrypt and decrypt messages using the session key.
  - `extract_session_key(mex, key_pos=0)`: Extracts the session key and returns the remaining concatenated message.

Security Considerations:
- The `cryptography` library ensures secure encryption, but this script is intended for educational purposes only and should not be used in production systems.
- The use of the session key enables end-to-end encryption between users, reducing the reliance on the KDC once the session key is distributed.

Example Usage:
- The script demonstrates the secure exchange of a session key between Alice and Bob via the KDC and the subsequent encrypted message communication using the session key.
"""


import os
from cryptography.fernet import Fernet


class KeyDistributionCenter:
    def __init__(self):
        self.archive = {}
        self.session_key = 0
        self.string_separator = b"||"

    def add_user(self, user_name):
        key = Fernet.generate_key()
        self.archive[user_name] = key
        return key

    def gen_session_key(self):
        self.session_key = Fernet.generate_key()

    def concat_message_format(self, a, b):
        return a + self.string_separator + b

    def sec_concat(self, a, b, key):
        cipher = Fernet(key)
        data_concat = self.concat_message_format(a, b)
        data_cipher = cipher.encrypt(data_concat)
        print("Data ciphred %s" % data_cipher)
        return data_cipher

    def start_session(self, user_a, user_b):
        # K_a_kdc(key_Sess, K_b_kdc(A, key_sess))
        self.gen_session_key()
        data_cipher_user_b = self.sec_concat(user_a.encode('utf-8'), self.session_key, self.archive.get(user_b))
        data_cipher_user_a = self.sec_concat(self.session_key, data_cipher_user_b, self.archive.get(user_a))
        return data_cipher_user_a


class User:
    def __init__(self, name=None):
        if name is None:
            self.name = "User" + str(os.urandom(8))
        else:
            self.name = name
        self._privat_key = b""
        self.f = None
        self._session_key = b""
        self.f_s = None
        self.string_separator = b"||"

    @property
    def private_key(self):
        return self._privat_key

    @private_key.setter
    def private_key(self, value):
        try:
            self._privat_key = value
            self.f = Fernet(self._privat_key)
        except Exception:
            raise (ValueError("Value not valid %s" % value))

    @property
    def session_key(self):
        return self._session_key

    @session_key.setter
    def session_key(self, value):
        try:
            self._session_key = value
            self.f_s = Fernet(self._session_key)
        except Exception:
            raise ValueError("Value not valid %s" % value)

    # Encryption con chiave privata con KDC
    def encrypt(self, mex):
        return self.f.encrypt(mex)

    def decrypt(self, mex):
        return self.f.decrypt(mex)

    # Encryption con chiave di sessione
    def encrypt_s(self, mex):
        return self.f_s.encrypt(mex)

    def decrypt_s(self, mex):
        return self.f_s.decrypt(mex)

    # estrae la chiave e ritorna il resto del messaggio concatenato
    def extract_session_key(self, mex, key_pos=0):
        extract = mex.split(self.string_separator)
        if key_pos==0:
            self.session_key = extract[0]
            return extract[1]
        else:
            self.session_key = extract[1]
            return extract[0]

KDC = KeyDistributionCenter()
Alice = User("Alice")
Bob = User("Bob")

Alice.private_key = KDC.add_user(Alice.name)
Bob.private_key = KDC.add_user(Bob.name)

# GET A SESSION KEY

mex_for_a = KDC.start_session(Alice.name, Bob.name)
mex_decrypt = Alice.decrypt(mex_for_a)
mex_for_b = Alice.extract_session_key(mex_decrypt)

mex_decrypt = Bob.decrypt(mex_for_b)
other_usr = Bob.extract_session_key(mex_decrypt, key_pos=1)

print("Now Bob have a session key with: %s" % other_usr)

# START MESSAGE SESSION

mex_a = b"this is a secret message"
mex_a_ENC = Alice.encrypt_s(mex_a)
print("Crypted mex:\nn%s" % mex_a_ENC)

mex_a_DEC = Bob.decrypt_s(mex_a_ENC)
print("Derypted mex:\n%s " % mex_a_DEC)