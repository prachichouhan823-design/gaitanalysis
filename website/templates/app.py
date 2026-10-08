import os

from flask import Flask, render_template, request

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)


@app.route("/", methods=["GET", "POST"])
def home():
    message = None

    if request.method == "POST":
        video = request.files.get("video")
        if video and video.filename:
            message = f"Video received: {video.filename}. Your gait analysis workflow is ready to process it."
        else:
            message = "Please choose a valid video file before submitting."

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)