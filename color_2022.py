import numpy as np
import cv2

rect_size = 50
max_width = 638
max_height = 480
isLeft = 1
start_point = [200, 100] #left bottom point
end_point = [250, 150] #right top point
color = "green"

default_zone_1_start = [125, 215]
default_zone_1_end = [default_zone_1_start[0]+rect_size, default_zone_1_start[1]+rect_size]
default_zone_2_start = [290, 215]
default_zone_2_end = [default_zone_2_start[0]+rect_size, default_zone_2_start[1]+rect_size]
default_zone_3_start = [463, 215]
default_zone_3_end = [default_zone_3_start[0]+rect_size, default_zone_3_start[1]+rect_size]

h_sensivity = 20
s_h = 255
v_h = 255
s_l = 50
v_l = 50
blue = [np.array([100, s_l, v_l]), np.array([130, s_h, v_h])]
yellow = [np.array([20, s_l, v_l]), np.array([45, s_h, v_h])]
red = [np.array([160, s_l, v_l]), np.array([180, s_h, v_h])]
purple = [np.array([100, s_l, v_l]), np.array([160, s_h, v_h])]
green = [np.array([40, s_l, v_l]), np.array([80, s_h, v_h])]
orange = [np.array([0 , 100, 140]), np.array([60, 220, 230])]
silver = [np.array([40, 30, 140]), np.array([100, 70, 230])]

def set_default_zone_1():
    global start_point, end_point
    start_point = list(default_zone_1_start)
    end_point = list(default_zone_1_end)

def set_default_zone_2():
    global start_point, end_point
    start_point = list(default_zone_2_start)
    end_point = list(default_zone_2_end)

def set_default_zone_3():
    global start_point, end_point
    start_point = list(default_zone_3_start)
    end_point = list(default_zone_3_end)

def move_zone_left():
    if start_point[0] - 50 >= 0:
        start_point[0] -= 50
        end_point[0] -= 50
    else:
        left_border_to_zero = start_point[0]
        start_point[0] -= left_border_to_zero
        end_point[0] -= left_border_to_zero

def move_zone_right():
    if end_point[0] + 50 <= max_width:
        end_point[0] += 50
        start_point[0] += 50
    else:
        right_border_to_max = max_width - end_point[0]
        end_point[0] += right_border_to_max
        start_point[0] += right_border_to_max

def move_zone_down():
    if end_point[1] + 50 <= max_height:
        end_point[1] += 50
        start_point[1] += 50
    else:
        lower_border_to_max = max_height - end_point[1]
        end_point[1] += lower_border_to_max
        start_point[1] += lower_border_to_max

def move_zone_up():
    if start_point[1] - 50 >= 0:
        start_point[1] -= 50
        end_point[1] -= 50
    else:
        upper_border_to_zero = start_point[1]
        start_point[1] -= upper_border_to_zero
        end_point[1] -= upper_border_to_zero

def get_color_range_by_color_name(colorName: str): 
    if colorName == "blue":
        return blue
    if colorName == "yellow":
        return yellow
    if colorName == "red":
        return red
    if colorName == "purple":
        return purple
    if colorName == "green":
        return green
    if colorName == "orange":
        return orange
    if colorName == "silver":
        return silver
    
def process(frame):
    #print(start_point)
    #print(end_point)
    width, height, channels = frame.shape
    #start_point = (int(height / 2 - rect_size / 2), int(width / 2 - rect_size / 2))
    #end_point = (int(height / 2 + rect_size / 2), int(width / 2 + rect_size / 2))


    text_color = (255, 0, 0)
    thickness = 2
    rect = cv2.rectangle(frame, start_point, end_point, text_color, thickness)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_lower_upper = get_color_range_by_color_name(color)
    mask_frame = hsv_frame[start_point[1]:end_point[1] + 1, start_point[0]:end_point[0] + 1]
    mask_color = cv2.inRange(mask_frame, color_lower_upper[0], color_lower_upper[1])


    green_rate = np.count_nonzero(mask_color) / (rect_size * rect_size)

    org = list(start_point)
    global isLeft
    if isLeft == 1:
        if start_point[0] - 140 >= 0:
            org = list(start_point)
            org[0] -= 140
        else:
            isLeft = 0
            org = [end_point[0], start_point[1]]
    else:
        if end_point[0] + 140 <= max_width:
            isLeft = 0
            org = [end_point[0], start_point[1]]
        else:
            isLeft = 1
            org = list(start_point)
            org[0] -= 10
    org[1] += 30

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.7

    if green_rate > 0.7:
        text = cv2.putText(rect, ' ' + color + ' ', org, font, fontScale, text_color, thickness, cv2.LINE_AA)
    else:
        text = cv2.putText(rect, ' not ' + color + ' ', org, font, fontScale, text_color, thickness, cv2.LINE_AA)

    av_hue = np.average(mask_frame[:, :, 0])
    av_sat = np.average(mask_frame[:, :, 1])
    av_val = np.average(mask_frame[:, :, 2])
    average = [int(av_hue), int(av_sat), int(av_val)]

    text = cv2.putText(rect, str(average) + " " + str(green_rate), (10, 50), font, fontScale, text_color, thickness,
                       cv2.LINE_AA)
    frame = text
    return frame

print('----Embedded Systems Laboratory Work 3----')
print('q - exit\n')

print('a - move zone left')
print('d - move zone right')
print('w - move zone up')
print('s - move zone down\n')

print('1 - first default zone')
print('2 - second default zone')
print('3 - third default zone\n')

print("To choose color press button corresponding with first letter of color name")
print('Colors: Blue, Yellow, Red, Purple, Green, Orange, Silver')
print('*for Silver use SHIFT+S')

# Open Default Camera
cap = cv2.VideoCapture(0)  # gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)

while (cap.isOpened()):
    # Take each Frame
    ret, frame = cap.read()

    # Flip Video vertically (180 Degrees)
    frame = cv2.flip(frame, 180)

    invert = process(frame)

    # Show video
    # cv2.imshow('Cam', frame)
    cv2.imshow('Inverted', invert)

    # Exit if "4" is pressed
    k = cv2.waitKeyEx(1) & 0xFF
    if k == 113:  # ord 4
        # Quit
        print('Shutting down...')
        print('Change da world… my final message. Goodb ye.\n\n\n')
        break
    elif k == 49: #1
        set_default_zone_1()
    elif k == 50: #2
        set_default_zone_2()
    elif k == 51: #3
        set_default_zone_3()
    elif k == 97: #a
        move_zone_left()
    elif k == 100: #d
        move_zone_right()
    elif k == 119: #w
        move_zone_up()
    elif k == 115: #s
        move_zone_down()
    elif k == 98: #b
        print("Blue color selected.")
        color = "blue"
    elif k == 121: #y
        color = "yellow"
        print("Yellow color selected.")
    elif k == 114: #r
        color = "red"
        print("Red color selected.")
    elif k == 112: #p
        color = "purple"
        print("Purple color selected.")
    elif k == 103: #g
        color = "green"
        print("Green color selected.")
    elif k == 111: #o
        color = "orange"
        print("Orange color selected.")
    elif k == 83: #S
        color = "silver"
        print("Silver color selected.")



# Release the Cap and Video
cap.release()
cv2.destroyAllWindows()

