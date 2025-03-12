# Minecraft AI Builder using Gemini

## Directory Structure

### data
    - Holds minecraft block data json of all available blocks
### src
    - Holds AI API call and build generation methods
### static
    - Holds helper functions in script.js and css styling for frontend
### templates
    - Holds index.html
### output
    - Holds output of program generation in layer text format and .schem file

## Installation

1. Install requirements:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Navigate to the backend directory:
    ```sh
    cd src
    ```

2. Run the main script:
    ```sh
    python main.py
    ```

## Usage

- Input the desired build in the webpage.
- Look for the output in the `output` folder.
- Refresh the page to see the build on the website and download the `.schem` file.