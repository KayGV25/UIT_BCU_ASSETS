#include <openssl/evp.h>  // For EVP encryption functions
#include <openssl/rand.h>  // For generating random bytes
#include <openssl/bio.h>   // For file I/O operations
#include <openssl/err.h>   // For error handling
#include <iostream>        // For standard I/O operations
#include <vector>          // For using std::vector to handle byte data
#include <string>          // For using std::string to handle input arguments

// Print OpenSSL errors to help with debugging
void print_openssl_errors() {
    ERR_print_errors_fp(stderr);
}

// Convert a hex string (e.g., "aabbcc") to a vector of bytes
std::vector<unsigned char> hex_to_bytes(const std::string& hex) {
    std::vector<unsigned char> bytes;
    for (size_t i = 0; i < hex.length(); i += 2) {
        std::string byteString = hex.substr(i, 2);
        unsigned char byte = static_cast<unsigned char>(strtol(byteString.c_str(), nullptr, 16));
        bytes.push_back(byte);
    }
    return bytes;
}

// Generate AES key and IV (Initial Vector) with a specified key size
void generate_key_iv(std::vector<unsigned char>& key, std::vector<unsigned char>& iv, int key_size) {
    key.resize(key_size);  // Resize the key to match the given key size (e.g., 32 bytes for AES-256)
    iv.resize(16);  // IV size is fixed to 128 bits (16 bytes)
    if (!RAND_bytes(key.data(), key.size()) || !RAND_bytes(iv.data(), iv.size())) {
        std::cerr << "Error generating random key or IV.";
        print_openssl_errors();
        exit(1);
    }
}

// AES encryption function using the specified mode (e.g., CBC, GCM)
void aes_encrypt(const std::vector<unsigned char>& plaintext, std::vector<unsigned char>& ciphertext,
                 const std::vector<unsigned char>& key, const std::vector<unsigned char>& iv, const EVP_CIPHER* cipher) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();  // Create a new cipher context
    if (!ctx) {
        std::cerr << "Error creating cipher context.";
        print_openssl_errors();
        exit(1);
    }

    // Initialize the encryption operation with the given key and IV
    if (EVP_EncryptInit_ex(ctx, cipher, nullptr, key.data(), iv.data()) != 1) {
        std::cerr << "Error initializing encryption.";
        print_openssl_errors();
        exit(1);
    }

    // Allocate space for the ciphertext
    ciphertext.resize(plaintext.size() + EVP_CIPHER_block_size(cipher));
    int len = 0, ciphertext_len = 0;

    // Encrypt the input data
    if (EVP_EncryptUpdate(ctx, ciphertext.data(), &len, plaintext.data(), plaintext.size()) != 1) {
        std::cerr << "Error during encryption.";
        print_openssl_errors();
        exit(1);
    }
    ciphertext_len = len;

    // Finalize the encryption
    if (EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len) != 1) {
        std::cerr << "Error finalizing encryption.";
        print_openssl_errors();
        exit(1);
    }
    ciphertext_len += len;

    ciphertext.resize(ciphertext_len);  // Resize the ciphertext to the actual length
    EVP_CIPHER_CTX_free(ctx);  // Free the cipher context
}

// AES decryption function using the specified mode
void aes_decrypt(const std::vector<unsigned char>& ciphertext, std::vector<unsigned char>& plaintext,
                 const std::vector<unsigned char>& key, const std::vector<unsigned char>& iv, const EVP_CIPHER* cipher) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();  // Create a new cipher context
    if (!ctx) {
        std::cerr << "Error creating cipher context.";
        print_openssl_errors();
        exit(1);
    }

    // Initialize the decryption operation with the given key and IV
    if (EVP_DecryptInit_ex(ctx, cipher, nullptr, key.data(), iv.data()) != 1) {
        std::cerr << "Error initializing decryption.";
        print_openssl_errors();
        exit(1);
    }

    // Allocate space for the plaintext
    plaintext.resize(ciphertext.size());
    int len = 0, plaintext_len = 0;

    // Decrypt the input data
    if (EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), ciphertext.size()) != 1) {
        std::cerr << "Error during decryption.";
        print_openssl_errors();
        exit(1);
    }
    plaintext_len = len;

    // Finalize the decryption
    if (EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len) != 1) {
        std::cerr << "Error finalizing decryption.";
        print_openssl_errors();
        exit(1);
    }
    plaintext_len += len;

    plaintext.resize(plaintext_len);  // Resize the plaintext to the actual length
    EVP_CIPHER_CTX_free(ctx);  // Free the cipher context
}

// Read a file using BIO (Binary I/O)
std::vector<unsigned char> bio_read(const std::string& filename) {
    BIO* bio = BIO_new_file(filename.c_str(), "rb");  // Open the file in binary mode
    if (!bio) {
        std::cerr << "Error opening file: " << filename << "\n";
        print_openssl_errors();
        exit(1);
    }

    std::vector<unsigned char> data;
    unsigned char buffer[1024];  // Buffer to read the file in chunks
    int bytesRead;
    while ((bytesRead = BIO_read(bio, buffer, sizeof(buffer))) > 0) {
        data.insert(data.end(), buffer, buffer + bytesRead);
    }
    BIO_free(bio);  // Free the BIO object
    return data;
}

// Write a file using BIO
void bio_write(const std::string& filename, const std::vector<unsigned char>& data) {
    BIO* bio = BIO_new_file(filename.c_str(), "wb");  // Open the file in binary mode
    if (!bio) {
        std::cerr << "Error writing to file: " << filename << "\n";
        print_openssl_errors();
        exit(1);
    }
    BIO_write(bio, data.data(), data.size());  // Write data to the file
    BIO_free(bio);  // Free the BIO object
}

// Get the appropriate cipher based on the mode (e.g., CBC, GCM)
const EVP_CIPHER* get_cipher(const std::string& mode) {
    if (mode == "ecb") return EVP_aes_256_ecb();
    if (mode == "cbc") return EVP_aes_256_cbc();
    if (mode == "ctr") return EVP_aes_256_ctr();
    if (mode == "ofb") return EVP_aes_256_ofb();
    if (mode == "cfb") return EVP_aes_256_cfb();
    if (mode == "cfb1") return EVP_aes_256_cfb1();
    if (mode == "cfb8") return EVP_aes_256_cfb8();
    if (mode == "gcm") return EVP_aes_256_gcm();
    std::cerr << "Unsupported mode: " << mode << "\n";
    exit(1);
}

// Main function to handle command-line arguments
int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <mode> <operation> [options]\n";
        std::cout << "Supported encryption mode: ecb, cbc, ctr, ofb, cfb, gcm\n";
        std::cout << "Supported operation genkey, encrypt, decrypt\n";
        return 1;
    }

    std::string mode = argv[1];
    std::string operation = argv[2];
    const EVP_CIPHER* cipher = get_cipher(mode);

    if (operation == "genkey") {
        std::vector<unsigned char> key, iv;
        generate_key_iv(key, iv, 32);
        // Print generated key and IV 
        std::cout << "Generated Key: ";
        for (unsigned char c : key) std::cout << c;
        std::cout << "\n";
        std::cout << "Generated IV: ";
        for (unsigned char c : iv) std::cout << c;
        std::cout << "\n";



    } else if ((operation == "encrypt" || operation == "decrypt") && argc == 7) {
        std::vector<unsigned char> key_in_hex = bio_read(argv[3]);
        std::vector<unsigned char> iv_in_hex = bio_read(argv[4]);
        if(operation == "encrypt"){
            std::vector<unsigned char> cipher_text;
            aes_encrypt(bio_read(argv[5]), cipher_text, key_in_hex, iv_in_hex, cipher);
            bio_write(argv[6], cipher_text);
        }
        if(operation == "decrypt"){
            std::vector<unsigned char> plain_text;
            aes_decrypt(bio_read(argv[5]), plain_text, key_in_hex, iv_in_hex, cipher);
            bio_write(argv[6], plain_text);
        }
    }
}