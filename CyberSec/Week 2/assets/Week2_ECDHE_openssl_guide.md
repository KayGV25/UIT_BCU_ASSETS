
# ECDHE Key Exchange using OpenSSL

Elliptic Curve Diffie-Hellman Ephemeral (ECDHE) is a version of Diffie-Hellman that uses elliptic curves for the key exchange, which provides better security with smaller key sizes.

## Step 1: Install OpenSSL
Ensure that OpenSSL is installed on your system:
```bash
openssl version
```

## Step 2: Select an Elliptic Curve
First, choose the elliptic curve to be used for the key exchange. You can list all supported curves with:
```bash
openssl ecparam -list_curves
```

For this guide, we will use the `prime256v1` curve, which is widely supported:
```bash
openssl ecparam -name prime256v1 -out ec_param.pem
```

## Step 3: Generate Private and Public Keys

### Party 1 (Client):
1. **Generate private key**:
   ```bash
   openssl ecparam -in ec_param.pem -genkey -noout -out client_private.pem
   ```

2. **Extract public key**:
   ```bash
   openssl ec -in client_private.pem -pubout -out client_public.pem
   ```

### Party 2 (Server):
1. **Generate private key**:
   ```bash
   openssl ecparam -in ec_param.pem -genkey -noout -out server_private.pem
   ```

2. **Extract public key**:
   ```bash
   openssl ec -in server_private.pem -pubout -out server_public.pem
   ```

## Step 4: Compute Shared Secret

Each party computes a shared secret using their private key and the other party's public key.

### Client:
```bash
openssl pkeyutl -derive -inkey client_private.pem -peerkey server_public.pem -out client_secret.bin
```

### Server:
```bash
openssl pkeyutl -derive -inkey server_private.pem -peerkey client_public.pem -out server_secret.bin
```

## Step 5: Verify the Shared Secret

Verify that both parties derived the same shared secret:
```bash
diff client_secret.bin server_secret.bin
```

## Step 6: Convert to Hex (Optional)

To view the shared secret in hexadecimal form:
```bash
certutil -dump client_secret.bin
certutil -dump server_secret.bin
```
