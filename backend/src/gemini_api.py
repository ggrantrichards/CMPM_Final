import google.generativeai as genai
import json
import re

# Configure the Gemini API with your API key.
genai.configure(api_key="AIzaSyD35idMpAjsv_t_uoq5jx-7UWEdmDxsB2E")

# Initialize the model.
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_build_with_gemini(size, build_type, description, max_retries=3):
    for attempt in range(max_retries):
        try:
            prompt = f"""
            Generate a Minecraft {build_type} build with a size of {size}x{size}. 
            The build must meet the following requirements:
            1. **Dynamic Shape**: The overall shape should be cubic, staying true to the given theme,
            but maintain a house-like appearance.

            2. **Four-Wall Design**: Each of the four walls must be clearly defined.
            Walls should be similar in style to maintain thematic consistency but should not necessarily be perfectly symmetrical. 

            3. **Floor**: The bottom layer (layer 0) must form a continuous,
            solid floor using appropriate blocks with no gaps.

            4. **Roofline and Roof**: The top layer (roof) must be a continuous, solid layer using appropriate blocks with no gaps.

            5. **Traversable Interior**: The interior of the build should be mostly hollow (air blocks),
            ensuring space for a 1x1x2 player to move freely.
            There must be no random or floating blocks inside;

            6. **Thematic Consistency**: All design choices
            (including block selection and architectural details)
            should strongly reflect the chosen {build_type} theme.

            7. **Block Restrictions**: 
            - Only use the following block abbreviations (each block occupies a 1x1x1 space) for exterior:
            "AA": "minecraft:air",
            "ST": "minecraft:stone",
            "GR": "minecraft:grass_block",
            "DT": "minecraft:dirt",
            "CD": "minecraft:coarse_dirt",
            "PD": "minecraft:podzol",
            "GN": "minecraft:granite",
            "PG": "minecraft:polished_granite",
            "DI": "minecraft:diorite",
            "PDI": "minecraft:polished_diorite",
            "AN": "minecraft:andesite",
            "PAN": "minecraft:polished_andesite",
            "CB": "minecraft:cobblestone",
            "DS": "minecraft:deepslate",
            "PDS": "minecraft:polished_deepslate",
            "CDS": "minecraft:cobbled_deepslate",
            "BB": "minecraft:blackstone",
            "PBS": "minecraft:polished_blackstone",
            "PBSB": "minecraft:polished_blackstone_bricks",
            "WD": "minecraft:oak_planks",
            "SP": "minecraft:spruce_planks",
            "BP": "minecraft:birch_planks",
            "JP": "minecraft:jungle_planks",
            "AP": "minecraft:acacia_planks",
            "DP": "minecraft:dark_oak_planks",
            "CP": "minecraft:crimson_planks",
            "WP": "minecraft:warped_planks",
            "OL": "minecraft:oak_log",
            "SL": "minecraft:spruce_log",
            "BL": "minecraft:birch_log",
            "DL": "minecraft:dark_oak_log",
            "CLG": "minecraft:crimson_stem",
            "WLG": "minecraft:warped_stem",
            "OS": "minecraft:oak_stairs",
            "SS": "minecraft:spruce_stairs",
            "BS": "minecraft:birch_stairs",
            "JS": "minecraft:jungle_stairs",
            "AS": "minecraft:acacia_stairs",
            "DOS": "minecraft:dark_oak_stairs",
            "CS": "minecraft:crimson_stairs",
            "WS": "minecraft:warped_stairs",
            "SB": "minecraft:stone_bricks",
            "BR": "minecraft:bricks",
            "OB": "minecraft:obsidian",
            "CL": "minecraft:clay",
            "TR": "minecraft:torch",
            "WN": "minecraft:glass_pane",
            "BK": "minecraft:bookshelf",
            "SD": "minecraft:sandstone",
            "NT": "minecraft:nether_bricks",
            "EB": "minecraft:end_stone_bricks",
            "GL": "minecraft:glass",
            "CT": "minecraft:crafting_table",
            "FN": "minecraft:furnace",
            "BF": "minecraft:blast_furnace",
            "SM": "minecraft:smoker",
            "CBF": "minecraft:cartography_table",
            "LBF": "minecraft:loom",
            "SFB": "minecraft:smithing_table",
            "STB": "minecraft:stonecutter",
            "BFB": "minecraft:barrel"

            Additionally, provide a list of block abbreviations that fit the theme of the build.
            Format the output as a JSON object with a key "layers" containing a list of layers,
            where each layer is a list of rows, and each row is a list of block abbreviations.
            Also include a key "allowed_blocks" containing a list of block abbreviations that fit the theme.
            """
            response = model.generate_content(prompt)
            
            raw_text = response.text.strip()
            if not raw_text:
                print(f"Attempt {attempt + 1}: Empty response from Gemini API.")
                continue

            try:
                response_json = json.loads(raw_text)
            except json.JSONDecodeError:
                json_match = re.search(r'```json\s*({.*?})\s*```', raw_text, re.DOTALL)
                if json_match:
                    response_json = json.loads(json_match.group(1))
                else:
                    print(f"Attempt {attempt + 1}: No valid JSON found in the response.")
                    continue

            if "layers" not in response_json or "allowed_blocks" not in response_json:
                print(f"Attempt {attempt + 1}: JSON response does not contain 'layers' or 'allowed_blocks' key.")
                continue

            layers = response_json["layers"]
            allowed_blocks = response_json["allowed_blocks"]
            
            # Convert allowed_blocks to a set to ensure it's hashable
            allowed_blocks = set(allowed_blocks)
            
            if not layers:
                print(f"Attempt {attempt + 1}: JSON response contains an empty 'layers' list.")
                continue

            return layers, allowed_blocks
        except Exception as e:
            print(f"Attempt {attempt + 1}: An error occurred while calling the Gemini API: {e}")
            continue

    print("Max retries reached. No valid response from Gemini API.")
    return [], set()  # Return an empty set for allowed_blocks
