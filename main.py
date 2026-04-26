from fastapi import FastAPI, Path,HTTPException,Query
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


# Query parameters
@app.get("/sort")
def sort_patients(sort_by: str = Query(...,description="sort on the basis of height,weight and bmi"), # ... means it is obvious query parameter 
                  order : str =Query('asc',description='sort in ascending or descending order')) : # optional parameters used for decide sorting order with default value asc 
    
    valid_fields =['height','weight','bmi']

    if sort_by not in valid_fields:
         raise HTTPException(status_code="400",detail=f"Invalid sort field select from {valid_fields} request from client")
    
    if order not in ['asc','desc']:
         raise HTTPException(status_code=400,detail="order not selected as asc or desc")
    
    data = load_json_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x : x.get(sort_by,0),reverse=sort_order)
    # sorted_data =sorted(data.items(),key = lambda x : x[1].get('bmi'),reverse=sort_order) #if we want to keep keys of actual json

    return sorted_data

@app.get("/search")
def search_details_by_patientID(patient_id : str = Query(...,description="show names using patients id",example="P001")):
     
     data = load_json_data()

     if patient_id not in data:
          raise HTTPException(status_code = 404,detail ="given patient id is not found")
     
     patient = data[patient_id]
     result ={key : patient[key] for key in ['name','age','gender','city']}
     
     return result