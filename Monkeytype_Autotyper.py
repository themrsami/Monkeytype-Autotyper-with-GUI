import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QPushButton, QLabel, QInputDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
import time
import random

class SeleniumThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Open Chrome and navigate to monkeytype.com
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome(options=options)
        driver.get('https://monkeytype.com')

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'words')))

        # Flag to control whether the script is typing or not
        typing = False

        # Set typing speed based on slider value (approximately 0.015 seconds per character)
        typing_speed = window.slider1.value() / 10000

        # Create an ActionChain object
        actions = ActionChains(driver)

        # Continuously fetch and type each word
        while True:
            if keyboard.is_pressed('right'):  # If right arrow key is pressed
                typing = not typing  # Toggle the typing flag

            if typing:
                try:
                    # Get the active word (including space)
                    word = driver.find_element(By.CSS_SELECTOR, '.word.active').text + ' '
                    # Type each character using Selenium's send_keys() method
                    for letter in word:
                        # Introduce a chance of making a mistake based on slider value
                        if random.random() < window.slider2.value() / 100:
                            actions.send_keys('a')  # Type a wrong letter
                            actions.perform()
                            time.sleep(typing_speed)
                            actions.send_keys('\b')  # Press backspace to correct the mistake
                            actions.perform()
                            time.sleep(typing_speed)
                        actions.send_keys(letter)
                        actions.perform()
                        time.sleep(typing_speed)  # Delay between each character (including space)
                    time.sleep(window.slider3.value() / 100)  # Random delay between words and spaces based on slider value
                except Exception as e:
                    print(f"An error occurred: {e}")
                    typing = False  # Stop typing if an error occurs

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.presets = {}

        self.slider1 = QSlider(Qt.Horizontal)
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider3 = QSlider(Qt.Horizontal)

        self.slider1.setRange(0, 100)
        self.slider1.setValue(50)
        self.slider2.setRange(0, 100)
        self.slider2.setValue(50)
        self.slider3.setRange(0, 100)
        self.slider3.setValue(50)

        self.label1 = QLabel("Typing Speed (characters per second): " + str(self.slider1.value()))
        self.label2 = QLabel("Mistake Chance (%): " + str(self.slider2.value()))
        self.label3 = QLabel("Delay Between Words (ms): " + str(self.slider3.value()))

        self.slider1.valueChanged.connect(lambda: self.label1.setText("Typing Speed (characters per second): " + str(self.slider1.value())))
        self.slider2.valueChanged.connect(lambda: self.label2.setText("Mistake Chance (%): " + str(self.slider2.value())))
        self.slider3.valueChanged.connect(lambda: self.label3.setText("Delay Between Words (ms): " + str(self.slider3.value())))

        self.button = QPushButton("Start")
        self.button.clicked.connect(self.start_script)

        self.save_button = QPushButton("Save Preset")
        self.load_button = QPushButton("Load Preset")

        self.save_button.clicked.connect(self.save_preset)
        self.load_button.clicked.connect(self.load_preset)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.slider1)
        layout.addWidget(self.label2)
        layout.addWidget(self.slider2)
        layout.addWidget(self.label3)
        layout.addWidget(self.slider3)
        layout.addWidget(self.button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def start_script(self):
        self.thread = SeleniumThread()
        self.thread.start()

    def save_preset(self):
        preset = {
            'typing_speed': self.slider1.value(),
            'mistake_chance': self.slider2.value(),
            'delay_between_words': self.slider3.value()
        }

        name, ok = QInputDialog.getText(self, 'Save Preset', 'Enter a name for the preset:')
        
        if ok:
            self.presets[name] = preset

            with open('presets.json', 'w') as f:
                json.dump(self.presets, f)

    def load_preset(self):
        try:
            with open('presets.json', 'r') as f:
                self.presets = json.load(f)

            name, ok = QInputDialog.getItem(self, 'Load Preset', 'Select a preset:', list(self.presets.keys()), 0, False)
            
            if ok:
                preset = self.presets[name]

                self.slider1.setValue(preset['typing_speed'])
                self.slider2.setValue(preset['mistake_chance'])
                self.slider3.setValue(preset['delay_between_words'])
                
        except FileNotFoundError:
            print("Preset file not found.")

app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QSlider::groove:horizontal {
        height: 8px;
        background: #535353;
    }
    QSlider::handle:horizontal {
        background: #ffffff;
        width: 18px;
    }
""")

window = MainWindow()
window.show()

sys.exit(app.exec_())
