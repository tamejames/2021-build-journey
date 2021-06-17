# James Liu (u5569470)

# Learnings:
# I learned about testing each function with a simple case before connecting them together (thanks to Johan Michalove, Mina Henein and Matt Heffernan for constantly reminding me about this). This was a very useful contrast to my initial approach of trying to generalise everything and writing everything up before running the code, and is certainly an approach I intend to take forwards, as it makes troubleshooting/debugging, as well as the overall task of writing the code, much more manageable. I also learned that print statements are a useful way to debug code (thanks Matt H!) and that tagged coordinates (though not used for my original intention of interpolation), were useful in visualising the arrays when I wanted to debug using print statements. I also learnt about libraries (in this case the 'math' library) while attempting a few different approaches to interpolating between shapes, in one case attempting to use the trigonometric functions available in the library. Though in this case, I also learned that libraries can have different versions too, with the 3ai-plotter laptop having a different version to the math library I imported - which forced me to learn how to find the function from documentation! (Thanks Mina for the suggestion on that.) This task also taught me different methods for interpolation using code (shout out to Johan Michalove and Sam Backwell). Last of all, it showed me the value of patience and seeking others for help, as this was the task where my frustration reached its peak (in the context of this homework) and I would not have been able to do it without input from others. It also served as a good example of how important motivation can be in getting a task done - in this case, attempting to replicate 'Return to Square' (a piece of art that I am deeply interested in) made the arduous task of debugging much more tolerable, as I had a clear goal in sight.

import axi
import math # Import python math function to provide access to functions such as math.dist()

# Set this variable to true when you wish to draw with the plotter.
draw = True

A4_PORT = (0, 0, 8.25, 11.75) # A4 Portrait bounds
A4_LAND = (0, 0, 11.75, 8.25) # A4 Landscape bounds
# Set your paper bounds here, to either landscape or portrait
BOUNDS = A4_PORT

# Function to draw regular polygon given the number of sides and desired side length
def draw_regular_polygon(turtle, total_sides, side_length, x_coord, y_coord):
    turtle.pu()
    turtle.goto(x_coord,y_coord)
    coordinate_array = [] # Create list to store coordinates of polygon
    max_x_coord = 0
    max_y_coord = 0
    # Loop cycles through once for every side of the regular polygon
    for iterator in range(total_sides):
        turtle.pd()
        turtle.fd(side_length) # draw first side of shape in the default "forward" direction (positive direction along x-axis as based on coordinate system of output image)
        turtle.right(180-(((total_sides-2)*180)/total_sides)) # Turtle must turn by (180deg - internal angle of regular polygon). Formula for internal angle of regular polygon is given by (n-2) * 180deg / n where n is number of sides (https://www.mathsisfun.com/geometry/interior-angles-polygons.html).
        coordinate_array.append(turtle.pos()) # Store coordinates for all vertices of polygon in coordinate_array i.e. will be of format [(x0,y0),(x1,y1)...]
        #print(coordinate_array)
        if abs(turtle.pos()[0]) > max_x_coord:
            max_x_coord = turtle.pos()[0]
        if abs(turtle.pos()[1]) > max_y_coord:
            max_y_coord = turtle.pos()[1]
    turtle.pu() # Put pen up once FOR loop stops (i.e. when polygon has been completed)
    turtle.home() # Return pen to home position (0,0)
    polygon_centre = (max_x_coord/2,y_coord/2) # Defining 'centre' of regular polygon as coordinate at half of total length and height
    polygon_outline_length = 0 # Create variable for total length of line that traces out polygon shape
    for iterator in range(len(coordinate_array)):
        if iterator + 1 < len(coordinate_array):
            polygon_outline_length += dist(coordinate_array[iterator],coordinate_array[iterator + 1]) # Find total length of the line tracing the polygon by adding the distances between consecutive points
        else:
            polygon_outline_length += dist(coordinate_array[iterator],coordinate_array[0]) # Second last point of polygon will connect back with the first point of the polygon
        
    return (coordinate_array, max_x_coord, max_y_coord, polygon_centre, polygon_outline_length) # Returns an array containing
    # 0) the coordinates for the vertices (corners) of the polygon (starting at the specified starting coordinates and initially moving forwards i.e. in the positive x-direction),
    # 1) the maximum x-coordinate of the polygon,
    # 2) the maximum y-coordinate of the polygon,
    # 3) the 'centre' of the polygon, and
    # 4) the total length of the line that traces the polygon.

def generate_points_on_line(turtle, polygon, total_number_of_points): # Note that 'polygon' refers to the output that is returned by function draw_regular_polygon()   
    # Create list that will store coordinates, with tag included. Format of each entry is (tag, x_coord, y_coord).
    tagged_coordinate_array_shape_1 = [] 
    coord_tag = 0 # Create starting value for coordinate tags

    # Create loop that will check each sequential pair of coordinates and work out how many points need to be generated between the two points in order to create the desired total number of points across the entire polygon
    for i in range(len(polygon[0])): # Note polygon[0] is an array containing the coordinates of the vertices of the polygon

        # Check each pair of coordinates from the coordinate array returned by polygon, starting with index pair 0 and 1 (first two coordinates), and ending with index pair 'final point' and 0, as completed shape will end at starting coordinate.

        # IF it is not the last line drawn in creating the polygon (i.e. not the line that returns to the starting point, in this case the first coordinate in the coordinate array)
        if i < len(polygon[0]) - 1: # Note polygon[0] is an array containing the coordinates of the vertices of the polygon

            # Calculate distance between the two coordinates
            distance_between_points = dist(polygon[0][i],polygon[0][i+1]) 
            # Calculate number of points needed --> ratio of distance between points : total polygon outline length * total_number_of_points we want to create across entire polygon
            number_of_points_needed = int(distance_between_points / polygon[4] * total_number_of_points) # Note that polygon[4] is polygon_outline_length. Using integer in order to be able to use to set range later on. USING INTEGER.

            # Find incremental distance along x- and y-coordinates between the pair of points in order to divide the line between the two points into the correct number of points
            x_increment = (polygon[0][i+1][0] - polygon[0][i][0]) / number_of_points_needed
            y_increment = (polygon[0][i+1][1] - polygon[0][i][1]) / number_of_points_needed

            # Add coordinates for incremental coordinates  to tagged coordinate array, with tag included
            for i_2 in range(number_of_points_needed + 1):
                shifting_x_coordinate = polygon[0][i][0] + i_2 * x_increment # Add increment along x-coordinate and assign value to shifting_x_coordinate
                shifting_y_coordinate = polygon[0][i][1] + i_2 * y_increment # Add increment along y-coordinate and assign value to shifting_y_coordinate
                tagged_coordinate_entry = (coord_tag,shifting_x_coordinate,shifting_y_coordinate) # Create the entry that will be added to the array of tagged coordinates
                tagged_coordinate_array_shape_1.append(tagged_coordinate_entry) # Add this tagged coordinate to the overall tagged coordinate array
                coord_tag += 1 # Increment coordinate tag by 1

        # Dealing with the final line of the polygon (which goes from the last coordinate in the array back to the first coordinate of the array)
        else:
            # Calculate distance between the final pair of points (final vertex in polygon vertex coordinate array and starting point)
            distance_between_points = dist(polygon[0][i],polygon[0][0])
            # Calculate number of points needed --> ratio of distance between points : total polygon outline length * total_number_of_points we want to create across entire polygon
            number_of_points_needed = int(distance_between_points / polygon[4] * total_number_of_points) # Note that polygon[4] is polygon_outline_length. USING INTEGER.

            # Find incremental distance along x- and y-coordinates between the last point in the array, and the first point - as the final line will be drawn between last point in starting point.
            x_increment = (polygon[0][0][0] - polygon[0][i][0]) / number_of_points_needed
            y_increment = (polygon[0][0][1] - polygon[0][i][1]) / number_of_points_needed
            for i_2 in range(number_of_points_needed + 1):
                shifting_x_coordinate = polygon[0][i][0] + i_2 * x_increment # Add increment along x-coordinate and assign value to shifting_x_coordinate
                shifting_y_coordinate = polygon[0][i][1] + i_2 * y_increment # Add increment along y-coordinate and assign value to shifting_y_coordinate
                tagged_coordinate_entry = (coord_tag,shifting_x_coordinate,shifting_y_coordinate) # Create the entry that will be added to the array of tagged coordinates
                tagged_coordinate_array_shape_1.append(tagged_coordinate_entry) # Add this tagged coordinate to the overall tagged coordinate array
                coord_tag += 1 # Increment coordinate tag by 1

    return tagged_coordinate_array_shape_1


def draw_from_points(turtle,tagged_coordinate_array):
    turtle.pu()
    tagged_coordinate_array.append(tagged_coordinate_array[0]) # Close the shape by appending the starting coordinate to the end so that the draw function knows to draw back to the starting point
    turtle.goto(tagged_coordinate_array[0][1],tagged_coordinate_array[0][2]) # Note array[0][1] is the x-coordinate of first pair in array, array[0][2] is y-coordinate
    turtle.pd()
    for i in range(len(tagged_coordinate_array)):
        turtle.goto(tagged_coordinate_array[i][1],tagged_coordinate_array[i][2])


# Function to interpolate coordinates between the outer shape (starting shape) and inner shape (goal shape) in order to generate coordinates for each transition shape.
# 3/3/2021 - Acknowledgement to Johan Michalove at the 3A Institute for explaining the weighted coordinates approach to interpolation.
def merge_shape_art(turtle, number_of_transition_shapes, outer_shape_tagged_array, inner_shape_tagged_array):
    # Create range of weights to calculate the change in each coordinate to create interpolated shape. Set range to be in steps equal to 1/number of transition shapes, as this will create evenly distributed interpolation.
    for transition in range(0,number_of_transition_shapes): # Set range so that loop iterates the correct number of times to produce that many transition shapes.
        weight = 1/number_of_transition_shapes # Set 'weighting' value (used to 'weight' coordinates in interpolation) to 1/number of transition shapes
        transition_array = []
        tag = 0

        # Check the length of the two arrays. If one is shorter, fill it out by appending its starting coordinate repeatedly until it has the same length as the longer array. This is currently a temporary fix, as the int() function is used when creating the arrays using the function generate_points_on_line, which can lead to slightly mismatched numbers of coordinates, which can in turn stop the program from functioning. These two lines have been tagged with "USING INTEGER" for searchability in future debugging if required.
        if len(outer_shape_tagged_array) != len(inner_shape_tagged_array):
            # If outer shape array is larger (i.e. has more coordinates)
            if len(outer_shape_tagged_array) > len(inner_shape_tagged_array):
                # While the outer shape array is larger, keep appending the first entry from the inner shape array to the inner shape array.
                while len(outer_shape_tagged_array) > len(inner_shape_tagged_array):
                    inner_shape_tagged_array.append(inner_shape_tagged_array[0])
            # If inner shape array is larger (i.e. has more coordinates)
            elif len(inner_shape_tagged_array) > len(outer_shape_tagged_array):
                # While the inner shape is array is larger, keep appending the first entry from the outer shape array to the outer shape array.
                while len(inner_shape_tagged_array) > len(outer_shape_tagged_array):
                    outer_shape_tagged_array.append(outer_shape_tagged_array[0])


        # Generate coordinates for each transition shape
        for coordinate in range(len(outer_shape_tagged_array)):
            new_x_coord = outer_shape_tagged_array[coordinate][1] * weight * transition + inner_shape_tagged_array[coordinate][1] * (1-weight*transition) # Calculate new x-coordinate by taking weighted average of x-coordinate of outer shape and x-coordinate of inner shape
            new_y_coord = outer_shape_tagged_array[coordinate][2] * weight * transition + inner_shape_tagged_array[coordinate][2] * (1-weight*transition) # Calculate new y-coordinate by taking weighted average of y-coordinate of outer shape and y-coordinate of inner shape
            transition_coord = (tag, new_x_coord, new_y_coord) # Added tag so that the draw_from_points function would work, as haven't yet decided whether to use tags or not. But may be useful, so not deleting just yet.
            tag += 1 # Increment tag
            transition_array.append(transition_coord) # Add new coordinates to array containing the coordinates for the transition shape

        #Trace the points for the transition shape
        draw_from_points(turtle,transition_array)

    return(transition_array)


def save_img(turtle, name = 'out'):
    drawing = turtle.drawing.rotate_and_scale_to_fit(BOUNDS[2], BOUNDS[3], step=90, padding=0.5) # scale letter to fit A4-sized paper
    im = drawing.render(bounds=BOUNDS) # render drawing+
    im.write_to_png(name + '.png') # save a image of your drawing in a file called name.png
    
def draw_img(turtle):
    drawing = turtle.drawing.rotate_and_scale_to_fit(BOUNDS[2], BOUNDS[3], step=90, padding=0.5) # scale letter to fit A4-sized paper
    axi.draw(drawing)

# Included dist function below as computer running the 3ai-plotter has a different version of the python 'math' library. Taken from math.dist() - source: https://docs.python.org/3/library/math.html. Acknowledgement to Mina Henein of the 3A Institute for suggesting I refer to the Python docs to find their original function.
def dist(p,q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    
def main():
    turtle = axi.Turtle()

    # How to use:
    # First you need to create the shapes you want to use (you'll need at least 2 shapes to generate the merging art effect). You can create shapes by calling the generate_points_on_line() function and the draw_regular_polygon function. You'll need to know:
    # Value 'A': How many sides you want your shape to have
    # Value 'B': How long you want each side of the shape to be
    # Value 'C': The x-coordinate of your shape
    # Value 'D': The y-coordinate of your shape
    # Value 'E': The number of points you want to use to define your shape (a bigger number will give you a higher quality shape and a smoother merge). Make sure this value is higher than the value 'A' you have chosen for the shape your are creating. Recommended to use at least 100 coordinates.

    # You can now create the shape (we'll call it 'shape_george') by writing:
    # shape_george = generate_points_on_line(turtle, draw_regular_polygon(turtle,A,B,C,D),E)
    # There are some example shapes below.
    shape_1 = generate_points_on_line(turtle, draw_regular_polygon(turtle,3,15,0,0),1000)
    shape_2 = generate_points_on_line(turtle, draw_regular_polygon(turtle,4,8,80,0),1000)
    #shape_3 = generate_points_on_line(turtle,draw_regular_polygon(turtle,12,3,10,0),100)
    #shape_4 = generate_points_on_line(turtle,draw_regular_polygon(turtle,25,1,10,20),100)

    # Now in order to merge the shapes, you simply need to know:
    # Value 'F': The number of transition shapes you want to see (i.e. the shapes that appear as one shape merges into another)
    # Value 'G': The name you've given the first shape (the one you want to start the merge from)
    # Value 'H': The name you've given your second shape (the one you want your starting shape to merge into)
    # You can now create your merge shape art using the values above by simply writing:
    # merge_shape_art(turtle,F,G,H)
    # There are some example merges below, using the art given above
    merge_shape_art(turtle,5,shape_1,shape_2)
    #merge_shape_art(turtle,20,shape_2,shape_3)
    #merge_shape_art(turtle,15,shape_3,shape_4)

    output_img = 'task4-out-james-2'
    save_img(turtle, output_img)
    # draw_img(turtle) # Uncomment to draw your image
    turtle.home() # Send turtle/plotter back to starting point (0,0) for next plotter user
     
if __name__ == '__main__':
    main()
