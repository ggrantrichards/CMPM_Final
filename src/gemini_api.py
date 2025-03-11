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
        1. **Floor**: The bottom layer (layer 0) must be a solid floor made of appropriate blocks (e.g., STONE, OAK_PLANKS, etc.).
        2. **Roof**: The top layer (last layer) must be a solid roof made of appropriate blocks (e.g., OAK_PLANKS, STONE_BRICKS, etc.).
        3. **Traversable**: The player (1x1x2 blocks) must be able to move through the build without obstruction. Ensure there are clear paths and no floating blocks. 
           Also ensure that each build has an entrance (I.E. Air Blocks on one of the borders of the build fit for the player's size). Builds should be generally hollow with plenty of space for player movement. 
           Do not crowd the inside space with useful blocks like crafting tables, chests, and furnaces, use them sparingly.
        4. **Aesthetic**: The build should align with the chosen style (e.g., a castle should look like a castle, a house should look like a house).
        5. **Blocks**: Only use the following block abbreviations as all blocks listed take up a 1x1x1 space:
            - "AA": "minecraft:air",
            - "ST": "minecraft:stone",
            - "GR": "minecraft:grass",
            - "DT": "minecraft:dirt",
            - "WD": "minecraft:planks",
            - "GL": "minecraft:glass",
            - "BR": "minecraft:brick_block",
            - "SB": "minecraft:stonebrick",
            - "SN": "minecraft:sand",
            - "OB": "minecraft:obsidian",
            - "CL": "minecraft:clay",
            - "TR": "minecraft:torch",
            - "WN": "minecraft:glass_pane",
            - "CH": "minecraft:chest",
            - "GS": "minecraft:glowstone",
            - "FW": "minecraft:furnace",
            - "BK": "minecraft:bookshelf",
            - "CB": "minecraft:cobblestone",
            - "SD": "minecraft:sandstone",
            - "NT": "minecraft:nether_brick",
            - "EB": "minecraft:end_bricks"

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