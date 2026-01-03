from flask import Flask, render_template, request
import os
from transformers import pipeline
from PIL import Image
import json

app =  Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

id_2_species = "class_idx_to_species_id.json"
species_2_name = "plantnet300K_species_id_2_name.json"

with open(id_2_species, 'r') as file:
    id_2_species_dict = json.load(file)

with open(species_2_name, 'r') as file:
    species_2_name_dict = json.load(file)

def get_species_name(label:str):
    return species_2_name_dict[id_2_species_dict[str(label)]]

def generate_predictions(image):
    res = classifier(image)
    predictions = []
    for i in range(3):
        species_name = get_species_name(res[i]["label"])
        conf_score =  round(res[i]["score"],2)
        predictions.append({"name":species_name, "score":conf_score})
    return predictions

# Load your Hugging Face model
classifier = pipeline(
    "image-classification",
    model="janjibDEV/vit-plantnet300k"
)

@app.route("/", methods=["GET","POST"])
def index():
    prediction = None
    display_image = None

    if request.method == "POST":    
        files = request.files["image"]
        image_path = os.path.join(app.config["UPLOAD_FOLDER"])
        files.save(image_path)
        display_image = image_path

        target_image = Image.open(display_image)
        # res = classifier(target_image)

        # prediction = (get_species_name(res[0]["label"]), round(res[0]["score"],2))
        prediction = generate_predictions(target_image)
    return render_template("index.html", display_image=display_image, prediction=prediction)

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
