#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import random
import logging



# Set up logging
def create_logging(logging_level, debug_file="debug.log"):
    logging.basicConfig(
        level = logging_level,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler(debug_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Logger successfully initialised")
    return logger

# User sets RGB goal using input method - manually enter RGB values
def set_rgb_goal():
    # Take user input for Goal_RGB combination
    r_goal = input("How much red do you want? (Number between 0 and 255, where 255 is the most red possible): ")
    g_goal = input("How much green do you want? (Number between 0 and 255, where 255 is the most green possible): ")
    b_goal = input("How much blue do you want? (Number between 0 and 255, where 255 is the most blue possible): ")

    # Change to int (add error checking)
    r_goal = int(r_goal)
    g_goal = int(g_goal)
    b_goal = int(b_goal)

    # Create RGB_goal tuple 
    rgb_goal = (r_goal, g_goal, b_goal)
    logger.info("Colour successfully set to RGB value of %s,%s,%s"%(r_goal, b_goal, g_goal))
    return rgb_goal
    #pass

    # Set limited examples for computation reasons

# Set limited guessing set for computer memory and speed reasons
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

    logging.debug("Random target set created for guessing: %s"%rgb_combo_list)

    return rgb_combo_list
    #pass

    # Take coordinates of goal light and colour of goal light



    # Check rgb prediction against goal, return correct or not

# Check predicted RGB value against goal RGB value
def check_rgb_prediction(rgb_goal,rgb_prediction):
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

    # Set 'prediction' light on LED matrix to predicted RGB colour

# Set 'prediction' light on LED matrix to predicted RGB colour
def finished_guessing(correct_guess_bool, latest_guess_rgb, number_of_guesses):
    if correct_guess_bool == False:
        print("didn't get it this time, even after %s guesses!"%number_of_guesses)
    else:
        print("got it right, RGB value is: %s. And it only took %s guesses :p"%(latest_guess_rgb,number_of_guesses))

    #pass

    # Take user input

# Ask user if they want to play again
def do_you_want_to_play_again():
    while True:
        answer = input("Do you want to play again? Enter yes or enter no.")
        if answer.upper() == "YES": return True
        elif answer.upper() == "NO": return False
        print("Didn't understand your input could you please reenter")
  
# Define class Graphics for controlling lights on LED matrix
class Graphics(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Graphics, self).__init__(*args, **kwargs)
        logger.debug("Graphics instance successfully initialised")

    def run(self):
        logging.info("Running graphics")
        
        while True:
            # Reset values
            guess_is_correct = False

            # User to input rgb goal value
            rgb_goal = set_rgb_goal()

            # Set goal lights
            self.set_goal_LED(rgb_goal)

            # Set lists for RGB combos
            list_of_untried_rgb_combos = set_rgb_range(rgb_goal)
            random.shuffle(list_of_untried_rgb_combos)

            list_of_tried_rgb_combos = [] # May be unnecessary if use pop() on each check
            
            number_of_guesses = 0
            while guess_is_correct == False and len(list_of_untried_rgb_combos) > 0:

                # Make rgb prediction
                rgb_prediction = list_of_untried_rgb_combos.pop()

                # Make rgb lights
                self.set_predicted_LED(rgb_prediction)
                self.set_predicted_graph_LED(rgb_prediction)

                # Increment number of guesses
                number_of_guesses += 1

                time.sleep(3)

                # Check rgb prediction
                guess_is_correct = check_rgb_prediction(rgb_goal, rgb_prediction)



            # Tell player correct answer
            finished_guessing(guess_is_correct, rgb_prediction, number_of_guesses)

            # Draw smileyface if correct
            self.draw_smiley()
            time.sleep(3)
            self.clear_smiley()
            # Check if player wants to continue playing            
            if do_you_want_to_play_again(): continue
            else: break
            
    def set_goal_LED(self, rgb_goal):
        x1 = 5 # Left most edge of light
        x2 = 7 # Right most edge of light
        y1 = 23 # Bottom edge of light
        y2 = 26 # Top edge of light
        
        logger.debug("Setting Goal to %s, %s, %s"%(rgb_goal))
        color = graphics.Color(rgb_goal[0],rgb_goal[1],rgb_goal[2])
        self.draw_rectangle(x1,x2,y1,y2,color)
        self.draw_G()
        self.draw_P()

    def set_predicted_LED(self, rgb_prediction):
        x1 = 5 # Left most edge of light
        x2 = 7 # Right most edge of light
        y1 = 15 # Bottom edge of light
        y2 = 18 # Top edge of light

        logger.debug("Setting Prediction to %s, %s, %s"%(rgb_prediction))
        color = graphics.Color(rgb_prediction[0],rgb_prediction[1],rgb_prediction[2])
        self.draw_rectangle(x1,x2,y1,y2,color)
        #pass

    def set_predicted_graph_LED(self, rgb_prediction):
        # Initialise red, green, blue LED colours
        red = graphics.Color(100, 0, 0)
        green = graphics.Color(0, 100, 0)
        blue = graphics.Color(0, 0, 100)
        faint_cyan = graphics.Color(0, 50, 50)
        no_colour = graphics.Color(0,0,0)

        # Initialising 
        r_prediction = rgb_prediction[0]
        g_prediction = rgb_prediction[1]
        b_prediction = rgb_prediction[2]

        # Graph x-axis (i.e. bottom edge of graph)
        graph_x_axis = 32
        graphics.DrawLine(self.matrix,32,0,32,32,faint_cyan)

        # Calculating required height of each bar in bar graph as a proportion out of 'predicted value / 256'. Values use 'int', which rounds down to nearest integer.
        r_graph_height = int(r_prediction * 32 / 256) + graph_x_axis
        g_graph_height = int(g_prediction * 32 / 256) + graph_x_axis
        b_graph_height = int(b_prediction * 32 / 256) + graph_x_axis

        # Specifying left and right edges of each bar graph
        r_graph_coords = [5,7,graph_x_axis+1,r_graph_height]
        g_graph_coords = [14,16,graph_x_axis+1,g_graph_height]
        b_graph_coords = [23,25,graph_x_axis+1,b_graph_height]

        # Clear graphs
        # Red graph
        self.draw_rectangle(r_graph_coords[0],r_graph_coords[1],r_graph_coords[2],graph_x_axis + 32,no_colour)
        # Green graph
        self.draw_rectangle(g_graph_coords[0],g_graph_coords[1],g_graph_coords[2],graph_x_axis + 32,no_colour)
        # Blue graph
        self.draw_rectangle(b_graph_coords[0],b_graph_coords[1],b_graph_coords[2],graph_x_axis + 32,no_colour)

        # Switching on LEDs to calculated proportional height
        # Red graph
        self.draw_rectangle(r_graph_coords[0],r_graph_coords[1],r_graph_coords[2],r_graph_coords[3],red)
        # Green graph
        self.draw_rectangle(g_graph_coords[0],g_graph_coords[1],g_graph_coords[2],g_graph_coords[3],green)
        # Blue graph
        self.draw_rectangle(b_graph_coords[0],b_graph_coords[1],b_graph_coords[2],b_graph_coords[3],blue)


        #pass

    def draw_rectangle(self,x1,x2,y1,y2,color):
        for row_value in range(y1,y2):
            graphics.DrawLine(self.matrix,row_value,x1,row_value,x2, color)        
        #pass


# Manual drawings - need to find better way to code

    # Manually draw letter G next to goal LED
    def draw_G(self):
        color = graphics.Color(100,100,100)
        graphics.DrawLine(self.matrix,26,11,26,13,color)
        graphics.DrawLine(self.matrix,25,11,22,11,color)
        graphics.DrawLine(self.matrix,22,12,22,13,color)
        graphics.DrawLine(self.matrix,22,13,24,13,color)
        #pass

    # Manually draw letter P next to prediction LED
    def draw_P(self):
        color = graphics.Color(100,100,100)
        graphics.DrawLine(self.matrix,18,11,14,11,color)
        graphics.DrawLine(self.matrix,18,11,18,13,color)
        graphics.DrawLine(self.matrix,17,13,16,13,color)
        graphics.DrawLine(self.matrix,16,13,16,12,color)
        #pass

    # Manually draw smileyface when correct - need to add code to clear smiley
    def draw_smiley(self):
        color = graphics.Color(100,100,100)
        graphics.DrawLine(self.matrix,9,11,9,11,color)
        graphics.DrawLine(self.matrix,9,13,9,13,color)
        graphics.DrawLine(self.matrix,7,10,6,11,color)
        graphics.DrawLine(self.matrix,6,11,6,13,color)
        graphics.DrawLine(self.matrix,6,13,7,14,color)
        
    # Manually clear smileyface
    def clear_smiley(self):
        color = graphics.Color(0,0,0)
        graphics.DrawLine(self.matrix,9,11,9,11,color)
        graphics.DrawLine(self.matrix,9,13,9,13,color)
        graphics.DrawLine(self.matrix,7,10,6,11,color)
        graphics.DrawLine(self.matrix,6,11,6,13,color)
        graphics.DrawLine(self.matrix,6,13,7,14,color)


# Main code
if __name__ == "__main__":
    global logger
    logger = create_logging(logging.DEBUG)

    graphics_instance = Graphics()
    graphics_instance.process()

    logger.info("Program exited successfully")

    

