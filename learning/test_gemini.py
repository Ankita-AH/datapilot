from dotenv import load_dotenv
load_dotenv()
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain what a data pipeline is, in one sentence."
)
print(interaction.output_text)