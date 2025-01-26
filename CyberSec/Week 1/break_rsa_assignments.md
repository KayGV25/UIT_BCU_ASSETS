
# **Assignments: Breaking RSA**  

This guide contains five detailed assignments focused on breaking RSA. Each assignment introduces a different vulnerability in RSA, providing instructions and code examples to help you explore the topic in depth.

---

## **Assignment 1: Factorization Attack on RSA Modulus**  

### Objective  

Demonstrate the vulnerability of RSA when small keys are used by factorizing the RSA modulus.  

### Instructions  

1. **Generate a small RSA key pair** (512-bit) using OpenSSL:

    ```bash
    openssl genpkey -algorithm RSA -out rsa_key.pem -pkeyopt rsa_keygen_bits:512
    ```

2. **Extract the modulus (n)** from the public key:

    ```bash
    openssl rsa -in rsa_key.pem -pubout -text -noout
    ```

3. **Use a factorization tool** like **MSieve** or **YAFU** to factor the modulus `n`.

4. **Verify the reconstruction** of the private key using the factors obtained.

### Deliverable  

- A report documenting the factorization process, along with code snippets and screenshots.

---

## **Assignment 2: Implement Wiener's Attack on Weak RSA Keys**  

### Objective  

Understand how using a small public exponent (e.g., `e = 3`) can make RSA vulnerable.

### Instructions  

1. **Create an RSA key pair** with a small public exponent:

    ```bash
    openssl genpkey -algorithm RSA -out weak_rsa.pem -pkeyopt rsa_keygen_bits:1024 -pkeyopt rsa_keygen_pubexp:3
    ```

2. **Encrypt a small message**:

    ```bash
    echo "Hello RSA" | openssl rsautl -encrypt -inkey weak_rsa.pem -pubin -out encrypted.bin
    ```

3. **Implement Wiener's attack** or use an available tool to recover the private key.

### Deliverable  

- Source code and an analysis explaining the vulnerability and results.

---

## **Assignment 3: Side-Channel Analysis of RSA Execution Time**  

### Objective  

Explore how side-channel timing attacks can leak private key information.

### Instructions  

1. **Write a script** to measure the decryption time of multiple RSA decryptions.
2. **Analyze the timing patterns** to infer bits of the private key.
3. **Suggest mitigation techniques** to prevent such timing attacks (e.g., constant-time operations).

### Example Code (Python)  

```python
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

key = RSA.generate(2048)
cipher = PKCS1_OAEP.new(key)

def measure_time():
    start = time.time()
    cipher.decrypt(cipher.encrypt(b"test message"))
    return time.time() - start

print(f"Decryption time: {measure_time()} seconds")
```

### Deliverable  

- A report with code, analysis, graphs, and recommendations to prevent timing attacks.

---

## **Assignment 4: Small Private Exponent Attack on RSA**  

### Objective  

Demonstrate the risk of using a small private exponent in RSA encryption.

### Instructions  

1. **Generate an RSA key pair** with a small private exponent:

    ```bash
    openssl genpkey -algorithm RSA -out rsa_small_d.pem -pkeyopt rsa_keygen_bits:1024
    ```

2. **Encrypt and decrypt a message** to confirm the functionality of the key pair:

    ```bash
    echo "RSA Test" | openssl rsautl -encrypt -inkey rsa_small_d.pem -pubin -out encrypted.bin
    openssl rsautl -decrypt -inkey rsa_small_d.pem -in encrypted.bin
    ```

3. **Use a small-d attack** tool or implement your own script to recover the private key.

### Deliverable  

- Code and a brief report explaining the attack and results.

---

## **Assignment 5: Padding Oracle Attack on RSA Encryption**  

### Objective  

Learn how improper padding schemes can make RSA encryption vulnerable to attacks.

### Instructions  

1. **Set up a vulnerable RSA system** using **PKCS#1 v1.5 padding**:

    ```bash
    openssl genpkey -algorithm RSA -out rsa_padding.pem -pkeyopt rsa_keygen_bits:1024
    ```

2. **Encrypt a message with PKCS#1 v1.5 padding**:

    ```bash
    echo "Oracle Attack" | openssl rsautl -encrypt -inkey rsa_padding.pem -pubin -out encrypted.bin -pkcs
    ```

3. **Implement a Padding Oracle Attack** to decrypt the message without the private key.

4. **Suggest secure alternatives**, such as **OAEP** padding, to mitigate the issue.

### Deliverable  

- Code implementation, decryption results, and recommendations for secure padding.

---

## **Submission Guidelines**  

- Ensure all assignments are submitted with:
  - Code (well-commented)
  - A brief report explaining the attack and your observations
  - Screenshots or graphs where appropriate
- Submit as a ZIP file containing all your work.

---

These assignments provide a comprehensive understanding of RSA vulnerabilities and hands-on experience with attacks. If you have any questions or encounter challenges, feel free to ask for assistance.
