import pandas as pd
import os

def process_task_report_files(input_file_path, output_file_path, end_date):
    dataframes = []

    for file in input_file_path:
        df = pd.read_csv(file)
        dataframes.append(df)

    data = pd.concat(dataframes, ignore_index=True)

    data['Project completion date of the user'] = data['Project completion date of the user'].replace('Null', pd.NA)
    data['Project completion date of the user'] = pd.to_datetime(data['Project completion date of the user'], errors='coerce')


    df = data[
        (data["Project completion date of the user"].isna()) |
        (data["Project completion date of the user"] < end_date)
    ]

    df["Task Evidence"] = df["Task Evidence"].replace(["Null", "null"], pd.NA)

    df = df[df["Task Evidence"].notna() & (df["Task Evidence"].str.strip() != "")]

    project_list = [
        "BH_प्रोजेक्ट बेस्ड लर्निंग आधारित माइक्रो इम्प्रूवमेंट प्रोजेक्ट (2-1)",
        "BH_प्रोजेक्ट बेस्ड लर्निंग आधारित माइक्रो इम्प्रूवमेंट प्रोजेक्ट (2-2)",
        "BH_प्रोजेक्ट बेस्ड लर्निंग आधारित माइक्रो इम्प्रूवमेंट प्रोजेक्ट_2-3"
    ]
    
    df['Project Title'] = df['Project Title'].str.strip("' ")

    filtered_df = df[df['Project Title'].isin(project_list)]

    filtered_tasks = filtered_df[
        (
            filtered_df["Tasks"].str.contains(r"शिक्षक कक्षा 6", na=False)
            | filtered_df["Tasks"].str.contains(r"शिक्षक कक्षा 7", na=False)
            | filtered_df["Tasks"].str.contains(r"शिक्षक कक्षा 8", na=False)
        )
    ]

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

    grouped_df = (
        grouped.groupby(
            ["Declared State", "Project Title", "District", "Block", "School Name", "School ID"], dropna=False
        ).size().reset_index(name="TaskCount")
    )

    result_df = grouped_df[
        ["Project Title", "Declared State", "District", "Block", "School Name", "School ID", "TaskCount"]
    ]

    result_df.to_csv(output_file_path, index=False)  

    print(f"Transformation complete. Output saved to {output_file_path}.")

if __name__ == "__main__":
    process_task_report_files("input_file_path", "output_file_path", "end_date")