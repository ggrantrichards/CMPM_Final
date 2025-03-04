import google.generativeai as genai

# Step 1: Set up the Gemini API key
genai.configure(api_key="AIzaSyD35idMpAjsv_t_uoq5jx-7UWEdmDxsB2E")

# Step 2: Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Step 3: Make a simple API call
def test_gemini():
    try:
        # Ask a simple question
        response = model.generate_content("What is the capital of France?")
        
        # Print the response
        print("Gemini API Response:")
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test
if __name__ == "__main__":
    test_gemini()