# built-in modules
import json
import os

# web dev modules
from flask import Flask, flash, render_template, request, url_for, redirect

from snowflake import *

from PIL import Image

# Flask constants, do not change!
ALLOWED_SYMBOLS = {'F', 'X', '-', '+', '[', ']', '<', '>'}
app = Flask(__name__)
app.secret_key = 'ax9o4klasi-0oakdn'  # random secret key (needed for flashing)


def eps_to_png(image_eps):
    """
    Transforms an eps image image_eps to a png image
    Saves the png image to the same directory of image_eps

    Args:
        image_eps (str): the filename of the image

    Returns:
        None
    """
    image = Image.open(image_eps).convert('RGBA')
    # get filename of image
    filename = image_eps.split('.')[0]
    image_png = filename + ".png"
    image.save(image_png)


def parse_rules(rules_json):
    """
    Extracts rules from json file into a dictionary to create l system with

    Args:
        rules_json (str): filename of .json file containing rules 

    Returns:
        rules (dict): dictionary containing rules for l system
    """
    rules_f = open(rules_json)
    rules_data = json.load(rules_f)
    return rules_data


def create_snowflake(axiom, num_iter, rules):
    """
    Creates the snowflake drawing by initializing L-system and Snowflake turtle. 
    Saves the image after turtle is done drawing.

    Args:
        rules (dict): dictionary of rules for L-system
                      NOTE: makes several assumptions about input rules:
                      1. Precondition only consists of 1 symbol
                      2. Rules only contain valid symbols
                      3. Dictionary is non-empty, i.e. at least 1 valid rule is defined
    
    Returns:
        None
    """
    lsystem = LSystem(rules)
    processed_string = lsystem.process_all(int(num_iter), axiom)

    s = Snowflake()
    s.draw_snowflake(processed_string)
    s.save()


@app.route("/", methods=["GET"])
def home():
    """
    Redirect the user from the root URL to the /draw URL.

    Args:
        None

    Returns:
        The required return by Flask so the user is redirected to the /draw URL
    """
    rules = parse_rules("rules.json")
    return render_template("draw_template.html", rules=rules.items())


@app.route("/draw", methods=["GET", "POST"])
def handle_draw():
    """
    Method that handles the /draw route.

    GET requests
        1. render draw_template.html

    POST requests
        1. flash and redirect back to /upload if axiom contains invalid symbols
        2. redirecto to /result with axiom and num_iter query parameters set to 
           values from form

    Args:
        None

    Returns:
        The required returns by Flask for the specified redirect/setting update
        behavior for both GET and POST requests as described above.
    """
    if request.method == "GET":
        rules = parse_rules("rules.json")
        return render_template("draw_template.html", rules=rules.items())
    elif request.method == "POST":
        rules_json = request.files["rules"]
        rules_json = rules_json.filename

        # if no file uploaded then use default "rules.json" file
        if rules_json == "":
            rules_json = "rules.json"
        
        # check that uploaded file is json file 
        if not rules_json.endswith(".json"):
            flash("Please upload a json file")
            return redirect("/draw")

        axiom = request.form.get("axiom")
        # check for invalid symbols in axiom input 
        for char in axiom:
            if char not in ALLOWED_SYMBOLS:
                flash("The only symbols allowed are: 'F', 'X', '-', '+', '[', ']', '<', '>'")
                return redirect("/draw")

        # get number of l system iterations
        num_iter = request.form.get("iterations")
        
        return redirect(url_for("handle_result", axiom=axiom, num_iter=num_iter, rules_json=rules_json))

@app.route("/result", methods=["GET"])
def handle_result():
    """
    Method that handles the /result route.

    The specified axiom, number of iterations and rules come as the query parameters
    "axiom", "num_iter" and "rules_json" respectively.

    GET requests:
        1. Use create_snowflake() to generate the image with turtle
        2. Convert the saved image from eps to opng
        3. Render result_template.html with appropriate context variables

    Args:
        None

    Returns:
        The required returns by Flask for the specified redirect/rendering
        behavior for GET requests as described above.
    """
    query_dict = request.args
    axiom = query_dict.get("axiom")
    num_iter = query_dict.get("num_iter")
    rules_json = query_dict.get("rules_json")
    rules = parse_rules(rules_json)

    create_snowflake(axiom, num_iter, rules)
    eps_to_png("static/snowflake.eps")
    return render_template("result_template.html", 
                           filename="snowflake.png", 
                           axiom=axiom, 
                           num_iter=num_iter,
                           rules=rules.items())


if __name__ == "__main__":
    app.run(port=5000, debug=True)
