from flask import Flask, render_template, request, send_from_directory, jsonify
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/run_demo", methods=["POST"])
def run_demo():
    try:
        num_comm = int(request.form.get("num_community_users", 10))
        num_other = int(request.form.get("num_other_users", 20))
        num_resources = int(request.form.get("num_resources", 10))
        num_tags = int(request.form.get("num_tags", 5))
        comm_act = int(request.form.get("community_activity", 10))
        other_act = int(request.form.get("other_activity", 5))

        result = subprocess.run(
            ["python", "uploads/demo_code.py"],
            input=f"no\n{num_comm}\n{num_other}\n{num_resources}\n{num_tags}\n{comm_act}\n{other_act}\n",
            capture_output=True,
            text=True
        )
        output = result.stdout[-2000:]
        image_url = "/uploads/graph.png" if os.path.exists("uploads/graph.png") else None
        return jsonify({"output": output, "image": image_url})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

