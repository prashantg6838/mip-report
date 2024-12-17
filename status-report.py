import pandas as pd
import os

# Specify the directory containing the files
directory_path = r"C:\Users\PRASHANT\Desktop\raw-status-data"

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
data = pd.concat(dataframes, ignore_index=True)

# Filter rows where [User sub type] = 'TEACHER'
data = data[data['User sub type'] == 'TEACHER']

# Step 2: Group data and calculate the required columns
transformed_data = data.groupby(['District', 'Block', 'School Name', 'School ID'], as_index=False).agg(
    TeachersStarted=('Project Status', lambda x: sum(x == 'started')),
    TeachersInProgress=('Project Status', lambda x: sum(x == 'inprogress')),
    TeachersSubmitted=('Project Status', lambda x: sum(x == 'submitted'))
)

# Calculate GRAND TOTAL
transformed_data['GRAND TOTAL'] = (
    transformed_data['TeachersStarted'] +
    transformed_data['TeachersInProgress'] +
    transformed_data['TeachersSubmitted']
)

# Calculate COMPLETE and INCOMPLETE
transformed_data['COMPLETE'] = (
    (transformed_data['TeachersStarted'] == 0) &
    (transformed_data['TeachersInProgress'] == 0) &
    (transformed_data['TeachersSubmitted'] > 0)
).astype(int)

transformed_data['INCOMPLETE'] = 1 - transformed_data['COMPLETE']

# Step 3: Save the transformed data to a CSV file
transformed_data.rename(columns={
    'School Name': 'School Name',
    'School ID': 'School ID'
}, inplace=True)  # Align column names with the SQL output

transformed_data.rename(columns={
    'TeachersStarted': 'NO. OF TEACHERS WHO STARTED THE PROJECT',
    'TeachersInProgress': 'NO. OF TEACHERS WHO ARE IN PROGRESS',
    'TeachersSubmitted':'NO. OF TEACHERS WHO SUBMITTED THE PROJECT'
},inplace=True)

print(transformed_data.head(1))
transformed_data.to_csv(r"C:\Users\PRASHANT\Desktop\status-report\status02.csv", index=False)  # Replace with your output file path

print("Data transformation complete. Output saved to 'status02.csv'.")
