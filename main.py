import cv2    #open library
import time
import glob                                                                               # a pattern-matching syntax used to locate files and directories in a filesystem
from emailing import send_email
import os
from threading import Thread

video = cv2.VideoCapture(0)                                                                    # class ,used to capture video from a camera or read video files
time.sleep(1)                                                                                  # time delay 1 second, Pauses the current thread
first_frame = None                                                                             # first frame created to compare other frames

status_list = []
count = 1                                                                                      # given name to 1st image (1.png)

def clean_folder():                                                                            # to clear folder
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

clean_folder()


while True:
    status = 0
    check, frame = video.read()                                                                # frames in BGR
    grey_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21,21), 0)                      #gaussian blur to blur grey frame/ 21,21 amount of blur/ 0 is standard deviation

    if first_frame is None:                                                                    # we gave first_frame = not going to change after the while loop executes one time,
        first_frame = grey_frame_gau

    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)                                     # absolute difference method to create new frame after two previous frame

    thresh_frame = cv2.threshold(delta_frame, 60 , 255, cv2.THRESH_BINARY)[1]    # This process, known as thresholding, converts a grayscale image into a binary
                                                                                               # [] thresh frame is a list , extract [1] value
    dil_frame = cv2.dilate(thresh_frame,None, iterations=2)                             # coverts object to bright light and bg to black to fill holes in image
                                                                                               # configuration is None , iterations, the higher we go ,
                                                                                               # more processing will applied to the method
    cv2.imshow("my video", dil_frame)                                                  # to see frames

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,  cv2.CHAIN_APPROX_SIMPLE)   # contour means shape of outer surface / RETR_EXTERNAL, used to retrieve only
                                                                                                 # extreme outer surfaces or contours / chain_approx_simple reduces the number of points
                                                                                                # stored for a contour, focusing on structural vertices (corners)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)                                                   # x ,y points of rectangle , w width, h height
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)                     # x+w is rectangle  expand as per object ,(0, 255, 0) Green rectangle, 3 is width

        if rectangle.any():                                                                     # when object is not in the frame, status is [0,0]
            status = 1                                                                          # when object enters it changes from [0,0] to [0,1] to [1,1]
                                                                                                # status stays [1,1] til the object is in frame
        cv2.imwrite(f"images/{count}.png", frame)                                       # status changes to [1,0] then [0,0] , when the object left the frame , and email is sent
        count = count + 1                                                                       # used slicing [-2:] to extract last two characters
        all_images = glob.glob("images/*.png")                                                  # print(status_list) to see results in terminal
        index = int(len(all_images) / 2)
        image_with_object = all_images[index]                                                   # used imwrite , image write to save images
                                                                                                # select all images using glob and select the middle image when object is in the frame



    status_list.append(status)
    status_list = status_list[-2:]


    if status_list[0] == 1 and status_list[1] == 0:                                             # Our program lags , becuase sed_email and clear_folder function runs simultaneously
        email_thread = Thread(target=send_email, args=(image_with_object, ))                    # to run program smoothly , used threading ,running multiple flows of execution (threads)
                                                                                                # concurrently(take turns not parallel) within a single process
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        # clean_thread.daemon = True                                                              # daemon allows funtion to execute in background while frames are executing

        email_thread.start()                                                                    # sent email by starting threading



    cv2.imshow("Video", frame) # original frame
    key = cv2.waitKey(1)                                                                        # waitkey is for delay frames capture

    if key == ord("q"):
        break

video.release()

clean_folder()

clean_thread.start()                                                                            # cleared folder after sending image

