import pandas as pd
# import numpy as np
from utils.date_util import convert_to_bs
from datetime import datetime
from utils.fuzzy_util import fuzz_check
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib

def convert(x):
    try:
        return convert_to_bs(x)
    except:
        return None

def calculate_age(birthdate):
    try:
        return current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    except:
        return None
    
def clean_df(df):
    df = df[['dob', 
            'gender', 
            'last_qualification', 
            #    'father_occupation', 
            #    'division', 
            'completed_date']].copy()

    df['dob'] = df['dob'].apply(convert)
    df['Age'] = df['dob'].apply(calculate_age)
    df = df.dropna(subset=['Age'])
    df = df[df['gender'] != 'other']
    return df

def prepare_df(df):
    df['completed'] = ~df['completed_date'].isna()
    df['completed'] = df['completed'].astype(int)
    df = df.drop(['completed_date', 'dob'], axis=1)

    enum_set = ['Inter', '+2', 'NEB', 'BBA', 'BBS', 'Isc', 'BA', 'BSc', 'Civil', 'SEE', 'Undergraduate']
    def fuzz_check_udf(x):
        return fuzz_check(x, enum_set, 55, 'unknown_profession')

    df['last_qualification'] = df['last_qualification'].fillna('unknown_profession').apply(fuzz_check_udf)
    gender_encoded = pd.get_dummies(df['gender'], drop_first=True)
    df = pd.concat([df, gender_encoded], axis=1)

    label_encoder = LabelEncoder()
    df['lq'] = label_encoder.fit_transform(df['last_qualification'])

    return df

def train_and_save_df(df):
    x = df[['male','Age','lq']].to_numpy()
    y = df['completed'].to_numpy()
    x_train , x_test , y_train , y_test = train_test_split(x,y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.fit_transform(x_test)

    # Experiment with various model in this section
    knn.fit(x_train,y_train)

    y_pred = knn.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"TRAINED WITH [ACCURACY]: {accuracy*100} %")

    joblib.dump(knn, '/home/samir/Desktop/rudraAnalytics/sub_projects/NEEM_PROD/ml/knn.joblib')


k= 5
knn = KNeighborsClassifier(n_neighbors=k)
current_date = datetime.now()

def train_phase(base):
    df = clean_df(base)
    df = prepare_df(df)
    train_and_save_df(df)