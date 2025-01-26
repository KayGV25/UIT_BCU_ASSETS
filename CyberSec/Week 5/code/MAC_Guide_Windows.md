
# Mandatory Access Control (MAC) Guide on Windows OS

Mandatory Access Control (MAC) enforces access policies that users cannot change. Windows uses security features such as Mandatory Integrity Control (MIC) and Group Policy to implement MAC-like restrictions. Here’s how to set up MAC-style access controls on Windows.

## Step 1: Configure Mandatory Integrity Control (MIC)

1. **Set Integrity Levels for Files or Folders**:
   - Open **Command Prompt** with Administrator privileges.
   - Use the following command to set integrity levels for files or folders:

     ```bash
     icacls "C:\path\to\folder" /setintegritylevel M
     ```

     Replace `"C:\path\to\folder"` with the actual path to the folder or file.
   - Available integrity levels:
     - **L** (Low) – Limited access; typically used for web browsers and downloaded files.
     - **M** (Medium) – Default access level for standard users.
     - **H** (High) – Required for administrative tasks; assigned to files and folders needing higher protection.

2. **Verify Integrity Levels**:
   - Run the command below to check the integrity level of a file or folder:

     ```bash
     icacls "C:\path\to\folder"
     ```

   - This displays the integrity level and existing permissions for the item.

## Step 2: Use Group Policy to Implement MAC-style Restrictions

1. **Open Group Policy Editor**:
   - Press `Win + R`, type `gpedit.msc`, and press **Enter**.
   - This opens the **Local Group Policy Editor**.

2. **Configure Policies for Specific Folders or Files**:
   - Navigate to **Computer Configuration** > **Windows Settings** > **Security Settings** > **File System**.
   - Right-click **File System** and select **Add File…**.
   - Browse to select the folder or file you want to restrict.
   - Set permissions by assigning access to specific users or groups.

3. **Configure Software Restriction Policies**:
   - Navigate to **Computer Configuration** > **Windows Settings** > **Security Settings** > **Software Restriction Policies**.
   - If no policies are defined, right-click **Software Restriction Policies** and select **New Software Restriction Policies**.
   - Add **Additional Rules** to define allowed or restricted applications and executable files for users or groups.

4. **Apply Group Policies for Higher Restrictions**:
   - Navigate to **Computer Configuration** > **Administrative Templates** > **System** > **Removable Storage Access**.
   - Set up restrictions for access to specific storage devices to enhance data security.

## Step 3: Test Access Restrictions

1. Attempt to access files or folders with different integrity levels or group policies to confirm that the restrictions are enforced.
2. Users with insufficient permissions should encounter access denied messages or restricted application access.

## Step 4: Monitor Access in Event Viewer

1. Open **Event Viewer** to view access and security logs:
   - Press `Win + R`, type `eventvwr.msc`, and press **Enter**.
2. Navigate to **Windows Logs** > **Security**.
3. Look for events related to access control and security policy enforcement:
   - **Event ID 4663**: An attempt to access an object (file, folder).
   - **Event ID 5140**: A network share object was accessed.

---

This completes the setup for Mandatory Access Control (MAC)-like configurations on Windows OS.
