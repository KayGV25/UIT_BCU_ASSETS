# Access Control
- Implement **Least privileges** 
- Must be implement iff the first 2 layers ![[Pasted image 20241115094144.png]]have been implemented. If not, then there is a risk of insider attack
- All data i current ages must be encrypt in some way before storing
# TOTP
- sending secret key in plaintext via qr code is not safe -> you can encrypt the key by aes then generate qr code for it
- TOTP(secretKey, currentTime)
## IRL
- We use password to generate AES key-key -> encrypt key -> QR -> Send
- QR -> Extract cipher -> Decrypt

# AAA
- AAA is a must to have layer in modern cybersecurity 
- Authentication: 
	- Validate user identity to ensure they are who they claim to be
	- We must validates user identity not only by Id but also with other information
- Authorization
- Accounting (Auditing): 
