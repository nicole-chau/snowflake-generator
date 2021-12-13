## Project Description

This is a web app that procedurally generates a snowflake design using a L-system. 

The L-system grammar used in this project consists of the following:


## Installation / Running Instructions


## Description of Code Structure

# snowflake.py
This file contains a Snowflake class (inherits from Turtle) and a LSystem class.
The Snowflake class contains the methods necessary for drawing using a turtle and 
a given L-system set of drawing instructions.

# server.py
This file contains the methods used for redirecting users to different pages based on different requests and also receives/sends information about the L-system settings that are used to draw the snowflake. 

# draw_template.html
This is the html template used to render the /draw page. 
It contains a description of the application and displays the default L-system settings (axiom, number of iterations, rules). It also contains a form that allows users to change the axiom, number of iterations and upload their own .json file defining new rules for the L-system grammar. 

# result_template.html
This is the html template used to render the /results page.
It displays an image showing the resulting snowflake generated and the L-system settings used the generate the image. 