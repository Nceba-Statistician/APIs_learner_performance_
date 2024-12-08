import pyodbc
import warnings
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json

warnings.filterwarnings("ignore")

conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=DESKTOP-SLF5UBP;"
    "Database=LearnerPerformanceDB;"
    "UID=demouser;"
    "PWD=roots;"
    "TrustServerCertificate=yes;"
)
    

query = "select * from Student_performance_api"

Student_performance_api = pd.read_sql_query(query, conn)


Student_performance_api["Gender"] = Student_performance_api["Gender"].map({1: "Male", 0: "Female"})
Student_performance_api["ParentalEducation"] = Student_performance_api["ParentalEducation"].map({0: "None", 1: "Poor", 2: "Below Average", 3: "Satisfactory", 4: "Excellent"})
Student_performance_api["ParentalSupport"] = Student_performance_api["ParentalSupport"].map({0: "None", 1: "Poor", 2: "Below Average", 3: "Satisfactory", 4: "Excellent"})
Student_performance_api["Sports"] = Student_performance_api["Sports"].map({1: "Yes", 0: "No"})
Student_performance_api["Music"] = Student_performance_api["Music"].map({1: "Yes", 0: "No"})


AggregatedStudentPerformance = Student_performance_api.groupby(["Age", "Gender", "ParentalEducation", "ParentalSupport"]).agg(
    AverageGPA=("GPA", "mean"),
    AverageAbsences=("Absences", "mean"),
    AverageStudyTimeWeekly=("StudyTimeWeekly", "mean")
).reset_index()

AggregatedStudentPerformance = AggregatedStudentPerformance.pivot(
    index=["Age", "ParentalEducation", "ParentalSupport"], columns="Gender").reset_index()

AggregatedStudentPerformance.columns = [
    "Age",
    "ParentalEducation", "ParentalSupport",
    "FemaleGPA", "MaleGPA", 
    "FemaleAbsences", "MaleAbsences",
    "FemaleStudyTimeWeekly", "MaleStudyTimeWeekly"
]

json_AggregatedStudentPerformance = AggregatedStudentPerformance.to_json(orient="records")

with open("out_AggregatedStudentPerformance.json", "w") as file:
    file.write(json_AggregatedStudentPerformance)

with open("out_AggregatedStudentPerformance.json", "r") as file:
    processed_lp = json.load(file)


