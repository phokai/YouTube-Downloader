import os
import sys
import threading
import youtube_dl
from design import *
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
frame = QWidget()
ui = Ui_Form()
ui.setupUi(frame)
frame.show()


def musicDownload():
    global musicThread
    musicThread = threading.Thread(target=musicInstall)
    musicThread.start()


def videoDownload():
    global videoThread
    videoThread = threading.Thread(target=videoInstall)
    videoThread.start()


def musicPath():
    global m_path_status
    try:
        m_path = QtWidgets.QFileDialog.getExistingDirectory()
        os.chdir(m_path)
        ui.m_path_src.setText(m_path)
        ui.m_info.setText("Folder path selected.")
        m_path_status = True

    except:
        m_path_status = False
        ui.m_info.setText("Error choosing file path!")


def videoPath():
    global v_path_status
    try:
        v_path = QtWidgets.QFileDialog.getExistingDirectory()
        os.chdir(v_path)
        ui.v_path_src.setText(v_path)
        ui.v_info.setText("Folder path selected.")
        v_path_status = True

    except:
        v_path_status = False
        ui.v_info.setText("Error choosing file path!")


def musicInstall():
    if len(ui.m_link.text()) < 5:
        ui.m_info.setText("A link has not been entered!")
    else:
        try:
            if m_path_status == True:
                try:
                    music_url = ui.m_link.text()
                    music_info = youtube_dl.YoutubeDL().extract_info(url=music_url, download=False)
                    file_name = f"{music_info['title']}.mp3"
                    settings = {
                        'format': 'bestaudio/best',
                        'keepvideo': False,
                        'outtmpl': file_name,
                        'progress_hooks': [pHook],
                    }
                    ui.m_info.setText("Music download started.")
                    with youtube_dl.YoutubeDL(settings) as ydl:
                        ydl.download([music_info['webpage_url']])
                    musicThread.append(musicThread)
                except:
                    ui.m_info.setText("The link entered is incorrect!")
                finally:
                    ui.m_info.setText("Music downloaded.")
        except:
            ui.m_info.setText("You didn't specify a download path!")


def videoInstall():
    if len(ui.v_link.text()) < 5:
        ui.v_info.setText("A link has not been entered!")
    else:
        try:
            if v_path_status == True:
                try:
                    video_url = ui.v_link.text()
                    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
                    # file_name = f"{video_info['title']}.mp4"
                    ydl_opts = {'progress_hooks': [pHook]}
                    ui.v_info.setText("Video download started.")
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    videoThread.append(videoThread)
                except:
                    ui.v_info.setText("The link entered is incorrect!")
                finally:
                    ui.v_info.setText("Video downloaded.")
        except:
            ui.v_info.setText("You didn't specify a download path!")


def pHook(d):
    if d['status'] == 'downloading':
        percentage = int(float(d['_percent_str'].strip()[:-1]))
        ui.progressBar.setValue(percentage)
    elif d['status'] == 'finished':
        ui.progressBar.setValue(100)


""" __________________________________________________ """
ui.m_path_button.clicked.connect(musicPath)
ui.v_path_button.clicked.connect(videoPath)
ui.m_download_button.clicked.connect(musicDownload)
ui.v_download_button.clicked.connect(videoDownload)

sys.exit(app.exec())
