#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import random


# Functions from graphics.pyx

# def DrawText(core.Canvas c, Font f, int x, int y, Color color, text):
#     return cppinc.DrawText(c.__getCanvas(), f.__font, x, y, color.__color, text.encode('utf-8'))

# def DrawCircle(core.Canvas c, int x, int y, int r, Color color):
#     cppinc.DrawCircle(c.__getCanvas(), x, y, r, color.__color)

# def DrawLine(core.Canvas c, int x1, int y1, int x2, int y2, Color color):
#     cppinc.DrawLine(c.__getCanvas(), x1, y1, x2, y2, color.__color)


# User sets RGB goal using input method - manually enter RGB values
def set_rgb_goal():
    # Take user input for Goal_RGB combination
    r_goal = input("How much red do you want? (Number between 0 and 255, where 255 is the most red possible): ")
    g_goal = input("How much green do you want? (Number between 0 and 255, where 255 is the most green possible): ")
    b_goal = input("How much blue do you want? (Number between 0 and 255, where 255 is the most blue possible): ")
    # Create RGB_goal tuple 
    rgb_goal = (r_goal, g_goal, b_goal)
    return rgb_goal
    #pass

# Set limited examples for computation reasons
def set_rgb_range(rgb_goal):
    number_of_values = 20
    r_list = random.sample(range(255),number_of_values-1) # Create list of random r-values (unique integer values between 0-255, with one less than the desired number of values to make space for the 'goal' value in the list)
    r_list.append(rgb_goal[0]) # Add the correct R value. Needs to be included BELOW the point where Goal_RGB combination is defined
    g_list = random.sample(range(255),number_of_values-1) # Create list of random g-values (unique integer values between 0-255, with one less than the desired number of values to make space for the 'goal' value in the list)
    g_list.append(rgb_goal[1]) # Add the correct G value. Needs to be included BELOW the point where Goal_RGB combination is defined
    b_list = random.sample(range(255),number_of_values-1) # Create list of random b-values (unique integer values between 0-255, with one less than the desired number of values to make space for the 'goal' value in the list)
    b_list.append(rgb_goal[2]) # Add the correct B value. Needs to be included BELOW the point where Goal_RGB combination is defined

    rgb_combo_list = [] # Initialise rgb list

    # Append each value into a list of rgb combinations (list length as defined by 'number_of_values' specified when calling function)
    for i in range(number_of_values):
        rgb_combo_list.append((r_list[i],g_list[i],b_list[i])) # Order is R,G,B

    return rgb_combo_list
    #pass


# Check rgb prediction against goal, return correct or not
def check_rgb_prediction(self,rgb_goal,rgb_prediction):
    if rgb_prediction == rgb_goal:
        print("RGB prediction is equal to RGB goal!")
        guess_is_correct = True
        return guess_is_correct
    else:
        print("RGB Prediction does not equal RGB goal...")
        guess_is_correct = False
        return guess_is_correct
        # Consider using 'continue' statement instead of explicitly assigning to False, as pre-existing value is false

    #pass

# Program to guess an RGB combination
def make_rgb_prediction(self,list_of_untried_rgb_combos):
    rgb_prediction = list_of_untried_rgb_combos.pop(random.randint(0,len(list_of_untried_rgb_combos)-1))
    return list_of_untried_rgb_combos,rgb_prediction
    #pass

def finished_guessing(self,correct_guess,number_of_guesses):
    if correct_guess == False:
        print("didn't get it this time, even after ",number_of_guesses,"guesses!")
    else:
        print("got it right, RGB value is: ",correct_guess,". And it only took ,",number_of_guesses,"guesses :p")

    #pass

# Take user input
def do_you_want_to_play_again(self):
    answer = input("Do you want to play again? Enter 1 for yes, enter 2 for no.")
    return answer
    #pass

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

        # Take coordinates of goal light and colour of goal light
    def set_goal_LED(self,rgb_goal):
        x1 = 5 # Left most edge of light
        x2 = 7 # Right most edge of light
        y1 = 23 # Bottom edge of light
        y2 = 26 # Top edge of light
        color = graphics.Color(rgb_goal[0],rgb_goal[1],rgb_goal[2])
        for row_value in range(y1,y2):
            graphics.DrawLine(canvas,x1,row_value,x2,row_value, color)
        #pass


        # Set 'prediction' light on LED matrix to predicted RGB colour
    def set_predicted_LED(self,rgb_prediction):
        x1 = 5 # Left most edge of light
        x2 = 7 # Right most edge of light
        y1 = 15 # Bottom edge of light
        y2 = 18 # Top edge of light
        color = graphics.Color(rgb_prediction[0],rgb_prediction[1],rgb_prediction[2])
        for row_value in range(y1,y2):
            graphics.DrawLine(canvas,x1,row_value,x2,row_value, color)
        #pass


        # Set LED strips to match the R, G, and B values
        # LED matrix has height = 64, width = 32
        # Graph will use height = 32, width = 32
        # Lower 32 LEDs will be used for Goal / Prediction / signalling correct answer
    def set_predicted_graph_LED(self,rgb_prediction):
        # Initialise red, green, blue LED colours
        red = graphics.Color(255, 0, 0)
        green = graphics.Color(0, 255, 0)
        blue = graphics.Color(0, 0, 255)
        faint_cyan = graphics.Color(0, 50, 50)

        # Initialising 
        r_prediction = rgb_prediction(0)
        g_prediction = rgb_prediction(1)
        b_prediction = rgb_prediction(2)
        
        # Graph x-axis (i.e. bottom edge of graph)
        graph_x_axis = 32
        graphics.DrawLine(canvas,32,0,32,32,faint_cyan)
        
        # Calculating required height of each bar in bar graph as a proportion out of 'predicted value / 256'. Values use 'int', which rounds down to nearest integer.
        r_graph_height = int(r_prediction * 32 / 256) + graph_x_axis
        g_graph_height = int(g_prediction * 32 / 256) + graph_x_axis
        b_graph_height = int(b_prediction * 32 / 256) + graph_x_axis

        # Specifying left and right edges of each bar graph
        r_graph_x_coords = [5,7]
        g_graph_x_coords = [14,16]
        b_graph_x_coords = [23,25]

        # Switching on LEDs to calculated proportional height
        # Red graph
        for n in range(graph_x_axis,r_graph_height):
            graphics.DrawLine(canvas,n,r_graph_x_coords[0],n,r_graph_x_coords[1], red)
        # Green graph
        for n in range(graph_x_axis,g_graph_height):
            graphics.DrawLine(canvas, n, g_graph_x_coords[0], n, g_graph_x_coords[1], green)
        # Blue graph
        for n in range(graph_x_axis,b_graph_height):
            graphics.DrawLine(canvas, n, b_graph_x_coords[0], n, b_graph_x_coords[1], blue)

        #pass
    def run(self):
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        # 
        while True:
            # Reset values
            guess_is_correct = False
            correct_guess = False

            # User to input rgb goal value
            rgb_goal = set_rgb_goal()
            print("TEST: ",rgb_goal)
            # Set goal lights
            self.set_goal_LED(rgb_goal)
            # Set lists for RGB combos
            list_of_untried_rgb_combos = set_rgb_range(rgb_goal)
            list_of_tried_rgb_combos = [] # May be unnecessary if use pop() on each check
            number_of_guesses = 0

            while guess_is_correct == False and len(list_of_untried_rgb_combos) > 0:

                # Make rgb prediction
                rgb_prediction = make_rgb_prediction(list_of_untried_rgb_combos)[0]
                list_of_untried_rgb_combos = make_rgb_prediction(list_of_untried_rgb_combos)[1]

                # Make rgb lights
                self.set_predicted_LED(rgb_prediction)
                self.set_predicted_graph_LED(rgb_prediction)

                # Check rgb prediction
                guess_is_correct = self.check_rgb_prediction(rgb_prediction)

                # Increment number of guesses
                number_of_guesses += 1

            # Tell player correct answer
            self.finished_guessing(correct_guess,number_of_guesses)

            # Check if player wants to continue playing
            user_response = self.do_you_want_to_play_again()
            if user_response == 1:
                print("here we go again!")
                continue
            else:
                print("thanks for playing :D")
                break


# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    
    if (not graphics_test.process()):
        graphics_test.print_help()
