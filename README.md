# Minecraft AI Builder using Gemini

## Backend Directory Structure

### data
    - Holds minecraft block data json of all available blocks
### src
    - Holds AI API call and build generation methods
### output
    - Holds output of program generation in layer text format and .schem file

## Frontend Directory Structure
### public
    - Holds style assets used on the frontend
### src
    - Holds the react components for the application

## Installation

1. Install requirements for backend:
    ```sh
    pip install -r requirements.txt
    ```
2. Navigate to the frontend:
    ```sh
    cd frontend/Client
    ```
3. Install requirements for frontend:
    ```sh
    npm install
    ```
4. Build the application:
    ```sh
    npm run build
    ```
## Running the Application

*** Before running please create a file called `.env` in `backend/src/` with the following content: ***
```
GEMINI_API_KEY=your-gemini-api-key-here
```
*** You can get any LLM api key or use gemini which was the original LLm for the project here: https://ai.google.dev/gemini-api/docs/api-key ***

1. Navigate to the backend directory and then run following command:
    ```sh
    cd src
    ```

2. Run the main script:
    ```sh
    python main.py
    ```
3. Open the App in your browser:
    ```sh
    http://127.0.0.1:8080
    ```
## Usage

- Input the desired build in the webpage.
- Look for the output in the `output` folder.
- Refresh the page to see the build on the website and download the `.schem` file.