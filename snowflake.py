import turtle
from tkinter import *

class Snowflake(turtle.Turtle):
    def __init__(self):
        """
        Construct an instance of the Snowflake class, which inherits from Turtle.

        Attributes:
            - self.color: color of drawing
            - self.distance: distance the turtle moves forward by in self.forward()
            - self.angle: angle the turtle rotates by in self.right() and self.left()
            - self.speed: speed of turtle; 0 = fastest
            - self.state_stack: list that will act as the stack for 
                                storing intermediate turtle positions
                                (initialized to empty list)
        
        Args:
            None
        """
        super().__init__()
        turtle.mode('logo')
        self.color('blue')
        self.pendown()
        self.hideturtle()

        self.distance = 40
        self.angle = 30
        self.speed(0)

        self.state_stack = []


    def _draw_branch(self, string):
        """
        Helper function for draw_snowflake()
        Draws a single branch of a snowflake based on instructions given in 
        string generated from L-system grammar.

        Drawing instructions (precondition : postcondition):
            - 'F', 'X' : go forward
            - '-' : rotate right
            - '+' : rotate left
            - '[' : save current state (position and orientation)
            - ']'  : restore previous state (position and orientation)
            - '<' : halve draw distance
            - '>' : double draw distance  

        Args:
            string (str): string generated from L-system rules 
        
        Returns:
            None 
        """
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
        """
        Draws a full snowflake by drawing 6 branches and rotating them by 
        an angle offset each time.

        Args:
            string (str): string generated from L-system rules
        
        Returns:
            None
        """
        for i in range(6):
            # reset turtle to origin
            self.home()
            self.right(60 * i)
            self._draw_branch(string)
    
    def save(self):
        """
        Saves the turtle drawing to a .eps file. File is saved in static folder under
        "snowflake.eps" filename.

        Args:
            None
        
        Returns:
            None
        """
        img = self.getscreen()
        img.getcanvas().postscript(file="static/snowflake.eps")


class LSystem():
    def __init__(self, rules):
        """
        Constructs an instance of the LSystem class.

        Attributes:
            - self.rules: rules that define grammar for L-system

        Args:
            rules (dict): dictionary of rules defining the L-system grammar 
                          where the key is the precondition and the value is the postcondition
        """
        self.rules = rules

    def _apply_rule(self, char):
        """
        Helper function for _process_once().
        Applies a rule to an input character by comparing it to key values
        in self.rules.

        Args:
            char (str): character representing precondition
        
        Returns:
            str: corresponding postcondition to the input char or the original char if 
                 no rule is defined for the input
        """
        if char in self.rules:
            if (type(self.rules[char]) is list):
                return self.rules[char][0]
            else:
                return self.rules[char]
        else:
            return char
    
    def _process_once(self, string):
        """
        Helper function for process_all().
        Generates a new string based on input string and specified rules for the
        current L-system, i.e. one iteration of the system.
        Calls _apply_rule on each character in the string.

        Args:
            string (str): string to process with rules
        
        Returns:
            str: string representing the processed string (each symbol in the input string
                 is replaced with its corresponding postcondition if a rule is defined for it)
        """
        new_string = ""
        for char in string:
            new_string += self._apply_rule(char)
        return new_string
    
    def process_all(self, num_iter, string):
        """
        Processes the input string by calling _process_once num_iter number of times.

        Args:
            num_iter (int): number of iterations to process string for
            string (str): string to process with rules, i.e axiom of L-system
        
        Returns:
            str: string represnting the fully processed string
        """
        new_string = string
        for i in range(num_iter):
            new_string = self._process_once(new_string)
        return new_string

    def __str__(self):
        """
        Implements the __str__ dunder method by returning a string representation
        of the L-system rules. 

        Args:
            None
        
        Returns:
            str: formatted string representation of self.rules
        """
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
    # generates a snowflake with default parameters

    # set up L-system
    rules = {'X': '<F[+FX][-FX]FFFF[+FX][-FX]FXF>'}
    lsystem = LSystem(rules)
    rules_str = lsystem.__str__()
    print("Rules: \n" + rules_str)

    processed_string = lsystem.process_all(2, 'FX')

    # draw snowflake using turtle and defined L-system
    s = Snowflake()
    s.draw_snowflake(processed_string)
    s.save()
    turtle.mainloop()
