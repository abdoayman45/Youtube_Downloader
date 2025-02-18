import tkinter as tk
from tkinter import scrolledtext, messagebox
import yt_dlp
import threading
import webbrowser

# إعدادات شريط التحميل
PROGRESS_BAR_WIDTH = 480  
PROGRESS_BAR_HEIGHT = 40  # حوالي 1 سم

# متغيرات للتحكم في التحميل العام
total_videos = 0           # عدد الفيديوهات الكلي
current_video_index = 0    # رقم الفيديو الحالي (من 0)
stop_downloading = False   # متغير لإيقاف التحميل عند الطلب
download_errors = False    # متغير لتحديد حدوث أخطاء أثناء التحميل

def update_progress(overall_progress):
    """
    تحديث شريط التقدم والنص الذي يظهر النسبة.
    overall_progress: قيمة بين 0 و 1.
    """
    new_width = overall_progress * PROGRESS_BAR_WIDTH
    progress_canvas.coords(progress_rect, 0, 0, new_width, PROGRESS_BAR_HEIGHT)
    # حذف النص السابق وإضافة النص الجديد
    progress_canvas.delete("progress_text")
    percentage = int(overall_progress * 100)
    progress_canvas.create_text(
        PROGRESS_BAR_WIDTH // 2,
        PROGRESS_BAR_HEIGHT // 2, 
        text=f"{percentage}%",
        fill="white",
        font=("Helvetica", 14, "bold"),
        tag="progress_text"
    )
    progress_canvas.update_idletasks()

def download_video_with_progress(url, video_index, total):
    """
    تحميل فيديو باستخدام yt_dlp مع استخدام progress hook لتحديث شريط التقدم.
    video_index: مؤشر الفيديو الحالي (من 0)
    total: العدد الكلي للفيديوهات
    """
    def progress_hook(d):
        # التحقق من طلب الإيقاف أثناء التحميل
        if stop_downloading:
            raise Exception("StopDownload")
        if d['status'] == 'downloading':
            # الحصول على نسبة تحميل الفيديو الحالي
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                video_progress = d.get('downloaded_bytes', 0) / total_bytes
            else:
                video_progress = 0
            # النسبة الكلية = نسبة الفيديوهات السابقة + نسبة تحميل الفيديو الحالي
            overall = (video_index + video_progress) / total
            root.after(0, update_progress, overall)
        elif d['status'] == 'finished':
            # عند الانتهاء من الفيديو، نحدث النسبة لتصبح الفيديو مكتمل
            overall = (video_index + 1) / total
            root.after(0, update_progress, overall)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',          # تحميل أفضل فيديو مع أفضل صوت ودمجهما
        'merge_output_format': 'mp4',                   # صيغة الدمج الناتجة
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0.0.0 Safari/537.36',    # يوزر اجينت لمحاكاة متصفح حقيقي 
        'progress_hooks': [progress_hook],
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        if str(e) == "StopDownload":
            # إذا كان سبب الإيقاف من المستخدم فلا نقوم بإظهار رسالة خطأ
            return
        else:
            global download_errors
            download_errors = True
            print(f"Error occurred while loading {url}: {str(e)}")

def download_all(urls):
    """
    تحميل جميع الفيديوهات وتحديث شريط التقدم بشكل تدريجي.
    """
    global total_videos
    total_videos = len(urls)
    for index, url in enumerate(urls):
        if stop_downloading:
            break
        clean_url = url.strip()
        if clean_url:
            print(f"Loading: {clean_url}")
            try:
                download_video_with_progress(clean_url, index, total_videos)
            except Exception as e:
                if str(e) == "StopDownload":
                    break
                else:
                    global download_errors
                    download_errors = True
                    print(f"Error occurred while loading {clean_url}: {str(e)}")
    def show_done():
        progress_canvas.delete("progress_text")
        if stop_downloading:
            progress_canvas.create_text(
                PROGRESS_BAR_WIDTH // 2,
                PROGRESS_BAR_HEIGHT // 2, 
                text="Download Stopped.\nتم إيقاف التحميل.",
                fill="white",
                font=("Helvetica", 12, "bold"),
                tag="progress_text"
            )
        elif download_errors:
            progress_canvas.create_text(
                PROGRESS_BAR_WIDTH // 2,
                PROGRESS_BAR_HEIGHT // 2, 
                text="Some videos failed to download.\nفشل تحميل بعض الفيديوهات.",
                fill="white",
                font=("Helvetica", 12, "bold"),
                tag="progress_text"
            )
        else:
            progress_canvas.create_text(
                PROGRESS_BAR_WIDTH // 2,
                PROGRESS_BAR_HEIGHT // 2, 
                text="All videos were successfully uploaded.\nتم تحميل جميع الفيديوهات بنجاح.",
                fill="white",
                font=("Helvetica", 12, "bold"),
                tag="progress_text"
            )
        # إعادة تفعيل زر التحميل وإلغاء تفعيل زر التوقف بعد الانتهاء
        download_button.config(state=tk.NORMAL, text="Download Videos")
        stop_button.config(state=tk.DISABLED)
    root.after(0, show_done)
    if stop_downloading:
        messagebox.showinfo("Download stopped", "Download process has been stopped.\nتم إيقاف عملية التحميل.")
    elif download_errors:
        messagebox.showerror("Download error", "Some videos failed to download. Please check the terminal for details.\nفشل تحميل بعض الفيديوهات. يرجى مراجعة التيرمينال للتفاصيل.")
    else:
        messagebox.showinfo("Upload completed", "All videos were successfully uploaded.\nتم تحميل جميع الفيديوهات بنجاح.")

def start_download():
    """
    قراءة الروابط من واجهة المستخدم وبدء عملية التحميل في خيط منفصل.
    """
    urls = text_area.get("1.0", tk.END).splitlines()
    # إزالة الفراغات من كل سطر
    valid_urls = [url.strip() for url in urls if url.strip() != ""]
    if not valid_urls:
        messagebox.showwarning("Attention!", "Please enter at least one link.")
        return

    # التحقق من أن كل رابط هو رابط يوتيوب
    for url in valid_urls:
        if "youtube.com" not in url and "youtu.be" not in url:
            messagebox.showerror("Error", "يجب كتابة روابط يوتيوب فقط")
            return

    # إعادة تعيين شريط التقدم وتفعيل التحميل
    progress_canvas.delete("all")
    global progress_rect, stop_downloading, download_errors
    progress_rect = progress_canvas.create_rectangle(0, 0, 0, PROGRESS_BAR_HEIGHT, fill="green", width=0)
    update_progress(0)
    stop_downloading = False
    download_errors = False  # إعادة تعيين متغير الأخطاء قبل بدء عملية التحميل

    # تعطيل زر التحميل وتغيير نصه وتفعيل زر التوقف
    download_button.config(state=tk.DISABLED, text="Downloading...")
    stop_button.config(state=tk.NORMAL)
    # بدء التحميل في خيط منفصل
    threading.Thread(target=download_all, args=(valid_urls,), daemon=True).start()

def stop_download():
    """
    دالة لتعيين متغير الإيقاف بحيث يتم وقف التحميل.
    """
    global stop_downloading
    stop_downloading = True
    # تعطيل زر التوقف عند الضغط عليه
    stop_button.config(state=tk.DISABLED)

def open_github():
    """
    فتح صفحة GitHub عند الضغط على الزر.
    """
    webbrowser.open("https://github.com/abdoayman45")

# إنشاء نافذة التطبيق
root = tk.Tk()
root.title("Youtube Downloader")

# منطقة النص لإدخال الروابط وشريط التقدم
label = tk.Label(root, text="Enter YouTube video links (link in each line):\nأدخل روابط فيديوهات يوتيوب (رابط في كل سطر):")
label.pack(pady=5)

text_area = scrolledtext.ScrolledText(root, width=60, height=20)
text_area.pack(pady=5)

progress_canvas = tk.Canvas(root, width=PROGRESS_BAR_WIDTH, height=PROGRESS_BAR_HEIGHT, bg="lightgray")
progress_canvas.pack(pady=5)
progress_rect = progress_canvas.create_rectangle(0, 0, 0, PROGRESS_BAR_HEIGHT, fill="green", width=0)

# إطار علوي يحتوي على زري "Download Videos" و"Stop Download" في المنتصف
top_button_frame = tk.Frame(root)
top_button_frame.pack(pady=10)

download_button = tk.Button(top_button_frame, text="Download Videos", command=start_download)
download_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(top_button_frame, text="Stop Download", command=stop_download, state=tk.DISABLED)
stop_button.grid(row=0, column=1, padx=5)

# إطار سفلي يحتوي على عبارة "Created by: Abdelrhaman" وزر "GITHUB" في المنتصف
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

created_label = tk.Label(bottom_frame, text="Created by: Abdelrhaman", font=("Helvetica", 10))
created_label.pack()

github_button = tk.Button(bottom_frame, text="GITHUB", command=open_github, 
                          bg="#24292e", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
github_button.pack(pady=(5,0))

# بدء الحلقة الرئيسية للواجهة
root.mainloop()
