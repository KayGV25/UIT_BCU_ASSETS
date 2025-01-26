
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

3. **Self-sign the ECC Certificate**  
   *Note: Self-signing is only applicable if you are the trusted root Certificate Authority (CA).*

   ```bash
   openssl x509 -signkey ec-private-key.pem -in ec-temp.csr -req -days 365 -out eccmycert.crt
   ```

4. **Verify the Certificate**

   ```bash
   openssl x509 -in eccmycert.crt -inform PEM -text -noout

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

## 4. Root CA task

### Step 1: Create CA Key Pair

1. **Generate the CA private key**  

   ```bash
   openssl ecparam -genkey -name prime256v1 -out ec-ca-key.pem
   ```

   This command generates an elliptic curve private key for the CA, using the `prime256v1` curve.

2. **Generate a CA public key certificate**  

   ```bash
   openssl req -new -x509 -key ec-ca-key.pem -days 3650 -out ec-ca-cert.pem
   ```

   - `-new -x509`: Generates a self-signed certificate.
   - `-key ec-ca-key.pem`: Uses the CA private key to sign its own certificate.
   - `-days 3650`: Sets the certificate’s validity period to 10 years (3650 days).
   - `-out ec-ca-cert.pem`: Specifies the output file for the CA certificate.

   During this command, you’ll be prompted to enter the CA details, such as the organization name and location. These details will appear in the CA certificate and serve as the **Issuer** information when signing certificates.

---

### Step 2: Self-Sign the CA Certificate

The previous command already generated a self-signed certificate (`ec-ca-cert.pem`) for the CA. This self-signed certificate can now be used to establish the CA's trust.

---

### Step 3: Sign Customer Certificate Requests

1. **Customer Creates CSR (Certificate Signing Request)**

   The customer should create a CSR. This request will include their public key and identifying information:

   ```bash
   openssl ecparam -name prime256v1 -genkey -out ec-customer-key.pem
   openssl req -new -key ec-customer-key.pem -out ec-customer.csr
   openssl req -text -noout -verify -in ec-customer.csr

   ``
   - `output'  ec-customer.csr`: The output cerificate witout signning by CA.

2. **CA Signs Customer CSR**

   Now, the CA can sign the customer's CSR (`ec-customer.csr`) using its own certificate and private key to create a signed certificate:

   ```bash
   openssl x509 -req -in ec-customer.csr -CA ec-ca-cert.pem -CAkey ec-ca-key.pem -CAcreateserial -days 365 -out ecccustomercert.crt
   ```

   - `-req`: Indicates the input is a CSR.
   - `-in ec-customer.csr`: Specifies the CSR file from the customer.
   - `-CA ec-ca-cert.pem`: Uses the CA certificate as the issuer.
   - `-CAkey ec-ca-key.pem`: Uses the CA’s private key to sign the certificate.
   - `-CAcreateserial`: Creates a unique serial number for the new certificate.
   - `-days 365`: Sets the validity period for the signed certificate (1 year).
   - `-out ecccustomercert.crt`: Specifies the output file for the signed certificate.

The resulting file `ecccustomercert.crt` is the customer’s signed certificate, which includes issuer information from the CA.

---

## Summary of Files Created

- **ec-ca-key.pem**: Private key of the CA.
- **ec-ca-cert.pem**: Self-signed certificate for the CA.
- **ec-customer-key.pem**: Private key for the customer.
- **ec-customer.csr**: Certificate Signing Request from the customer.
- **ecccustomercert.crt**: Signed certificate for the customer, issued by the CA.
