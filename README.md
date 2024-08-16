Instructions to install dependencies and run the script:

# Instructions to Install Google Tesseract Engine

## MacOS

1. Install Homebrew (if not already installed):
   Open a terminal and run:
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Google Tesseract via Homebrew:
    Type the following in a terminal:
    ```brew install tesseract```

3. Verify your installation:
    Once you see that the installation has completed, type the following command:
    ```tesseract -v```

## Linux (Ubuntu)

1. Update Package List: 
    Open a terminal and run:
    ```sudo apt update```

2. Install Google Tesseract:
   Type the following in a terminal:
   ```sudo apt install tesseract-ocr```

3. Verify your installation:
    Once you see that the installation has completed, type the following command:
    ```tesseract -v```

## Windows

1. Download the Installer: 
    Download the Tesseract installer from the official GitHub repository: Tesseract at UB Mannheim

2. Run the Installer:
    Double-click the downloaded .exe file. 
    Follow the on-screen instructions to complete the installation.
3. Add Tesseract to System Path (Optional but recommended):
    Open the Start Menu and search for "Environment Variables".
    Click on "Edit the system environment variables".
    In the System Properties window, click on the "Environment Variables" button.
    In the Environment Variables window, find the "Path" variable in the "System variables" section and select it.
    Click on "Edit", then "New", and add the path to the Tesseract installation (e.g., C:\Program Files\Tesseract-OCR).
    Click "OK" to close all windows.

4. Verify Installation: 
    Open Command Prompt and run:
    ```tesseract -v```


# Instructions to Install Poppler

1. Follow instructions for your specific OS at the link below:
    https://pypi.org/project/pdf2image/

# Instructions for downloading Python modules

1. Create a virtual environment in directory of script:

    Link to Python venv documentation for further reference	:
    https://docs.python.org/3/library/venv.html

    Open a terminal or command prompt and run the following:
    ```python -m venv /path/to/new/virtual/environment```
    Replace "/path/to/new/virtual/environment" with the venv name you would like to use.
    Activate the vent using the following command:
    ```source /path/to/new/virtual/environment/bin/activate```

2. Install the necessary modules:
    Run the following command in a terminal or command prompt:
    ```pip install -r requirements.txt```

    Run ```pip list``` to make sure the modules were installed successfully.

3. Set directory of Google Tesseract within script:

   Open manual_ocr_python
   Modify the line that say ```pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'```
   Replace with the installation directory for Google Tesseract.



