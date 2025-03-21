import os
import cv2
import glob
import numpy as np
from PIL import Image

# Türkçe karakterleri geri çevirmek için eşleme tablosu
turkish_map = {
    "cc_": "ç", "CC": "Ç",
    "ii_": "ı", "II": "İ",
    "uu_": "ü", "UU": "Ü",
    "oo_": "ö", "OO": "Ö",
    "gg_": "ğ", "GG": "Ğ",
    "ss_": "ş", "SS": "Ş"
}

# Türkçe karakterleri geri döndüren fonksiyon
def convert_to_turkish(folder_name):
    turkish_name = turkish_map.get(folder_name, folder_name)
    if "_" in turkish_name:  # Küçük harflerde "_" varsa kaldır
        turkish_name = turkish_name.replace("_", "")
    return turkish_name

# Ana veri seti klasörü
dataset_path = r"C:\Users\furka\Desktop\dataset"

# Çıktı dosyalarının kaydedileceği klasör
output_path = r"C:\Users\furka\Desktop\prepared_dataset"
os.makedirs(output_path, exist_ok=True)

# Klasörleri tara (0-9 ve harf klasörleri)
for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)
    if not os.path.isdir(folder_path):
        continue  # Klasör değilse geç

    # TXT içinde yazılacak karakteri belirle
    turkish_char = convert_to_turkish(folder)

    # Klasördeki tüm JPG dosyalarını al
    image_files = glob.glob(os.path.join(folder_path, "*.jpg"))

    for img_idx, img_path in enumerate(image_files):
        # Görseli oku
        img = cv2.imread(img_path)
        if img is None:
            print(f"Hata: {img_path} dosyası açılamadı!")
            continue

        # Görüntüyü siyah-beyaza çevir
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Dosya adları
        base_filename = f"{folder}_{img_idx}"
        tif_filename = os.path.join(output_path, f"{base_filename}.tif")
        box_filename = os.path.join(output_path, f"{base_filename}.box")
        txt_filename = os.path.join(output_path, f"{base_filename}.gt.txt")

        # TIF kaydet
        img_pil = Image.fromarray(img_gray)
        img_pil.save(tif_filename)

        # BOX dosyası oluştur
        with open(box_filename, "w", encoding="utf-8") as box_file:
            h, w = img_gray.shape
            box_file.write(f"{turkish_char} 0 0 {w} {h} 0\n")

        # TXT dosyası oluştur (Türkçe karakterle yazılacak)
        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(turkish_char)

print("✅ İşlem tamamlandı! Tüm dosyalar başarıyla oluşturuldu.")
