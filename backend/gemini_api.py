import google.generativeai as genai
import json
import re

# Configure the Gemini API
genai.configure(api_key="AIzaSyD35idMpAjsv_t_uoq5jx-7UWEdmDxsB2E")

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_build_with_gemini(size, build_type):
    try:
        # Create a prompt for the Gemini API
        prompt = f"""
        Generate a Minecraft {build_type} build with a size of {size}x{size}. 
        The build must meet the following requirements:
        1. **Floor**: The bottom layer (layer 0) must be a solid floor made of appropriate blocks (e.g., STONE, OAK_PLANKS, etc.).
        2. **Roof**: The top layer (last layer) must be a solid roof made of appropriate blocks (e.g., OAK_PLANKS, STONE_BRICKS, etc.).
        3. **Traversable**: The player (1x1x2 blocks) must be able to move through the build without obstruction. Ensure there are clear paths and no floating blocks. 
           Also ensure that each build has an entrance (I.E. Air Blocks on one of the borders of the build fit for the player's size). Builds should be generally hollow with plenty of space for player movement. 
           DO not crowd the inside space with useful blocks like crafting tables and furnaces when the build type permits it use blocks sparingly on the inside.
        4. **Aesthetic**: The build should align with the chosen style (e.g., a castle should look like a castle, a house should look like a house).
        5. **Blocks**: Only use the following block abbreviations as all blocks listed take up a 1x1x1 space:
           - "AA": "AIR",
           - "ST": "STONE",
           - "GR": "GRASS_BLOCK",
           - "DT": "DIRT",
           - "WD": "OAK_PLANKS",
           - "GL": "GLASS",
           - "BR": "BRICKS",
           - "SB": "STONE_BRICKS",
           - "SN": "SAND",
           - "SP": "SPRUCE_PLANKS",
           - "OB": "OBSIDIAN",
           - "CL": "CLAY",
           - "TR": "TORCH",
           - "WN": "GLASS_PANE",
           - "FL": "OAK_PLANKS",
           - "CH": "CHEST",
           - "LT": "LANTERN",
           - "FW": "FURNACE",
           - "BK": "BOOKSHELF",
           - "CB": "COBBLESTONE",
           - "SD": "SANDSTONE",
           - "NT": "NETHER_BRICKS",
           - "EB": "END_STONE_BRICKS"

        Format the output as a JSON object with a key "layers" containing a list of layers, where each layer is a list of rows, and each row is a list of block abbreviations.
        """

        # Call the Gemini API
        response = model.generate_content(prompt)

        # Print the raw response for debugging
        print("Gemini API Raw Response:")
        print(response.text)

        # Extract JSON from the Markdown code block
        json_string = re.search(r'```json\s*({.*?})\s*```', response.text, re.DOTALL)
        if not json_string:
            raise ValueError("No valid JSON found in the response.")

        # Parse the JSON string
        response_json = json.loads(json_string.group(1))
        layers = response_json.get("layers", [])

        return layers
    except Exception as e:
        if "finish_reason" in str(e) and "4" in str(e):
            print("Error: The model detected copyrighted material and cannot generate the build.")
        else:
            print(f"An error occurred while calling the Gemini API: {e}")
        return []