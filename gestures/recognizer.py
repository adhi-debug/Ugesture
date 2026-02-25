import math


class GestureRecognizer:
    def __init__(self, frame_height=480, min_speed=0.5, max_speed=2.0):
        self.wave_threshold = 50
        self.prev_wrist_x = None
        self.prev_wrist_y = None
        self.prev_pinch = False
        self.frame_height = frame_height
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.last_speed = None   # prevents speed spam

    # ---------- DISTANCE ----------
    def calculate_distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    # ---------- FINGER STATE ----------
    def fingers_up(self, hand):
        """Return [thumb, index, middle, ring, pinky] booleans"""
        fingers = []

        # thumb (simple right-hand assumption)
        fingers.append(hand[4][0] > hand[3][0])

        # other fingers: tip above pip joint
        fingers.append(hand[8][1] < hand[6][1])   # index
        fingers.append(hand[12][1] < hand[10][1]) # middle
        fingers.append(hand[16][1] < hand[14][1]) # ring
        fingers.append(hand[20][1] < hand[18][1]) # pinky

        return fingers

    # ---------- MAIN RECOGNITION ----------
    def recognize(self, landmarks):
        if not landmarks:
            return None

        hand = landmarks[0]
        wrist = hand[0]
        thumb_tip = hand[4]
        index_tip = hand[8]

        gesture = None

        # ---------- PINCH = PLAY / PAUSE ----------
        pinch_distance = self.calculate_distance(thumb_tip, index_tip)
        is_pinched = pinch_distance < 40

        if is_pinched and not self.prev_pinch:
            gesture = "pause"
        elif not is_pinched and self.prev_pinch:
            gesture = "play"

        self.prev_pinch = is_pinched

        # ---------- WAVE LEFT / RIGHT ----------
        if self.prev_wrist_x is not None:
            delta_x = wrist[0] - self.prev_wrist_x

            if delta_x > self.wave_threshold:
                gesture = "forward"

            elif delta_x < -self.wave_threshold:
                gesture = "backward"

        # ---------- FINGER GESTURES ----------
        fingers = self.fingers_up(hand)

        # index + middle only → mute
        if fingers[1] and fingers[2] and not any(fingers[3:]):
            gesture = "mute"

        # only index → unmute
        elif fingers[1] and not fingers[2] and not any(fingers[3:]):
            gesture = "unmute"

        # ---------- SPEED CONTROL (ONLY IF NO OTHER GESTURE) ----------
        if gesture is None and self.prev_wrist_y is not None:

            normalized_y = wrist[1] / self.frame_height

            speed = self.max_speed - (
                (self.max_speed - self.min_speed) * normalized_y
            )

            speed = round(speed, 2)

            # only emit if changed enough
            if self.last_speed is None or abs(speed - self.last_speed) > 0.15:
                self.last_speed = speed
                gesture = {"set_speed": speed}

        # save wrist position
        self.prev_wrist_x = wrist[0]
        self.prev_wrist_y = wrist[1]

        return gesture