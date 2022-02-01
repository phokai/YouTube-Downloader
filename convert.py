from PyQt6 import uic
# dönüştürülecek ui dosyasına verilecek dosya adı
with open('design.py', 'w', encoding="utf-8") as fout:
    uic.compileUi('design.ui', fout)     # ui dosyasını seç
