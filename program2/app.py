from flask import Flask, request, render_template_string
import os
import subprocess
import zipfile
import sys
import yagmail
import re

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Mashup Web Service</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input { padding: 6px; margin: 6px 0; width: 250px; }
        button { padding: 8px 15px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>🎵 Mashup Generator</h2>
    <form method="post">
        <label>Singer Name:</label><br>
        <input name="singer" required><br>

        <label>Number of Videos:</label><br>
        <input name="n" type="number" min="1" required><br>

        <label>Duration (seconds per clip):</label><br>
        <input name="d" type="number" min="1" required><br>

        <label>Email ID:</label><br>
        <input name="email" type="email" required><br><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form["singer"]
        n = request.form["n"]
        d = request.form["d"]
        email = request.form["email"]

        if not is_valid_email(email):
            return "<h3>Invalid Email Address!</h3>"

        output_file = "final_mashup.mp3"
        zip_file = "mashup.zip"

        try:
         
            program1_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "program1",
                "mashup_generator.py"
            )

            # Run Program 1
            subprocess.run(
                [sys.executable, program1_path, singer, n, d, output_file],
                check=True
            )

            # Zip the output file
            with zipfile.ZipFile(zip_file, "w") as z:
                z.write(output_file)

            # Load sender credentials from environment variables
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")

            if not sender_email or not sender_password:
                return "<h3>Email credentials not configured on server.</h3>"

            # Send email
            yag = yagmail.SMTP(sender_email, sender_password)
            yag.send(
                to=email,
                subject="Your Mashup File 🎵",
                contents="Attached is your generated mashup.",
                attachments=[zip_file]
            )

            return "<h3>Mashup sent successfully to your email!</h3>"

        except Exception as e:
            return f"<h3>Error occurred: {e}</h3>"

    return render_template_string(HTML_FORM)


if __name__ == "__main__":
    app.run(debug=True)
