import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

students = pd.read_csv("/home/samir/Desktop/rudraAnalytics/NEEM/data/factored/students.csv")
students['admission_date'] = pd.to_datetime(students['admission_date'], format='%Y-%m-%d', errors='coerce')
df = students
df['YearWeek'] = df['admission_date'].dt.to_period('M')
new_intakes_count = df['YearWeek'].value_counts().sort_index()

new_intakes_count.index = new_intakes_count.index.astype(str)
plt.figure(figsize=(10, 6))
plt.bar(new_intakes_count.index, new_intakes_count.values)
plt.xlabel('Year-Week')
plt.ylabel('Number of New Intakes')
plt.title('Number of New Intakes Over Time (Weekly)')
plt.xticks(rotation=45)
# plt.show()

current_date = datetime.now()
week_index = current_date.strftime('%Y%m%dT%H')
output_image_path = f"/home/samir/Desktop/rudraAnalytics/NEEM_PROD/data/processed/neem_intake_weekly_report_{week_index}.png"

# Save the image with a high resolution (DPI can be adjusted)
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
plt.show()
