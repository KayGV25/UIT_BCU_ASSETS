
- Entity include; User, End-devices, Network device, Programs, Process, ...
-> We must have a way to secure and authenticate the server/device we're connecting to
We have 2 mechanism in the last section:
- Use encryption to encrypt data so that no one except the receiver can read
- Authenticate who sent the message
# Network secure protocol
## Motivations
- Mutual authentication
- System parameters and cryptographic algorithms
- Key agreement
## Notes
- All biometric modules don't locally store or can be edit but only can be check if correct via API
- Adversarial sample attacks: Risk in ML/DL modules

## Mutual authentication
- Both user and server need to authenticate each other -> mutual authentication
- Client will send a list of available algorithm to encrypt data and server will choose