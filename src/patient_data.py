import pandas as pd
from pathlib import Path


# Get the main CVMaXx folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Patient data file
PATIENT_FILE = BASE_DIR / "dataset" / "patients.csv"


def load_patients():
    """Load all patient records from the CSV file."""
    
    if not PATIENT_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(PATIENT_FILE)


def get_patient(patient_id):
    """Get one patient using their patient ID."""
    
    patients = load_patients()

    if patients.empty:
        return None

    patient = patients[patients["patient_id"] == patient_id]

    if patient.empty:
        return None

    return patient.iloc[0].to_dict()