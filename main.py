import pandas as pd
import os
from status_report import process_status_report_files
from task_report import process_task_report_files

def process_files(input_file_path,output_file_path,start_date,end_date,report_type):
    if report_type == "Status Report" : 
        process_status_report_files(input_file_path,output_file_path,start_date,end_date)
    else :
        process_task_report_files(input_file_path,output_file_path,start_date,end_date)