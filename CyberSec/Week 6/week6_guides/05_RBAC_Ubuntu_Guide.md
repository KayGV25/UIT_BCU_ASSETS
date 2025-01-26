
# Role-Based Access Control (RBAC) in Ubuntu

## Step 1: What is RBAC?

- **RBAC** is a security model where permissions are assigned to roles, and users inherit these permissions by being assigned to roles.
- In Ubuntu, **groups** are used as roles to implement RBAC.

---

## Step 2: Managing Groups in Ubuntu

### 1. Create a New Group

To create a group:

```bash
sudo groupadd groupname
```

**Example**:

```bash
sudo groupadd developers
```

This creates a group named `developers`.

---

### 2. Add a User to a Group

To assign a user to a group:

```bash
sudo usermod -aG groupname username
```

**Example**:

```bash
sudo usermod -aG developers alice
```

This adds the user `alice` to the `developers` group.

---

### 3. View Group Membership

To check which groups a user belongs to:

```bash
groups username
```

**Example**:

```bash
groups alice
```

Output might show:

```
alice : alice developers
```

---

## Step 3: Assigning Permissions to Groups

### 1. Assign File or Directory Ownership

To set a group as the owner of a file or directory:

```bash
sudo chown :groupname /path/to/file_or_directory
```

**Example**:

```bash
sudo chown :developers /var/www/project
```

This assigns ownership of `/var/www/project` to the `developers` group.

---

### 2. Set Group Permissions

To define what the group can do with the file or directory:

```bash
sudo chmod g+rwx /path/to/file_or_directory
```

**Example**:

```bash
sudo chmod g+rwx /var/www/project
```

This grants the `developers` group **read**, **write**, and **execute** permissions for `/var/www/project`.

---

### 3. Default Group Permissions

To ensure that files created in a directory inherit the group ownership:

1. Set the **sticky group bit**:

   ```bash
   sudo chmod g+s /path/to/directory
   ```

**Example**:

```bash
sudo chmod g+s /var/www/project
```

Files created in `/var/www/project` will automatically belong to the `developers` group.

---

## Step 4: Use `sudo` for Elevated Privileges

### 1. Add Users to the `sudo` Group

Users in the `sudo` group can execute commands as the superuser:

```bash
sudo usermod -aG sudo username
```

**Example**:

```bash
sudo usermod -aG sudo alice
```

### 2. Customize `sudo` Access

To grant specific permissions to a group:

1. Open the sudoers file:

   ```bash
   sudo visudo
   ```

2. Add a rule for the group:

   ```bash
   %developers ALL=(ALL) NOPASSWD: ALL
   ```

   This allows the `developers` group to run all commands without a password prompt.

---

## Step 5: Real-World Example: Managing a Development Team

### Scenario

You have a directory `/var/www/project` where only developers should have access.

1. Create the `developers` group:

   ```bash
   sudo groupadd developers
   ```

2. Add team members to the group:

   ```bash
   sudo usermod -aG developers alice
   sudo usermod -aG developers bob
   ```

3. Set group ownership for the directory:

   ```bash
   sudo chown -R :developers /var/www/project
   ```

4. Set group permissions:

   ```bash
   sudo chmod -R g+rwx /var/www/project
   ```

5. Enable group inheritance for new files:

   ```bash
   sudo chmod g+s /var/www/project
   ```

Now, all files created in `/var/www/project` will automatically belong to the `developers` group.

---

## Step 6: Verify Permissions

1. Check ownership and permissions:

   ```bash
   ls -l /var/www/project
   ```

2. Test group access by switching to a group member:

   ```bash
   su alice
   cd /var/www/project
   ```

---

## Step 7: Best Practices for RBAC in Ubuntu

1. Use descriptive group names to reflect roles (e.g., `admins`, `developers`, `auditors`).
2. Regularly review group membership:

   ```bash
   sudo getent group
   ```

3. Avoid assigning direct permissions to users; always use groups.

---

This guide covers creating and managing groups, assigning permissions, and implementing RBAC in Ubuntu. Let me know if you need further clarification!
