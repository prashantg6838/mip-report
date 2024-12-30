import pandas as pd
import os

def process_status_report_files(input_file_path, output_file_path, start_date, end_date)-> None:
    if not os.path.isdir(input_file_path):
        raise FileNotFoundError(f"Input directory does not exist: {input_file_path}")
    
    csv_files = [f for f in os.listdir(input_file_path) if f.endswith('.csv')]
    if not csv_files:
        raise ValueError("No CSV files found in the input directory.")

    dataframes = []

    for file in csv_files:
        file_path = os.path.join(input_file_path, file) 
        df = pd.read_csv(file_path) 
        dataframes.append(df) 

    required_columns = [
        "UUID", "User Type", "User sub type", "Declared State", "District", "Block",
        "School Name", "School ID", "Declared Board", "Org Name", "Program Name", 
        "Program ID", "Project ID", "Project Title", "Project Objective", 
        "Project start date of the user", "Project completion date of the user", 
        "Project Duration", "Project last Synced date", "Project Status", 
        "Certificate Status"
    ]

    for df in dataframes:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in {file}: {missing_columns}")

    data = pd.concat(dataframes, ignore_index=True)

    data = data[data['User sub type'] == 'TEACHER']
        
    filtered_df = data[
    (data["Project completion date of the user"] > start_date) & 
    (data["Project completion date of the user"] < end_date)
    ]

    transformed_data = filtered_df.groupby(['District', 'Block', 'School Name', 'School ID'], as_index=False).agg(
        TeachersStarted=('Project Status', lambda x: sum(x.str.strip().str.lower() == 'started')),
        TeachersInProgress=('Project Status', lambda x: sum(x.str.strip().str.lower() == 'inprogress')),
        TeachersSubmitted=('Project Status', lambda x: sum(x.str.strip().str.lower() == 'submitted'))
    )
    print(transformed_data)
    transformed_data['GRAND TOTAL'] = (
        transformed_data['TeachersStarted'] +
        transformed_data['TeachersInProgress'] +
        transformed_data['TeachersSubmitted']
    )

    transformed_data['COMPLETE'] = (
        (transformed_data['TeachersStarted'] == 0) &
        (transformed_data['TeachersInProgress'] == 0) &
        (transformed_data['TeachersSubmitted'] > 0)
    ).astype(int)

    transformed_data['INCOMPLETE'] = 1 - transformed_data['COMPLETE']

    transformed_data.rename(columns={
        'TeachersStarted': 'NO. OF TEACHERS WHO STARTED THE PROJECT',
        'TeachersInProgress': 'NO. OF TEACHERS WHO ARE IN PROGRESS',
        'TeachersSubmitted': 'NO. OF TEACHERS WHO SUBMITTED THE PROJECT'
    }, inplace=True)

    transformed_data.to_csv(output_file_path, index=False)
    print(f"Data transformation complete. Output saved to {output_file_path}")
