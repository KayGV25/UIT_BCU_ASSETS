
The size of Hash must be double the size of the encryption (e.g AES128 -> SHA256)

# Flaw of SHA v2
- Can have extension attack  -> must implement some way to prevent padding 
# Standard for information processing
- For Hash Function:
	- FIPS 202
- For Digital Signature:
	- FIPS 204 
	- FIPS 205
# HMAC
- The secret key can be pre-deployed in production

## HMAC vs DSA
- HMAC is smaller and faster
- DSA is more secure
# DSA
## Secure/Protect secret key
- Can use cold device