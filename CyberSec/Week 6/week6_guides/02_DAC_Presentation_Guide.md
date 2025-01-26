
# Discretionary Access Control (DAC) - Step-by-Step Presentation

## Step 1: Check the List of Files or Folders

**Command**:

```bash
sudo ls /path/to/your/fileorfolder/
```

**Explanation**:

- The `ls` command lists the files and folders in the specified directory.
- Adding `sudo` ensures you have the necessary privileges to view restricted directories.

**Example**:

```bash
sudo ls /var/log/
```

---

## Step 2: Check Permissions of Files or Folders

**Command**:

```bash
sudo ls -l /path/to/your/fileorfolder/
# example:
sudo ls -l /var/log/apt
```

**Explanation of Results**:

- The `-l` option shows detailed information about each file and folder, including permissions.
- Example output:

  ```bash
  -rw-r--r--  1 user group 1234 Nov 20 10:00 example.txt
  ```

  - **`-rw-r--r--`**: Permissions (read, write, execute for owner, group, and others).
  - **`1`**: Number of links to the file.
  - **`user`**: Owner of the file.
  - **`group`**: Group associated with the file.
  - **`1234`**: File size in bytes.
  - **`Nov 20 10:00`**: Last modified date and time.
  - **`example.txt`**: File name.

---

## Step 3: Change Permissions

**Command**:

```bash
chmod <permissions> <file>
```

**Explanation**:

- Use either **numeric mode** or **symbolic mode** to change permissions.

### Example 1: Numeric Mode

- Command:

  ```bash
  chmod 644 example.txt
  ```

  - Sets permissions to `rw- r-- r--` (110=6; 100=4, 100=4)
    - Owner: Read (`r`), Write (`w`)
    - Group: Read (`r`)
    - Others: Read (`r`)

### Example 2: Symbolic Mode

- Command:

  ```bash
  chmod u+w example.txt
  ```

  - Adds write (`w`) permission to the owner (user).

---

## Step 4: Check the Results

**Command**:

```bash
sudo ls -l /path/
```

**Explanation**:

- Verify if the permissions have been updated as expected.
- Example output after changing to `chmod 644 example.txt`:

  ```
  -rw-r--r--  1 user group 1234 Nov 20 10:00 example.txt
  ```

---

## Interactive Demonstration (Real-World Scenario)

### Scenario: Restrict Access to a Sensitive File

1. **Create the file**:

   ```bash
   touch secret.txt
   ```

2. **Check the default permissions**:

   ```bash
   ls -l secret.txt
   ```

   Example:

   ```
   -rw-rw-r--  1 user group 0 Nov 20 10:00 secret.txt
   ```

3. **Change permissions to restrict access**:

   ```bash
   chmod 600 secret.txt
   ```

   - `600`: Owner can read/write, others have no access.

4. **Verify the updated permissions**:

   ```bash
   ls -l secret.txt
   ```

   Output:

   ```
   -rw-------  1 user group 0 Nov 20 10:00 secret.txt
   ```

---

## Encourage Audience Participation

- Ask participants to explain the output of `ls -l`.
- Have them try different `chmod` commands (e.g., `chmod 750`, `chmod o+r`) and observe results.
