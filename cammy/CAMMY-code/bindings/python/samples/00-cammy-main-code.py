#!/usr/bin/env python
################################################################
# IMPORT RELEVANT LIBRARIES

from samplebase import SampleBase
from rgbmatrix import graphics
import time
import random
import logging

# For camera
import picamera
import time
from PIL import Image

# For models
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import csv
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

# INITIALISE GLOBAL VARIABLES

# Label number for each image captured by camera
image_label = 0


################################################################
# DEFINE RELEVANT FUNCTIONS

# For models
def c_model(R,G,B):
    c_model = pickle.load(open('c_guess_model_linreg.sav', 'rb')) # Consider having this line when initialising the overall program
    predicted_c = c_model.predict([[R,G,B]])
    return predicted_c

def m_model(R,G,B):
    m_model = pickle.load(open('m_guess_model_linreg.sav', 'rb'))
    predicted_m = m_model.predict([[R,G,B]])
    return predicted_m

def y_model(R,G,B):
    y_model = pickle.load(open('y_guess_model_linreg.sav', 'rb'))
    predicted_y = y_model.predict([[R,G,B]])
    return predicted_y

def w_model(R,G,B):
    w_model = pickle.load(open('w_guess_model_linreg.sav', 'rb'))
    predicted_w = w_model.predict([[R,G,B]])
    return predicted_w

def b_model(R,G,B):
    b_model = pickle.load(open('b_guess_model_linreg.sav', 'rb'))
    predicted_b = b_model.predict([[R,G,B]])
    return predicted_b


def model_test(R,G,B):
    c = c_model(R,G,B)[0]
    m = m_model(R,G,B)[0]
    y = y_model(R,G,B)[0]
    w = w_model(R,G,B)[0]
    b = b_model(R,G,B)[0]
    c_int = int(c)
    m_int = int(m)
    y_int = int(y)
    w_int = int(w)
    b_int = int(b)

    to_clip_array = [c_int,m_int,y_int,w_int,b_int]
    clipped_array = np.clip(to_clip_array,0,101)
    print('''
        ----------------------
        ----------------------
        ----------------------
        ''')
    print("CYAN PAINT REQUIRED (unclipped -ve values): {}%".format(c_int))
    print("MANGENTA PAINT REQUIRED (unclipped -ve values): {}%".format(m_int))
    print("YELLOW PAINT REQUIRED (unclipped -ve values): {}%".format(y_int))
    print("WHITE PAINT REQUIRED (unclipped -ve values): {}%".format(w_int))
    print("BLACK PAINT REQUIRED (unclipped -ve values): {}%".format(b_int))

    c_int = clipped_array[0]
    m_int = clipped_array[1]
    y_int = clipped_array[2]
    w_int = clipped_array[3]
    b_int = clipped_array[4]

    cmywb_sum = c_int + m_int + y_int + w_int + b_int
    # normalise to 100%
    if cmywb_sum == 100:
        print("the sum: ",cmywb_sum)
        #print("in the if")
        c = c_int
        m = m_int
        y = y_int
        w = w_int
        b = b_int

    else:
        #print("in the else")
        c = int(c_int/cmywb_sum*100)
        m = int(m_int/cmywb_sum*100)
        y = int(y_int/cmywb_sum*100)
        w = int(w_int/cmywb_sum*100)
        b = int(b_int/cmywb_sum*100)
    
    return [c,m,y,w,b]


################################################################
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


# Ask user if they want to play again
def do_you_want_to_play_again():
    while True:
        answer = input("Do you want to play again? Enter yes or enter no: ")
        if answer.upper() == "YES": return True
        elif answer.upper() == "NO": return False
        print("Didn't understand your input could you please reenter")
  
# Define class Graphics for controlling lights on LED matrix
class Graphics(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Graphics, self).__init__(*args, **kwargs)
        logger.debug("Graphics instance successfully initialised")
        ## matt test code delete later if you want ###############
        # image_label = 0

    def run(self):
        logging.info("Running graphics")
        
        while True:



            ################################################################
            # TAKE PHOTO WITH CAMERA & SAVE PHOTO AS JPEG
            # Input: User run program
            # Output: JPEG

            with picamera.PiCamera() as camera:
                #image_label = 0
                camera.resolution = (400,400)
                camera.start_preview()
                time.sleep(3)
                #camera.capture("/home/pi/Desktop/cam_test_image_%s.jpg" % image_label)
                #camera.capture(f"cam_test_image_{image_label}.jpg")
                camera.capture("cam_test_image_0.jpg")
                #image_label += 1



            ################################################################
            # CROP IMAGE
            # Input: JPEG
            # Output: [r,g,b]
            
            # Open image for cropping
            original_image = Image.open("cam_test_image_0.jpg")

            # Setting the points for cropped image
            left = 150
            top = 150
            right = 250
            bottom = 250

            # Crop image using above points
            cropped_image = original_image.crop((left, top, right, bottom))

            # Save cropped image for future use
            #cropped_image.save("cam_test_image_cropped_%s.jpg" % image_label)
            cropped_image.save("cam_test_image_cropped_0.jpg")


            ################################################################
            # CALCULATE AVERAGE RGB VALUES

            # Find average RGB across cropped_image
            cropped_image_rgb = Image.open("cam_test_image_cropped_0.jpg")
            pixels = cropped_image_rgb.load()
            cropped_image_rgb = cropped_image.convert("RGB")

            # Initialise array for holding sum of all RGBs; intialise iterator for pixels in cropped image
            sum_rgb = [0,0,0]
            pixel_count = 0

            # Iterate through pixels using width and height of image
            for x in range(cropped_image_rgb.width):
                for y in range(cropped_image_rgb.height):
                    pixel_count += 1
                    for i in range(3):
                        sum_rgb[i] += pixels[x,y][i]

            # Calculate average RGB
            average_rgb = [0,0,0]
            for i in range(len(sum_rgb)):
                average_rgb[i] = int(sum_rgb[i]/pixel_count)
            
            
            # # Increment image label number for next image
            # image_label += 1
            
            print("Average RGB: ",average_rgb)
            
            

            ################################################################
            # FEED RGB INTO MODEL TO GET CMYWB VALUES
            # Input: [r,g,b]
            # Output: [c,m,y,w,b]
            cmywb_prediction = model_test(average_rgb[0],average_rgb[1],average_rgb[2])
            #print("cmywb prediction from model: ",cmywb_prediction)

            # Set prediction light. Input = an array [c,m,y,w,b] where values are integer percentages
            # Output = LED matrix illuminated as bar graph
            
            self.set_predicted_graph_LED(cmywb_prediction)


            # Draw smileyface if correct
            # self.draw_smiley()
            # time.sleep(3)
            # self.clear_smiley()
            
            # Check if player wants to continue playing            
            if do_you_want_to_play_again(): continue
            else: break
            
    # def set_goal_LED(self, rgb_goal):
    #     x1 = 5 # Left most edge of light
    #     x2 = 7 # Right most edge of light
    #     y1 = 23 # Bottom edge of light
    #     y2 = 26 # Top edge of light
        
    #     logger.debug("Setting Goal to %s, %s, %s"%(rgb_goal))
    #     color = graphics.Color(rgb_goal[0],rgb_goal[1],rgb_goal[2])
    #     self.draw_rectangle(x1,x2,y1,y2,color)
    #     self.draw_G()
    #     self.draw_P()

    # def set_predicted_LED(self, rgb_prediction):
    #     x1 = 5 # Left most edge of light
    #     x2 = 7 # Right most edge of light
    #     y1 = 15 # Bottom edge of light
    #     y2 = 18 # Top edge of light

    #     logger.debug("Setting Prediction to %s, %s, %s"%(rgb_prediction))
    #     color = graphics.Color(rgb_prediction[0],rgb_prediction[1],rgb_prediction[2])
    #     self.draw_rectangle(x1,x2,y1,y2,color)
    #     #pass

    def set_predicted_graph_LED(self, cmywb_prediction):
        # Initialise red, green, blue LED colours
        cyan = graphics.Color(0, 100, 100)
        magenta = graphics.Color(100, 0, 100)
        yellow = graphics.Color(100, 100, 0)
        white = graphics.Color(70, 70, 70)
        black = graphics.Color(20, 20, 20)
        no_colour = graphics.Color(0,0,0)
        blue = graphics.Color(0,0,50)

        # Initialising 
        c_prediction = cmywb_prediction[0]
        m_prediction = cmywb_prediction[1]
        y_prediction = cmywb_prediction[2]
        w_prediction = cmywb_prediction[3]
        b_prediction = cmywb_prediction[4]
        
        #print("cmywb prediction in set_predicted_graph_LED function: ",cmywb_prediction)
        print('''
        ----------------------
        ----------------------
        ----------------------
        ''')
        print("CYAN PAINT REQUIRED: {}%".format(c_prediction))
        print("MANGENTA PAINT REQUIRED: {}%".format(m_prediction))
        print("YELLOW PAINT REQUIRED: {}%".format(y_prediction))
        print("WHITE PAINT REQUIRED: {}%".format(w_prediction))
        print("BLACK PAINT REQUIRED: {}%".format(b_prediction))
        print('''
        ----------------------
        ----------------------
        ----------------------
        ''')
        
        # Graph x-axis (i.e. bottom edge of graph)
        graph_x_axis = 13
        graphics.DrawLine(self.matrix,graph_x_axis,0,graph_x_axis,32,blue)

        # Calculating required height of each bar in bar graph as a proportion out of 'predicted value / 256'. Values use 'int', which rounds down to nearest integer.
        c_graph_height = int(c_prediction / 2) + graph_x_axis
        #print("c graph height: ",c_graph_height)
        m_graph_height = int(m_prediction / 2) + graph_x_axis
        y_graph_height = int(y_prediction / 2) + graph_x_axis
        w_graph_height = int(w_prediction / 2) + graph_x_axis
        b_graph_height = int(b_prediction / 2) + graph_x_axis

        # Specifying left and right edges of each bar graph
        # c_graph_coords = [3,4,graph_x_axis+1,c_graph_height]
        # print("c graph coords: ",c_graph_coords)
        # m_graph_coords = [9,10,graph_x_axis+1,m_graph_height]
        # y_graph_coords = [15,16,graph_x_axis+1,y_graph_height]
        # w_graph_coords = [21,22,graph_x_axis+1,w_graph_height]
        # b_graph_coords = [27,28,graph_x_axis+1,b_graph_height]       
        # c_graph_coords = [3,4,graph_x_axis+1,c_graph_height]

        c_graph_coords = [27,28,graph_x_axis+1,c_graph_height]
        #print("c graph coords: ",c_graph_coords)
        b_graph_coords = [21,12,graph_x_axis+1,b_graph_height]  
        y_graph_coords = [14,15,graph_x_axis+1,y_graph_height]
        m_graph_coords = [9,10,graph_x_axis+1,m_graph_height]
        w_graph_coords = [3,4,graph_x_axis+1,w_graph_height]
       

        # Clear graphs
        # Cyan graph
        self.draw_rectangle(c_graph_coords[0],c_graph_coords[1],c_graph_coords[2],graph_x_axis + 50,no_colour)
        # Magenta graph
        self.draw_rectangle(m_graph_coords[0],m_graph_coords[1],m_graph_coords[2],graph_x_axis + 50,no_colour)
        # Yellow graph
        self.draw_rectangle(y_graph_coords[0],y_graph_coords[1],y_graph_coords[2],graph_x_axis + 50,no_colour)
        # White graph
        self.draw_rectangle(w_graph_coords[0],w_graph_coords[1],w_graph_coords[2],graph_x_axis + 50,no_colour)
        # Black graph
        self.draw_rectangle(b_graph_coords[0],b_graph_coords[1],b_graph_coords[2],graph_x_axis + 50,no_colour)

        # Switching on LEDs to calculated proportional height
        # Cyan graph
        self.draw_rectangle(c_graph_coords[0],c_graph_coords[1],c_graph_coords[2],c_graph_coords[3],cyan)
        # Magenta graph
        self.draw_rectangle(m_graph_coords[0],m_graph_coords[1],m_graph_coords[2],m_graph_coords[3],magenta)
        # Yellow graph
        self.draw_rectangle(y_graph_coords[0],y_graph_coords[1],y_graph_coords[2],y_graph_coords[3],yellow)
        # White graph
        self.draw_rectangle(w_graph_coords[0],w_graph_coords[1],w_graph_coords[2],w_graph_coords[3],white)
        # Black graph
        self.draw_rectangle(b_graph_coords[0],b_graph_coords[1],b_graph_coords[2],b_graph_coords[3],blue)

        #pass

    def draw_rectangle(self,x1,x2,y1,y2,color):
        for row_value in range(y1,y2):
            graphics.DrawLine(self.matrix,row_value,x1,row_value,x2, color)        
        #pass


# Manual drawings - need to find better way to code

    # # Manually draw letter G next to goal LED
    # def draw_(self):
    #     color = graphics.Color(100,100,100)
    #     graphics.DrawLine(self.matrix,26,11,26,13,color)
    #     graphics.DrawLine(self.matrix,25,11,22,11,color)
    #     graphics.DrawLine(self.matrix,22,12,22,13,color)
    #     graphics.DrawLine(self.matrix,22,13,24,13,color)
    #     #pass

    # # Manually draw letter P next to prediction LED
    # def draw_P(self):
    #     color = graphics.Color(100,100,100)
    #     graphics.DrawLine(self.matrix,18,11,14,11,color)
    #     graphics.DrawLine(self.matrix,18,11,18,13,color)
    #     graphics.DrawLine(self.matrix,17,13,16,13,color)
    #     graphics.DrawLine(self.matrix,16,13,16,12,color)
    #     #pass

    # # Manually draw smileyface when correct - need to add code to clear smiley
    # def draw_smiley(self):
    #     color = graphics.Color(100,100,100)
    #     graphics.DrawLine(self.matrix,9,11,9,11,color)
    #     graphics.DrawLine(self.matrix,9,13,9,13,color)
    #     graphics.DrawLine(self.matrix,7,10,6,11,color)
    #     graphics.DrawLine(self.matrix,6,11,6,13,color)
    #     graphics.DrawLine(self.matrix,6,13,7,14,color)
        
    # # Manually clear smileyface
    # def clear_smiley(self):
    #     color = graphics.Color(0,0,0)
    #     graphics.DrawLine(self.matrix,9,11,9,11,color)
    #     graphics.DrawLine(self.matrix,9,13,9,13,color)
    #     graphics.DrawLine(self.matrix,7,10,6,11,color)
    #     graphics.DrawLine(self.matrix,6,11,6,13,color)
    #     graphics.DrawLine(self.matrix,6,13,7,14,color)


# Main code
if __name__ == "__main__":
    global logger
    logger = create_logging(logging.DEBUG)



    ################################################################
    # LED VISUALISER GRAPHING
    graphics_instance = Graphics()
    graphics_instance.process()

    logger.info("Program exited successfully")

    

