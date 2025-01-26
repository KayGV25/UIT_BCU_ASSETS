
# AAA Guide on Ubuntu Linux

This guide walks you through the following steps on Ubuntu Linux:

1. Creating user groups
2. Creating users and assigning them to groups
3. Setting up files and folders with access control
4. Logging in as users to test access
5. Checking logs for auditing

## Step 1: Create User Groups

1. Open a terminal.
2. Use the following commands to create two groups, `group1` and `group2`:

   ```bash
   sudo groupadd group1
   sudo groupadd group2
   ```

## Step 2: Create Users and Assign Them to Groups

1. Create three new users (`user1`, `user2`, and `user3`) with the following commands:

   ```bash
   sudo adduser user1
   sudo adduser user2
   sudo adduser user3
   ```

   Follow the prompts to set up passwords for each user.
2. Assign each user to a group. For example:

   ```bash
   sudo usermod -aG group1 user1
   sudo usermod -aG group2 user2
   sudo usermod -aG group2 user3
   ```

## Step 3: Create Files or Folders and Implement Access Control

1. Create a directory (e.g., `TestFolder`) and set specific permissions for each group:

   ```bash
   sudo mkdir /home/TestFolder
   sudo chown :group1 /home/TestFolder
   sudo chmod 770 /home/TestFolder  # Full access for owner and group, no access for others
   ```

2. To allow `group2` to access the folder with read-only permissions, add an ACL (Access Control List):

   ```bash
   sudo setfacl -m g:group2:rx /home/TestFolder
   ```

## Step 4: Login with Users and Test Access

1. Switch users in the terminal to `user1`, `user2`, or `user3` using the following command:

   ```bash
   su - user1  # Replace 'user1' with 'user2' or 'user3' as needed
   ```

2. Try accessing the `TestFolder` directory:
   - Verify that `user1` has full access (if they belong to `group1`).
   - Confirm that `user2` and `user3` have only read-only access (if they belong to `group2`).

## Step 5: Check Logs for Auditing

1. Ubuntu Linux logs authentication and access events in `/var/log/auth.log`.
2. Use the following command to view recent log entries:

   ```bash
   sudo tail /var/log/auth.log
   ```

3. You can also monitor specific events, such as user login attempts and group access events.

---

This completes the AAA setup on Ubuntu Linux.
