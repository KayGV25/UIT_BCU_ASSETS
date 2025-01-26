
# AES
- Advance Encryption System
- Encryption and Decryption use the same key -> Symmetric
## Operation used
- Substitute bytes (Substitution): Use a predefine map to substitute
- Shift rows (Permutation)
- Mix columns (Substitution)
- Add round key (Substitution)

# Elliptic Group
- Can generate random positions on the curve -> generate secure private key pair 
- (READ CHAPTER 10 of BOOK) file:///C:/Users/khuon/Desktop/UIT/CyberSec/Books/02_Cryptography%20and%20Network%20Security_%20Principles%20and%20Practice.pdf

## Choosing Curve 
- Must have 2x bits of the encryption (e.g. for aes-128 -> use secp256k1 (256 bits))