from google.genai import types
from llm import ask

print("TEXT TEST:", ask('Reply with only this JSON: {"status": "ok"}'))

pdf = open("papers/Pandey_2012.pdf", "rb").read()
print("PDF TEST:", ask([
    types.Part.from_bytes(data=pdf, mime_type="application/pdf"),
    "From Table 1, give the 2003 pH, dry bulk density and soil organic C (%) as JSON only.",
]))
