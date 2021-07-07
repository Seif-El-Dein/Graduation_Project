import cv2

def Capture_Sample(counter):

    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    image = cv2.resize(image,(640,480))
    cv2.imwrite('/home/pi/Desktop/Samples/'+str(counter)+'.jpg', image)
    del(camera)

if __name__ == '__main__':

    cnt = 0
    for i in range(3):
        cnt += 1
        Capture_Sample(cnt)