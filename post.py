from fastapi import FastAPI,HTTPException,Path,Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
from fastapi.responses import JSONResponse
import json

app =FastAPI()

#pydantic model for patient data
class Patient(BaseModel):
    id : Annotated[str,Field(...,description="Id of the patiient",examples=["P001"])]
    name : Annotated[str, Field(...,description="name of the patient")]
    city : Annotated[str,Field(...,description="city name of the patient")]
    age : Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender : Annotated[Literal["Male",'Female','Others'],Field(...,description ="Gender of the patient")]
    height : Annotated[float,Field(...,gt = 0,description='Height in metersof the patient')]
    weight : Annotated[float,Field(...,gt = 0,description='Weight in kilograms of the patient')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight / self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return "Under Weight"
        elif self.bmi <25 :
            return 'Normal'
        else:
            return 'Obese'
        
# note : when client give the request_body (patient data) it does not contain the bmi and verdict

# utilty functions
def load_data():
    try:
        with open('patients.json','r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    

def store_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f,indent=4)
    


# routes and endpoint creation
@app.get("/")
def root():
    return {"message": "Hello , Ready to go"}


@app.get("/about")
def about():
    return {"message" : " A fully functional API to manage your patient records"}



@app.get("/view")
def view():
    data  =load_data()
    return data


@app.get("/view/{patients_id}") 
def view_patients(patients_id : str = Path(...,description="The ID of the patient you want to view",example=["P001"])): #pass the path parameter into the function
    data = load_data()

    if patients_id in data:
            return data[patients_id]
 
    raise HTTPException(status_code=404, detail="Patient not found")



@app.get("/sort")
def sort_patients(sort_by: str = Query(...,description="sort on the basis of height,weight and bmi"), # ... means it is obvious query parameter 
                  order : str =Query('asc',description='sort in ascending or descending order')) : # optional parameters used for decide sorting order with default value asc 
    
    valid_fields =['height','weight','bmi']

    if sort_by not in valid_fields:
         raise HTTPException(status_code=400,detail=f"Invalid sort field select from {valid_fields} request from client")
    
    if order not in ['asc','desc']:
         raise HTTPException(status_code=400,detail="order not selected as asc or desc")
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x : x.get(sort_by,0),reverse=sort_order)

    return sorted_data


# POST method   
@app.post("/create")
def create_patient(patient : Patient): # in this step pydantic do all the validation
    # step1: load existing data
    data = load_data()

    # step 2:check if the patient already exist or not in database
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exist")
    
    # step 3:new patient added to the database
    # data is dictionary and patient is Pydantic object of Patient class
    # need to convert the pydantic model into dictionary
    data[patient.id] = patient.model_dump(exclude = ['id'])

    # step 4: save the dictionary into the patient.json file in json format
    store_data(data)

    # step 5: give a response to the client
    return JSONResponse(status_code=201,content={"message":"Patient created successfully"})


