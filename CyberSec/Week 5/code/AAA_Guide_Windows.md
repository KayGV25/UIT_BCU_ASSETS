
# AAA Guide on Windows OS

This guide walks you through the following steps:
1. Creating user groups
2. Creating users and assigning them to groups
3. Setting up files and folders with access control
4. Logging in as users to test access
5. Checking Windows Event Viewer for auditing

## Step 1: Create User Groups

1. Open **Computer Management**:
   - Right-click on **This PC** on your desktop or in File Explorer.
   - Select **Manage**.
2. In the Computer Management window, navigate to **Local Users and Groups** > **Groups**.
3. Right-click in the Groups section and select **New Group**.
4. Name your groups (e.g., `Group1` and `Group2`), then click **Create**.

## Step 2: Create Users and Assign Them to Groups

1. In **Computer Management**, navigate to **Local Users and Groups** > **Users**.
2. Right-click in the Users section and select **New User** to create three new users (e.g., `User1`, `User2`, and `User3`).
3. For each user:
   - Set a **username** and **password**.
   - Ensure **User must change password at next logon** is unchecked.
   - Click **Create** and then **Close**.
4. Assign users to groups:
   - Right-click on each user and select **Properties**.
   - In the **Properties** window, go to the **Member Of** tab.
   - Click **Add...**, enter the group name (e.g., `Group1` or `Group2`), and click **OK**.

## Step 3: Create Files or Folders and Implement Access Control

1. Create a folder (e.g., `TestFolder`) and some files within it.
2. Right-click on the folder and select **Properties**.
3. Go to the **Security** tab and click **Edit** to set access permissions.
4. Click **Add...** to add specific groups (`Group1` and `Group2`) or users (`User1`, `User2`, etc.).
5. Set permissions (e.g., `Read`, `Write`, or `Full Control`) for each group or user, and then click **OK**.

## Step 4: Login with Users and Test Access

1. Log out or use **Switch User** to log in as each user (`User1`, `User2`, or `User3`).
2. Try accessing the `TestFolder` and files:
   - Confirm that users have permissions according to the settings you configured.
   - For example, `User1` might have `Read` access while `User2` has `Full Control`.

## Step 5: Check Windows Events for Auditing

1. Open **Event Viewer**:
   - Press `Win + R`, type `eventvwr.msc`, and press **Enter**.
2. In Event Viewer, navigate to **Windows Logs** > **Security**.
3. Look for events related to logins and access control:
   - **Event ID 4624**: A successful logon.
   - **Event ID 4625**: A failed logon attempt.
   - **Event ID 4663**: File access events, if auditing is enabled.

To enable file access auditing:
   - Right-click on the folder (`TestFolder`) and select **Properties**.
   - Go to the **Security** tab and click **Advanced**.
   - Go to the **Auditing** tab and click **Add...**.
   - Select the users or groups you want to audit and set the types of access to audit (e.g., **Read**, **Write**).
   - Click **OK** to save the auditing settings.

Now, any access to the folder by the specified users or groups will be logged in Event Viewer under the Security log.

---

This completes the AAA setup on Windows OS.
