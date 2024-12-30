# from flask import Flask, render_template, request, flash, redirect, url_for
# from main import process_files

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         input_path = request.form.get("input_path")
#         output_path = request.form.get("output_path")
#         start_date = request.form.get("start_date")
#         end_date = request.form.get("end_date")
#         report_type = request.form.get("task") 
#         print(f"start_date = {start_date}")
#         print(f"end_date = {end_date}")
#         print(f"report_type = {report_type}")
#         print(f"input_path = {input_path}")
#         print(f"output_path = {output_path}")
#         try:
#             process_files(input_path, output_path, start_date, end_date, report_type)
#             flash("File processed successfully!", "success")
#         except Exception as e:
#             flash(f"Error: {str(e)}", "error")

#         # Redirect to the same page to prevent form re-submission
#         return redirect(url_for("index"))

#     # For GET requests, render the template
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)
