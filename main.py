import tkinter as tk
import threading
from pynput import keyboard
import translator
from ui import Snipper

def trigger_text_translation():
    threading.Thread(target=translator.translate_and_replace, daemon=True).start()

def trigger_crop_translation():
    def on_crop_done(img):
        threading.Thread(target=translator.process_image_crop, args=(img,), daemon=True).start()
    
    root.after(0, lambda: Snipper(root, on_crop_done))

def start_hotkeys():
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+c': trigger_text_translation,
        '<ctrl>+<alt>+s': trigger_crop_translation
    }) as h:
        h.join()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    listener_thread = threading.Thread(target=start_hotkeys, daemon=True)
    listener_thread.start()
    
    print("--- Çeviri Aracı Çalışıyor ---")
    print("1. Metin Seçip Çevirme  : Ctrl + Alt + C  (Metnin üzerine Türkçe karşılığını yazar)")
    print("2. Ekran Kırpıp Çevirme : Ctrl + Alt + S  (Seçilen alanın çevirisini panoya kopyalar)")
    
    root.mainloop()