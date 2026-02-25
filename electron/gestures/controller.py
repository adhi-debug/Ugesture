# ---------- HIDE MEDIAPIPE / TF LOGS FIRST ----------
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["GLOG_minloglevel"] = "3"

import cv2
from gestures.detector import HandDetector
from gestures.recognizer import GestureRecognizer
from gestures.actions import GestureActions
import warnings
warnings.filterwarnings("ignore")


class GestureController:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.detector = HandDetector()
        self.recognizer = GestureRecognizer()
        self.actions = GestureActions()
        self.window_name = "Ugesture - Hand Control"

    def run(self):

        if not self.cap.isOpened():
            print("camera_error", flush=True)
            return

        print("camera_started", flush=True)

        # create window once
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        while True:

            # ✅ detect if user pressed X on window
            if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("window_closed", flush=True)
                break

            success, frame = self.cap.read()

            if not success:
                print("frame_failed", flush=True)
                break

            # detect hands
            frame, landmarks = self.detector.find_hands(frame)

            # recognize gestures
            if landmarks:
                gesture = self.recognizer.recognize(landmarks)
                if gesture:
                    self.actions.perform(gesture)

            cv2.imshow(self.window_name, frame)

            # exit on Q key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("quit_key", flush=True)
                break

        # cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        print("camera_stopped", flush=True)


# ---------- AUTO CAMERA SEARCH ----------
if __name__ == "__main__":

    print("controller_starting", flush=True)

    found = False

    for idx in range(3):
        controller = GestureController(camera_index=idx)

        if controller.cap.isOpened():
            print(f"camera_index_{idx}", flush=True)
            controller.run()
            found = True
            break
        else:
            print(f"camera_try_{idx}_failed", flush=True)

    if not found:
        print("no_camera_found", flush=True)