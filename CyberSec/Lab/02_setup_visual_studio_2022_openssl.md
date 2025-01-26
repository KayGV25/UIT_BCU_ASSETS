
# Setting Up C/C++ Development Libraries and Visual Studio Code with Visual Studio 2022

This guide will walk you through the setup of a C/C++ development environment using **Visual Studio 2022**, **OpenSSL**, and **Visual Studio Code** on Windows.

---

## 1. Install Visual Studio Code

Visual Studio Code (VS Code) is a lightweight code editor with great support for C/C++ development.

1. Download Visual Studio Code from the official site: [VS Code Download](https://code.visualstudio.com/download).
2. Install it by following the instructions provided on the website.

---

## 2. Install Visual Studio 2022

Visual Studio 2022 offers a powerful C/C++ compiler and tools for development.

1. **Download Visual Studio 2022** from the official site: [Visual Studio Download](https://visualstudio.microsoft.com/).
2. **During installation**, select the following components:
   - **Desktop development with C++**.
   - **C++ CMake tools for Windows**.
   - **Windows 10 SDK** (or the latest available version).
3. **Finish the installation** by following the on-screen instructions.

---

## 3. Install Perl and NASM

OpenSSL requires Perl and NASM for building from source.

1. **Download Strawberry Perl** from: [Strawberry Perl](https://strawberryperl.com/).
2. Install Strawberry Perl by following the provided instructions.

3. **Add Strawberry Perl to the System Path**:
   - Open **System Properties** > **Environment Variables**.
   - In **System variables**, select **Path** and click **Edit**.
   - Click **New** and add:
     ```
     C:\Strawberry\perl\bin
     C:\Strawberry\c\bin
     ```
   - **Verify Perl installation**:
     Open a new command prompt and run:
     ```bash
     perl -v
     ```

4. **Install NASM**:
   - Download NASM from: [NASM Download](https://www.nasm.us/).
   - Install NASM and add it to the system **Path**.
   - Verify NASM installation by running:
     ```bash
     nasm -v
     ```

---

## 4. Compile the OpenSSL Library

OpenSSL is a robust library for implementing SSL and TLS protocols. Below are the steps to compile it using the Visual Studio 2022 environment.

### 4.1. Compile with Visual Studio 2022

1. **Download OpenSSL** from: [OpenSSL Source](https://www.openssl.org/source/).
2. **Open the "x64 Native Tools Command Prompt for VS 2022"**.
3. **Navigate to the extracted OpenSSL directory** and run the following commands:
   ```bash
   "C:\Strawberry\perl\bin\perl.exe" Configure VC-WIN64A --prefix=C:/openssl
   nmake
   nmake test
   nmake install
   ```

4. **Verify the installation**:
   - Open a command prompt and type:
     ```bash
     openssl version
     ```

---

## 5. Set Up Windows Environment for `cl.exe`

1. **Locate `cl.exe`**:
   - Typically found in `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\<version>\bin\Hostx64\x64`.

2. **Add `cl.exe` to the System Path**:
   - Open **System Properties** > **Environment Variables**.
   - In **System variables**, select **Path** and click **Edit**.
   - Click **New** and add the path to `cl.exe`. (exclude cl.exe)

3. **Verify the Setup**:
   - Open a new command prompt and run:
     ```bash
     cl
     ```

---

## 6. Compile and Run a C++ Program

After completing the setup, you can test your environment.

1. **Create a simple C++ program** and save it in VS Code:
   ```cpp
   #include <iostream>
   using namespace std;

   int main() {
       cout << "Hello, World!" << endl;
       return 0;
   }
   ```
2. **Open a Command Prompt** (or Developer Command Prompt) and navigate to your program's directory.
3. **Compile the program** using:
   ```bash
   cl /EHsc hello.cpp
   ```
4. **Run the program**:
   ```bash
   hello.exe
   ```

---

## 7. Additional Resources

- [Visual Studio Documentation](https://learn.microsoft.com/en-us/visualstudio/)
- [OpenSSL Documentation](https://www.openssl.org/)
- [Strawberry Perl](https://strawberryperl.com/)
- [NASM Documentation](https://www.nasm.us/)

