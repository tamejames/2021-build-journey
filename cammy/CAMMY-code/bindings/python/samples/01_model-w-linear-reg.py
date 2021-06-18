# Supervised learning model for CAMMY (a colour-mixing cyber-physical system)

# Model W: Finding W (white) label based on RGB values as features

import numpy as np
import matplotlib.pyplot as plt
import sklearn
import csv
import pandas as pd
import pickle


# Source: https://colab.research.google.com/drive/1ubYJwGZvtSTKxc-mSpPE8iGfQjRsd2HX

# 0. ABOUT THIS MODEL
# This model will take RGB values and predict a 'W percent by paint vol' value.
# This is the proportion of acrylic white paint (by volume) required to recreate the RGB colour based on physical experiments. The data for these experiments are stored
# in the file 'image-data-by-paint-percentage.csv'.


# 1. OPEN DATA
# Import the "image_data" dataset by reading the data from the csv file
image_data = pd.read_csv('image-data-by-paint-percentage.csv')
# Show first 5 rows of data (incl heading) so that we can visually inspect the data we have imported
print(image_data[0:4])


# 2. FEATURE EXTRACTION
# Set features as RGB
features = image_data.loc[:,('R','G','B')]
# Set label for 'W percent by paint vol'
labels = image_data.loc[:,'W percent by paint vol']
# # We then convert the feature and labels dataframes to 
# # numpy ndarrays, which can interface with the scikit-learn models
X = features.to_numpy()
y = labels.to_numpy()
# # Visual inspection of features and labels
# print(X)
# print(y)


# 3. INITIALISE MODEL
# Model initialised - source: https://scikit-learn.org/stable/modules/tree.html#classification
from sklearn.linear_model import LinearRegression


# 4. SPLITTING DATA INTO TEST/TRAIN SETS
# Copied from https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
from sklearn.model_selection import train_test_split 
# Specifying data split - in this case 20% for testing, 80% for training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Note: random_state --> the number 42 just corresponds to the seed of Randomness, you can use another number, for example 101. Each time that you run your model, the values selected will be the same, but if you change this number the values selected will be different and your accuracy could have variety but you will be sure that your model is robust if your accuracy keeps following the same.
# Source: https://www.researchgate.net/post/Why_random_state_in_train_test_split_is_equal_42


# 5. TRAIN YOUR MODEL HERE
# Train model using the training data - as defined in the train_test_split function above
reg = LinearRegression().fit(X_train,y_train)


# 6. EVALUATE YOUR MODEL ON TEST SET HERE
# Generate predictions on test set (predicting labels given test features)
predictions = reg.predict(X_test)
# Print out predicted values for visual inspection
print('predictions: ',predictions)
print('X train: ',len(X_train))
print('X_test:',len(X_test))
# Use clf.score() to find mean accuracy of model when makign predictions on test set
score = reg.score(X_test,y_test)
print('x_test',X_test)
print('y_test',y_test)
print("raw score: ",score)


# 7. SAVE MODEL FOR LATER USE
filename = 'w_guess_model_linreg.sav'
pickle.dump(reg,open(filename,'wb'))
loaded_model = pickle.load(open('w_guess_model_linreg.sav', 'rb'))
#result = loaded_model.score([[57,121,63]], [48])
#print(result)
print("model run completed")

# ----------------------------------------------------------------



# # 8. CROSS VALIDATION
# # Original source: https://colab.research.google.com/drive/1Fv1OPcgv_77p6ZGpzxNckka3o3G-LpOD#scrollTo=yCNO7p5xsnHs
# # # More about cross validation at https://scikit-learn.org/stable/modules/cross_validation.html
# # from sklearn.model_selection import cross_val_score

# # Initialise list of coordinates for plotting
# coord_list = []
# # Initialise iterator starting from value 1 - this is used to represent the max_depth value
# n = 1
# # While iterator less than 20, assign iterator value to max_depth and calculate mean score using cross_val_score.
# # Assign mean score as y-coordinate and iterator value as x-coordinate for plotting

# from sklearn.model_selection import cross_val_score
# while n < 10:
#   x_coord = n
#   scores = cross_val_score(reg, X, y, cv=4)
#   #print('y: ',y)
#   y_coord = scores
#   #print("ycoord: ",y_coord)
#   new_coord = (x_coord,y_coord)
#   coord_list.append(new_coord)
#   n += 1

# # Visual check of coordinate list
# # print(coord_list)

# # Plotting tuple coordinates (source: https://stackoverflow.com/questions/18458734/how-do-i-plot-list-of-tuples-in-python)
# plt.plot(*zip(*coord_list)) 
# plt.show()
# #scores = cross_val_score(clf, X, y, cv=4)
# #print("CV Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


