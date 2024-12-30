import streamlit as st
from main import process_files
import os
import pandas as pd
import tempfile

def main():
    # Set up the page
    st.set_page_config(page_title="File Processor", layout="centered")

    # Add custom CSS for styling
    st.markdown(
        """
        <style>
            .container {
                background-color: #ffffff;
                padding: 20px 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 400px;
                margin: auto;
            }
            h1 {
                color: #333333;
                text-align: center;
            }
            label {
                font-weight: bold;
            }
            .stButton>button {
                width: 100%;
                background-color: #007bff;
                color: #ffffff;
                font-size: 16px;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #0056b3;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create the app UI
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.title("File Processor")

    # Input fields
    input_file = st.file_uploader("Choose an input CSV file", type=["csv"])
    report_type = st.selectbox("Select Report Type:", ["Task Report", "Status Report"])
    start_date = st.date_input("Start Date:")
    end_date = st.date_input("End Date:")

    # Process button
    if st.button("Process"):
        if input_file:
            try:
                # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_input_file:
                    tmp_input_file.write(input_file.getbuffer())
                    input_path = tmp_input_file.name

                # Create a temporary file for the output
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_output_file:
                    output_path = tmp_output_file.name

                # Convert dates to strings
                start_date_str = start_date.strftime("%Y-%m-%d")
                end_date_str = end_date.strftime("%Y-%m-%d")
                print(f"start_date = {start_date_str}")
                print(f"end_date = {end_date_str}")
                print(f"report_type = {report_type}")
                print(f"input_path = {input_path}")
                print(f"output_path = {output_path}")

                # Process the files
                process_files(input_path, output_path, start_date_str, end_date_str, report_type)

                # Read the processed file and provide a download link
                processed_df = pd.read_csv(output_path)
                st.success("File processed successfully!")
                st.download_button(
                    label="Download Processed File",
                    data=processed_df.to_csv(index=False).encode('utf-8'),
                    file_name='processed_file.csv',
                    mime='text/csv'
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please upload an input CSV file.")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
