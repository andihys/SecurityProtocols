# RSA Encryption and Digital Signatures

This project demonstrates the use of RSA encryption and digital signatures to secure communication between two users, Alice and Bob. It uses the `cryptography` library for public-key cryptography.

## Features

- **Asymmetric Key Generation:**
  - Each user generates their own RSA key pair (private and public keys).

- **Public Key Exchange:**
  - Users share their public keys for encryption and signature verification.

- **Message Security:**
  - Messages are encrypted using the recipient's public key for confidentiality.
  - Messages are signed using the sender's private key for authentication and integrity.

## How It Works

1. **Key Generation:**
   - Each user generates a unique RSA key pair during initialization.

2. **Public Key Sharing:**
   - Users exchange public keys to enable secure communication.

3. **Message Signing:**
   - A message is signed with the sender's private key for authentication.

4. **Message Encryption:**
   - The message is encrypted with the recipient's public key for confidentiality.

5. **Verification and Decryption:**
   - The recipient verifies the sender's signature using their public key.
   - The recipient decrypts the message using their private key.

## Example Workflow

1. **Public Key Exchange:**
   - Alice and Bob exchange public keys.

2. **Message Sending:**
   - Alice encrypts the message using Bob's public key.
   - Alice signs the encrypted message with her private key.

3. **Message Receiving:**
   - Bob verifies Alice's signature.
   - Bob decrypts the message using his private key.

## Requirements

- Python 3.6+
- `cryptography` library

## Installation

Install the `cryptography` library:

```bash
pip install cryptography
```