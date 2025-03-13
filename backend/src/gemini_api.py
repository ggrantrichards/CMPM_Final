import google.generativeai as genai
import json
import re

# Configure the Gemini API with your API key.
genai.configure(api_key="AIzaSyD35idMpAjsv_t_uoq5jx-7UWEdmDxsB2E")

# Initialize the model.
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_build_with_gemini(size, build_type, description):
    try:
        prompt = f"""
        Generate a Minecraft {build_type} build with a size of {size}x{size}. 
        The build must meet the following requirements:
        1. **Dynamic Shape**: The overall shape should be non-cubic and dynamic, staying true to the given theme,
        but maintain a house-like appearance.

        2. **Four-Wall Design**: Each of the four walls must be clearly defined.
        Walls should be similar in style to maintain thematic consistency but should not necessarily be perfectly symmetrical.  
        Air blocks (AA) must only be used intentionally to alter a wall's shape
        (e.g., for design features or to create an entrance) and must not appear randomly.

        3. **Floor**: The bottom layer (layer 0) must form a continuous,
        solid floor using appropriate blocks with no gaps.

        4. **Roofline and Roof**: The roof must have a defined roofline that fits the theme,
        which may include dynamic elements (such as a sloped or tapered design).
        The top layer (or layers forming the roof) should be solid and gap-free, using appropriate blocks.

        5. **Traversable Interior**: The interior of the build should be mostly hollow,
        ensuring one space for a 1x1x2 player to move freely.
        There must be no random or floating blocks inside;
        any air blocks within are only there to form the intended dynamic shape. 
        It should sparsely use decorative blocks selected from the interior section to add to the aesthetic. 
        Interior blocks:

        "LT": "minecraft:lantern",
        "CH": "minecraft:chest",
        "FW": "minecraft:furnace",
        “CT”: "minecraft:crafting_table,

        6. **Entrance**: There must be exactly one open entrance, sized 1x1x2,
        located in the center of one of the walls.
        This is the only intentional gap in that wall, ensuring a clear and defined entry point.

        7. **Thematic Consistency**: All design choices
        (including block selection and architectural details)
        should strongly reflect the chosen {build_type} theme.

        8. **Block Restrictions**: 
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
        "GL": "minecraft:glass"

        9. **Validation and Regeneration**: If any aspect of the build fails to meet the above criteria
        (e.g., missing floor, random air blocks, incorrect wall design, improper entrance placement/size,
        lack of dynamic shape, or thematic inconsistency),
        then consider the output invalid and regenerate the design until all conditions are satisfied.

        Format the output as a JSON object with a key "layers" containing a list of layers,
        where each layer is a list of rows, and each row is a list of block abbreviations.
        """
        response = model.generate_content(prompt)
        print("Gemini API Raw Response:")
        print(response.text)
        raw_text = response.text.strip()
        if not raw_text:
            raise ValueError("Empty response from Gemini API.")

        # Try to parse the response as JSON
        try:
            response_json = json.loads(raw_text)
        except json.JSONDecodeError:
            # If the response is not valid JSON, try to extract JSON from Markdown
            json_match = re.search(r'```json\s*({.*?})\s*```', raw_text, re.DOTALL)
            if json_match:
                response_json = json.loads(json_match.group(1))
            else:
                # If no JSON is found, log the raw response for debugging
                print("No valid JSON found in the response. Raw response:")
                print(raw_text)
                raise ValueError("No valid JSON found in the response.")

        layers = response_json.get("layers", [])
        if not layers:
            raise ValueError("JSON response does not contain 'layers' key or it is empty.")
        return layers
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return []