from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Initialize FastAPI app
app = FastAPI()

# Set your OpenAI API key (replace with your actual API key)
key = os.getenv('OPEN_AI_KEY')

openai.api_key = key

# Load the content of your resume (ensure the resume.txt file is in the same directory as app.py)
resume_path = './resume.txt'

# Check if the resume file exists
if os.path.exists(resume_path):
    with open(resume_path, "r") as file:
        resume_content = file.read()
else:
    resume_content = "No resume available."

# Pydantic model for incoming data validation
class ChatRequest(BaseModel):
    prompt: str

# Function to interact with OpenAI based on your resume content
def chat_with_openai(prompt):
    try:
        # Concatenate the resume content with the user prompt
        full_prompt = f"The following is the content of my resume:\n\n{resume_content}\n\nUser question: {prompt}"

        # Send the prompt to OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7  # Adjust temperature for creativity
        )
        
        # Extract the content of the response
        reply = response.choices[0].message.content
        return reply
    
    except Exception as e:
        return f"An error occurred: {e}"

# POST request to handle chatbot interaction
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Get the prompt from the request body
        prompt = request.prompt
        if not prompt:
            return {"error": "No prompt provided"}

        # Get the response from OpenAI
        response = chat_with_openai(prompt)
        
        return {"response": response}
    
    except Exception as e:
        return {"error": str(e)}

