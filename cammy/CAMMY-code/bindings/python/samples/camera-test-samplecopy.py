import picamera
import time

from PIL import Image


with picamera.PiCamera() as camera:
    camera.resolution = (400,400)
    camera.start_preview()
    time.sleep(2)
    camera.capture("/home/pi/Desktop/cam_test_image.jpg")

print("displaying image now")

im = Image.open("/home/pi/Desktop/cam_test_image.jpg")


# Size of the image in pixels (size of orginal image)
# (This is not mandatory)
width, height = im.size
print("image size before crop: ",im.size)

# Setting the points for cropped image
left = 5
top = height / 4
right = 164
bottom = 3 * height / 4
  
# Cropped image of above dimension
# (It will not change orginal image)
im1 = im.crop((left, top, right, bottom))


print("image size after crop: ",im1.size)
im1.show()