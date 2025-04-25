import openai
import os

openai.api_key = os.getenv("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")  # Or replace with your key directly
# openai.api_key = "sk-..."

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
        
user_list: list[User] = []

@app.get("/users")
async def get_users():
    return {"users": user_list}

@app.post("/users")
async def add_user(user: User):
    user_list.append(user)
    return {"users": user_list}

@app.delete("/users")
async def delete_user(index: int = 0):
    user_list.pop(index)
    return {"users": user_list}



class Employer(BaseModel):
    employer_name: str
    username: str
        
employer_list: list[Employer] = []

@app.get("/employers")
async def get_employers():
    return {"employers": employer_list}

@app.post("/employers")
async def add_employer(employer: Employer):
    employer_list.append(employer)
    return {"employers": employer_list}

@app.delete("/employers")
async def delete_employer(index: int = 0):
    employer_list.pop(index)
    return {"employers": employer_list}



class JobListing(BaseModel):
    title: str
    location: str
    type: str
    experience: str
    salary: str
        
listing_list: list[JobListing] = []

@app.get("/listings")
async def get_listings():
    return {"listings": listing_list}

@app.post("/listings")
async def add_listing(listing: JobListing):
    listing_list.append(listing)
    return {"listings": listing_list}

@app.delete("/listings")
async def delete_listing(index: int = 0):
    listing_list.pop(index)
    return {"listings": listing_list}

@app.get("/recommendation")
async def get_recommendation(username: str):
    user = next((u for u in user_list if u.username == username), None)
    if not user:
        return {"error": "User not found"}

    job_descriptions = "\n".join([f"{j.title} in {j.location}, {j.type}, requires {j.experience}, salary: {j.salary}" for j in listing_list])
    
    prompt = (
        f"Given the following user: {user.first_name} {user.last_name}, "
        f"recommend one suitable job from the following listings:\n\n{job_descriptions}\n\n"
        f"Respond with just the recommended job title and a short reason."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful career assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {"recommendation": reply}
    except Exception as e:
        return {"error": str(e)}
