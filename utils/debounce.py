import time

class Debounce:
    def __init__(self, cooldown=1.0):
        """
        cooldown: minimum time (in seconds) between the same action
        """
        self.cooldown = cooldown
        self.last_action_time = {}
    
    def ready(self, action_name: str) -> bool:
        """
        Returns True if enough time has passed since the last action.
        Otherwise, returns False.
        """
        now = time.time()
        last_time = self.last_action_time.get(action_name, 0)

        if now - last_time >= self.cooldown:
            self.last_action_time[action_name] = now
            return True
        return False
