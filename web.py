from flask import Flask, request, render_template
import main

app = Flask(__name__)

@app.route("/", methods=["POST"])
def info():
    #face_to_search_location = request.form["face_to_search_directory"]
    #print(face_to_search_location)
    action = request.form["action"]
    try:
        action = int(action)
    except ValueError:
        return "Input Error"
    
    return "Done"

@app.route("/")
def index():
    return render_template("software_MP.html")


app.run(host="0.0.0.0", port=80, debug=True)

