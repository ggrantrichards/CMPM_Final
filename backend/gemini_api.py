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
3. Walls and structure: The build should not be entirely cubic; it must incorporate interior air blocks to create open spaces for player movement. Include an entrance (a gap of AIR) in one of the borders.
4. Aesthetic: The build should reflect the description provided. Ensure that the design is realistic and layered, with open interior space.
5. Block usage: Only use the following block abbreviations - each corresponds to a real Minecraft block that is a full block (1x1x1) and behaves normally:
   - "AA": "AIR",
   - "ST": "STONE",
   - "GR": "GRASS_BLOCK",
   - "DT": "DIRT",
   - "CD": "COARSE_DIRT",
   - "PD": "PODZOL",
   - "GN": "GRANITE",
   - "PG": "POLISHED_GRANITE",
   - "DI": "DIORITE",
   - "PDI": "POLISHED_DIORITE",
   - "AN": "ANDESITE",
   - "PAN": "POLISHED_ANDESITE",
   - "CB": "COBBLESTONE",
   - "DS": "DEEPSLATE",
   - "PDS": "POLISHED_DEEPSLATE",
   - "CDS": "COBBLED_DEEPSLATE",
   - "BB": "BLACKSTONE",
   - "PBS": "POLISHED_BLACKSTONE",
   - "PBSB": "POLISHED_BLACKSTONE_BRICKS",
   - "WD": "OAK_PLANKS",
   - "SP": "SPRUCE_PLANKS",
   - "BP": "BIRCH_PLANKS",
   - "JP": "JUNGLE_PLANKS",
   - "AP": "ACACIA_PLANKS",
   - "DP": "DARK_OAK_PLANKS",
   - "CP": "CRIMSON_PLANKS",
   - "WP": "WARPED_PLANKS",
   - "OL": "OAK_LOG",
   - "SL": "SPRUCE_LOG",
   - "BL": "BIRCH_LOG",
   - "DL": "DARK_OAK_LOG",
   - "CLG": "CRIMSON_STEM",
   - "WLG": "WARPED_STEM",
   - "OS": "OAK_STAIRS",
   - "SS": "SPRUCE_STAIRS",
   - "BS": "BIRCH_STAIRS",
   - "JS": "JUNGLE_STAIRS",
   - "AS": "ACACIA_STAIRS",
   - "DS": "DARK_OAK_STAIRS",
   - "CS": "CRIMSON_STAIRS",
   - "WS": "WARPED_STAIRS",
   - "OSL": "OAK_SLAB",
   - "SSL": "SPRUCE_SLAB",
   - "BSL": "BIRCH_SLAB",
   - "JSL": "JUNGLE_SLAB",
   - "ASL": "ACACIA_SLAB",
   - "DSL": "DARK_OAK_SLAB",
   - "CSL": "CRIMSON_SLAB",
   - "WSL": "WARPED_SLAB",
   - "SB": "STONE_BRICKS",
   - "BR": "BRICKS",
   - "OB": "OBSIDIAN",
   - "CL": "CLAY",
   - "TR": "TORCH",
   - "DR": "OAK_DOOR",
   - "WN": "GLASS_PANE",
   - "CH": "CHEST",
   - "LT": "LANTERN",
   - "FW": "FURNACE",
   - "BK": "BOOKSHELF",
   - "SD": "SANDSTONE",
   - "NT": "NETHER_BRICKS",
   - "EB": "END_STONE_BRICKS",
   - "GL": "GLASS"

Format the output as a JSON object with a key "layers" containing a list of layers. Each layer is a list of rows, and each row is a list of block abbreviations. Ensure the design is realistic and layered (i.e. not a completely solid cube).
"""
        # Call the Gemini API
        response = model.generate_content(prompt)
        
        # Debug: print raw response text
        print("Gemini API Raw Response:")
        print(response.text)
        
        # Extract JSON from a Markdown code block (```json ... ```)
        json_match = re.search(r'```json\s*({.*?})\s*```', response.text, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in the response.")
        
        response_json = json.loads(json_match.group(1))
        layers = response_json.get("layers", [])
        return layers
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return []
