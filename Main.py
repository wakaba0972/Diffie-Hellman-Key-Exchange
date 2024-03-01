from tkinter import Tk
from widget import *

root=Tk()

root.resizable(0, 0)
#root.iconbitmap('Krito_Kun.ico')
root.title('Diffie–Hellman Key Exchange Emulator')

a=Cauculate_box(root)


w=root.winfo_screenwidth()
h=root.winfo_screenheight()
root.update()
x= (w-root.winfo_width())//2
y= (h-root.winfo_height())//2
root.geometry("+%d+%d" % (x, y-30))

a.start()
root.mainloop()
