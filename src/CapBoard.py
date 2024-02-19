import cv2
import numpy as np

class CapBoard:
    def __init__(self):
        self.size_change_speed = 1
        self.con_pos_x = 0
        self.con_pos_y = 0
        self.con_width = 480
        self.con_height = 270
        self.width = 1280
        self.height = 960
        self.coord_x = 0
        self.coord_y = 0
        self.key_actions = {
            ord('w') : ('con_pos_y', '-', 'size_change_speed'),
            ord('a') : ('con_pos_x', '-', 'size_change_speed'),
            ord('s') : ('con_pos_y', '+', 'size_change_speed'),
            ord('d') : ('con_pos_x', '+', 'size_change_speed'),
            ord('q') : ('con_width', '-', 'size_change_speed'),
            ord('e') : ('con_width', '+', 'size_change_speed'),
            ord('z') : ('con_height', '-', 'size_change_speed'),
            ord('x') : ('con_height', '+', 'size_change_speed'),
            ord('-') : ('size_change_speed', '+', '1'),
            ord('+') : ('size_change_speed', '-', '1')
        }
    def draw_contours(self):
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Frame", self.width, self.height)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
        
            cv2.rectangle(frame, (self.con_pos_x, self.con_pos_y), (self.con_width + self.con_pos_x, self.con_height + self.con_pos_y), (0, 255, 0), 1)

            #Recognition
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            mask = cv2.inRange(hsv_frame, lower_red, upper_red)

            # Применение маски только внутри прямоугольника
            roi = mask[self.con_pos_y:self.con_pos_y+self.con_height, self.con_pos_x:self.con_pos_x+self.con_width]

            # Поиск контуров
            contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Отображение контуров
            cv2.drawContours(frame[self.con_pos_y:self.con_pos_y+self.con_height, self.con_pos_x:self.con_pos_x+self.con_width], contours, -1, (0, 0, 255), 2)
            #end
            # Отображение кадра
            text_position_x = "Position X: " + str(self.con_pos_x)
            text_contour_width = "Contour Width: " + str(self.con_width)
            text_size_change = "Change speed: " + str(self.size_change_speed)
            text_coord_x = "Coord X: " + str(self.coord_x)
            text_coord_y = "Coord Y: " + str(self.coord_y)
            frame = self.put_text(frame, text_position_x, int(self.height/2 - 10))
            frame = self.put_text(frame, text_contour_width, int(self.height/2 - 30))
            frame = self.put_text(frame, text_size_change, int(self.height/2 - 50))
            frame = self.put_text(frame, text_coord_x, int(self.height/2 - 70))
            frame = self.put_text(frame, text_coord_y, int(self.height/2 - 90))
            cv2.imshow("Frame", frame)
            self.UpdateInput()
            

        cap.release()
        cv2.destroyAllWindows()

    def UpdateInput(self):
        key = cv2.waitKey(33)
        if (key == ord('d')):
            self.con_pos_x+=self.size_change_speed
        elif (key == ord('a')):
            self.con_pos_x-=self.size_change_speed
        elif (key == ord('w')):
            self.con_pos_y-=self.size_change_speed
        elif (key == ord('s')):
            self.con_pos_y+=self.size_change_speed
        elif (key == ord('q')):
            self.con_width-=self.size_change_speed
        elif (key == ord('e')):
            self.con_width+=self.size_change_speed
        elif (key == ord('z')):
            self.con_height-=self.size_change_speed
        elif (key == ord('x')):
            self.con_height+=self.size_change_speed
        elif (key == ord('+')):
            self.size_change_speed+=1
        elif (key == ord('-')):
            self.size_change_speed-=1

    def put_text(self, frame, line, pos_y):
        font = cv2.FONT_HERSHEY_SIMPLEX 
        org = (int(self.width/2 - 160), pos_y) 
        fontScale = 0.4
        color = (255, 0, 255) 
        thickness = 1
        frame = cv2.putText(frame, line, org, font,
                            fontScale, color, thickness, cv2.LINE_AA)
        return frame