Minecraft AI Builder using Gemini

/data
    - Holds minecraft block data json of all available blocks
/src
    - Holds AI API call and build generation methods
/static
    - Holds helper functions in script.js and css styling for frontend
/templates
    - Holds index.html
/output
    - Holds output of program generation in layer text format and .schem file

install requirements with:
pip install -r requirements.txt
source ~/myenv/bin/activate

after dependencies installed run:
cd backend
python main.py

Input desired build in webpage and look for output in output folder or refresh page to see build in website and download .schem file