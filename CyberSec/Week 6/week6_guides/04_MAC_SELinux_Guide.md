
# Mandatory Access Control (MAC) - Using SELinux in Ubuntu

## Step 1: What is SELinux?
- **SELinux** (Security-Enhanced Linux) is a powerful Mandatory Access Control (MAC) framework.
- It enforces access control policies to confine programs and system processes, reducing the potential impact of vulnerabilities.
- Policies in SELinux define access rules based on:
  - Users
  - Roles
  - Types (labels)
  - Security contexts

---

## Step 2: Install SELinux
To use SELinux, you must install and enable it on your Ubuntu system.

### Install SELinux
1. Update the package list:
   ```bash
   sudo apt update
   ```
2. Install SELinux packages:
   ```bash
   sudo apt install selinux selinux-utils selinux-basics policycoreutils
   ```

### Enable SELinux
1. Enable SELinux with:
   ```bash
   sudo selinux-activate
   ```
2. Reboot the system to apply changes:
   ```bash
   sudo reboot
   ```

---

## Step 3: Check SELinux Status
To verify if SELinux is enabled and its mode:
```bash
sestatus
```

### Example Output:
```
SELinux status:                 enabled
Current mode:                   enforcing
Policy version:                 32
```
- **Enforcing**: SELinux policies are enforced.
- **Permissive**: SELinux logs violations but does not enforce policies.
- **Disabled**: SELinux is turned off.

---

## Step 4: SELinux Modes

### Enforcing Mode
- Fully enforces SELinux policies.
- Blocks any action not explicitly allowed.

### Permissive Mode
- Logs policy violations but does not enforce them.
- Useful for debugging.

### Changing Modes
- Temporarily switch to permissive mode:
  ```bash
  sudo setenforce 0
  ```
- Switch back to enforcing mode:
  ```bash
  sudo setenforce 1
  ```
- To permanently set the mode, edit `/etc/selinux/config`:
  ```bash
  SELINUX=enforcing
  ```

---

## Step 5: Managing SELinux Policies

### 1. List File Security Contexts
View the SELinux labels of files:
```bash
ls -Z
```

### 2. Relabel Files
Relabel a file or directory with the default SELinux context:
```bash
sudo restorecon -v /path/to/file
```

### 3. Modify Policies
Use `semanage` to manage SELinux policies.

#### Example: Allow a Web Server to Bind on Port 8080
1. Check if the port is allowed:
   ```bash
   sudo semanage port -l | grep 8080
   ```
2. Add the port if it's not allowed:
   ```bash
   sudo semanage port -a -t http_port_t -p tcp 8080
   ```

---

## Step 6: Example: Confine `nginx` with SELinux
1. Install nginx:
   ```bash
   sudo apt install nginx
   ```

2. Check the SELinux context for nginx files:
   ```bash
   ls -Z /etc/nginx/
   ```

3. Allow nginx to serve files from a custom directory:
   - Relabel the directory with `httpd_sys_content_t`:
     ```bash
     sudo chcon -R -t httpd_sys_content_t /path/to/your/directory
     ```

4. Restart nginx:
   ```bash
   sudo systemctl restart nginx
   ```

---

## Step 7: Monitor SELinux Logs
To debug issues or check violations:
```bash
sudo ausearch -m AVC,USER_AVC
```

---

## Encourage Audience Participation
- Have participants switch SELinux between enforcing and permissive modes.
- Ask them to modify a file's security context using `chcon` and `restorecon`.
- Discuss logs from `sudo ausearch -m AVC` for denied actions.
