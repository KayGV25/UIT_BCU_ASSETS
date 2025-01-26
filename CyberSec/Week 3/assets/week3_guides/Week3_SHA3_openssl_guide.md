
# SHA-3 Hashing using OpenSSL

SHA-3 (Secure Hash Algorithm 3) is a cryptographic hash function standardized by NIST as an alternative to the SHA-2 family. This guide shows how to generate and verify SHA-3 hashes using OpenSSL.

## Step 1: Install OpenSSL

Ensure that OpenSSL is installed and supports SHA-3:

```bash
openssl version
```

If OpenSSL is installed but does not recognize SHA-3, ensure you are using the latest version.

---

## Step 2: Choose a SHA-3 Algorithm

SHA-3 offers several variants with different output lengths:

- **SHA3-224** (224-bit output)
- **SHA3-256** (256-bit output)
- **SHA3-384** (384-bit output)
- **SHA3-512** (512-bit output)

Choose one that meets your needs based on security and performance.

---

## Step 3: Generate a SHA-3 Hash

### Hash a Text File

Use OpenSSL to hash a file with SHA-3.

Example for **SHA3-256**:
```bash
openssl dgst -sha3-256 -out hash.sha3 file.txt
```

Replace `-sha3-256` with other SHA-3 variants (`-sha3-224`, `-sha3-384`, `-sha3-512`) if needed.

---

## Step 4: Verify a SHA-3 Hash

To verify a SHA-3 hash, compare the original and newly computed hash outputs.

1. **Hash generation**:
   ```bash
   openssl dgst -sha3-256 file.txt
   ```

2. **Compare with stored hash**:
   ```bash
   diff hash.sha3 <(openssl dgst -sha3-256 file.txt)
   ```

---

## Step 5: Generate a HMAC with SHA-3

Use SHA-3 with HMAC (Hash-based Message Authentication Code) for secure authentication.

```bash
openssl dgst -sha3-256 -hmac "secret_key" -out hmac.sha3 file.txt
```

Verify the HMAC by re-running the command with the same key and input.

---

## Step 6: Hash a String

To hash a string directly:

```bash
echo -n "Hello, World!" | openssl dgst -sha3-256
```

Remove `-n` if you want to include the trailing newline in the hash calculation.

---

## Conclusion

This guide covers basic usage of SHA-3 hashing with OpenSSL, including generating and verifying hashes and HMACs. SHA-3 offers additional flexibility and security as a modern alternative to SHA-2.
