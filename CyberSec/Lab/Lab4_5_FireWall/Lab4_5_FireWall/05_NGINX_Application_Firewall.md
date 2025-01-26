
# Guide: Setting Up an Application Firewall for NGINX

An **application firewall** for NGINX helps secure your web applications by filtering traffic at the application layer, inspecting requests for malicious content, and preventing attacks such as SQL injection, cross-site scripting (XSS), and file inclusion.

---

## **1. Introduction to NGINX Application Firewalls**

### **What is an Application Firewall?**

- An application firewall works at the application layer (Layer 7) to monitor and filter HTTP/HTTPS requests and responses.
- It protects web applications from common attacks like:
  - **SQL Injection**
  - **Cross-Site Scripting (XSS)**
  - **Remote File Inclusion**

### **Tools for NGINX Application Firewalls**

1. **ModSecurity**: A widely used, open-source web application firewall.
2. **NAXSI**: A lightweight WAF module for NGINX, focused on preventing XSS and SQL injection.

This guide focuses on **ModSecurity**, which provides robust protection and integrates seamlessly with NGINX.

---

## **2. Installing ModSecurity for NGINX**

1. **Update the System**:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install NGINX with ModSecurity Support**:

   ```bash
   sudo apt install nginx libnginx-mod-security -y
   ```

3. **Verify Installation**:
   Check if the ModSecurity module is loaded:

   ```bash
   nginx -V 2>&1 | grep -- '--with-http_modsecurity_module'
   ```

4. **Install the OWASP Core Rule Set (CRS)**:
   The CRS provides a set of pre-configured rules to block common attacks.

   ```bash
   sudo apt install modsecurity-crs
   sudo cp /usr/share/modsecurity-crs/crs-setup.conf.example /etc/modsecurity/crs-setup.conf
   ```

5. **Enable ModSecurity**:
   Enable the ModSecurity configuration in `/etc/nginx/nginx.conf`:

   ```nginx
   http {
       include /etc/nginx/modsecurity/modsecurity.conf;

       server {
           ...
       }
   }
   ```

---

## **3. Configuring ModSecurity**

1. **Edit the ModSecurity Configuration File**:
   Open the ModSecurity configuration file:

   ```bash
   sudo nano /etc/modsecurity/modsecurity.conf
   ```

   Update the following settings:

   ```bash
   SecRuleEngine On
   SecRequestBodyAccess On
   SecResponseBodyAccess On
   ```

2. **Enable Logging**:
   Ensure logging is enabled for better monitoring:

   ```bash
   SecAuditEngine On
   SecAuditLog /var/log/modsecurity/audit.log
   ```

3. **Customize the OWASP Core Rule Set (CRS)**:
   Edit `/etc/modsecurity/crs-setup.conf` to enable or disable specific rules.

4. **Reload NGINX**:
   Apply changes by reloading the NGINX service:

   ```bash
   sudo systemctl reload nginx
   ```

---

## **4. Testing ModSecurity**

1. **Simulate an SQL Injection**:
   Use a tool like `curl` to test the firewall:

   ```bash
   curl "http://<your-domain>/?id=1' OR '1'='1"
   ```

   The request should be blocked, and the incident logged in `/var/log/modsecurity/audit.log`.

2. **Inspect Logs**:
   View detailed logs for blocked requests:

   ```bash
   sudo tail -f /var/log/modsecurity/audit.log
   ```

---

## **5. Advanced Configurations**

### **Restricting Specific HTTP Methods**

Block HTTP methods like `PUT` and `DELETE` to prevent unauthorized access:

```bash
SecRule REQUEST_METHOD "@streq PUT" "id:1001,phase:1,deny,status:403,msg:'PUT method not allowed'"
SecRule REQUEST_METHOD "@streq DELETE" "id:1002,phase:1,deny,status:403,msg:'DELETE method not allowed'"
```

### **Rate Limiting**

Add rules to limit the number of requests per client:

```bash
SecRule IP:ATTACKER "@gt 10" "id:1003,phase:1,deny,status:429,msg:'Rate limit exceeded'"
SecAction "phase:1,id:1004,setvar:ip.attacker=+1,expirevar:ip.attacker=60"
```

---

## **6. Installing NAXSI (Alternative Lightweight WAF)**

If you prefer a simpler, lighter WAF, use NAXSI.

1. **Install NAXSI**:

   ```bash
   sudo apt install nginx-naxsi
   ```

2. **Enable NAXSI Rules**:
   Add the following to your NGINX configuration:

   ```nginx
   location / {
       include /etc/nginx/naxsi_core.rules;
   }
   ```

3. **Reload NGINX**:

   ```bash
   sudo systemctl reload nginx
   ```

4. **Customize NAXSI Rules**:
   Edit `/etc/nginx/naxsi_core.rules` to tailor the rule set for your application.

---

## **7. Monitoring and Maintenance**

1. **Monitor Logs**:
   - For ModSecurity:

     ```bash
     sudo tail -f /var/log/modsecurity/audit.log
     ```

   - For NAXSI:

     ```bash
     sudo tail -f /var/log/nginx/error.log
     ```

2. **Update Rule Sets**:
   - Regularly update the OWASP Core Rule Set:

     ```bash
     sudo apt update && sudo apt upgrade
     ```

3. **Test the Firewall Regularly**:
   - Use tools like `curl`, `nmap`, and vulnerability scanners to test the firewall.

---

## **8. Best Practices**

1. **Enable Only Required Rules**:
   - Disable unnecessary rules in `/etc/modsecurity/crs-setup.conf` to avoid blocking legitimate traffic.

2. **Use a Combination of WAFs**:
   - Combine ModSecurity with NAXSI for layered protection.

3. **Enable Rate Limiting**:
   - Implement IP-based rate limiting to prevent DDoS attacks.

4. **Monitor Traffic**:
   - Regularly inspect logs and integrate with monitoring tools like Fail2Ban or ELK stack for better insights.

---

This guide provides comprehensive steps to set up an application firewall for NGINX using ModSecurity or NAXSI. Let me know if you need further assistance!
