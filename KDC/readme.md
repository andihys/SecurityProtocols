# Key Distribution Center (KDC) and Secure Session Key Exchange

This project implements a basic simulation of a Key Distribution Center (KDC) to facilitate secure session key exchange and encrypted communication between users. It uses the `cryptography` library to perform symmetric encryption and decryption with Fernet keys.

## Features

- **Key Distribution Center (KDC):**
  - Generates and distributes private keys for users.
  - Creates secure session keys for communication between users.
  - Facilitates secure session key exchange.

- **User Class:**
  - Manages private and session keys.
  - Encrypts and decrypts messages using session keys.
  - Signs and verifies messages for authentication.

## How It Works

1. **Initialization:**
   - Users are registered with the KDC and receive private keys.

2. **Session Key Exchange:**
   - The KDC generates a session key.
   - The session key is securely encrypted and distributed to users via their private keys.

3. **Encrypted Communication:**
   - Users encrypt messages using the session key for secure communication.

## Example Workflow

1. **Session Key Generation:**
   - Alice and Bob register with the KDC to receive private keys.
   - Alice requests a session key to communicate with Bob.
   - The KDC generates a session key and encrypts it for both Alice and Bob.

2. **Message Encryption:**
   - Alice encrypts a message using the session key.
   - Bob decrypts the message using the same session key.

3. **Authentication:**
   - Session keys ensure confidentiality and integrity of the messages exchanged.

## Requirements

- Python 3.6+
- `cryptography` library

## Installation

Install the `cryptography` library:

```bash
pip install cryptography
```