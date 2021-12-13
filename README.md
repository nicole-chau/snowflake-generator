# Snowflake Generator Web App

## Project Description

This is a web app that procedurally generates a snowflake design using a L-system. 

The L-system grammar used in this project consists of the following:
- Axiom (initial configuration)
  - Default: 'FX'
- Symbols that correspond to rendering/drawing instructions:
  - 'F', 'X' : go forward
  - '-' : rotate right
  - '+' : rotate left
  - '[' : save current state (position and orientation)
  - ']'  : restore previous state (position and orientation)
  - '<' : halve draw distance
  - '>' : double draw distance  
- Grammar: rules determining what symbols should appear based on different contexts (i.e. given a single symbol (precondition), replace it with a set of symbols (post condition)
  - 'X' &rarr; '<F[+FX][-FX]FFFF[+FX][-FX]FXF>'

The drawing is created using the turtle module. The turtle's movements are defined by the generated L-system. 

On the home page of the website, a description of the application is displayed along with default L-system settings that can be used to draw a snowflake. Users are also able to modify the axiom, number of iterations and upload their own rules in a .json file format to generate their own snowflake patterns. Once the "Draw snowflake" button is clicked, the turtle starts to draw based on the defined L-system. The image is then saved and displayed on the "/results" page, where the L-system settings used to create the pattern are also displayed. 

Default snowflake pattern:  
<img src="https://user-images.githubusercontent.com/74137085/145895972-e3ebecf7-e670-440b-ad0b-c6ce6aa84228.png" alt="alt text" width="300px" height="300px">

Class defintions (+ dunder methods):
- Snowflake (\__init__)
- LSystem (\__init__, \__str__)

First-party module: json

Third-party modules: turtle, flask

## Installation / Running Instructions
Installation requirements:
```
pip install turtle
pip install flask
pip install pillow
```

Running instructions:
To launch the website, run
```
python3 server.py
```
The server is hosted on localhost:5000.

## Description of Code Structure

See individual files for description of specific functions.

### snowflake.py
This file contains a Snowflake class (inherits from Turtle) and a LSystem class.
The Snowflake class contains the methods necessary for drawing using a turtle and 
a given L-system set of drawing instructions.

### server.py
This file contains the methods used for redirecting users to different pages based on different requests and also receives/sends information about the L-system settings that are used to draw the snowflake. 

### draw_template.html
This is the html template used to render the /draw page. 
It contains a description of the application and displays the default L-system settings (axiom, number of iterations, rules). It also contains a form that allows users to change the axiom, number of iterations and upload their own .json file defining new rules for the L-system grammar. 

### result_template.html
This is the html template used to render the /results page.
It displays an image showing the resulting snowflake generated and the L-system settings used the generate the image. 

### rules.json
This file contains the default rules for the L-system. 
