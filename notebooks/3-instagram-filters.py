# Handle variable names existing as functions/modules
from __future__ import absolute_import
# Handle Python2 compatibility
from __future__ import division
from __future__ import print_function

__version__ = '1.0.0'
__author__ = 'Raymond Abargos'

import cv2
import numpy as np
import random
import pyaudio
import wave
from threading import Thread

p = pyaudio.PyAudio()

def apply_invert(frame):
	return cv2.bitwise_not(frame)

def apply_alpha_convert(frame):
    try:
        frame.shape[3]
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        
    return frame

def apply_blend(frame1, frame2, mask):
    alpha = mask / 255.0
    blended = cv2.convertScaleAbs(frame1 * (1-alpha) + (frame2 * alpha))
    
    return blended

def apply_sepia(frame, intensity=0.5):
    blue, green, red = 20, 66, 112
    frame = apply_alpha_convert(frame)
    frame_height, frame_width, frame_channel = frame.shape
    sepia_bgra = (blue, green, red, 1)
    
    overlay = np.full((frame_height, frame_width, 4), sepia_bgra, dtype='uint8')
    
    frame = cv2.addWeighted(overlay, intensity, frame, 1.0, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    return frame

def apply_red(frame, intensity=0.5):
    blue, green, red = 0, 0, 255
    frame = apply_alpha_convert(frame)
    frame_height, frame_width, frame_channel = frame.shape
    sepia_bgra = (blue, green, red, 1)
    
    overlay = np.full((frame_height, frame_width, 4), sepia_bgra, dtype='uint8')
    
    frame = cv2.addWeighted(overlay, intensity, frame, 1.0, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    return frame

def apply_blue(frame, intensity=0.5):
    blue, green, red = 255, 0, 0
    frame = apply_alpha_convert(frame)
    frame_height, frame_width, frame_channel = frame.shape
    sepia_bgra = (blue, green, red, 1)
    
    overlay = np.full((frame_height, frame_width, 4), sepia_bgra, dtype='uint8')
    
    frame = cv2.addWeighted(overlay, intensity, frame, 1.0, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    return frame

def apply_green(frame, intensity=0.5):
    blue, green, red = 0, 255, 0
    frame = apply_alpha_convert(frame)
    frame_height, frame_width, frame_channel = frame.shape
    sepia_bgra = (blue, green, red, 1)
    
    overlay = np.full((frame_height, frame_width, 4), sepia_bgra, dtype='uint8')
    
    frame = cv2.addWeighted(overlay, intensity, frame, 1.0, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    return frame

def apply_disco(frame, intensity=0.5):
    blue, green, red = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    frame = apply_alpha_convert(frame)
    frame_height, frame_width, frame_channel = frame.shape
    sepia_bgra = (blue, green, red, 1)
    
    overlay = np.full((frame_height, frame_width, 4), sepia_bgra, dtype='uint8')
    
    frame = cv2.addWeighted(overlay, intensity, frame, 1.0, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    return frame

def apply_portrait_mode(frame):
    frame = apply_alpha_convert(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blurred = cv2.GaussianBlur(frame, (21, 21), 0)
    
    blended = apply_blend(frame, blurred, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    
    return frame

def stream_music():
    CHUNK = 1024
    
    file = 'C:\\Users\\raymond.d.abargos\\Downloads\\instagram_beats.wav'
    wf = wave.open(file, 'rb')
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(CHUNK)
    
    while True:
        stream.write(data)
        data = wf.readframes(CHUNK)
        
        k = cv2.waitKey(1)
        
        if k == ord('q') or k == 27:
            stream.stop_stream()
            stream.close()
            
            p.terminate()
            break


def stream_video():
    cap = cv2.VideoCapture(0)
    
    while True:
        _, frame = cap.read()
        
#        invert = apply_invert(frame)
#        sepia = apply_sepia(frame)
#        red = apply_red(frame)
#        blue = apply_blue(frame)
#        green = apply_green(frame)
        disco = apply_disco(frame)
#        portrait = apply_portrait_mode(frame)
        
        
#        cv2.imshow('Frame', frame)
#        cv2.imshow('Inverted Frame', invert)
#        cv2.imshow('Sepia Frame', sepia)
#        cv2.imshow('Red Frame', red)
#        cv2.imshow('Blue Frame', blue)
#        cv2.imshow('Green Frame', green)
        cv2.imshow('Disco Frame', disco)
#        cv2.imshow('Portrait', portrait)
        
        k = cv2.waitKey(1)
        
        if k == ord('q') or k == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

def test_thread():
    thread1 = Thread(target = stream_video)
    thread1.start()
    thread2 = Thread(target = stream_music)
    thread2.start()
    thread1.join()
    thread2.join()
    print("Thread finished. Exiting...")

test_thread()

