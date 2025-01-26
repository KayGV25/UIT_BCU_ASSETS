
# OpenSSL Guide: AES and RSA Usage

## Table of Contents

1. [AES Encryption and Decryption](#aes-encryption-and-decryption)
   - [Generate AES Key](#generate-aes-key)
   - [Encrypt with AES](#encrypt-with-aes)
   - [Decrypt with AES](#decrypt-with-aes)
2. [RSA Encryption and Decryption](#rsa-encryption-and-decryption)
   - [Generate RSA Key Pair](#generate-rsa-key-pair)
   - [Encrypt with RSA](#encrypt-with-rsa)
   - [Decrypt with RSA](#decrypt-with-rsa)

---

## AES Encryption and Decryption

### Generate AES Key

Use the following command to generate a 256-bit AES key:

```bash
openssl rand -out aes_key.bin 32
//hexdump -x aes_key.bin
```

- **`32`**: Number of bytes (256 bits) for the AES key.

### Encrypt with AES

Use AES in CBC mode to encrypt a file.

```bash
openssl enc -list
openssl enc -aes-256-ctr -in plaintext.txt -out encrypted.bin -pass file:./aes_key.bin

```

- **`-aes-256-cbc`**: Specifies AES with 256-bit key in CBC mode.
- **`-salt`**: Adds random salt to prevent rainbow table attacks.
- **`-pass file:./aes_key.bin`**: Provides the key for encryption.

### Decrypt with AES

Use the same AES key to decrypt the file.

```bash
openssl enc -aes-256-ctr -d -in encrypted.bin -out decrypted.txt -pass file:./aes_key.bin
```

- **`-d`**: Decrypts the input file.

---

## RSA Encryption and Decryption

### Generate RSA Key Pair

Create a 2048-bit RSA private key and extract the public key.

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

Extract the public key from the private key:

```bash
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

### Encrypt with RSA

Encrypt a file using the public key.

```bash
openssl rsautl -encrypt -inkey public_key.pem -pubin -in plaintext.txt -out encrypted.bin
```

- **`-encrypt`**: Specifies encryption mode.
- **`-pubin`**: Indicates the input key is a public key.

### Decrypt with RSA

Decrypt the file using the private key.

```bash
openssl rsautl -decrypt -inkey private_key.pem -in encrypted.bin -out decrypted.txt
```

- **`-decrypt`**: Specifies decryption mode.

---

## Notes

- Ensure that OpenSSL is installed on your system.
- Use strong keys and appropriate modes for security.
- Keep private keys secure and do not share them.

---

