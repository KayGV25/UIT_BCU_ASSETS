#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <iostream>
#include <vector>
#include <string>

extern "C" {

// Print OpenSSL errors to help with debugging
void print_openssl_errors() {
    ERR_print_errors_fp(stderr);
}

// Generate RSA keys and save to files using BIO
__declspec(dllexport) void generate_rsa_keys(int bits, const char* public_key_file, const char* private_key_file) {
    RSA* rsa = RSA_new();
    BIGNUM* bn = BN_new();
    BN_set_word(bn, RSA_F4);  // Common public exponent 65537

    if (RSA_generate_key_ex(rsa, bits, bn, nullptr) != 1) {
        std::cerr << "Error generating RSA key pair.\n";
        print_openssl_errors();
        exit(1);
    }

    BIO* bio_pub = BIO_new_file(public_key_file, "wb");
    PEM_write_bio_RSA_PUBKEY(bio_pub, rsa);
    BIO_free(bio_pub);

    BIO* bio_priv = BIO_new_file(private_key_file, "wb");
    PEM_write_bio_RSAPrivateKey(bio_priv, rsa, nullptr, nullptr, 0, nullptr, nullptr);
    BIO_free(bio_priv);

    RSA_free(rsa);
    BN_free(bn);
    std::cout << "RSA keys generated successfully.\n";
}

// Encrypt data using RSA public key
__declspec(dllexport) int rsa_encrypt(const char* public_key_file, const char* input, const char* output) {
    BIO* bio = BIO_new_file(public_key_file, "rb");
    if (!bio) {
        std::cerr << "Error opening public key file.\n";
        print_openssl_errors();
        return -1;
    }
    RSA* rsa = PEM_read_bio_RSA_PUBKEY(bio, nullptr, nullptr, nullptr);
    BIO_free(bio);

    std::vector<unsigned char> plaintext(input, input + strlen(input));
    std::vector<unsigned char> ciphertext(RSA_size(rsa));

    int len = RSA_public_encrypt(plaintext.size(), plaintext.data(), ciphertext.data(), rsa, RSA_PKCS1_OAEP_PADDING);
    if (len == -1) {
        std::cerr << "Error during encryption.\n";
        print_openssl_errors();
        RSA_free(rsa);
        return -1;
    }

    std::ofstream out(output, std::ios::binary);
    out.write(reinterpret_cast<char*>(ciphertext.data()), len);
    RSA_free(rsa);
    return 0;
}

// Decrypt data using RSA private key
__declspec(dllexport) int rsa_decrypt(const char* private_key_file, const char* input_file, const char* output_file) {
    BIO* bio = BIO_new_file(private_key_file, "rb");
    if (!bio) {
        std::cerr << "Error opening private key file.\n";
        print_openssl_errors();
        return -1;
    }
    RSA* rsa = PEM_read_bio_RSAPrivateKey(bio, nullptr, nullptr, nullptr);
    BIO_free(bio);

    std::ifstream in(input_file, std::ios::binary);
    std::vector<unsigned char> ciphertext((std::istreambuf_iterator<char>(in)), {});

    std::vector<unsigned char> plaintext(RSA_size(rsa));
    int len = RSA_private_decrypt(ciphertext.size(), ciphertext.data(), plaintext.data(), rsa, RSA_PKCS1_OAEP_PADDING);
    if (len == -1) {
        std::cerr << "Error during decryption.\n";
        print_openssl_errors();
        RSA_free(rsa);
        return -1;
    }

    std::ofstream out(output_file);
    out.write(reinterpret_cast<char*>(plaintext.data()), len);
    RSA_free(rsa);
    return 0;
}
}
