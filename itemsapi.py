import uvicorn
from  fastapi import FastAPI, HTTPException
import pyodbc
import warnings
from fastapi.middleware.cors import CORSMiddleware
from itemsprocessing import processed_lp

warnings.filterwarnings("ignore")
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=DESKTOP-SLF5UBP;"
    "Database=LearnerPerformanceDB;"
    "UID=demouser;"
    "PWD=roots;"
    "TrustServerCertificate=yes;"
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    try:
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    
@app.get("/")
async def read_root():
    return {"fastapi"}

@app.get("/items_processed") 
async def read_items_processed():
    return processed_lp

@app.get("/items_get")
async def read_items():
    conn = get_db_connection()
    items = conn.cursor().execute("select * from Student_performance_api").fetchall()
    return [
        {
            "StudentID": item.StudentID,"Age": item.Age, "Gender": item.Gender, "Ethnicity": item.Ethnicity,
            "ParentalEducation": item.ParentalEducation, "StudyTimeWeekly": item.StudyTimeWeekly,
            "Absences": item.Absences, "Tutoring": item.Tutoring, "ParentalSupport": item.ParentalSupport,
            "Extracurricular": item.Extracurricular, "Sports": item.Sports, "Music": item.Music,
            "Volunteering": item.Volunteering, "GPA": item.GPA, "GradeClass": item.GradeClass
        } for item in items
    ]
    
@app.post("/items_post")
async def create_items(
    StudentID: int, Age: int, Gender: bool, Ethnicity: int, ParentalEducation: int, StudyTimeWeekly: float,
    Absences: int, Tutoring: bool, ParentalSupport: int, Extracurricular: bool, Sports: bool, Music: bool,
    Volunteering: bool, GPA: float, GradeClass: int
):
    conn = get_db_connection()
    conn.cursor().execute(
        "insert into Student_performance_api (StudentID, Age, Gender, Ethnicity, ParentalEducation, StudyTimeWeekly, Absences, Tutoring, ParentalSupport, Extracurricular, Sports, Music, Volunteering, GPA, GradeClass) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        StudentID, Age, Gender, Ethnicity, ParentalEducation, StudyTimeWeekly, Absences,
        Tutoring, ParentalSupport, Extracurricular, Sports, Music, Volunteering,
        GPA, GradeClass
    ))
    conn.commit()
    return [
        {
            "StudentID": StudentID, "Age": Age, "Gender": Gender, "Ethnicity": Ethnicity,
            "ParentalEducation": ParentalEducation, "StudyTimeWeekly": StudyTimeWeekly,
            "Absences": Absences, "Tutoring": Tutoring, "ParentalSupport": ParentalSupport,
            "Extracurricular": Extracurricular, "Sports": Sports, "Music": Music,
            "Volunteering": Volunteering, "GPA": GPA, "GradeClass": GradeClass
        }
    ]
    
@app.put("/items_put")
async def update_items(
    StudentID: int, Age: int, Gender: bool, Ethnicity: int, ParentalEducation: int, StudyTimeWeekly: float,
    Absences: int, Tutoring: bool, ParentalSupport: int, Extracurricular: bool, Sports: bool, Music: bool,
    Volunteering: bool, GPA: float, GradeClass: int
):
    conn = get_db_connection()
    conn.cursor().execute(
        """
update Student_performance_api
set Age = ?,
    Gender = ?,
    Ethnicity = ?,
    ParentalEducation = ?,
    StudyTimeWeekly = ?,
    Absences = ?,
    Tutoring = ?,
    ParentalSupport = ?,
    Extracurricular = ?,
    Sports = ?,
    Music = ?,
    Volunteering = ?,
    GPA = ?,
    GradeClass = ?
where StudentID = ?

""", (Age, Gender, Ethnicity, ParentalEducation, StudyTimeWeekly, Absences, Tutoring, ParentalSupport,
      Extracurricular, Sports, Music, Volunteering, GPA, GradeClass, StudentID)
    )
    conn.commit()
    return {"message":"Object updated succesfully!"}

@app.delete("/items_delete")
async def delete_items(
    StudentID: int
):
    conn = get_db_connection()
    conn.cursor().execute("delete from Student_performance_api where StudentID = ?", (StudentID))
    conn.commit()
    return {"message": f"Sudent with ID {StudentID} deleted successfully!"}

if __name__=="_main_":
    uvicorn.run(app)

# uvicorn itemsapi:app --host 127.0.0.1 --port 8000
# uvicorn itemsapi:app --reload
# uvicorn itemsapi:app --host localhost --port 8000
# uvicorn itemsapi:app --host 0.0.0.0 --port 8000
