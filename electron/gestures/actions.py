import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from gestures.utils import resource_path


class GestureActions:
    def __init__(self):
        self.last_action = None
        self.cooldown = 0.5
        self.last_time = time.time()
        self.playing = False
        self.current_speed = 1.0
        self.driver = None   # lazy-loaded

    # ---------- GET / CREATE DRIVER ----------
    def get_driver(self):
        """Attach to existing Chrome debug session only when needed"""
        if self.driver:
            return self.driver

        try:
            chrome_options = Options()
            chrome_options.add_experimental_option(
                "debuggerAddress", "127.0.0.1:9222"
            )

            driver_path = resource_path("assets/chromedriver.exe")
            service = Service(driver_path)

            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # focus page to ensure JS works
            self.driver.execute_script("document.body.focus();")

            print("chrome_connected", flush=True)
            return self.driver

        except Exception as e:
            print("chrome_not_running", flush=True)
            print(str(e), flush=True)
            return None

    # ---------- PERFORM ACTION ----------
    def perform(self, action):
        if not action:
            return

        # handle dict speed separately
        if isinstance(action, dict) and action.get("set_speed") is not None:
            driver = self.get_driver()
            if not driver:
                return

            speed = action["set_speed"]
            speed = max(0.25, min(speed, 3))
            self.current_speed = speed

            driver.execute_script(f"""
                let vid=document.querySelector('video');
                if(vid) vid.playbackRate={speed};
            """)

            print(f"speed_{speed}", flush=True)
            return

        # cooldown check
        now = time.time()
        if self.last_action == action and (now - self.last_time) < self.cooldown:
            return

        self.last_action = action
        self.last_time = now

        driver = self.get_driver()
        if not driver:
            return

        # ---------- PLAY / PAUSE ----------
        if action == "play":
            if not self.playing:
                driver.execute_script("document.querySelector('video').play()")
                self.playing = True

        elif action == "pause":
            if self.playing:
                driver.execute_script("document.querySelector('video').pause()")
                self.playing = False

        # ---------- VOLUME ----------
        elif action == "volume_up":
            driver.execute_script("""
                let vid=document.querySelector('video');
                if(vid) vid.volume=Math.min(vid.volume+0.05,1);
            """)

        elif action == "volume_down":
            driver.execute_script("""
                let vid=document.querySelector('video');
                if(vid) vid.volume=Math.max(vid.volume-0.05,0);
            """)

        # ---------- SEEK ----------
        elif action == "forward":
            driver.execute_script("""
                let vid=document.querySelector('video');
                if(vid) vid.currentTime+=5;
            """)

        elif action == "backward":
            driver.execute_script("""
                let vid=document.querySelector('video');
                if(vid) vid.currentTime-=5;
            """)

        # ---------- MUTE ----------
        elif action == "mute":
            driver.execute_script("""
                let vid=document.querySelector('video');
                if(vid) vid.muted=true;
            """)

        elif action == "unmute":
            driver.execute_script("""
                let vid=document.querySelector('video');
                if(vid) vid.muted=false;
            """)

        # ---------- EXIT ----------
        elif action == "exit":
            print("exit", flush=True)
            sys.exit(0)

        # send clean action name to Electron
        print(action, flush=True)