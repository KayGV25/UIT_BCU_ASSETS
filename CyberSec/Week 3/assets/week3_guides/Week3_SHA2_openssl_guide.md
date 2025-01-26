
# SHA-2 Hashing using OpenSSL

SHA-2 (Secure Hash Algorithm 2) is a family of cryptographic hash functions widely used for ensuring data integrity. This guide demonstrates how to use OpenSSL to generate SHA-2 hashes for your data.

## Step 1: Install OpenSSL

Ensure that OpenSSL is installed and accessible on your system:

```bash
openssl version
```

If OpenSSL is not installed, follow the installation instructions based on your operating system.

---

## Step 2: Choose a SHA-2 Algorithm

SHA-2 provides multiple variants with different output lengths, including:

- **SHA-224** (224-bit output)
- **SHA-256** (256-bit output)
- **SHA-384** (384-bit output)
- **SHA-512** (512-bit output)

Use one that fits your security and performance requirements.

---

## Step 3: Generate a SHA-2 Hash

### Hash a Text File

Use OpenSSL to compute the hash of a file.

Example for **SHA-256**:
```bash
openssl dgst -sha256 -out hash.sha256 file.txt
```

Replace `-sha256` with other SHA-2 variants (e.g., `-sha512`, `-sha384`) if needed.

---

## Step 4: Verify a SHA-2 Hash

To verify the hash, compare the original and newly computed hash outputs.

1. **Hash generation**:
   ```bash
   openssl dgst -sha256 file.txt
   ```

2. **Compare with stored hash**:
   ```bash
   diff hash.sha256 <(openssl dgst -sha256 file.txt)
   ```

---

## Step 5: Generate a HMAC with SHA-2

Use SHA-2 with HMAC (Hash-based Message Authentication Code) for secure authentication.

```bash
openssl dgst -sha256 -hmac "secret_key" -out hmac.sha256 file.txt
```

Verify the HMAC by re-running the command with the same key and input.

---

## Step 6: Hash a String

To hash a string directly (e.g., in scripts):

```bash
echo -n "Hello, World!" | openssl dgst -sha256
```

Remove `-n` if you want to include the trailing newline in the hash calculation.

---

## Conclusion

This guide covers basic usage of SHA-2 hashing with OpenSSL, including generating and verifying hashes and HMACs. These tools help ensure the integrity and authenticity of your data.
