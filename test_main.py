
import subprocess
import pyautogui
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

subprocess.Popen(['C:/Program Files/Palo Alto Networks/GlobalProtect/PanGPA.exe'])
time.sleep(0.5)

x1, y1 = 3550, 1800

screenshot = pyautogui.screenshot(region=(x1, y1, 300, 300))

text = pytesseract.image_to_string(screenshot)
print(type(text))
print(text.strip())