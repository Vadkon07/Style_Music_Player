import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from tkinter import ttk

root = Tk()
root.geometry("480x250")
root.title("Simple Music Player")
root.config(bg='#000000')
root.resizable(False, False)
mixer.init()

lbl = Label(root)
lbl.place(x=0, y=0)

def update(ind):
   frame = frms[ind]
   ind += 1
   if ind == frmcount:
       ind = 0
   lbl.config(image=frame)
   root.after(40, update, ind)

def addMusic():
   path = filedialog.askdirectory()
   if path:
       os.chdir(path)
       songs = os.listdir(path)

       for song in songs:
           if song.endswith(".mp3"):
               Playlist.insert(END, song)

def playMusic():
    global current_song_path
    music_name = Playlist.get(ACTIVE)
    current_song_path = os.path.join(os.getcwd(), music_name)
    print(music_name[0:-4])
    mixer.music.load(current_song_path)
    mixer.music.play()

def set_volume(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

def update_slider():
    if mixer.music.get_busy():
        pos = mixer.music.get_pos() / 1000
        length = mixer.music.get_length()
        position_slider.set((pos / length) * 100)
    root.after(1000, update_slider)


frm_music = Frame(root, bd=2, relief=RIDGE, width=485, height=100)
frm_music.place(x=0, y=10)

btn_p = Button(root, text="Play", fg="White", bg='#0f0f0f', height=2, width=10, command=playMusic)
btn_p.place(x=40, y=130)

btn_s = Button(root, text="Stop", fg="White", bg='#0f0f0f', height=2, width=10, command=mixer.music.stop)
btn_s.place(x=130, y=130)

btn_v = Button(root, text="Unpause", fg="White", bg='#0f0f0f', height=2, width=10, command=mixer.music.unpause)
btn_v.place(x=210, y=130)

btn_ps = Button(root, text="Pause", fg="White", bg='#0f0f0f', height=2, width=10, command=mixer.music.pause)
btn_ps.place(x=300, y=130)

btn_browse = Button(root, text="Browse Music", font=('Arial,bold', 14), fg="White", bg="#000000", width=45, command=addMusic)
btn_browse.place(x=0, y=210)

volume_slider = ttk.Scale(root, from_=100, to=0, orient='vertical', command=set_volume)
volume_slider.set(50)
volume_slider.pack(pady=50)
volume_slider.place(x=450, y=90)

Scroll = Scrollbar(frm_music)
Playlist = Listbox(frm_music, width=100, font=('Arial,bold', 12), bg='#000000', fg='#00ff00', selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)

#mixer.music.play(-1)
update_slider()

root.after(0, update, 0)
root.mainloop()

