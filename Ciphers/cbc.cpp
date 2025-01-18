/*
 * CBC (Cipher Block Chaining) Mode Encryption
 * --------------------------------------------
 * CBC is a block cipher mode that improves security by chaining blocks together during encryption.
 * Each plaintext block is XORed with the previous ciphertext block before encryption.
 * This ensures that identical plaintext blocks produce different ciphertext blocks, provided
 * a unique initialization vector (IV) is used for each encryption session.
 *
 * However, CBC requires a random and unpredictable IV to be secure, and the IV must be shared
 * with the recipient for decryption. Although CBC is more secure than ECB, it has been largely
 * replaced in many applications by more modern modes like GCM or CTR due to performance and security advantages.
 */

#include <iostream>
#include <vector>
#include <cstring>

// Mock encryption function to simulate block encryption (e.g., AES)
void mockEncryptBlock(const uint8_t* inputBlock, uint8_t* outputBlock, const uint8_t* key, size_t blockSize) {
    for (size_t i = 0; i < blockSize; ++i) {
        outputBlock[i] = inputBlock[i] ^ key[i % blockSize]; // Simple XOR for demonstration
    }
}

// CBC encryption function
std::vector<uint8_t> cbcEncrypt(const std::vector<uint8_t>& plaintext, const std::vector<uint8_t>& key, const std::vector<uint8_t>& iv, size_t blockSize) {
    if (key.size() < blockSize || iv.size() != blockSize) {
        throw std::invalid_argument("Key size must be at least equal to the block size, and IV size must match block size.");
    }

    size_t plaintextSize = plaintext.size();
    size_t paddedSize = ((plaintextSize + blockSize - 1) / blockSize) * blockSize;

    std::vector<uint8_t> paddedPlaintext(paddedSize, 0);
    std::memcpy(paddedPlaintext.data(), plaintext.data(), plaintextSize);

    std::vector<uint8_t> ciphertext(paddedSize);

    std::vector<uint8_t> previousBlock = iv;

    for (size_t i = 0; i < paddedSize; i += blockSize) {
        std::vector<uint8_t> currentBlock(blockSize);

        // XOR plaintext block with the previous ciphertext block (or IV for the first block)
        for (size_t j = 0; j < blockSize; ++j) {
            currentBlock[j] = paddedPlaintext[i + j] ^ previousBlock[j];
        }

        // Encrypt the current block
        mockEncryptBlock(currentBlock.data(), &ciphertext[i], key.data(), blockSize);

        // Update the previous block to the current ciphertext block
        std::memcpy(previousBlock.data(), &ciphertext[i], blockSize);
    }

    return ciphertext;
}

int main() {
    const size_t blockSize = 16; // Example block size (e.g., AES-128 uses 16 bytes)
    std::vector<uint8_t> key = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                                0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F};
    std::vector<uint8_t> iv = {0xFF, 0xEE, 0xDD, 0xCC, 0xBB, 0xAA, 0x99, 0x88,
                               0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11, 0x00};
    std::vector<uint8_t> plaintext = {'T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 't', 'e', 's', 't', '.'};

    std::vector<uint8_t> ciphertext = cbcEncrypt(plaintext, key, iv, blockSize);

    std::cout << "Ciphertext (hex): ";
    for (uint8_t byte : ciphertext) {
        std::cout << std::hex << (int)byte << " ";
    }
    std::cout << std::endl;

    return 0;
}
