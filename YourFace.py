import cv2 as cv
import numpy as np

record_file_name = 'YourFace'
record_file_extension = '.mp4'

def record_your_face():
    video = cv.VideoCapture(0)

    if video.isOpened():
        fps = video.get(cv.CAP_PROP_FPS)
        wait_input_time = (int)(1/fps*1000)
        recorder = cv.VideoWriter()
        while True:
            valid, img= video.read()
        
            if not valid :
                break
        
            if not recorder.isOpened():
                record_file = record_file_name + record_file_extension
                fps = video.get(cv.CAP_PROP_FPS)
                h, w, *_ = img.shape
                is_color = (img.ndim > 2) and (img.shape[2] == 3)
                recorder.open(record_file, cv.VideoWriter_fourcc(*'mp4v'), fps, (w, h), is_color)
            
            
            recorder.write(img)
        
            cv.circle(img, (20,20), 7, (0,0,255),-1)
            cv.putText(img, "Recording...", (30, 23), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), thickness=2)
            cv.putText(img, "Recording...", (30, 23), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
            
            cv.imshow('YourFace', img)

            
            key = cv.waitKeyEx(wait_input_time)
            if key == 27:
                cv.destroyAllWindows()
                recorder.release()
                video.release()
                break
            elif key == 32:
                cv.destroyAllWindows()
                recorder.release()
                video.release()
                review_your_face()
                break;
                
                
frame_step = 1

def review_your_face():
    video = cv.VideoCapture(record_file_name + record_file_extension)
    is_reverse_horizon = False
    is_reverse_vertical = False
    
    if video.isOpened():
        fps = video.get(cv.CAP_PROP_FPS)
        wait_input_time = (int)(1/fps*1000)
        total_frame = (int)(video.get(cv.CAP_PROP_FRAME_COUNT))
        
        
        
        while True:
            valid, img = video.read()
            
            if not valid:
                video.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue
            img_height, img_width, *_ = img.shape
            cur_frame = video.get(cv.CAP_PROP_POS_FRAMES)
            
            cv.circle(img, (20,20), 7, (255,0,0),-1)
            cv.putText(img, "Watching your face again... Why?", (30, 23), cv.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255),thickness=2)
            cv.putText(img, "Watching your face again... Why?", (30, 23), cv.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))
            
            
            if is_reverse_horizon:
                if img_width % 2 == 0:
                    img[:, (int)(img_width/2):(int)(img_width)] = img[:, (int)((img_width/2)):0:-1]
                else:
                    img[:, (int)(img_width/2) + 2:(int)(img_width)] = img[:, (int)((img_width/2)):0:-1]
            if is_reverse_vertical:
                if img_height % 2 == 0:
                    img[(int)(img_height/2):(int)(img_height), :] = img[(int)((img_height/2)):0:-1, :]
                else:
                    img[(int)(img_height/2) + 2:(int)(img_height), :] = img[(int)((img_height/2)):0:-1, :]
            
            cv.imshow('YourFace', img)
            
            key = cv.waitKeyEx(wait_input_time)
            
            if key == 27:
                cv.destroyAllWindows()
                video.release()
                break
            elif key == 32:
                cv.destroyAllWindows()
                video.release()
                record_your_face()
                break
            elif key == ord('+') or key == ord('='):
                video.set(cv.CAP_PROP_POS_FRAMES, max(cur_frame + frame_step,total_frame))
            elif key == ord('-') or key == ord('_'):
                video.set(cv.CAP_PROP_POS_FRAMES, min(cur_frame - frame_step,0))       
            elif key == ord('s') or key == ord('S'):
                temp_key = cv.waitKey()
                if not (temp_key == ord('s') or temp_key == ord('S')):
                  temp_key = cv.waitKey()
            elif key == ord('h') or key == ord('H'):
                is_reverse_horizon = not is_reverse_horizon
            elif key == ord('v') or key == ord('V'):
                is_reverse_vertical = not is_reverse_vertical
                
                
if __name__ == '__main__':
    record_your_face()