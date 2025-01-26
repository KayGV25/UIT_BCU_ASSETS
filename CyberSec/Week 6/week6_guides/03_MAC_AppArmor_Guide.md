
# Mandatory Access Control (MAC) - Using AppArmor in Ubuntu

## Step 1: What is AppArmor?

- **AppArmor** is a Mandatory Access Control (MAC) framework for Linux.
- It enforces security policies on a per-program basis, restricting what applications can do or access.
- It uses **profiles** to define what system resources (files, network, etc.) a program can access.

---

## Step 2: Install AppArmor

To use AppArmor, you need to install and enable it.

### Install AppArmor

1. Update the package list:

   ```bash
   sudo apt update
   ```

2. Install AppArmor:

   ```bash
   sudo apt install apparmor apparmor-utils
   ```

### Enable AppArmor

1. Ensure AppArmor is enabled and running:

   ```bash
   sudo systemctl status apparmor
   ```

   - If not active, start and enable it:

     ```bash
     sudo systemctl start apparmor
     sudo systemctl enable apparmor
     ```

---

## Step 3: Check AppArmor Status

To verify which profiles are loaded and their enforcement mode:

```bash
sudo aa-status
```

### Example Output

```
12 profiles are loaded.
10 profiles are in enforce mode.
2 profiles are in complain mode.
```

- **Enforce mode**: Fully restricts applications based on the profile.
- **Complain mode**: Logs violations without enforcing the restrictions.

---

## Step 4: Managing AppArmor Profiles

### 1. List Profiles

View all available profiles:

```bash
ls /etc/apparmor.d/
```

### 2. Add a New Profile

1. Use the `aa-genprof` tool to generate a profile for an application:

   ```bash
   sudo aa-genprof /path/to/application
   ```

2. Follow the interactive prompts to specify what resources the application can access.

### 3. Enable a Profile

To enforce a specific profile:

```bash
sudo aa-enforce /etc/apparmor.d/profile-name
```

### 4. Switch to Complain Mode

To debug or log an application’s behavior without enforcing restrictions:

```bash
sudo aa-complain /etc/apparmor.d/profile-name
```

### 5. Disable a Profile

To disable a profile entirely:

```bash
sudo aa-disable /etc/apparmor.d/profile-name
```

---

## Step 5: Real-World Example: Restricting Access for `nginx`

1. Install **nginx**:

   ```bash
   sudo apt install nginx
   ```

2. Generate a profile for nginx:

   ```bash
   sudo aa-genprof /usr/sbin/nginx
   ```

3. Follow the prompts to allow or deny access to specific system resources.

4. Enable the profile in enforce mode:

   ```bash
   sudo aa-enforce /etc/apparmor.d/usr.sbin.nginx
   ```

5. Verify the profile is enforced:

   ```bash
   sudo aa-status
   ```

---

## Step 6: Monitor and Log AppArmor Activity

To check logs for AppArmor denials or violations:

```bash
sudo journalctl | grep apparmor
```

---

## Encourage Audience Participation

- Ask participants to list loaded profiles using `aa-status`.
- Have them create and enforce a profile for a simple application like `/bin/bash`.
- Discuss logs from `sudo journalctl | grep apparmor` for denied operations.
