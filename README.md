# MobaXterm Keygen

## Prerequisites

- **Python**: Ensure that Python is properly installed and added to the system PATH.
- **MobaXterm**: The keygen is specifically designed for use with MobaXterm and requires it to be installed on your system.
- **Administrator Rights**: Running the script requires administrative privileges to perform all necessary operations correctly.

## Usage

1. Clone or download the repository.
2. Make sure Python is installed and added to the PATH.
3. Run the batch script (`.bat` file) to initiate the process.

### Running the Batch Script

The batch script will perform the following steps:

1. **Check Python Installation**: If Python is not found, the user will be prompted to install Python.
2. **Check Keygen Script**: If the `MobaXterm-Keygen.py` script is not found, an error message along with an audio notification will be displayed.
3. **Check Administrator Rights**: If the script is not executed with administrative privileges, the user will be prompted to restart it with the necessary rights.
4. **Run Python Keygen**: The batch script runs the keygen script to generate the license file.

### Python Script Functionality

- **License File Creation**: The Python script generates a license file (`custom.mxtpro`) for the specified username, encrypting and encoding it using a custom Base64 variant.
- **Detecting MobaXterm Version**: The script reads the `version.dat` file from the MobaXterm installation directory to determine the installed version and create a compatible license.
- **Interactive Prompts**: The user is prompted to enter their username and is informed of any issues (e.g., running instances of MobaXterm that need to be terminated).

## Important Notes

- **Administrator Rights**: The script requires administrative privileges to perform tasks such as terminating MobaXterm processes and copying the generated license file to the installation directory.
- **Progress Indicators and Notifications**: The batch and Python scripts provide visual progress indicators and audio notifications during execution.

## License

This project is licensed under the GPLv3 License. For more information, please refer to the LICENSE file.

## Disclaimer

This script is intended for educational purposes only. Unauthorized use of software that violates the respective terms of use or license agreements may have legal consequences. Use at your own risk.
