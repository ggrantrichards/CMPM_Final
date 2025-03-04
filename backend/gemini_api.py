import google.generativeai as genai
import json

# Configure the Gemini API
genai.configure(api_key="AIzaSyD35idMpAjsv_t_uoq5jx-7UWEdmDxsB2E")

# Initialize the model
model = genai.GenerativeModel('gemini-2.0')

def generate_build_with_gemini(size, build_type):
    try:
        # Create a prompt for the Gemini API
        prompt = f"""
        Generate a Minecraft {build_type} build with a size of {size}x{size}. 
        Provide the block layout for each layer from bottom to top using the following abbreviations:
        - ST: STONE
        - GR: GRASS_BLOCK
        - DT: DIRT
        - WD: OAK_PLANKS
        - GL: GLASS
        - BR: BRICKS
        - SB: STONE_BRICKS
        - SN: SAND
        - SP: SPRUCE_PLANKS
        - IR: IRON_BLOCK
        - GD: GOLD_BLOCK
        - DM: DIAMOND_BLOCK
        - LB: LAPIS_BLOCK
        - EM: EMERALD_BLOCK
        - RD: REDSTONE_BLOCK
        - OB: OBSIDIAN
        - CL: CLAY
        - SL: STONE_SLAB
        - TR: TORCH
        - DR: OAK_DOOR
        - WN: GLASS_PANE
        - RF: OAK_STAIRS
        - FL: OAK_PLANKS
        - WL: COBBLESTONE_WALL
        - CH: CHEST
        - LT: LANTERN
        - FW: FURNACE
        - BD: BED
        - BK: BOOKSHELF
        - CB: COBBLESTONE
        - SD: SANDSTONE
        - NT: NETHER_BRICKS
        - EB: END_STONE_BRICKS

        Format the output as a JSON object with a key "layers" containing a list of layers, where each layer is a list of rows, and each row is a list of block abbreviations.
        """

        # Call the Gemini API
        response = model.generate_content(prompt)

        # Print the raw response for debugging
        print("Gemini API Raw Response:")
        print(response.text)

        # Parse the response into layers
        try:
            # Attempt to parse the response as JSON
            response_json = json.loads(response.text)
            layers = response_json.get("layers", [])
        except json.JSONDecodeError:
            # If JSON parsing fails, assume the response is a plain text list
            layers = eval(response.text)  # Fallback to eval (use with caution)

        return layers
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return []