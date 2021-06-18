import numpy as np
import matplotlib.pyplot as plt
import sklearn
import csv
import pandas as pd
import pickle

loaded_model = pickle.load(open('c_guess_model_linreg.sav', 'rb'))
print("test1")
#result = loaded_model.score([[57,121,63]], [48])
predicted_c = loaded_model.predict([[0,100,100]])
print("test2")
print(predicted_c) # this is type numpy.ndarray
print("test3")
print(predicted_c[0]) # this is type float
print(int(predicted_c[0])) # this is type int

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
    cmywb_sum = c_int + m_int + y_int + w_int + b_int
    # normalise to 100%
    if cmywb_sum == 100:
        print("the sum: ",cmywb_sum)
        print("in the if")
        c = c_int
        m = m_int
        y = y_int
        w = w_int
        b = b_int

    else:
        print("in the else")
        c = int(c_int/cmywb_sum*100)
        m = int(m_int/cmywb_sum*100)
        y = int(y_int/cmywb_sum*100)
        w = int(w_int/cmywb_sum*100)
        b = int(b_int/cmywb_sum*100)
    
    
    return [c,m,y,w,b]

test_rgb = [141,139,142]
test_cmywb = model_test(test_rgb[0],test_rgb[1],test_rgb[2])
print(test_cmywb)