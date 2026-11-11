import time
import numpy as np
import pyperclip
import pyautogui
import easyocr
from deep_translator import MyMemoryTranslator

print("EasyOCR modeli ve çevirici yükleniyor...")
reader = easyocr.Reader(['en', 'tr'])
# Google engeli yerine MyMemory API kullanıyoruz
translator = MyMemoryTranslator(source='en-US', target='tr-TR')
print("Model hazır!")

def translate_text(text: str) -> str:
    if not text or not text.strip():
        return ""
    try:
        # Metin uzunsa parçalayarak gönderir
        return translator.translate(text)
    except Exception as e:
        print(f"Çeviri hatası: {e}")
        return text

def translate_and_replace():
    """Seçili metni Ctrl+C yapıp çevirir ve seçili alanın üzerine Ctrl+V ile yapıştırır."""
    pyperclip.copy("")
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    
    selected_text = pyperclip.paste()
    if not selected_text or not selected_text.strip():
        return
    
    translated = translate_text(selected_text)
    if translated and translated != selected_text:
        pyperclip.copy(translated)
        time.sleep(0.05)
        pyautogui.hotkey('ctrl', 'v')

def process_image_crop(image_pil):
    """Ekran görüntüsünden OCR yapıp metni çevirir ve panoya kopyalar."""
    img_np = np.array(image_pil)
    results = reader.readtext(img_np, detail=0)
    extracted_text = " ".join(results)
    
    if not extracted_text.strip():
        print("\n[OCR]: Metin okunamadı.\n")
        return

    translated = translate_text(extracted_text)
    if translated:
        pyperclip.copy(translated)
        print(f"\n[SS Çevirisi Panoya Kopyalandı ve Hazır]:\n{translated}\n")