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

try:
    Bob.verify_mex(signature=signed_m, message=encrypted_m, user='Alice')
    print('Signature verified by Bob\n')
    decryped_m = Bob.decrypt_mex(encrypted_m)
    print('Message decrypted by Bob:\n%s\n' % decryped_m)
except Exception as e:
    print('\nProtocol not completed!\n\n%s' % e)