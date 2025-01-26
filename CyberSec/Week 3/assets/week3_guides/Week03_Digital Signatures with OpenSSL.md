
# Digital Signatures with OpenSSL (RSA-PSS, DSA, and ECDSA)

This guide provides instructions for generating digital signatures using OpenSSL for RSA-PSS, DSA, and ECDSA key types.

---

## 1. RSA-PSS (Probabilistic Signature Scheme)

### Generate RSA Key Pair

- **Create RSA Private Key**

  ```bash
  openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out rsa-pss-private.pem
  ```

- **Extract the Public Key**

  ```bash
  openssl rsa -in rsa-pss-private.pem -pubout -out rsa-pss-public.pem
  ```

### Create and Verify Digital Signature

1. **Create a Digital Signature for message.txt**

   ```bash
   openssl dgst -sha256 -sigopt rsa_padding_mode:pss -sign rsa-pss-private.pem -out rsa-pss-signature.bin message.txt
   ```

2. **Verify the Digital Signature for message.txt and rsa-pss-signature.bin**

   ```bash
   openssl dgst -sha256 -sigopt rsa_padding_mode:pss -verify rsa-pss-public.pem -signature rsa-pss-signature.bin message.txt
   ```

---

## 2. DSA (Digital Signature Algorithm)

### Generate DSA Key Pair

- **Create DSA Parameters**

  ```bash
  openssl dsaparam -out dsa-param.pem 3072
  ```

- **Generate DSA Private Key using Parameters**

  ```bash
  openssl genpkey -paramfile dsa-param.pem -out dsa-private.pem
  ```

- **Extract the Public Key**

  ```bash
  openssl dsa -in dsa-private.pem -pubout -out dsa-public.pem
  ```

### Create and Verify Digital Signature using DSA

1. **Create a Digital Signature for message.txt**

   ```bash
   openssl dgst -sha256 -sign dsa-private.pem -out dsa-signature.bin message.txt
   ```

2. **Verify the Digital Signature for message.txt and dsa-signature.bin**

   ```bash
   openssl dgst -sha256 -verify dsa-public.pem -signature dsa-signature.bin message.txt
   ```

---

## 3. ECDSA (Elliptic Curve Digital Signature Algorithm)

### Generate ECDSA Key Pair

- **Choose Curve and Generate Private Key**

  ```bash
  openssl ecparam -name prime256v1 -genkey -noout -out ecdsa-private.pem
  ```

- **Extract the Public Key**

  ```bash
  openssl ec -in ecdsa-private.pem -pubout -out ecdsa-public.pem
  ```

### Create and Verify Digital Signature using ECC

1. **Create a Digital Signature**

   ```bash
   openssl dgst -sha256 -sign ecdsa-private.pem -out ecdsa-signature.bin message.txt
   ```

2. **Verify the Digital Signature**

   ```bash
   openssl dgst -sha256 -verify ecdsa-public.pem -signature ecdsa-signature.bin message.txt
   ```

---

This guide provides steps for generating and verifying digital signatures using RSA-PSS, DSA, and ECDSA. Ensure that `message.txt` contains the data you wish to sign.
