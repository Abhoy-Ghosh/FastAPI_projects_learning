from fastapi import FastAPI, Path,HTTPException
import json



app = FastAPI()


#helper function to load data from json file
def load_json_data(): 
    with open('patients.json','r') as f:
        data =json.load(f)
    return data


@app.get("/")
def root():
    return {"message": "Hello , Ready to go"}


@app.get("/about")
def about():
    return {"message" : " A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    data  =load_json_data()
    return data

@app.get("/view/{patients_id}") # patients_id -> path parameter
def view_patients(patients_id : str = Path(...,description="The ID of the patient you want to view",example="P001")): #pass the path parameter into the function
   # path function should be called where we pass path params in the function
    # ... means all parameters are required
    # load all the patients data
    data = load_json_data()

    # try to check the patient exist with the patient_id or through error
    if patients_id in data:
            return data[patients_id]
 
    # return {"error": "Patient not found"} # return by function if the patient is not found
    raise HTTPException(status_code=404, detail="Patient not found")