import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import yt_dlp
import time
import threading
from queue import Queue
from urllib.parse import urlparse
import re

class TikTokDownloader:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("TikTok Video Downloader - Batch Download")
        self.window.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Download queue
        self.download_queue = Queue()
        self.is_downloading = False
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="TikTok Video Downloader - Batch",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=10)
        
        # URLs TextArea Frame
        self.urls_frame = ctk.CTkFrame(self.main_frame)
        self.urls_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.urls_label = ctk.CTkLabel(
            self.urls_frame,
            text="Masukkan URL TikTok (satu URL per baris):",
            font=("Helvetica", 12)
        )
        self.urls_label.pack(anchor="w", padx=5, pady=5)
        
        self.urls_text = scrolledtext.ScrolledText(
            self.urls_frame,
            height=10,
            width=70,
            font=("Helvetica", 10)
        )
        self.urls_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(fill="x", padx=20, pady=10)
        
        self.paste_button = ctk.CTkButton(
            self.buttons_frame,
            text="Tempel URLs",
            command=self.paste_urls,
            width=120
        )
        self.paste_button.pack(side="left", padx=5)
        
        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="Hapus URLs",
            command=self.clear_urls,
            width=120
        )
        self.clear_button.pack(side="left", padx=5)
        
        # Download Location
        self.location_frame = ctk.CTkFrame(self.main_frame)
        self.location_frame.pack(fill="x", padx=20, pady=10)
        
        self.location_entry = ctk.CTkEntry(
            self.location_frame,
            placeholder_text="Lokasi penyimpanan...",
            width=600
        )
        self.location_entry.pack(side="left", padx=5)
        
        self.browse_button = ctk.CTkButton(
            self.location_frame,
            text="Pilih",
            width=70,
            command=self.browse_location
        )
        self.browse_button.pack(side="right", padx=5)
        
        # Status Frame
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        # Current download status
        self.current_label = ctk.CTkLabel(
            self.status_frame,
            text="Status: Siap",
            font=("Helvetica", 12)
        )
        self.current_label.pack(pady=5)
        
        # Progress Bars
        self.total_progress_label = ctk.CTkLabel(
            self.status_frame,
            text="Total Progress:",
            font=("Helvetica", 10)
        )
        self.total_progress_label.pack(pady=2)
        
        self.total_progress = ctk.CTkProgressBar(self.status_frame)
        self.total_progress.pack(fill="x", padx=5, pady=2)
        self.total_progress.set(0)
        
        self.current_progress_label = ctk.CTkLabel(
            self.status_frame,
            text="Current Video Progress:",
            font=("Helvetica", 10)
        )
        self.current_progress_label.pack(pady=2)
        
        self.current_progress = ctk.CTkProgressBar(self.status_frame)
        self.current_progress.pack(fill="x", padx=5, pady=2)
        self.current_progress.set(0)
        
        # Download Button
        self.download_button = ctk.CTkButton(
            self.main_frame,
            text="Mulai Download",
            command=self.start_batch_download,
            height=40,
            font=("Helvetica", 14, "bold")
        )
        self.download_button.pack(pady=20)
        
        # Log Frame
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_label = ctk.CTkLabel(
            self.log_frame,
            text="Log Unduhan:",
            font=("Helvetica", 12)
        )
        self.log_label.pack(anchor="w", padx=5, pady=2)
        
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            height=6,
            width=70,
            font=("Helvetica", 10)
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def paste_urls(self):
        """Tempel URLs dari clipboard"""
        try:
            clipboard_text = self.window.clipboard_get()
            current_text = self.urls_text.get("1.0", tk.END).strip()
            if current_text:
                self.urls_text.insert(tk.END, "\n" + clipboard_text)
            else:
                self.urls_text.insert(tk.END, clipboard_text)
        except:
            messagebox.showerror("Error", "Tidak dapat mengambil teks dari clipboard")
    
    def clear_urls(self):
        """Hapus semua URLs dari text area"""
        self.urls_text.delete("1.0", tk.END)
    
    def browse_location(self):
        """Buka dialog untuk memilih lokasi download"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, folder_path)
    
    def add_log(self, message):
        """Tambah pesan ke log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def is_valid_tiktok_url(self, url):
        """Validasi URL TikTok"""
        tiktok_patterns = [
            r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
            r'https?://(?:www\.)?vm\.tiktok\.com/\w+',
            r'https?://(?:www\.)?vt\.tiktok\.com/\w+'
        ]
        return any(re.match(pattern, url) for pattern in tiktok_patterns)
    
    def download_single_video(self, url, location, current_index, total_videos):
        """Unduh satu video TikTok"""
        try:
            self.current_label.configure(text=f"Mengunduh video {current_index + 1} dari {total_videos}")
            self.current_progress.set(0)
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', 0)
                    if total > 0:
                        # Update current video progress
                        progress = downloaded / total
                        self.current_progress.set(progress)
                        
                        # Update total progress
                        total_progress = (current_index + progress) / total_videos
                        self.total_progress.set(total_progress)
                elif d['status'] == 'finished':
                    self.current_progress.set(1)
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(location, '%(id)s.%(ext)s'),
                'progress_hooks': [progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = os.path.join(location, f"{info['id']}.{info['ext']}")
                self.add_log(f"✓ Berhasil mengunduh: {url}")
                return True
                
        except Exception as e:
            self.add_log(f"❌ Gagal mengunduh {url}: {str(e)}")
            return False
    
    def process_download_queue(self):
        """Proses antrian unduhan"""
        location = self.location_entry.get().strip()
        urls = [url.strip() for url in self.urls_text.get("1.0", tk.END).splitlines() if url.strip()]
        total_videos = len(urls)
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls):
            if self.is_valid_tiktok_url(url):
                if self.download_single_video(url, location, i, total_videos):
                    successful += 1
                else:
                    failed += 1
            else:
                self.add_log(f"❌ URL tidak valid: {url}")
                failed += 1
                
            # Update total progress
            self.total_progress.set((i + 1) / total_videos)
        
        self.current_label.configure(text="Download selesai!")
        self.add_log(f"\nDownload selesai!\nBerhasil: {successful}\nGagal: {failed}")
        self.download_button.configure(state="normal", text="Mulai Download")
        self.is_downloading = False
    
    def start_batch_download(self):
        """Mulai proses download batch"""
        if self.is_downloading:
            return
        
        location = self.location_entry.get().strip()
        urls = [url.strip() for url in self.urls_text.get("1.0", tk.END).splitlines() if url.strip()]
        
        if not urls:
            messagebox.showerror("Error", "Mohon masukkan URL TikTok")
            return
        if not location:
            messagebox.showerror("Error", "Mohon pilih lokasi penyimpanan")
            return
            
        self.is_downloading = True
        self.download_button.configure(state="disabled", text="Sedang Mengunduh...")
        self.log_text.delete("1.0", tk.END)
        self.total_progress.set(0)
        self.current_progress.set(0)
        
        # Mulai thread download
        download_thread = threading.Thread(target=self.process_download_queue)
        download_thread.daemon = True
        download_thread.start()
    
    def run(self):
        """Jalankan aplikasi"""
        self.window.mainloop()

if __name__ == "__main__":
    app = TikTokDownloader()
    app.run()