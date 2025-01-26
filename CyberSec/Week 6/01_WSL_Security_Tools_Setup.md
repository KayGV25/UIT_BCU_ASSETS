
# Step-by-Step Guide for WSL and Security Tools Setup

## Step 1: Enable Windows Features for WSL

1. Open **PowerShell** as Administrator.
2. Run the following commands to enable required features:

   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

3. Restart your computer to apply changes.

4. After the restart, set WSL 2 as the default version:

   ```powershell
   wsl --install
   wsl --set-default-version 2
   wsl --update
   ```

## Step 2: Install a Linux Distribution

1. Open **Microsoft Store**.
2. Search for a Linux distribution like **Ubuntu 22.04**.
3. Click **Get** to download and install it.
4. Open PowerShell or cmd **as Administrator**

```bash
   wsl --install
```

5. Set up your username and password during the first run:
   - Create a username and password for your Linux instance.

6. Shutdow nd resstart WSL in PowerShell or cmd **as Administrator**

```bash
wsl --shutdown
wsl -d ubuntu
sudo apt-get update
```

## Step 3: Setup Access Control Tools in WSL

### **Discretionary Access Control (DAC)**

DAC is the default permission model in Linux.

1. **Check File Permissions:**

   ```bash
   # Check a list files in current folder or path 
   sudo ls /path/to/your/folder
   # Check File Permissions
   sudo ls -l /path/to/filename
   ```

2. **Change Permissions:**

   ```bash
   sudo chmod 750 /path/to/filename
   # Read (r), Write (w), Execute (x); Owner (u), Group (g), Others (o)
   # --- there binary for each group: u:rwx; g:rwx; o:rwx;
   # 750: 7=111-->Owner=rwx; 5=101 ---> Group=r-x; 0=000 --> Others=---;
   ```

3. **Change Ownership:**

   ```bash
   chown user:group /path/to/filename
   ```

### **Mandatory Access Control (MAC)**

Use tools like **AppArmor** or **SELinux** for MAC.

#### AppArmor Setup

1. **Install AppArmor:**

   ```bash
   sudo apt update
   sudo apt install apparmor
   ```

2. **Enable AppArmor Profiles:**
   - Enable profiles for services or applications.
   - Modify profiles in `/etc/apparmor.d/`.

#### SELinux Setup for MAC

1. **Install SELinux:**

   ```bash
   sudo apt install policycoreutils selinux-basics selinux-utils -y

   ```

2. **Enable SELinux:**

   ```bash
   sudo selinux-activate
   sudo reboot -i
   # Checking
   getenforce
   ```

### **Role-Based Access Control (RBAC)**

Use `sudo` or external tools for RBAC.

1. **Edit Sudoers File:**

   ```bash
   sudo visudo
   ```

2. Add specific permissions for users or groups.

### **Attribute-Based Access Control (ABAC)**

Implement ABAC using policy engines like **Open Policy Agent (OPA)**.

1. **Install OPA:**

   ```bash
   curl -L -o opa https://openpolicyagent.org/downloads/v0.70.0/opa_linux_amd64_static
   chmod +x opa
   sudo mv opa /usr/local/bin/
   ```

### **Policy-Based Access Control (PBAC)**

Configure PBAC using `iptables` or `firewalld`.

```bash
sudo apt-get install iptables
sudo apt-get install firewalld
```
---

## Step 4: Setup Firewall Tools

### UFW (Uncomplicated Firewall)

1. **Install UFW:**

   ```bash
   sudo apt install ufw
   ```

2. **Enable UFW:**

   ```bash
   sudo ufw enable
   ```

3. **Add Rules:**
   - Allow SSH:

     ```bash
     sudo ufw allow ssh
     ```

   - Deny specific IPs:

     ```bash
     sudo ufw deny from 192.168.1.100
     ```

### iptables

1. **Install iptables:**

   ```bash
   sudo apt install iptables
   ```

2. **Add Rules:**

   ```bash
   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   ```

---

## Step 5: Setup VPN Tools

### OpenVPN

1. **Install OpenVPN:**

   ```bash
   sudo apt install openvpn
   ```

2. **Download and Configure VPN Profiles:**
   - Obtain `.ovpn` files from your VPN provider.
   - Place them in `/etc/openvpn/`.

3. **Connect to a VPN:**

   ```bash
   sudo openvpn --config /etc/openvpn/your-vpn-config.ovpn
   ```

### WireGuard

1. **Install WireGuard:**

   ```bash
   sudo apt install wireguard
   ```

2. **Generate Keys:**

   ```bash
   wg genkey | tee privatekey | wg pubkey > publickey
   ```

3. **Configure `/etc/wireguard/wg0.conf`:**

   ```bash
   [Interface]
   PrivateKey = your-private-key
   Address = 10.0.0.1/24

   [Peer]
   PublicKey = peer-public-key
   Endpoint = peer-endpoint:51820
   AllowedIPs = 0.0.0.0/0
   ```

4. **Start WireGuard:**

   ```bash
   sudo wg-quick up wg0
   ```

---

This guide ensures you can configure WSL, access control, firewall, and VPN tools step by step. Let me know if you need further assistance!
