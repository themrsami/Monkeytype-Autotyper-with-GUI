import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QPushButton, QLabel, QInputDialog
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QPalette, QColor
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
        self.total_errors_made = 0

    def run(self):
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get('https://monkeytype.com')

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'words')))

        # Typing control flag
        typing = False
        actions = ActionChains(driver)
        start_time = time.time()

        while True:
            if keyboard.is_pressed('right'):  # Toggle typing on/off
                typing = not typing

            if typing:
                try:
                    word = driver.find_element(By.CSS_SELECTOR, '.word.active').text + ' '
                    for i, letter in enumerate(word):
                        speed = random.uniform(window.sliderMinSpeed.value(), window.sliderMaxSpeed.value()) / 1000

                        # Introduce a chance of making a mistake
                        if random.random() < window.sliderMistakeChance.value() / 100 and self.total_errors_made < window.sliderTotalErrors.value():
                            actions.send_keys('a')  # Typing a wrong letter
                            actions.perform()
                            time.sleep(speed)
                            self.total_errors_made += 1
                            continue  # Move forward with the error

                        actions.send_keys(letter)
                        actions.perform()
                        time.sleep(speed)

                        # Introduce a rare pause within the word
                        if i < len(word) - 1 and random.random() < 0.1:
                            time.sleep(random.uniform(0.05, 0.2))

                    # Gradually decrease typing speed
                    if time.time() - start_time > random.uniform(3, 5):
                        new_min_speed = window.sliderMinSpeed.value() + 2
                        if new_min_speed > window.sliderMaxSpeed.value():
                            new_min_speed = window.sliderMinSpeed.value() - 30
                            if new_min_speed < 10:
                                new_min_speed = 10
                        window.sliderMinSpeed.setValue(new_min_speed)
                        time.sleep(random.uniform(0.2, 0.6))
                        start_time = time.time()

                    # Variable pause between words
                    time.sleep(random.uniform(0, window.sliderVariablePause.value() / 1000))

                except Exception as e:
                    print(f"An error occurred: {e}")
                    typing = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.presets = {}

        # Initialize sliders
        self.sliderMinSpeed = QSlider(Qt.Horizontal)
        self.sliderMaxSpeed = QSlider(Qt.Horizontal)
        self.sliderMistakeChance = QSlider(Qt.Horizontal)
        self.sliderMaxPause = QSlider(Qt.Horizontal)
        self.sliderVariablePause = QSlider(Qt.Horizontal)
        self.sliderTotalErrors = QSlider(Qt.Horizontal)

        # Set slider ranges and default values
        self.sliderMinSpeed.setRange(10, 100)
        self.sliderMinSpeed.setValue(30)
        self.sliderMaxSpeed.setRange(10, 100)
        self.sliderMaxSpeed.setValue(70)
        self.sliderMistakeChance.setRange(0, 100)
        self.sliderMistakeChance.setValue(5)
        self.sliderMaxPause.setRange(0, 100)
        self.sliderMaxPause.setValue(50)
        self.sliderVariablePause.setRange(0, 500)
        self.sliderVariablePause.setValue(100)
        self.sliderTotalErrors.setRange(0, 100)
        self.sliderTotalErrors.setValue(10)

        # Create labels for sliders
        self.labelMinSpeed = QLabel(f"Min Typing Speed (ms/char): {self.sliderMinSpeed.value()}")
        self.labelMaxSpeed = QLabel(f"Max Typing Speed (ms/char): {self.sliderMaxSpeed.value()}")
        self.labelMistakeChance = QLabel(f"Mistake Chance (%): {self.sliderMistakeChance.value()}")
        self.labelMaxPause = QLabel(f"Max Pause Time (ms): {self.sliderMaxPause.value()}")
        self.labelVariablePause = QLabel(f"Variable Pause Time (ms): {self.sliderVariablePause.value()}")
        self.labelTotalErrors = QLabel(f"Total Errors: {self.sliderTotalErrors.value()}")

        # Connect sliders to labels
        self.sliderMinSpeed.valueChanged.connect(lambda: self.labelMinSpeed.setText(f"Min Typing Speed (ms/char): {self.sliderMinSpeed.value()}"))
        self.sliderMaxSpeed.valueChanged.connect(lambda: self.labelMaxSpeed.setText(f"Max Typing Speed (ms/char): {self.sliderMaxSpeed.value()}"))
        self.sliderMistakeChance.valueChanged.connect(lambda: self.labelMistakeChance.setText(f"Mistake Chance (%): {self.sliderMistakeChance.value()}"))
        self.sliderMaxPause.valueChanged.connect(lambda: self.labelMaxPause.setText(f"Max Pause Time (ms): {self.sliderMaxPause.value()}"))
        self.sliderVariablePause.valueChanged.connect(lambda: self.labelVariablePause.setText(f"Variable Pause Time (ms): {self.sliderVariablePause.value()}"))
        self.sliderTotalErrors.valueChanged.connect(lambda: self.labelTotalErrors.setText(f"Total Errors: {self.sliderTotalErrors.value()}"))

        # Initialize buttons
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.start_script)
        self.saveButton = QPushButton("Save Preset")
        self.loadButton = QPushButton("Load Preset")
        self.saveButton.clicked.connect(self.save_preset)
        self.loadButton.clicked.connect(self.load_preset)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.labelMinSpeed)
        layout.addWidget(self.sliderMinSpeed)
        layout.addWidget(self.labelMaxSpeed)
        layout.addWidget(self.sliderMaxSpeed)
        layout.addWidget(self.labelMistakeChance)
        layout.addWidget(self.sliderMistakeChance)
        layout.addWidget(self.labelMaxPause)
        layout.addWidget(self.sliderMaxPause)
        layout.addWidget(self.labelVariablePause)
        layout.addWidget(self.sliderVariablePause)
        layout.addWidget(self.labelTotalErrors)
        layout.addWidget(self.sliderTotalErrors)
        layout.addWidget(self.startButton)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.loadButton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Set window properties
        self.setWindowTitle("MonkeyType Bot")
        self.resize(400, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #535353;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #5c5c5c;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QLabel {
                margin: 5px;
            }
        """)

    def start_script(self):
        self.thread = SeleniumThread()
        self.thread.start()

    def save_preset(self):
        preset = {
            'min_speed': self.sliderMinSpeed.value(),
            'max_speed': self.sliderMaxSpeed.value(),
            'mistake_chance': self.sliderMistakeChance.value(),
            'max_pause': self.sliderMaxPause.value(),
            'variable_pause': self.sliderVariablePause.value(),
            'total_errors': self.sliderTotalErrors.value()
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

                self.sliderMinSpeed.setValue(preset['min_speed'])
                self.sliderMaxSpeed.setValue(preset['max_speed'])
                self.sliderMistakeChance.setValue(preset['mistake_chance'])
                self.sliderMaxPause.setValue(preset['max_pause'])
                self.sliderVariablePause.setValue(preset['variable_pause'])
                self.sliderTotalErrors.setValue(preset['total_errors'])
                
        except FileNotFoundError:
            print("Preset file not found.")

app = QApplication(sys.argv)

palette = QPalette()
palette.setColor(QPalette.Window, QColor("#2b2b2b"))
palette.setColor(QPalette.WindowText, QColor("#ffffff"))
palette.setColor(QPalette.Base, QColor("#2b2b2b"))
palette.setColor(QPalette.AlternateBase, QColor("#3a3a3a"))
palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
palette.setColor(QPalette.ToolTipText, QColor("#ffffff"))
palette.setColor(QPalette.Text, QColor("#ffffff"))
palette.setColor(QPalette.Button, QColor("#3a3a3a"))
palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
palette.setColor(QPalette.BrightText, QColor("#ff0000"))
palette.setColor(QPalette.Highlight, QColor("#535353"))
palette.setColor(QPalette.HighlightedText, QColor("#000000"))
app.setPalette(palette)

window = MainWindow()
window.show()

sys.exit(app.exec_())
