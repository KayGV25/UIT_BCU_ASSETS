
# X.509 Certificate Creation and Signing with OpenSSL

This guide provides step-by-step instructions for generating and signing X.509 certificates using OpenSSL, including both RSA and ECC key types, and checking server certificates.

---

## 1. RSA Certificates

### Generate RSA Private and Public Keys

- **Base64 Form (PEM format)**

  ```bash
  openssl genrsa -out rsaprivate.pem 3072
  openssl rsa -in rsaprivate.pem -pubout -out rsapubkey.pem
  ```

- **Binary Form (DER format)**

  ```bash
  openssl rsa -in rsaprivate.pem -outform DER -out rsa-private.der
  openssl rsa -in rsaprivate.pem -outform DER -pubout -out rsa-pubkey.der
  ```

### Generate an RSA Certificate

1. **Create a Certificate Signing Request (CSR)**

   ```bash
   openssl req -key rsaprivate.pem -new -out temp.csr
   ```

2. **Check the CSR**

   ```bash
   openssl req -text -noout -verify -in temp.csr
   ```

3. **Self-sign the Certificate**  
   *Note: Self-signing is only applicable if you are the trusted root Certificate Authority (CA).*

   ```bash
   openssl x509 -signkey rsaprivate.pem -in temp.csr -req -days 365 -out mycert.crt
   ```

4. **Verify the Certificate**

   ```bash
   openssl x509 -in mycert.crt -inform PEM -text -noout
   ```

*Optional tool:* You may use `certutil.exe` for additional certificate management functions.

---

## 2. ECC (Elliptic Curve Cryptography) Certificates

### Generate ECC Private and Public Keys

1. **List Available Curves** (optional)

   ```bash
   openssl ecparam -list_curves
   ```

2. **Generate Private Key**

   ```bash
   openssl ecparam -name prime256v1 -genkey -noout -out ec-private-key.pem
   ```

3. **Generate Public Key**

   ```bash
   openssl ec -in ec-private-key.pem -pubout -out ec-public-key.pem
   ```

### Generate an ECC Certificate

1. **Create a Certificate Signing Request (CSR)**

   ```bash
   openssl req -key ec-private-key.pem -new -out ec-temp.csr
   ```

2. **Check the CSR**

   ```bash
   openssl req -text -noout -verify -in ec-temp.csr
   ```

---

## 3. Checking Server Certificates

### Example: Checking Certificates of Common Websites

- **Check Vietcombank's Server Certificate**

  ```bash
  echo | openssl s_client -servername www.vietcombank.com.vn -connect www.vietcombank.com.vn:443 2>resul.txt | openssl x509 -text
  ```

- **Check Facebook's Server Certificate and Save Output**

  ```bash
  echo | openssl s_client -servername www.facebook.com -connect www.facebook.com:443 2> cert | openssl x509 -out facebook.cer -text
  ```

### Display Certificate Content

```bash
openssl x509 -in certificate.crt -inform PEM -text -noout
```

### Display Certificate Revocation List (CRL)

```bash
openssl crl -in g6.crl -text -noout
```

---

This guide should help you create and sign RSA and ECC X.509 certificates, as well as validate server certificates. Remember to replace domain names and filenames as needed.
