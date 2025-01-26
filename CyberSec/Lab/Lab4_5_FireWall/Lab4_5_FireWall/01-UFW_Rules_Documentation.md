
# UFW Rules Documentation

## 1. Rules for Network Layers

These rules manage traffic based on network protocols and routing. They operate at lower layers of the OSI model (Layer 3(IP) and Layer 4(port)).

---

### Basic Traffic Rules
- **Allow All Traffic on a Specific Port**:
  ```bash
  sudo ufw allow 22
  ```
  Allows incoming traffic on port `22` (typically SSH).

- **Deny Traffic on a Specific Port**:
  ```bash
  sudo ufw deny 22
  ```
  Denies incoming traffic on port `22`.

- **Allow Traffic on a Port with a Specific Protocol**:
  ```bash
  sudo ufw allow 1194/udp
  ```
  Allows incoming traffic on port `1194` using the UDP protocol.

- **Block Traffic from a Specific IP**:
  ```bash
  sudo ufw deny from 192.168.1.100
  ```
  Denies all traffic originating from the IP `192.168.1.100`.

- **Block Traffic from a Subnet**:
  ```bash
  sudo ufw deny from 192.168.1.0/24
  ```
  Denies all traffic from the subnet `192.168.1.0/24`.

---

### Advanced Routing Rules
- **Route Forwarding Between Interfaces**:
  ```bash
  sudo ufw route allow in on tun0 out on eth0
  ```
  Allows traffic to be routed between `tun0` (VPN interface) and `eth0` (internet interface).

- **Limit Connections to prevent DDOS**:

```bash
# Application name 
  sudo ufw limit ssh
# Or port
  sudo ufw limit 22
# Or port/protocols
 sudo ufw limit 53/udp
# Remove limit
sudo ufw delete limit ssh
...

```
  Applies a rate limit to SSH connections to prevent brute-force attacks. Default Rate-Limiting: **6 connections within 30 seconds from a single IP address**

- **Set Default Behavior**:
  - Deny all incoming traffic:
    ```bash
    sudo ufw default deny incoming
    ```
  - Allow all outgoing traffic:
    ```bash
    sudo ufw default allow outgoing
    ```

---

### Interface-Specific Rules
- **Allow Traffic on a Specific Interface**:
  ```bash
  sudo ufw allow in on eth0
  ```
  Allows traffic only on `eth0` (e.g., Ethernet interface).

- **Block Traffic on a Specific Interface**:
  ```bash
  sudo ufw deny in on wlan0
  ```
  Denies all incoming traffic on the `wlan0` interface (e.g., WiFi).

---

## 2. Rules for Application Layer

These rules manage traffic for specific applications and services, working at the higher layers of the OSI model (Layer 7).

---

### Application Profiles
- **List Available Application Profiles**:
  ```bash
  sudo ufw app list
  ```
  Lists all predefined application profiles available for UFW.

- **Allow Traffic for an Application**:
  ```bash
  sudo ufw allow "OpenSSH"
  ```
  Allows incoming traffic for the `OpenSSH` application profile.

- **Deny Traffic for an Application**:
  ```bash
  sudo ufw deny "Apache"
  ```
  Denies incoming traffic for the `Apache` application profile.

---

### Logging and Monitoring
- **Enable Logging**:
  ```bash
  sudo ufw logging on
  ```
  Enables logging of UFW traffic.

- **Set Logging Level**:
  ```bash
  sudo ufw logging medium
  ```
  Sets the logging level (options: `low`, `medium`, `high`, `full`).

---

### DNS and HTTP/HTTPS Rules
- **Allow DNS Traffic**:
  ```bash
  sudo ufw allow 53
  ```
  Allows DNS traffic on port `53`.

- **Allow HTTP and HTTPS Traffic**:
  ```bash
  sudo ufw allow 80
  sudo ufw allow 443
  ```
  Allows HTTP (`80`) and HTTPS (`443`) traffic.

- **Block HTTP Traffic**:
  ```bash
  sudo ufw deny 80
  ```
  Blocks all HTTP traffic.

---

### Managing Services by Ports
- **Allow Specific Service Ports**:
  - Allow SSH:
    ```bash
    sudo ufw allow ssh
    ```
  - Allow OpenVPN:
    ```bash
    sudo ufw allow 1194/udp
    ```
  - Allow MySQL:
    ```bash
    sudo ufw allow 3306
    ```

- **Deny Specific Service Ports**:
  - Deny FTP:
    ```bash
    sudo ufw deny 21
    ```
  - Deny SMTP:
    ```bash
    sudo ufw deny 25
    ```

---

### Default Application Layer Rules
- Allow all outgoing traffic:
  ```bash
  sudo ufw default allow outgoing
  ```
- Deny all incoming traffic:
  ```bash
  sudo ufw default deny incoming
  ```
