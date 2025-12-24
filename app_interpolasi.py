import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- BAGIAN 1: LOGIKA METODE NUMERIK (ALGORITMA LAGRANGE) ---
def hitung_lagrange(x_points, y_points, x_target):
    """
    Menghitung nilai interpolasi menggunakan metode Lagrange secara manual.
    Ini adalah inti dari penerapan metode numerik tugas ini.
    """
    n = len(x_points)
    hasil = 0.0

    for i in range(n):
        term = y_points[i]
        for j in range(n):
            if i != j:
                term = term * (x_target - x_points[j]) / (x_points[i] - x_points[j])
        hasil += term
    
    return hasil

# --- BAGIAN 2: LOGIKA GUI (TAMPILAN) ---
def proses_interpolasi():
    try:
        # 1. Ambil data dari input user
        raw_x = entry_x.get()
        raw_y = entry_y.get()
        raw_target = entry_target.get()

        # 2. Parsing string ke list angka (float)
        x_data = [float(i) for i in raw_x.split(',')]
        y_data = [float(i) for i in raw_y.split(',')]
        x_target = float(raw_target)

        # Validasi panjang data
        if len(x_data) != len(y_data):
            messagebox.showerror("Error", "Jumlah data X dan Y harus sama!")
            return

        # 3. Jalankan Metode Numerik
        y_hasil = hitung_lagrange(x_data, y_data, x_target)

        # 4. Tampilkan Hasil Angka
        label_hasil.config(text=f"Hasil Estimasi (y): {y_hasil:.4f}")

        # 5. Tampilkan Grafik (Visualisasi)
        plot_grafik(x_data, y_data, x_target, y_hasil)

    except ValueError:
        messagebox.showerror("Error", "Pastikan input berupa angka dipisah koma.\nContoh: 6, 8, 10")

def plot_grafik(x_data, y_data, x_target, y_hasil):
    # Bersihkan grafik sebelumnya
    ax.clear()

    # Buat kurva halus untuk interpolasi
    # Kita buat 100 titik di antara min(x) dan max(x) agar garisnya melengkung bagus
    x_smooth = np.linspace(min(x_data), max(x_data), 100)
    y_smooth = [hitung_lagrange(x_data, y_data, val) for val in x_smooth]

    # Plot 1: Garis Kurva Interpolasi (Biru)
    ax.plot(x_smooth, y_smooth, 'b-', label='Kurva Lagrange')

    # Plot 2: Titik Data Asli (Hitam)
    ax.plot(x_data, y_data, 'ko', label='Data Diketahui')

    # Plot 3: Titik Hasil Prediksi (Merah Besar)
    ax.plot(x_target, y_hasil, 'ro', markersize=10, label='Hasil Estimasi')

    # Dekorasi Grafik
    ax.set_title("Visualisasi Interpolasi Lagrange")
    ax.set_xlabel("Sumbu X (Waktu/Jam)")
    ax.set_ylabel("Sumbu Y (Nilai/Suhu)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Refresh canvas agar gambar muncul
    canvas.draw()

# --- BAGIAN 3: SETUP JENDELA UTAMA ---
root = tk.Tk()
root.title("Aplikasi Interpolasi Lagrange - Tugas Metode Numerik")
root.geometry("800x600")

# Frame Input
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(side=tk.TOP, fill=tk.X)

# Input X
tk.Label(frame_input, text="Data X (pisahkan koma):").grid(row=0, column=0, sticky="w")
entry_x = tk.Entry(frame_input, width=40)
entry_x.grid(row=0, column=1, padx=5, pady=5)
entry_x.insert(0, "6, 8, 10, 12") # Default value

# Input Y
tk.Label(frame_input, text="Data Y (pisahkan koma):").grid(row=1, column=0, sticky="w")
entry_y = tk.Entry(frame_input, width=40)
entry_y.grid(row=1, column=1, padx=5, pady=5)
entry_y.insert(0, "24, 26, 29, 32") # Default value

# Input Target
tk.Label(frame_input, text="Cari nilai X:").grid(row=2, column=0, sticky="w")
entry_target = tk.Entry(frame_input, width=40)
entry_target.grid(row=2, column=1, padx=5, pady=5)
entry_target.insert(0, "9") # Default value

# Tombol Hitung
btn_hitung = tk.Button(frame_input, text="HITUNG & PLOT", command=proses_interpolasi, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_hitung.grid(row=3, column=1, pady=10, sticky="e")

# Label Output
label_hasil = tk.Label(frame_input, text="Hasil Estimasi (y): -", font=("Arial", 14, "bold"), fg="blue")
label_hasil.grid(row=4, column=0, columnspan=2, pady=10)

# Area Grafik (Matplotlib embedded in Tkinter)
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Jalankan Aplikasi
root.mainloop()