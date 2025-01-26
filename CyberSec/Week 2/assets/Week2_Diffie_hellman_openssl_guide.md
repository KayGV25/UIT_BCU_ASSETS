
# Diffie-Hellman Key Exchange using OpenSSL

The Diffie-Hellman (DH) key exchange algorithm allows two parties to securely exchange cryptographic keys over a public channel. This guide will walk you through the process of performing a DH key exchange using OpenSSL.

## Step 1: Install OpenSSL

Ensure that OpenSSL is installed on your system. You can verify this by running the following command:

```bash
openssl version
```

If not installed, you can install OpenSSL using your package manager. For example:
- On Ubuntu/Debian: `sudo apt-get install openssl`
- On Fedora/CentOS: `sudo yum install openssl`
- On macOS: `brew install openssl`

## Step 2: Generate DH Parameters

The first step is to generate Diffie-Hellman parameters. This defines the prime number (p) and the base (g).

```bash
openssl dhparam -out dhparam.pem 2048
```

- `dhparam.pem` is the output file containing the DH parameters.
- `2048` is the size of the prime number (p). You can also use 1024, 3072, or 4096.

## Step 3: Generate Private and Public Keys

Once the DH parameters are generated, each party needs to generate their own private and public keys.

### Party 1 (client):

1. **Generate private key:**
   ```bash
   openssl genpkey -paramfile dhparam.pem -out client_private.pem
   ```

2. **Extract public key:**
   ```bash
   openssl pkey -in client_private.pem -pubout -out client_public.pem
   ```
3. **Read the keys**
```bash
openssl pkey -in client_private.pem -text -noout
openssl pkey -in client_public.pem -pubin -text -noout
```

### Party 2 (Server):

1. **Generate private key:**
   ```bash
   openssl genpkey -paramfile dhparam.pem -out server_private.pem
   ```

2. **Extract public key:**
   ```bash
   openssl pkey -in server_private.pem -pubout -out server_public.pem
   ```
3. **Read the keys**
```bash
openssl pkey -in server_private.pem -text -noout
openssl pkey -in server_public.pem -pubin -text -noout
```

## Step 4: Compute Shared Secret

Each party computes a shared secret using their private key and the other party's public key.

### Party 1 (Client):

To compute the shared secret on Client’s side using her private key and Server’s public key:

```bash
openssl pkeyutl -derive -inkey client_private.pem -peerkey server_public.pem -out client_secret.bin
```

### Party 2 (Server):

Similarly, Server computes the shared secret using his private key and Client’s public key:

```bash
openssl pkeyutl -derive -inkey server_private.pem -peerkey client_public.pem -out server_secret.bin
```

## Step 5: Verify the Shared Secret

At this point, both Alice and Bob should have derived the same shared secret. You can compare the secrets (in binary) to verify that the key exchange worked correctly.

```bash
diff server_secret.bin client_secret.bin
```

If there's no output from the `diff` command, the files are identical, meaning the shared secret is the same.

## Step 6: Optionally Convert to Hex

If you want to view the shared secret in a human-readable form, you can convert it to hexadecimal:

```bash
certutil -dump server_secret.bin
certutil -dump client_secret.bin
```

This should show identical output for both Client and Server, confirming that the Diffie-Hellman key exchange was successful.
