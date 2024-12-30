import streamlit as st
from main import process_files
import os

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
    input_path = st.text_input("Input Path (File or Folder):", placeholder="Enter input file or folder path")
    output_path = st.text_input("Output Path (File or Folder):", placeholder="Enter output file or folder path")
    report_type = st.selectbox("Select Report Type:", ["Task Report", "Status Report"])
    start_date = st.date_input("Start Date:")
    end_date = st.date_input("End Date:")

    # Process button
    if st.button("Process"):
        if input_path and output_path:
            if os.path.isfile(input_path) or os.path.isdir(input_path):
                try:
                    # Convert dates to strings
                    start_date_str = start_date.strftime("%Y-%m-%d")
                    end_date_str = end_date.strftime("%Y-%m-%d")
                    print(f"start_date = {start_date_str}")
                    print(f"end_date = {end_date_str}")
                    print(f"report_type = {report_type}")
                    print(f"input_path = {input_path}")
                    print(f"output_path = {output_path}")
                    process_files(input_path, output_path, start_date_str, end_date_str, report_type)
                    st.success("File processed successfully!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error("Invalid input path. Please enter a valid file or folder path.")
        else:
            st.error("Please provide both input path and output file.")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
