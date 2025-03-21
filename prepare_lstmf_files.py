import os
import subprocess

# Klasör yollarını belirleme
desktop_path = os.path.expanduser("~/Desktop")  # Masaüstü yolu
dataset_dir = os.path.join(desktop_path, "prepared_dataset")  # Ana klasör

# Klasörlerin tanımlanması
image_dir = dataset_dir  # .tif dosyaları burada
box_dir = dataset_dir    # .box dosyaları burada
txt_dir = dataset_dir    # .gt.txt dosyaları burada
output_dir = os.path.join(dataset_dir, "lstmf_output")  # Çıktı klasörü

# Eğer lstmf_output klasörü yoksa oluştur
os.makedirs(output_dir, exist_ok=True)

# prepared_dataset klasöründeki tüm .tif dosyalarını işle
for filename in os.listdir(image_dir):
    if filename.endswith(".tif"):  # Sadece .tif dosyaları seç
        base_name = os.path.splitext(filename)[0]
        
        tif_file = os.path.join(image_dir, filename)
        box_file = os.path.join(box_dir, base_name + ".box")
        txt_file = os.path.join(txt_dir, base_name + ".gt.txt")
        lstmf_file = os.path.join(output_dir, base_name + ".lstmf")

        # Eğer hem .box hem .gt.txt dosyaları varsa devam et
        if os.path.exists(box_file) and os.path.exists(txt_file):
            print(f"📄 İşleniyor: {filename}")

            # Tesseract komutunu oluştur
            command = [
                "tesseract",
                tif_file,
                "training",
                "--psm", "6",
                "--oem", "1", 
                "lstm.train" 
            ]

            # Çıktıyı lstmf dosyasına yönlendir
            with open(lstmf_file, "wb") as f:
                subprocess.run(command, stdout=f, stderr=subprocess.DEVNULL)

            print(f"✅ {lstmf_file} oluşturuldu.")
        else:
            # Eksik dosyaları göster
            if not os.path.exists(box_file):
                print(f"⚠ Eksik .box dosyası: {box_file}")
            if not os.path.exists(txt_file):
                print(f"⚠ Eksik .gt.txt dosyası: {txt_file}")

print("\n✅ Tüm .lstmf dosyaları başarıyla oluşturuldu!")
