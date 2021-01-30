# -*- coding: utf-8 -*
import tkinter as tk
import cv2
from PIL import Image,ImageTk
from UI import UI

if __name__ == "__main__":
    root = tk.Tk()
    ui = UI(root)
    root.mainloop()
    cv2.destroyAllWindows()