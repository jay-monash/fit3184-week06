from fastapi import FastAPI, HTTPException, Path
import os
from fastapi.responses import HTMLResponse
import json
import os
from typing import Dict


app = FastAPI()
COUNTER_FILE = "counter.txt"
COUNTERS_FILE = "counters.json"

@app.post("/api/v2/fit3184/increment")
def increment_fit3184_visitor():
    """
    POST is the correct method for actions that change server state.
    This is not idempotent, which is correct for an 'increment' action.
    """
    try:
        count = 0
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "r") as f:
                content = f.read().strip()
                count = int(content) if content else 0
        
        count += 1
        
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
            
        return {"message": "Visitor count incremented", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing counter: {str(e)}")

@app.get("/api/v2/fit3184", response_class=HTMLResponse)
def get_visitor_page():
    """
    Returns an HTML page that triggers a POST request to increment
    the counter and then redirects to the GET endpoint.
    """
    return """
    <html>
        <head>
            <title>FIT3184 Visitor Counter</title>
        </head>
        <body>
            <h1>Updating visitor count...</h1>
            <script>
                // 1. Send the POST request to increment
                fetch('/api/v2/fit3184/increment', { method: 'POST' })
                    .then(response => {
                        // 2. Redirect to the GET endpoint after success
                        window.location.href = '/api/v2/fit3184content';
                    })
                    .catch(error => {
                        console.error('Error incrementing counter:', error);
                        document.body.innerHTML = '<h1>Error updating count.</h1>';
                    });
            </script>
        </body>
    </html>
    """


@app.get("/api/v2/fit3184content")
def get_fit3184_content():
    """
    GET remains safe and idempotent, only returning the current state.
    """
    count = 0
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            content = f.read().strip()
            count = int(content) if content else 0
            
    return {"message": f"This is the FIT3184 handbook, currently {count} visitors."}



def load_counters() -> Dict[str, int]:
   """Load counters from a JSON file, returning an empty dict if the file is missing or corrupt."""
   if not os.path.exists(COUNTERS_FILE):
       return {}
   try:
       with open(COUNTERS_FILE, "r") as f:
           return json.load(f)
   except (json.JSONDecodeError, IOError) as e:
       # In a production environment, implement proper logging here
       return {}

def save_counters(counters: Dict[str, int]):
   """Persist the current counters dictionary to a JSON file."""
   try:
       with open(COUNTERS_FILE, "w") as f:
           json.dump(counters, f)
   except IOError as e:
       # In a production environment, implement proper logging here
       pass

@app.get("/courses")
def get_courses():
   return load_counters()

@app.post("/api/v2/fit{unit_code}")
async def get_unit_count(unit_code: str = Path(..., regex="^[0-9]{4}$")):
   """
   Endpoint to increment and return visitor count for dynamic FIT unit codes.
   The regex regex="^fit[0-9]{4}$" ensures the path starts with 'fit' followed by 4 digits.
   """
   try:
       unit_code = f"fit{unit_code}"
       counters = load_counters()
       count = counters.get(unit_code, 0)
       count += 1
       counters[unit_code] = count
       save_counters(counters)
       return {
           "unit": unit_code,
           "message": f"Welcome to the {unit_code} handbook. You are visitor number {count}."
       }
   except Exception as e:
       # Catch generic exceptions to prevent leaking server details
       raise HTTPException(status_code=500, detail="An internal error occurred while processing the request.")
