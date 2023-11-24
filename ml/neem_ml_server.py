import pandas as pd
from utils.date_util import convert_to_bs
from datetime import datetime
from utils.fuzzy_util import fuzz_check
from sklearn.preprocessing import LabelEncoder, StandardScaler

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
    students = df[['id', 'student_name']]
    df = df[['dob', 'gender', 'last_qualification']].copy()

    df['dob'] = df['dob'].apply(convert)
    df['Age'] = df['dob'].apply(calculate_age)
    df = df.dropna(subset=['Age'])
    df = df[df['gender'] != 'other']
    return students, df

def prepare_df(df):
    df = df.drop(['dob'], axis=1)

    enum_set = ['Inter', '+2', 'NEB', 'BBA', 'BBS', 'Isc', 'BA', 'BSc', 'Civil', 'SEE', 'Undergraduate']
    def fuzz_check_udf(x):
        return fuzz_check(x, enum_set, 55, 'unknown_profession')

    df['last_qualification'] = df['last_qualification'].fillna('unknown_profession').apply(fuzz_check_udf)
    gender_encoded = pd.get_dummies(df['gender'], drop_first=True)
    df = pd.concat([df, gender_encoded], axis=1)

    label_encoder = LabelEncoder()
    df['lq'] = label_encoder.fit_transform(df['last_qualification'])

    return df.drop(['gender', 'last_qualification'], axis=1)


current_date = datetime.now()
knn_loaded = joblib.load('/home/samir/Desktop/rudraAnalytics/sub_projects/NEEM_PROD/ml/knn.joblib')


def identify(base):
    students, df = clean_df(base)
    df = prepare_df(df)
    x = df[['male','Age','lq']].to_numpy()
    scaler = StandardScaler()
    x_test = scaler.fit_transform(x)

    df['Prediction'] = knn_loaded.predict(x_test)

    filtered_df = df[df['Prediction'] == 0]

    return students[students.index.isin(filtered_df.index)].reset_index(drop=True)
