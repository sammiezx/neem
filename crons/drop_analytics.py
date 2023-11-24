import sys
file_path = '/home/samir/Desktop/rudraAnalytics/sub_projects/NEEM_PROD'
sys.path.append(file_path)

from utils.mysql_util import get_dataframe
from ml.neem_train_drop_correlation import train_phase
from ml.neem_ml_server import identify
df = get_dataframe()
train_phase(df)

# NOW THE MAIN ARCHITECTURE

# A) DO WE TEST ON NEW DATA AND PREDICT IF THE DROP PROBABLITY HIGH
# OR
# B) DO WE TAKE THE WHOLE DATA AND FIND THE NEXT POSSIBLE SET OF DROPPERS

# we'll do B for now

df = identify(df)
df.to_csv(f"{file_path}/data/possible_students_to_drop.csv", index=False)


