import picamera
import time
import csv
from PIL import Image

image_label = 0

with open('/home/pi/Desktop/camera_test_image_data.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Image Label","R","G","B"])

# Take 10 test images
    # while True:
    #     with picamera.PiCamera() as camera:
    #         camera.resolution = (400,400)
    #         camera.start_preview()
    #         time.sleep(10)

    while image_label < 10:
        # Take image with camera and save
        with picamera.PiCamera() as camera:
            camera.resolution = (400,400)
            camera.start_preview()
            time.sleep(3)
            camera.capture("/home/pi/Desktop/cam_test_image_%s.jpg" % image_label)
        

        # Open image for cropping
        original_image = Image.open("/home/pi/Desktop/cam_test_image_%s.jpg" % image_label)

        # Setting the points for cropped image
        left = 150
        top = 150
        right = 250
        bottom = 250
        
        # Crop image using above points
        cropped_image = original_image.crop((left, top, right, bottom))

        # Save cropped image for future use
        cropped_image.save("/home/pi/Desktop/cam_test_image_cropped_%s.jpg" % image_label)

        # Find average RGB across cropped_image
        cropped_image_rgb = Image.open("/home/pi/Desktop/cam_test_image_cropped_%s.jpg" % image_label)
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

        print("pixel count: ",pixel_count)
        print(average_rgb)

        writer.writerow([image_label,average_rgb[0],average_rgb[1],average_rgb[2]])

        # Iterate image_label
        image_label += 1

