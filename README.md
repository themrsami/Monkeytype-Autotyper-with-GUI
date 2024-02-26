# Monkeytype Autotyper

This is a Python program that simulates typing on the website monkeytype.com. It uses Selenium WebDriver for browser automation and PyQt5 for the GUI. The program allows you to adjust the typing speed, the chance of making a mistake, and the delay between words.

## Features

- **Typing Speed**: Adjust the speed at which the program types.
- **Mistake Chance**: Set the probability of the program making a mistake while typing.
- **Delay Between Words**: Control the delay between typing each word.
- **Save/Load Presets**: Save your settings as a preset and load them later.

## How to Use

1. Adjust the sliders to set the typing speed, mistake chance, and delay between words.
2. Click the "Start" button to start the script. The script starts when the 'right' arrow key is pressed. You can change this key in the line `if keyboard.is_pressed('right'):` by replacing `'right'` with the key of your choice.
3. To save your settings, click the "Save Preset" button and enter a name for the preset.
4. To load a preset, click the "Load Preset" button and select the preset you want to load.

## Requirements

- Python 3
- Selenium WebDriver
- PyQt5
- keyboard

## Installation

1. Clone this repository.
2. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Run the script:

```bash
python Monkeytype_Autotyper.py
```

![image](https://github.com/themrsami/Monkeytype-Autotyper-with-GUI/assets/91170768/0c4ad252-71d6-4c9a-8de6-033dd7ccd983)

![image](https://github.com/themrsami/Monkeytype-Autotyper-with-GUI/assets/91170768/0ae4da90-5fa1-4df7-be71-fbfc73813d61)

![image](https://github.com/themrsami/Monkeytype-Autotyper-with-GUI/assets/91170768/f2025267-609e-4c84-abe2-554e4174a077)






## Troubleshooting

If the script is not working, make sure you have the latest version of ChromeDriver installed and it’s in your PATH. You can download it from the ChromeDriver website. Make sure to choose the version that matches your installed version of Chrome.

## Contributing
Suggestions and pull requests are welcome. If you have any ideas or find any bugs, please open an issue or submit a pull request.

## Contact
Github - [https://www.github.com/themrsami]
Facebook - [https://www.facebook.com/themrsami]
Twitter - [https://www.twitter.com/themrsami]
LinkedIn - [https://www.linkedin.com/in/usama-nazir]


Please feel free to reach out if you have any questions or suggestions.
