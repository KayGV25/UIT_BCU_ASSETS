
# Discretionary Access Control (DAC) Guide on Windows OS

This guide explains how to set up Discretionary Access Control (DAC) on Windows OS, allowing specific users or groups to access files and folders according to custom permissions.

## Step 1: Create User Groups

1. Open **Computer Management**:
   - Right-click on **This PC** on your desktop or in File Explorer.
   - Select **Manage**.
2. In the Computer Management window, navigate to **Local Users and Groups** > **Groups**.
3. Right-click in the Groups section and select **New Group**.
4. Name your groups (e.g., `Managers` and `Employees`), then click **Create**.

## Step 2: Create Users and Assign Them to Groups

1. In **Computer Management**, navigate to **Local Users and Groups** > **Users**.
2. Right-click in the Users section and select **New User** to create users (e.g., `UserA`, `UserB`, and `UserC`).
3. For each user:
   - Set a **username** and **password**.
   - Ensure **User must change password at next logon** is unchecked.
   - Click **Create** and then **Close**.
4. Assign users to groups:
   - Right-click on each user and select **Properties**.
   - In the **Properties** window, go to the **Member Of** tab.
   - Click **Add...**, enter the group name (e.g., `Managers` or `Employees`), and click **OK**.

## Step 3: Create Files or Folders and Apply DAC Permissions

1. Create a folder (e.g., `ProjectFiles`) and some files within it.
2. Right-click on the folder and select **Properties**.
3. Go to the **Security** tab and click **Edit** to modify access permissions.
4. Click **Add...** to add specific users or groups (e.g., `Managers`, `Employees`, `UserA`).
5. Set custom permissions for each group or user:
   - **Managers** group may have `Full Control`.
   - **Employees** group may have `Read` or `Write` access only.
   - Individual users can have customized permissions, such as `Modify` or `Read`.

## Step 4: Testing Access Control

1. Log out or use **Switch User** to log in as each user (`UserA`, `UserB`, or `UserC`).
2. Attempt to access the `ProjectFiles` folder:
   - Confirm that users have permissions according to the DAC settings configured.
   - For example, a user in the **Managers** group should have full access, while a user in the **Employees** group may have limited access.

## Step 5: View Access Control Events in Event Viewer (Optional)

1. To monitor file access events, enable auditing for the folder:
   - Right-click on the folder and select **Properties**.
   - Go to the **Security** tab, click **Advanced**, then go to the **Auditing** tab.
   - Click **Add...** and select users or groups to audit, setting the types of access to monitor (e.g., **Read**, **Write**).
   - Click **OK** to save the auditing settings.
2. Open **Event Viewer** to view access events:
   - Press `Win + R`, type `eventvwr.msc`, and press **Enter**.
   - In Event Viewer, navigate to **Windows Logs** > **Security**.
   - Look for event IDs related to file access, such as **4663** for file or folder access.

---

This completes the setup for Discretionary Access Control (DAC) on Windows OS.
