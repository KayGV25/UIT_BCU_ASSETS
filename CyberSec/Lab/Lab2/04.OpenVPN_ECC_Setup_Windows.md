
# Setting Up OpenVPN with ECC Certificates on Windows

This guide outlines the steps to set up an OpenVPN server on Windows using ECC certificates for secure VPN connections.

### Prerequisites

1. **Install OpenVPN for Windows**:
   - Download and install OpenVPN from [OpenVPN’s official site](https://openvpn.net/community-downloads/).
   - During installation, ensure that the Easy-RSA package is selected, as we’ll use it for certificate management.

2. **OpenSSL Installation**:
   - Install OpenSSL for Windows if it’s not included with your OpenVPN installation.
   - Ensure OpenSSL is added to your system’s PATH so you can use it from the command line.

---

## Step 1: Set Up Easy-RSA for ECC Key Generation

1. **Navigate to the Easy-RSA directory**:
   - Open a Command Prompt as Administrator.
   - Change to the Easy-RSA directory in your OpenVPN installation (typically located in `C:\Program Files\OpenVPN\easy-rsa`).

2. **Initialize Easy-RSA**:
   
   ```cmd
   .\EasyRSA-Start.bat
   ```

3. **Edit the Configuration for ECC**:
   - Open the `vars.bat` file in a text editor (e.g., Notepad).
   - Modify the following lines to enable ECC:

     ```bat
     set EASYRSA_ALGO=ec              :: Set algorithm to ECC
     set EASYRSA_CURVE=prime256v1     :: Choose the ECC curve (e.g., prime256v1)
     set EASYRSA_DIGEST=sha256        :: Use SHA-256 for the certificate hash
     ```

4. **Initialize the PKI (Public Key Infrastructure)**:

   ```cmd
   .\EasyRSA-Start.bat
   easyrsa init-pki
   ```

5. **Generate the CA ECC Certificate**:

   ```cmd
   easyrsa build-ca
   ```

   When prompted, set a passphrase and provide a Common Name (e.g., “OpenVPN-CA”) for your CA.

---

## Step 2: Generate Server and Client ECC Certificates

1. **Generate the Server Certificate and Key**:
   
   ```cmd
   easyrsa build-server-full server nopass
   ```

   This will generate an ECC server certificate without requiring a passphrase.

2. **Generate Client Certificates**:

   ```cmd
   easyrsa build-client-full client1 nopass
   ```

   Replace `client1` with a unique name for each client.

3. **Generate Diffie-Hellman Parameters**:

   ```cmd
   easyrsa gen-dh
   ```

4. **Generate the TLS-Auth Key**:

   ```cmd
   openvpn --genkey --secret ta.key
   ```

   The `ta.key` file will be used to secure the connection against unauthorized access.

---

## Step 3: Configure the OpenVPN Server

1. **Locate the OpenVPN Configuration Directory**:
   - By default, OpenVPN's configuration files are in `C:\Program Files\OpenVPN\config`.

2. **Create the Server Configuration File**:
   - Create a new file in the `config` directory named `server.ovpn` with the following settings:

     ```ini
     port 1194
     proto udp
     dev tun

     ca ca.crt
     cert server.crt
     key server.key
     dh dh.pem
     tls-auth ta.key 0

     # Configure TLS versions and cipher suites
     tls-version-min 1.2
     cipher AES-256-GCM
     auth SHA256
     ncp-ciphers AES-256-GCM:AES-128-GCM

     # Configure server IP and routing
     server 10.8.0.0 255.255.255.0
     ifconfig-pool-persist ipp.txt

     # Enable compression, keep-alive, and logging
     keepalive 10 120
     comp-lzo
     persist-key
     persist-tun
     status openvpn-status.log
     verb 3
     ```

   - Ensure that paths to `ca.crt`, `server.crt`, `server.key`, `dh.pem`, and `ta.key` point to the files created in Easy-RSA.

3. **Copy Certificates and Keys** to the OpenVPN configuration folder:
   - Copy `ca.crt`, `server.crt`, `server.key`, `dh.pem`, and `ta.key` from the Easy-RSA `pki` directory to `C:\Program Files\OpenVPN\config`.

---

## Step 4: Enable IP Forwarding on Windows

1. **Enable IP Routing** in Windows Registry:
   - Open the Registry Editor (`regedit`).
   - Navigate to `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters`.
   - Find or create a `DWORD` entry named `IPEnableRouter` and set its value to `1`.

2. **Restart the Computer** for changes to take effect.

---

## Step 5: Start the OpenVPN Server

1. **Start OpenVPN as Administrator**:
   - Run OpenVPN GUI as Administrator.
   - In the OpenVPN GUI, right-click the icon in the taskbar and select “Connect” for `server.ovpn`.

2. **Check OpenVPN Server Status**:
   - The OpenVPN GUI will indicate if the server starts successfully.
   - Logs are available in the OpenVPN installation directory (`C:\Program Files\OpenVPN\log`).

---

## Step 6: Set Up OpenVPN Clients

1. **Create Client Configuration**:

   Create a configuration file for the client (e.g., `client.ovpn`) with the following content:

   ```ini
   client
   dev tun
   proto udp
   remote your-server-ip 1194
   resolv-retry infinite
   nobind
   persist-key
   persist-tun
   remote-cert-tls server
   cipher AES-256-GCM
   auth SHA256
   comp-lzo
   verb 3

   <ca>
   # Insert contents of ca.crt here
   </ca>
   
   <cert>
   # Insert contents of client1.crt here
   </cert>
   
   <key>
   # Insert contents of client1.key here
   </key>
   
   <tls-auth>
   # Insert contents of ta.key here
   </tls-auth>
   ```

2. **Distribute Client Configurations**:
   - Provide each client with a unique `.ovpn` file and corresponding certificate and key.
   - Import this `.ovpn` configuration into the OpenVPN client software on each client device.

---

## Summary of Files Created

- **ca.crt**: ECC CA certificate.
- **server.crt**: ECC server certificate.
- **server.key**: ECC private key for the server.
- **client1.crt**: ECC client certificate.
- **client1.key**: ECC private key for the client.
- **ta.key**: TLS authentication key.

---

With this setup, your OpenVPN server on Windows now uses ECC certificates and strong cipher suites, supporting secure, encrypted connections for clients.
