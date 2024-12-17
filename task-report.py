import pandas as pd
import os

# Specify the directory containing the files
directory_path = r"C:\Users\PRASHANT\Desktop\raw-task-data"

# List all CSV files in the directory
csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

# Initialize an empty list to store DataFrames
dataframes = []

# Loop through each file and read it
for file in csv_files:
    file_path = os.path.join(directory_path, file)  # Full file path
    df = pd.read_csv(file_path)  # Read the CSV file
    dataframes.append(df)  # Add the DataFrame to the list

# Combine all DataFrames into a single DataFrame (optional)
df = pd.concat(dataframes, ignore_index=True)

df = df[df['Project Title'] == 'BH_प्रोजेक्ट बेस्ड लर्निंग आधारित माइक्रो इम्प्रूवमेंट प्रोजेक्ट (2-1)']

# Filter out rows where "Task Evidence" is Null
df_filtered = df[df["Task Evidence"].notna()]

# Further filter rows based on "Tasks" containing specific keywords and "Project completion date of the user"
filtered_tasks = df_filtered[
    (
        df_filtered["Tasks"].str.contains(r"शिक्षक कक्षा 6", na=False)
        | df_filtered["Tasks"].str.contains(r"शिक्षक कक्षा 7", na=False)
        | df_filtered["Tasks"].str.contains(r"शिक्षक कक्षा 8", na=False)
    )
    & (df_filtered["Project completion date of the user"] < "2024-11-01")
]

# Group by the specified columns and calculate the task count
grouped = (
    filtered_tasks
    .groupby([
        "Declared State",
        "Project Title",
        "District",
        "Block",
        "School Name",
        "School ID",
        "Tasks"
    ])
    .size()
    .reset_index(name="Taskcount")
)



# # Step 2: Filter the data based on conditions
# filtered_data = data[
#     (data['Task Evidence'].notna()) &
#     (
#         data['Tasks'].str.contains('शिक्षक कक्षा 6') |
#         data['Tasks'].str.contains('शिक्षक कक्षा 7') |
#         data['Tasks'].str.contains('शिक्षक कक्षा 8')
#     ) &
#     (data['Project completion date of the user'] < '2024-11-01')
# ]


# # Step 3: Group data to count tasks
# extracted_field = filtered_data.groupby([
#     'Declared State', 'District', 'Block', 'School Name', 'School ID', 'Tasks'
# ], as_index=False).size().rename(columns={'size': 'TaskCount'})

# print(extracted_field)

# # Step 4: Further group data to calculate TaskCount per school
# modified_task_report = extracted_field.groupby([
#     'Declared State', 'District', 'Block', 'School Name', 'School ID'
# ], as_index=False)['TaskCount'].sum()

# # Step 5: Save the result to a CSV file
grouped.to_csv(r"C:\Users\PRASHANT\Desktop\modified-task-data\Modified-task-report.csv", index=False)  # Replace with the actual path

print("Transformation complete. Output saved to 'Modified-task-report4.csv'.")
