import turtle
from tkinter import *

class Snowflake(turtle.Turtle):
    def __init__(self):
        super().__init__()
        turtle.mode('logo')
        self.color('blue')
        self.pendown()
        self.hideturtle()

        self.distance = 40
        self.angle = 30
        self.speed(0)

        self.state_stack = []
        self.dist_stack = []


    """
    F, X : go forward
    - : rotate right
    + : rotate left
    [ : save current state (position and orientation)
    ] : restore previous state (position and orientation)
    < : halve draw distance
    > : double draw distance  
    """
    def draw_branch(self, string):
        for char in string:
            if char == 'F' or char == 'X':
                self.forward(self.distance)
            elif char == '-':
                self.right(self.angle)
            elif char == '+':
                self.left(self.angle)
            elif char == '[':
                curr_state = self.position()
                curr_angle = self.heading()
                self.state_stack.append((curr_state, curr_angle))
            elif char == ']':
                prev_state = self.state_stack.pop()
                self.setposition(prev_state[0])
                self.setheading(prev_state[1])
            elif char == '<':
                self.distance = self.distance / 2
            elif char == '>':
                self.distance = self.distance * 2
    
    def draw_snowflake(self, string):
        for i in range(6):
            self.home()
            self.right(60 * i)
            self.draw_branch(string)
    
    def save(self):
        img = self.getscreen()
        img.getcanvas().postscript(file="static/snowflake.eps")


# L system rule
class LSystem():
    """
    axiom (str)
    rules (dict)
    angle (int) : angle to rotate by 
    """
    def __init__(self, rules):
        self.rules = rules
    
    """
    F -> F[-FX][+FX]
    F[-F][+F]F[-F[-F]][[+F]F][+F[-F]][[+F]F]F[-F][+F]F


    F[-FX][+FX]F[-FX][+FX][+F[-FX][+FX]X][-F[-FX][+FX]X]


    'F': 'F[-F][+F]F'
    F[-F][+F]F[-F[-F][+F]F][+F[-F][+F]F]F[-F][+F]F
    """
    def apply_rule(self, char):
        if char in self.rules:
            if (type(self.rules[char]) is list):
                return self.rules[char][0]
            else:
                return self.rules[char]
        else:
            return char
    
    def _process_once(self, string):
        new_string = ""
        for char in string:
            new_string += self.apply_rule(char)
        return new_string
    
    def process_all(self, num_iter, string):
        new_string = string
        for i in range(num_iter):
            new_string = self._process_once(new_string)
        return new_string

    def __str__(self):
        rules_list = []
        for key, value in self.rules.items():
            rule = key + " --> " + value
            rules_list.append(rule)
        
        rules_str = ""
        for rule in rules_list:
            rules_str += rule
            rules_str += "\n"
        
        return rules_str


if __name__ == "__main__":
    rules = {'X': '<F[+FX][-FX]FFFF[+FX][-FX]FXF>'}
    lsystem = LSystem(rules)
    rules_str = lsystem.__str__()
    print("Rules: \n" + rules_str)

    processed_string = lsystem.process_all(2, 'FX')

    s = Snowflake()
    s.draw_snowflake(processed_string)
    s.save()
    turtle.mainloop()
