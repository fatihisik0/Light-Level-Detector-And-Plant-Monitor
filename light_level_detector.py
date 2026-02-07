import cv2  # OpenCV: Kamerayı açan ve görüntüyü işleyen ana kütüphane
import numpy as np  # NumPy: Matematiksel işlemler (Ortalama hesaplama) için
import matplotlib.pyplot as plt  # Matplotlib: Canlı grafik çizmek için
from collections import deque  # Deque: Verileri hafızada tutan kayan pencere (Eski veriyi siler, yeniyi ekler)
import time  # Zaman ölçümleri için

# --- PENCERE İSİMLERİ (Sabitler) ---
WIN_MAIN = "Plant Monitoring System (Quit: q)"
WIN_ROI = "Computer Vision (ROI)"
WIN_REPORT = "ANALYSIS REPORT"

# Grafik stilini ayarla
plt.style.use("seaborn-v0_8-darkgrid")
plt.ion()  # INTERACTIVE ON: Grafiğin kodu dondurmadan canlı akmasını sağlar

# --- Ayarlar ---
window_size = 100  # Grafikte gösterilecek son veri sayısı (Hafıza yönetimi)
light_levels = deque(maxlen=window_size) # Işık verilerini tutan liste
timestamps = deque(maxlen=window_size)   # Zaman verilerini tutan liste

required_light_threshold = 90  #"Bitki için gereken minimum ışık eşiği"
good_light_duration = 0        # Bitkinin verimli ışık aldığı toplam süreyi sayar

# Kamerayı başlat (0 genelde laptop kamerasıdır)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açilamadi!")
    exit()

# --- ADIM 1: ROI SEÇİMİ  ---
# "Tüm odayı değil, sadece bitkiyi analiz etmek için Region of Interest (İlgi Alanı) seçiyoruz."
ret, first_frame = cap.read()
if ret:
    print("\n--- SETUP ---")
    print("Bitkiyi secin ve ENTER'a basin.")
    # selectROI fonksiyonu fare ile kare çizmemizi sağlar
    r = cv2.selectROI("Target Selection", first_frame, showCrosshair=True, fromCenter=False)
    cv2.destroyWindow("Target Selection") # Seçim bitince pencereyi kapat
    
    # Seçilen alanın koordinatlarını alıyoruz (x, y, genişlik, yükseklik)
    roi_x, roi_y, roi_w, roi_h = int(r[0]), int(r[1]), int(r[2]), int(r[3])
    
    # Eğer seçim yapılmazsa tüm ekranı varsayıyoruz
    if roi_w == 0 or roi_h == 0:
        roi_x, roi_y, roi_w, roi_h = 0, 0, first_frame.shape[1], first_frame.shape[0]

# Zamanlayıcıları başlat
start_time = time.time()
last_time = time.time()
elapsed_time = 0

# --- Grafik Penceresini Hazırla ---
fig_live, ax_live = plt.subplots(figsize=(6, 3))
line_live, = ax_live.plot([], [], color="green", label="Plant Light") # Çizgi ayarı
ax_live.axhline(required_light_threshold, color="red", linestyle="--") # Kırmızı eşik çizgisi
ax_live.set_ylim(0, 255) # Işık değeri her zaman 0-255 arasındadır (8-bit görüntü)

# Pencereleri ekranda konumlandır (Üst üste binmesin diye)
cv2.namedWindow(WIN_MAIN)
cv2.namedWindow(WIN_ROI)
cv2.moveWindow(WIN_MAIN, 0, 0)      # Ana ekran sol üstte
cv2.moveWindow(WIN_ROI, 660, 0)     # ROI ekranı sağında

try:
    # --- SONSUZ DÖNGÜ (Canlı Analiz) ---
    while True:
        ret, frame = cap.read() # Kameradan anlık kareyi oku
        if not ret: break
        
        # Süre hesaplamaları (Döngü süresi farkını alıyoruz)
        current_time_abs = time.time()
        time_diff = current_time_abs - last_time
        last_time = current_time_abs
        elapsed_time = current_time_abs - start_time

        # --- ADIM 2: GÖRÜNTÜ İŞLEME (EN ÖNEMLİ KISIM) ---
        
        # 1. KESME İŞLEMİ (Slicing): Sadece seçilen kareyi alıyoruz.
        roi_frame = frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
        
        # 2. GRİ TONLAMAYA ÇEVİRME
        # HOCA SORARSA: "Renklerin (RGB) parlaklık hesabına etkisi yoktur, işlemciyi yormamak için griye çeviriyoruz."
        gray_roi = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
        
        # 3. PARLAKLIK HESAPLAMA (IŞIĞI ÖLÇEN KOD BURASI!)
        #"Piksellerin ortalama değerini (mean) alarak ortamın aydınlık seviyesini buluyorum."
        avg_brightness = np.mean(gray_roi)

        # --- ADIM 3: KARAR MEKANİZMASI (Algoritma) ---
        status = "IDEAL" if avg_brightness >= required_light_threshold else "LOW LIGHT!"
        color = (0, 255, 0) if status == "IDEAL" else (0, 0, 255) # Yeşil veya Kırmızı

        # Eğer ışık idealse süreyi sayacımıza ekliyoruz
        if status == "IDEAL":
            good_light_duration += time_diff

        # --- ADIM 4: GÖRSELLEŞTİRME (HUD) ---
        # Ana ekranda takip ettiğimiz bölgeyi kare içine alıyoruz
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), color, 2)
        
        # Bilgileri ekrana yazdırıyoruz (putText)
        cv2.putText(frame, f"Light: {avg_brightness:.1f}", (roi_x, roi_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, f"Optimal Light Duration: {good_light_duration:.1f} s", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
        cv2.putText(frame, status, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # --- GRAFİK GÜNCELLEME ---
        light_levels.append(avg_brightness) # Listeye yeni veriyi ekle
        timestamps.append(elapsed_time)     # Zamanı ekle
        line_live.set_xdata(timestamps)     # Grafiği güncelle
        line_live.set_ydata(light_levels)
        ax_live.relim()
        ax_live.autoscale_view()
        plt.pause(0.001) # Grafiğin çizilmesi için çok kısa bekle

        # Pencereleri göster
        cv2.imshow(WIN_MAIN, frame)
        cv2.imshow(WIN_ROI, roi_frame)

        # 'q' tuşuna basılırsa döngüyü kır
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

# --- TEMİZLİK (CLEANUP) ---
# Program kapanırken her şeyi temizliyoruz ki çökme olmasın
cap.release()              # Kamerayı serbest bırak
plt.close('all')           # Grafiği kapat
cv2.destroyAllWindows()    # Tüm pencereleri yok et
cv2.waitKey(1)             
time.sleep(0.5)            # Sisteme nefes aldır (Rapor ekranı açılmadan önce)

# --- RAPOR EKRANI OLUŞTURMA ---
print("Rapor oluşturuluyor...")

# Sıfıra bölünme hatasını önlemek için kontrol
if elapsed_time <= 0: elapsed_time = 0.1

# İstatistikleri hesapla
efficiency = (good_light_duration / elapsed_time) * 100
avg_light = np.mean(light_levels) if light_levels else 0
max_light = np.max(light_levels) if light_levels else 0
min_light = np.min(light_levels) if light_levels else 0

# Siyah boş bir tuval oluştur (Matris oluşturuyoruz)
report_card = np.zeros((400, 600, 3), dtype=np.uint8)
eff_color = (0, 255, 0) if efficiency > 50 else (0, 0, 255)

# Rapor üzerine yazıları yaz
cv2.putText(report_card, "--- ANALYSIS REPORT ---", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.line(report_card, (50, 70), (550, 70), (255, 255, 255), 2)

start_y = 120
spacing = 40
cv2.putText(report_card, f"Total Time: {elapsed_time:.1f} sn", (50, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
cv2.putText(report_card, f"Duration Time: {good_light_duration:.1f} sn", (50, start_y + spacing), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1)
cv2.putText(report_card, f"Duration: %{efficiency:.1f}", (50, start_y + spacing*2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, eff_color, 2)
cv2.putText(report_card, f"Avg Light: {avg_light:.1f} (Max: {max_light:.1f})", (50, start_y + spacing*3), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)

cv2.putText(report_card, "For Exit press to q...", (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
# Raporu göster
cv2.namedWindow(WIN_REPORT)
cv2.moveWindow(WIN_REPORT, 300, 150)
cv2.imshow(WIN_REPORT, report_card)

# Kullanıcı bir tuşa basana kadar bekle
cv2.waitKey(0)
cv2.destroyAllWindows()