"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

# In-memory student database
students = {
    "michael@mergington.edu": {"name": "Michael", "grade": 10},
    "daniel@mergington.edu": {"name": "Daniel", "grade": 11},
    "emma@mergington.edu": {"name": "Emma", "grade": 11},
    "sophia@mergington.edu": {"name": "Sophia", "grade": 12},
    "john@mergington.edu": {"name": "John", "grade": 9},
    "olivia@mergington.edu": {"name": "Olivia", "grade": 10},
    "liam@mergington.edu": {"name": "Liam", "grade": 12},
    "noah@mergington.edu": {"name": "Noah", "grade": 11},
    "ava@mergington.edu": {"name": "Ava", "grade": 10},
    "mia@mergington.edu": {"name": "Mia", "grade": 9},
    "amelia@mergington.edu": {"name": "Amelia", "grade": 11},
    "harper@mergington.edu": {"name": "Harper", "grade": 10},
    "ella@mergington.edu": {"name": "Ella", "grade": 12},
    "scarlett@mergington.edu": {"name": "Scarlett", "grade": 11},
    "james@mergington.edu": {"name": "James", "grade": 10},
    "benjamin@mergington.edu": {"name": "Benjamin", "grade": 12}
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/students")
def get_students():
    return students


@app.get("/students/{email}")
def get_student(email: str):
    if email not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[email]


@app.post("/students")
def add_student(email: str, name: str, grade: int):
    if email in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[email] = {"name": name, "grade": grade}
    return {"message": f"Student {name} added", "student": students[email]}


@app.put("/students/{email}")
def update_student(email: str, name: str = None, grade: int = None):
    if email not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if name is not None:
        students[email]["name"] = name
    if grade is not None:
        students[email]["grade"] = grade
    return {"message": f"Student {email} updated", "student": students[email]}


@app.delete("/students/{email}")
def delete_student(email: str):
    if email not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[email]
    return {"message": f"Student {email} removed"}


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student exists
    if email not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
