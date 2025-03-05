import google.generativeai as genai
import json
import re

# Configure the Gemini API
genai.configure(api_key="AIzaSyD35idMpAjsv_t_uoq5jx-7UWEdmDxsB2E")

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_build_with_gemini(size, description):
    try:
        prompt = f"""
Generate a Minecraft build described as "{description}" with a size of {size}x{size}. 
The build must meet the following requirements:
1. Floor: The bottom layer (layer 0) should be a solid or patterned floor using appropriate blocks (e.g., STONE, OAK_PLANKS, OAK_SLAB, etc.).
2. Roof: The top layer should be a solid or decorative roof using blocks like OAK_PLANKS, STONE_BRICKS, or appropriate slabs.
3. Walls and structure: The build should not be entirely cubic; it must incorporate interior air blocks to create open spaces for player movement. Include an entrance (a gap of AIR) in one of the borders. Use stairs (e.g., OAK_STAIRS, SPRUCE_STAIRS) and slabs (e.g., OAK_SLAB, SPRUCE_SLAB) for decorative or functional elements.
4. Aesthetic: The build should reflect the description provided. Ensure that the design is realistic and layered, with open interior space.
5. Block usage: Only use the following block abbreviations. Each abbreviation corresponds to a real Minecraft block:
   - "AA": "AIR",
   - "ST": "STONE",
   - "GR": "GRASS_BLOCK",
   - "DT": "DIRT",
   - "WD": "OAK_PLANKS",
   - "OS": "OAK_STAIRS",
   - "OSL": "OAK_SLAB",
   - "GL": "GLASS",
   - "BR": "BRICKS",
   - "SB": "STONE_BRICKS",
   - "SN": "SAND",
   - "SP": "SPRUCE_PLANKS",
   - "SS": "SPRUCE_STAIRS",
   - "SSL": "SPRUCE_SLAB",
   - "OB": "OBSIDIAN",
   - "CL": "CLAY",
   - "TR": "TORCH",
   - "DR": "OAK_DOOR",
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

Format the output as a JSON object with a key "layers" containing a list of layers. Each layer is a list of rows, and each row is a list of block abbreviations. The design should be realistic and layered, not a fully filled cube.
"""
        # Call the Gemini API
        response = model.generate_content(prompt)
        
        # Print the raw response for debugging
        print("Gemini API Raw Response:")
        print(response.text)
        
        # Extract JSON from a Markdown code block (```json ... ```)
        json_string = re.search(r'```json\s*({.*?})\s*```', response.text, re.DOTALL)
        if not json_string:
            raise ValueError("No valid JSON found in the response.")
        
        # Parse the JSON string
        response_json = json.loads(json_string.group(1))
        layers = response_json.get("layers", [])
        
        return layers
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return []
