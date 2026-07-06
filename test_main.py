
import subprocess
import pyautogui
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

subprocess.Popen(['C:/Program Files/Palo Alto Networks/GlobalProtect/PanGPA.exe'])
time.sleep(0.5)

x1, y1 = 3550, 1800
x1, y1 = 1600, 817
x1, y1 = 2185, 1075   # MSI laptop OCR box top-left

screenshot = pyautogui.screenshot(region=(x1, y1, 360, 470))
screenshot.save("WUHU.jpg")

text = pytesseract.image_to_string(screenshot)
print(type(text))
print(text.strip())