from fastapi import FastAPI
from pydantic import BaseModel
from rapidfuzz import process

app = FastAPI()

# Predefined keywords for auto-completion
darion_keywords = ["let", "print", "function", "for each", "if", "else", "return", "import", "while", "do"]

# Sample syntax corrections
syntax_corrections = {
    "funtion": "function",
    "prnt": "print",
    "retun": "return",
    "fr each": "for each",
    "wihle": "while"
}

class CodeRequest(BaseModel):
    code: str

@app.post("/autocomplete/")
async def autocomplete(request: CodeRequest):
    """Returns suggested words for auto-completion."""
    input_text = request.code.split()[-1]  # Last word
    suggestions = process.extract(input_text, darion_keywords, limit=3)
    return {"suggestions": [s[0] for s in suggestions]}

@app.post("/correct/")
async def correct_code(request: CodeRequest):
    """Returns corrected syntax if any mistakes are found."""
    words = request.code.split()
    corrected_words = [syntax_corrections.get(word, word) for word in words]
    return {"corrected_code": " ".join(corrected_words)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)