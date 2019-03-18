from tkinter import *
from download import download_to_file


def let():
    download_to_file(url.get(), filename.get())


r = Tk()
r.title('Quandl downloader')
Label(r, text='URL').grid(row=0)
Label(r, text='File Name').grid(row=3)
url = Entry(r)
filename = Entry(r)
url.grid(row=0, column=1)
filename.grid(row=3, column=1)
button = Button(r, text='Download', width=25, command=let)
button.grid(row=5)
r.mainloop()

