
# Advanced Settings: PBAC and Network Access Control for NGINX Using `iptables`

## **1. Implementing PBAC for NGINX**

### **Define Access Policies for Specific Resources**

PBAC involves defining rules based on **policies**, which may include IP addresses, times, ports, or request types. Below are examples:

---

### **Restrict Access to Specific Resources**

For example, allow only specific users or IPs to access the `/admin` endpoint.

1. **Edit the NGINX Configuration**:
   Add the following block in `/etc/nginx/sites-available/default`:

   ```nginx
   location /admin {
       allow 192.168.1.100;  # Specific trusted IP
       allow 203.0.113.50;   # Another trusted IP
       deny all;             # Deny everyone else
   }
   ```

2. **Reload NGINX** to apply the changes:

   ```bash
   sudo systemctl reload nginx
   ```

---

### **Time-Based Access**

Allow access to a specific resource only during working hours.

1. **Add a Time-Based Rule** in the NGINX configuration:
   Use the `$time_iso8601` variable to log access attempts outside allowed hours.

   ```nginx
   location /secure {
       set $deny_access 0;

       if ($time_iso8601 !~ "^2024-11-23T0[89]|1[0-7]:[0-5][0-9]:") {
           set $deny_access 1;
       }

       if ($deny_access) {
           return 403;
       }

       root /var/www/secure;
   }
   ```

2. Reload the NGINX service:

   ```bash
   sudo systemctl reload nginx
   ```

---

### **User Agent Filtering**

Deny or allow traffic based on the client's user agent.

1. **Add the Filter in NGINX**:

   ```nginx
   location / {
       if ($http_user_agent ~* "curl|wget|bot") {
           return 403;
       }
   }
   ```

2. Reload the NGINX service:

   ```bash
   sudo systemctl reload nginx
   ```

---

## **2. Network Access Control Using `iptables`**

`iptables` provides powerful capabilities to restrict and control traffic to and from your NGINX server.

---

### **Basic Rules for NGINX**

1. **Allow HTTP and HTTPS Traffic**:

   ```bash
   sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
   ```

2. **Block Unnecessary Ports**:
   - Drop all incoming traffic except for HTTP, HTTPS, and SSH:

     ```bash
     sudo iptables -P INPUT DROP
     sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
     sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
     sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
     sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
     ```

3. **Save the Rules**:
   Persist the rules across reboots:

   ```bash
   sudo iptables-save > /etc/iptables/rules.v4
   ```

---

### **Advanced Network Access Control**

#### **1. Rate Limiting to Prevent DDoS**

Limit the number of connections per IP to prevent abuse or DoS attacks.

1. **Add a Rate Limit Rule**:
   Limit each IP to 50 new connections per minute:

   ```bash
   sudo iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 50 -j DROP
   ```

2. **Monitor Connection Limits**:
   List the connection limits currently in place:

   ```bash
   sudo iptables -L -v
   ```

---

#### **2. GeoIP-Based Blocking**

Use `iptables` with GeoIP to block traffic from specific countries.

1. **Install the Required Package**:

   ```bash
   sudo apt install xtables-addons-common
   sudo apt install geoip-database
   ```

2. **Create GeoIP Rules**:
   For example, block traffic from China and Russia:

   ```bash
   sudo iptables -A INPUT -m geoip --src-cc CN,RU -j DROP
   ```

---

#### **3. Restrict Access to NGINX Backend Ports**

Protect backend services (e.g., NGINX status page) from public access:

1. Block public access to a specific backend port:

   ```bash
   sudo iptables -A INPUT -p tcp --dport 8080 -s 192.168.1.0/24 -j ACCEPT
   sudo iptables -A INPUT -p tcp --dport 8080 -j DROP
   ```

---

#### **4. Implement Logging for Dropped Packets**

Log all dropped packets for auditing purposes.

1. **Add a Logging Rule**:

   ```bash
   sudo iptables -A INPUT -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
   ```

2. **View Logs**:
   Check the logs in `/var/log/syslog` or using `journalctl`:

   ```bash
   sudo journalctl -f
   ```

---

## **3. Combining PBAC and `iptables` for Enhanced Control**

### Example: Allow Access to `/secure` Endpoint Only for a Specific IP Range

1. **NGINX Configuration**:
   Add this block to `/etc/nginx/sites-available/default`:

   ```nginx
   location /secure {
       allow 192.168.1.0/24;  # Allow internal IP range
       deny all;
   }
   ```

2. **`iptables` Rule to Restrict Access**:
   Only allow traffic to `/secure` endpoint (port 443) from internal IPs:

   ```bash
   sudo iptables -A INPUT -p tcp --dport 443 -s 192.168.1.0/24 -j ACCEPT
   sudo iptables -A INPUT -p tcp --dport 443 -j DROP
   ```

---

## **Best Practices**

1. **Regularly Audit Firewall Rules**:
   - Use `sudo iptables -L -v` to review rules and logs.
   - Clean up unused or redundant rules.

2. **Implement Logging and Monitoring**:
   - Monitor `/var/log/nginx/access.log` for unauthorized attempts.
   - Use tools like `fail2ban` to ban IPs with repeated failed login attempts.

3. **Backup Firewall Rules**:
   - Save rules regularly:

     ```bash
     sudo iptables-save > /etc/iptables/rules.v4
     ```

4. **Test All Configurations**:
   - Use tools like `curl` and `nmap` to test access rules and ensure proper restrictions.

---

This guide provides a detailed approach to securing NGINX using **PBAC** and **iptables**. Let me know if you need further assistance!
