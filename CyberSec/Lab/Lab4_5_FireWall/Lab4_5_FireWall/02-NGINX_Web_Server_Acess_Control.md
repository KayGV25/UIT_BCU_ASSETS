
# Step-by-Step Guide: NGINX Web Server with Access Control

## **Step 1: Installing and Setting Up NGINX**

1. **Update the System**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install NGINX**:
   ```bash
   sudo apt-get install nginx -y
   ```

3. **Start and Enable the NGINX Service**:
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

4. **Verify NGINX Installation**:
   - Visit your server's IP address in a web browser (e.g., `http://<your-server-ip>` or http://localhost/).
   - You should see the default NGINX welcome page.

---

## **Step 2: Configuring TLS with Certificates with Certificate Authority Let’s Encrypt and OpenSSL**

### **Option 1: Using Let’s Encrypt**
1. **Set Up Your Domain Name**
- Edit the DNS settings to point to your server's IP address:

A Record: @yourserver IP
CNAME Record: Host-Value:www-example.com
- Allow up to 48 hours for DNS propagation.
- Verify: Use tools like `nslookup` or `dig` to confirm DNS resolution:
  ```bash
  nslookup example.com
  dig example.com +short
  ```

2. **Install Certbot for Let’s Encrypt**:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

3. **Obtain a TLS Certificate**:
   Replace `<your-domain>` with your actual domain name:
   ```bash
   sudo certbot --nginx -d <your-domain> -d www.<your-domain>
   ```

4. **Verify Auto-Renewal**:
   ```bash
   sudo certbot renew --dry-run
   ```

5. **Test HTTPS**:
   - Visit `https://<your-domain>` to ensure the certificate is active and valid.

### **Option 2: Using Custom Certificates**

1. **Generate a Self-Signed Certificate**:
   ```bash
   sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
   ```

2. **Create a Diffie-Hellman Parameter**:
   ```bash
   sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
   ```

3. **Configure NGINX for TLS**:
   Edit `/etc/nginx/sites-available/default`:
   ```nginx
   server {
       listen 443 ssl;
       server_name <your-domain>;

       ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
       ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
       ssl_dhparam /etc/ssl/certs/dhparam.pem;

       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;

       location / {
           root /var/www/html;
           index index.html;
       }
   }
   ```

### **Option 3: Using Custom Certificates**
Use your ZeroSSL certificate

4. **Reload NGINX**:
   ```bash
   sudo systemctl reload nginx
   ```

---

## **Step 3: Role-Based Access Control (RBAC)**

### **Using Basic Authentication for Roles**

1. **Install the htpasswd Tool**:
   ```bash
   sudo apt install apache2-utils -y
   ```

2. **Create User Credentials**:
   Replace `username` with the role/user you want to create:
   ```bash
   sudo htpasswd -c /etc/nginx/.htpasswd username
   ```

3. **Edit the NGINX Configuration**:
   Add this block to `/etc/nginx/sites-available/default`:
   ```nginx
   location /admin {
       auth_basic "Restricted Access";
       auth_basic_user_file /etc/nginx/.htpasswd;
   }
   ```

4. **Test RBAC**:
   - Access `http://<your-domain>/admin` and log in with your username and password.

---

## **Step 4: Attribute-Based Access Control (ABAC)**

### **Using IP Address Restrictions**

1. **Restrict Access to Specific Attributes**:
   Add this block to `/etc/nginx/sites-available/default`:
   ```nginx
   location /admin {
       allow 192.168.1.0/24;  # Allow a specific subnet
       allow 203.0.113.5;     # Allow a specific IP
       deny all;              # Deny all other access
   }
   ```

2. **Reload NGINX**:
   ```bash
   sudo systemctl reload nginx
   ```

3. **Test ABAC**:
   - Access `/admin` from allowed and denied IPs to confirm the behavior.

---

## **Step 5: Network Access Control (NAC) Using UFW**

1. **Allow HTTP and HTTPS Traffic**:
   ```bash
   sudo ufw allow 'Nginx Full'
   ```

2. **Restrict SSH to Specific IPs**:
   Replace `192.168.1.100` with your allowed IP:
   ```bash
   sudo ufw allow from 192.168.1.100 to any port 22
   ```

3. **Block All Other Incoming Traffic**:
   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   ```

4. **Enable UFW**:
   ```bash
   sudo ufw enable
   ```

5. **Verify Firewall Rules**:
   ```bash
   sudo ufw status verbose
   ```

---

## **Step 6: Policy-Based Access Control (PBAC)**

### **Restrict HTTP Methods**
Limit allowed HTTP methods (e.g., allow only `GET` and `POST`):
```nginx
location /api {
    limit_except GET POST {
        deny all;
    }
}
```

### **Enforce Request Body Size Limits**
Prevent abuse with overly large requests:
```nginx
http {
    client_max_body_size 1M;
}
```

---

## **Best Practices**

1. **Strong TLS Configuration**:
   Ensure only strong ciphers are used:
   ```nginx
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_ciphers HIGH:!aNULL:!MD5;
   ```

2. **Enable Logging**:
   Monitor `/var/log/nginx/access.log` and `/var/log/nginx/error.log`.

3. **Regular Audits**:
   - Rotate credentials for RBAC.
   - Update ABAC rules to reflect changing attributes.

---

This guide integrates RBAC, ABAC, PBAC, and NAC to ensure secure and controlled access to your NGINX web server.
