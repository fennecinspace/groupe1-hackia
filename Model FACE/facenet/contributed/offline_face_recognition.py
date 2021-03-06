# coding=utf-8
"""Performs face detection in realtime.

Based on code from https://github.com/shanren7/real_time_face_recognition
"""
# MIT License
#
# Copyright (c) 2017 François Gervais
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import sys
import time

import cv2

import face
# from google.colab import files

import numpy as np

global confused
global good
global unknown

person = 'Camilo'
allowedUser = ['Adriano','Alex','Arnaud','Arnauld','Belarbi','Camilo','Larhmam','Michel','Mohamed','Olivier','Pierre','Sidi','Thomas']
allowedUser.remove(person)
print(allowedUser)

# def add_overlays(frame, faces, frame_rate):
#     if faces is not None:
#         for face in faces:
#             face_bb = face.bounding_box.astype(int)
#             cv2.rectangle(frame,
#                           (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
#                           (0, 255, 0), 2)
#             if face.name is not None:
#                 cv2.putText(frame, face.name+str(np.max(face.proba)), (face_bb[0], face_bb[3]),
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
#                             thickness=2, lineType=2)
#
#     cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
#                 thickness=2, lineType=2)


def add_overlays(frame, faces, frame_rate, confused,good,unknown):
    names=[]
    if faces is not None:
        for face in faces:
            if face.name is not None:
                if face.name in allowedUser:
                    confused += 1
                elif face.name == 'UNKNOWN':
                    unknown += 1
                else:
                    good+=1
                    if (confused==50):
                        print ("Congratulations, you are well authentified")
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame,
                          (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                          (0, 255, 0), 2)
            if face.name is not None:
                cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)
    return confused,good,unknown


def main(args):
    confused=0
    good=0
    unknown=0
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    videoFileName = "video.mp4"
    treatedFileName = "output.mp4"
    face_recognition = face.Recognition()
    start_time = time.time()
    cap = cv2.VideoCapture(videoFileName)

    #Get the FPS to reconstruct the video at the rigth speed
    fpsValue = cap.get(cv2.CAP_PROP_FPS)
    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    out = cv2.VideoWriter(apiPreference=0,filename=treatedFileName,fourcc=cv2.VideoWriter_fourcc(*'MP4V'),fps=fpsValue,frameSize=(round(frameWidth),round(frameHeight)))



    if args.debug:
        print("Debug enabled")
        face.debug = True

    i=0
    # while (cap.isOpened()):
    while (confused < 50):
        # Capture frame-by-frame
        i=i+1
        ret, frame = cap.read()
        if ret == False:
          break
        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)

            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        # add_overlays(frame, faces, frame_rate)
        confused, good, unknown = add_overlays(frame, faces, frame_rate,confused,good,unknown)
        print('good',good)
        print('confused',confused)
        print('unknown',unknown)

        frame_count += 1
        out.write(frame)



    # while (ok < 50):
    #     # Capture frame-by-frame
    #     ret, frame = video_capture.read()
    #     frame = cv2.resize(frame, (640,480), interpolation=cv2.INTER_AREA)
    #     if (frame_count % frame_interval) == 0:
    #         faces = face_recognition.identify(frame)
    #
    #         # Check our current fps
    #         end_time = time.time()
    #         if (end_time - start_time) > fps_display_interval:
    #             frame_rate = int(frame_count / (end_time - start_time))
    #             start_time = time.time()
    #             frame_count = 0
    #
    #     ok=add_overlays(frame, faces, frame_rate, ok)
    #     print(ok)
    #     frame_count += 1
    #     cv2.imshow('Video', frame)
    #
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='Enable some debug outputs.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
