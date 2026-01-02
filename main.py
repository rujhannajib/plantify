from flask import Flask, render_template, request
import os

app =  Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

@app.route("/", methods=["GET","POST"])
def index():

    display_image = None

    if request.method == "POST":    
        files = request.files["image"]
        image_path = os.path.join(app.config["UPLOAD_FOLDER"])
        files.save(image_path)
        display_image = image_path

    return render_template("index.html", display_image=display_image)

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
