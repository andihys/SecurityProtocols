/*
 * ECB (Electronic Codebook) Mode Encryption
 * -------------------------------------------
 * ECB is a block cipher mode in which each input block
 * is encrypted independently using the same algorithm and key.
 * This means that identical input blocks produce identical output blocks,
 * making the mode vulnerable to statistical analysis attacks and the
 * detection of patterns in the data.
 * For this reason, ECB is NOT considered secure and should not be used
 * in real-world applications. More secure modes include CBC, GCM, or CTR.
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

// ECB encryption function
std::vector<uint8_t> ecbEncrypt(const std::vector<uint8_t>& plaintext, const std::vector<uint8_t>& key, size_t blockSize) {
    if (key.size() < blockSize) {
        throw std::invalid_argument("Key size must be at least equal to the block size.");
    }

    size_t plaintextSize = plaintext.size();
    size_t paddedSize = ((plaintextSize + blockSize - 1) / blockSize) * blockSize;

    std::vector<uint8_t> paddedPlaintext(paddedSize, 0);
    std::memcpy(paddedPlaintext.data(), plaintext.data(), plaintextSize);

    std::vector<uint8_t> ciphertext(paddedSize);

    for (size_t i = 0; i < paddedSize; i += blockSize) {
        mockEncryptBlock(&paddedPlaintext[i], &ciphertext[i], key.data(), blockSize);
    }

    return ciphertext;
}

int main() {
    const size_t blockSize = 16; // Example block size (e.g., AES-128 uses 16 bytes)
    std::vector<uint8_t> key = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                                0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F};
    std::vector<uint8_t> plaintext = {'T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 't', 'e', 's', 't', '.'};

    std::vector<uint8_t> ciphertext = ecbEncrypt(plaintext, key, blockSize);

    std::cout << "Ciphertext (hex): ";
    for (uint8_t byte : ciphertext) {
        std::cout << std::hex << (int)byte << " ";
    }
    std::cout << std::endl;

    return 0;
}
