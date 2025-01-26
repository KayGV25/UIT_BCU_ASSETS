#include <openssl/rsa.h>         // For RSA functions
#include <openssl/pem.h>         // For PEM file I/O
#include <openssl/bio.h>         // For BIO operations
#include <openssl/err.h>         // For error handling
#include <iostream>              // For standard I/O
#include <vector>                // For handling byte data
#include <string>                // For string operations

// Print OpenSSL errors for debugging purposes
void print_openssl_errors() {
    ERR_print_errors_fp(stderr);
}

// Generate RSA keys and save them to files using BIO
void generate_rsa_keys(int bits, const std::string& public_key_file, const std::string& private_key_file) {
    RSA* rsa = RSA_new();
    BIGNUM* bn = BN_new();
    BN_set_word(bn, RSA_F4);  // Common public exponent 65537

    // Generate the RSA key pair
    if (RSA_generate_key_ex(rsa, bits, bn, nullptr) != 1) {
        std::cerr << "Error generating RSA key pair.\n";
        print_openssl_errors();
        exit(1);
    }

    // Save the public key
    BIO* bio_pub = BIO_new_file(public_key_file.c_str(), "wb");
    PEM_write_bio_RSA_PUBKEY(bio_pub, rsa);
    BIO_free(bio_pub);

    // Save the private key
    BIO* bio_priv = BIO_new_file(private_key_file.c_str(), "wb");
    PEM_write_bio_RSAPrivateKey(bio_priv, rsa, nullptr, nullptr, 0, nullptr, nullptr);
    BIO_free(bio_priv);

    RSA_free(rsa);
    BN_free(bn);
    std::cout << "RSA keys generated successfully.\n";
}

// Load a public key from a file using BIO
RSA* load_public_key(const std::string& public_key_file) {
    BIO* bio = BIO_new_file(public_key_file.c_str(), "rb");
    if (!bio) {
        std::cerr << "Error opening public key file.\n";
        print_openssl_errors();
        exit(1);
    }
    RSA* rsa = PEM_read_bio_RSA_PUBKEY(bio, nullptr, nullptr, nullptr);
    BIO_free(bio);
    return rsa;
}

// Load a private key from a file using BIO
RSA* load_private_key(const std::string& private_key_file) {
    BIO* bio = BIO_new_file(private_key_file.c_str(), "rb");
    if (!bio) {
        std::cerr << "Error opening private key file.\n";
        print_openssl_errors();
        exit(1);
    }
    RSA* rsa = PEM_read_bio_RSAPrivateKey(bio, nullptr, nullptr, nullptr);
    BIO_free(bio);
    return rsa;
}

// Encrypt data using RSA public key
std::vector<unsigned char> rsa_encrypt(RSA* rsa, const std::vector<unsigned char>& plaintext) {
    std::vector<unsigned char> ciphertext(RSA_size(rsa));
    int len = RSA_public_encrypt(plaintext.size(), plaintext.data(), ciphertext.data(), rsa, RSA_PKCS1_OAEP_PADDING);
    if (len == -1) {
        std::cerr << "Error during encryption.\n";
        print_openssl_errors();
        exit(1);
    }
    ciphertext.resize(len);
    return ciphertext;
}

// Decrypt data using RSA private key
std::vector<unsigned char> rsa_decrypt(RSA* rsa, const std::vector<unsigned char>& ciphertext) {
    std::vector<unsigned char> plaintext(RSA_size(rsa));
    int len = RSA_private_decrypt(ciphertext.size(), ciphertext.data(), plaintext.data(), rsa, RSA_PKCS1_OAEP_PADDING);
    if (len == -1) {
        std::cerr << "Error during decryption.\n";
        print_openssl_errors();
        exit(1);
    }
    plaintext.resize(len);
    return plaintext;
}

// Read a file using BIO
std::vector<unsigned char> bio_read(const std::string& filename) {
    BIO* bio = BIO_new_file(filename.c_str(), "rb");
    if (!bio) {
        std::cerr << "Error opening input file: " << filename << "\n";
        print_openssl_errors();
        exit(1);
    }

    std::vector<unsigned char> data;
    unsigned char buffer[1024];
    int bytesRead;
    while ((bytesRead = BIO_read(bio, buffer, sizeof(buffer))) > 0) {
        data.insert(data.end(), buffer, buffer + bytesRead);
    }
    BIO_free(bio);
    return data;
}

// Write a file using BIO
void bio_write(const std::string& filename, const std::vector<unsigned char>& data) {
    BIO* bio = BIO_new_file(filename.c_str(), "wb");
    if (!bio) {
        std::cerr << "Error opening output file: " << filename << "\n";
        print_openssl_errors();
        exit(1);
    }
    BIO_write(bio, data.data(), data.size());
    BIO_free(bio);
}

// Main function to handle command-line arguments
int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <command> [options]\n";
        std::cerr << "Commands:\n";
        std::cerr << "  genkey <bits> <public_key.pem> <private_key.pem>  Generate RSA key pair\n";
        std::cerr << "  encrypt <public_key.pem> <input> <output>         Encrypt a file\n";
        std::cerr << "  decrypt <private_key.pem> <input> <output>       Decrypt a file\n";
        return 1;
    }

    std::string command = argv[1];

    if (command == "genkey" && argc == 5) {
        int bits = std::stoi(argv[2]);
        generate_rsa_keys(bits, argv[3], argv[4]);
    } else if (command == "encrypt" && argc == 5) {
        RSA* rsa = load_public_key(argv[2]);
        std::vector<unsigned char> plaintext = bio_read(argv[3]);
        std::vector<unsigned char> ciphertext = rsa_encrypt(rsa, plaintext);
        bio_write(argv[4], ciphertext);
        RSA_free(rsa);
        std::cout << "Encryption completed.\n";
    } else if (command == "decrypt" && argc == 5) {
        RSA* rsa = load_private_key(argv[2]);
        std::vector<unsigned char> ciphertext = bio_read(argv[3]);
        std::vector<unsigned char> plaintext = rsa_decrypt(rsa, ciphertext);
        bio_write(argv[4], plaintext);
        RSA_free(rsa);
        std::cout << "Decryption completed.\n";
    } else {
        std::cerr << "Invalid command or arguments.\n";
        return 1;
    }

    return 0;
}
