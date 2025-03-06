import google.generativeai as genai
import json
import re

# Configure the Gemini API with your API key.
genai.configure(api_key="AIzaSyD35idMpAjsv_t_uoq5jx-7UWEdmDxsB2E")

# Initialize the model.
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
5. Block usage: Only use the following block abbreviations – each corresponds to a real Minecraft block (1x1x1) that behaves normally:
   - "AA": "minecraft:air",
   - "ST": "minecraft:stone",
   - "GR": "minecraft:grass_block",
   - "DT": "minecraft:dirt",
   - "CD": "minecraft:coarse_dirt",
   - "PD": "minecraft:podzol",
   - "GN": "minecraft:granite",
   - "PG": "minecraft:polished_granite",
   - "DI": "minecraft:diorite",
   - "PDI": "minecraft:polished_diorite",
   - "AN": "minecraft:andesite",
   - "PAN": "minecraft:polished_andesite",
   - "CB": "minecraft:cobblestone",
   - "DS": "minecraft:deepslate",
   - "PDS": "minecraft:polished_deepslate",
   - "CDS": "minecraft:cobbled_deepslate",
   - "BB": "minecraft:blackstone",
   - "PBS": "minecraft:polished_blackstone",
   - "PBSB": "minecraft:polished_blackstone_bricks",
   - "WD": "minecraft:oak_planks",
   - "SP": "minecraft:spruce_planks",
   - "BP": "minecraft:birch_planks",
   - "JP": "minecraft:jungle_planks",
   - "AP": "minecraft:acacia_planks",
   - "DP": "minecraft:dark_oak_planks",
   - "CP": "minecraft:crimson_planks",
   - "WP": "minecraft:warped_planks",
   - "OL": "minecraft:oak_log",
   - "SL": "minecraft:spruce_log",
   - "BL": "minecraft:birch_log",
   - "DL": "minecraft:dark_oak_log",
   - "CLG": "minecraft:crimson_stem",
   - "WLG": "minecraft:warped_stem",
   - "OS": "minecraft:oak_stairs",
   - "SS": "minecraft:spruce_stairs",
   - "BS": "minecraft:birch_stairs",
   - "JS": "minecraft:jungle_stairs",
   - "AS": "minecraft:acacia_stairs",
   - "DOS": "minecraft:dark_oak_stairs",
   - "CS": "minecraft:crimson_stairs",
   - "WS": "minecraft:warped_stairs",
   - "OSL": "minecraft:oak_slab",
   - "SSL": "minecraft:spruce_slab",
   - "BSL": "minecraft:birch_slab",
   - "JSL": "minecraft:jungle_slab",
   - "ASL": "minecraft:acacia_slab",
   - "DSL": "minecraft:dark_oak_slab",
   - "CSL": "minecraft:crimson_slab",
   - "WSL": "minecraft:warped_slab",
   - "SB": "minecraft:stone_bricks",
   - "BR": "minecraft:bricks",
   - "OB": "minecraft:obsidian",
   - "CL": "minecraft:clay",
   - "TR": "minecraft:torch",
   - "DR": "minecraft:oak_door",
   - "WN": "minecraft:glass_pane",
   - "CH": "minecraft:chest",
   - "LT": "minecraft:lantern",
   - "FW": "minecraft:furnace",
   - "BK": "minecraft:bookshelf",
   - "SD": "minecraft:sandstone",
   - "NT": "minecraft:nether_bricks",
   - "EB": "minecraft:end_stone_bricks",
   - "GL": "minecraft:glass"

Format the output as a JSON object with a key "layers" containing a list of layers.
Each layer is a list of rows, and each row is a list of block abbreviations.
Ensure the design is realistic and layered (i.e., not a completely solid cube).
        """
        response = model.generate_content(prompt)
        print("Gemini API Raw Response:")
        print(response.text)
        raw_text = response.text.strip()
        if not raw_text:
            raise ValueError("Empty response from Gemini API.")
        try:
            response_json = json.loads(raw_text)
        except Exception:
            json_match = re.search(r'```json\s*({.*?})\s*```', raw_text, re.DOTALL)
            if json_match:
                response_json = json.loads(json_match.group(1))
            else:
                raise ValueError("No valid JSON found in the response.")
        layers = response_json.get("layers", [])
        if not layers:
            raise ValueError("JSON response does not contain 'layers' key or it is empty.")
        return layers
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return []
