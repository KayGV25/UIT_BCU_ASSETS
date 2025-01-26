
# Discretionary Access Control (DAC) Guide on Ubuntu Linux

This guide explains how to set up Discretionary Access Control (DAC) on Ubuntu Linux, allowing specific users or groups to access files and folders according to customized permissions.

## Step 1: Create User Groups

1. Open a terminal.
2. Use the following commands to create two groups, `managers` and `employees`:

   ```bash
   sudo groupadd managers
   sudo groupadd employees
   ```

## Step 2: Create Users and Assign Them to Groups

1. Create new users (`userA`, `userB`, and `userC`) with the following commands:

   ```bash
   sudo adduser managerA
   sudo adduser employeeB
   sudo adduser emoloyeeC
   ```

   Follow the prompts to set up passwords for each user.
2. Assign each user to a group. For example:

   ```bash
   sudo usermod -aG managers userA
   sudo usermod -aG employees userB
   sudo usermod -aG employees userC
   ```

## Step 3: Create Files or Folders and Apply DAC Permissions

1. Create a directory (e.g., `ProjectFiles`) and set specific permissions for each group:

   ```bash
   sudo mkdir /home/ProjectFiles
   sudo chown :managers /home/ProjectFiles
   sudo chmod 770 /home/ProjectFiles  # Full access for owner and group, no access for others
   ```

2. To allow the `employees` group to access the folder with read-only permissions, add an Access Control List (ACL):

   ```bash
   sudo setfacl -m g:employees:rx /home/ProjectFiles
   ```

## Step 4: Testing Access Control

1. Switch users in the terminal to `userA`, `userB`, or `userC` using the following command:

   ```bash
   su - userA  # Replace 'userA' with 'userB' or 'userC' as needed
   ```

2. Try accessing the `ProjectFiles` directory:
   - Verify that `userA` (in `managers` group) has full access.
   - Confirm that `userB` and `userC` (in `employees` group) have read-only access.

## Step 5: View Access Events in Logs (Optional)

1. Ubuntu Linux logs file access and permission events in `/var/log/auth.log`.
2. Use the following command to view recent log entries:

   ```bash
   sudo tail /var/log/auth.log
   ```

3. You can also monitor access to specific directories using audit tools (e.g., `auditd`), which can be installed and configured for detailed access monitoring.

To install `auditd` and configure auditing for `ProjectFiles`:

   ```bash
   sudo apt update
   sudo apt install auditd
   sudo auditctl -w /home/ProjectFiles -p rwxa -k project_access
   ```

4. View audit logs using:

   ```bash
   sudo ausearch -k project_access
   ```

---

This completes the setup for Discretionary Access Control (DAC) on Ubuntu Linux.
