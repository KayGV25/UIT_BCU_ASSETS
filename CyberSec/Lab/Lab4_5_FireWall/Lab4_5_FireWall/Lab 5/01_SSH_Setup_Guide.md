
# Step-by-Step Guide: Setting Up SSH on Ubuntu

---

## 1. Set Up SSH Server

1. **Install OpenSSH Server:**

   ```bash
   sudo apt update
   sudo apt install openssh-server
   sudo apt install openssh-client
   # Checking
   which ssh
   man ssh
   ```

2. **Start and Enable SSH Service:**

   ```bash
   sudo systemctl start ssh
   sudo systemctl enable ssh
   ```

3. **Verify SSH Server is Running:**

   ```bash
   sudo systemctl status ssh
   ```

4. **Allow SSH Through Firewall (if applicable):**

   ```bash
   sudo ufw allow ssh
   sudo ufw reload
   ```

---

## 2. Generate ECC Certificates for Server

1. **Create Server's Key Pair (No pasphrase):**

   ```bash
   sudo ssh-keygen -t ecdsa -b 521 -f /etc/ssh/ssh_server_ecdsa_key
   # Verify
   sudo ls /etc/ssh/
   # The result should have `ssh_server_ecdsa_key` and `ssh_server_ecdsa_key.pub`
   ```

2. **Set Permissions for Private Key:**

   ```bash
   # rw------- (110 000 000)
   sudo chmod 600 /etc/ssh/ssh_host_ecdsa_key
   ```

3. **Configure SSH to Use ECC Key:**
   Edit `/etc/ssh/sshd_config` and ensure the following lines are set:

   ```bash
   sudo nano /etc/ssh/sshd_config
   Port 22
   HostKey /etc/ssh/ssh_server_ecdsa_key
   TrustedUserCAKeys /etc/ssh/ssh_server_ecdsa_key.pub
   PubkeyAuthentication yes
      # Ciphers and MACs
   Ciphers aes256-gcm@openssh.com,aes256-ctr
   MACs hmac-sha2-512,hmac-sha2-256
   ```

4. **Restart SSH Service:**

   ```bash
   #Add the Key to the Agent
      sudo chmod 600 /etc/ssh/ssh_server_ecdsa_key
      sudo chown $USER:$USER /etc/ssh/ssh_server_ecdsa_key
      sudo systemctl restart ssh
   #Checking
      sudo systemctl status ssh
   ```

---

## 3. Sign Certificate for Clients

1. **Generate Client's ECC Key Pair:**

   ```bash
   ssh-keygen -t ecdsa -b 521 -f ~/.ssh/client_ecdsa_key
   ```

2. **Sign Client's Public Key:**
   - Assume the server acts as a Certificate Authority (CA):

     ```bash
     ssh-keygen -s /etc/ssh/ssh_server_ecdsa_key -I client_cert_id ~/.ssh/client_ecdsa_key.pub
     ```

3. **Copy Signed Certificate to the Client:**

   ```bash
   # Copy the file client_ecdsa_key-cert.pub tp your client
   scp ~/.ssh/client_ecdsa_key-cert.pub user@client:/home/user/.ssh/
   ```

4. **Enable Certificate Authentication on Server:**
   Add the CA public key to `/etc/ssh/sshd_config`:

   ```ini
   TrustedUserCAKeys /etc/ssh/ssh_server_ecdsa_key.pub
   ```

5. **Restart SSH Service:**

   ```bash
   sudo systemctl restart ssh
   ```

---

## 4. Set Ciphers and MACs for Servers

1. **Edit SSH Configuration:**
   Open `/etc/ssh/sshd_config` and specify the preferred ciphers and MACs:

   ```ini
   Ciphers aes256-gcm@openssh.com,aes256-ctr
   MACs hmac-sha2-512,hmac-sha2-256
   ```

2. **Save and Restart SSH Service:**

   ```bash
   sudo systemctl restart ssh
   ```

3. **Test Configuration:**
   Check SSH configuration for errors:

   ```bash
   sudo sshd -t
   ```

---

## 5. Remote Login Using Password or Certificate

1. **Enable Password Authentication (if needed):**
   Edit `/etc/ssh/sshd_config`:

   ```ini
   PasswordAuthentication yes
   ```

2. **Enable Certificate Authentication:**
   Ensure the following line exists in `/etc/ssh/sshd_config`:

   ```ini
   PubkeyAuthentication yes
   ```

3. **Restart SSH Service:**

   ```bash
   sudo systemctl restart ssh
   ```

4. **Test Login with Password:**

   ```bash
   ssh user@server_ip
   eg. ssh ngoctu@172.17.199.227
   ```

5. **Test Login with Certificate:**
   From the client machine:

   ```bash
   ssh -i ~/.ssh/client_ecdsa_key user@server_ip
   ```

---

## Additional Tips

- **Harden Security:**
  - Disable root login: Set `PermitRootLogin no` in `/etc/ssh/sshd_config`.
  - Limit users: Use `AllowUsers` or `AllowGroups` directives in `sshd_config`.

- **Monitor Logs:**
  View SSH logs for troubleshooting:

  ```bash
  sudo tail -f /var/log/auth.log
  ```

- **Keep OpenSSH Updated:**
  Ensure the SSH server is updated for the latest security patches:

  ```bash
  sudo apt update && sudo apt upgrade openssh-server
  ```
