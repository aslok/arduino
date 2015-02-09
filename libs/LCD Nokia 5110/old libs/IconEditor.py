# -*- coding: utf-8 -*-
from Tkinter import *

W, H = 84, 48

def hexf(x):
  return hex(x)[2:].upper().rjust(2, "0")

class Application(Frame):
  def __init__(self, master = None):
    Frame.__init__(self, master)
    self.pack()
    self.canvas = Canvas(self, width = 588, height = 336, highlightthickness = 0)
    self.canvas.bind("<Button-1>", self.click)
    self.canvas.pack(padx = 5, pady = 5)
    frame = Frame(self)
    frame.pack()
    Label(frame, text = "Width:").pack(padx = 5, pady = 5, side = LEFT)
    self.sw = Spinbox(frame, values = [i for i in xrange(W, 0, -1)], width = 4, state = "readonly")
    self.sw.pack(padx = 5, pady = 5, side = LEFT)
    Label(frame, text = "Height:").pack(padx = 5, pady = 5, side = LEFT)
    self.sh = Spinbox(frame, values = [i for i in xrange(H, 0, -1)], width = 4, state = "readonly")
    self.sh.pack(padx = 5, pady = 5, side = LEFT)
    Button(frame, text = "Apply", command = self.resize).pack(padx = 5, pady = 5, side = LEFT)
    frame = Frame(self)
    frame.pack(padx = 5, fill = X)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side = RIGHT, fill = Y)
    self.text = Text(frame, font = ('times', 12), width = 50, height = 5, wrap = WORD, yscrollcommand = scrollbar.set)
    self.text.pack(fill = X)
    scrollbar.config(command = self.text.yview)
    frame = Frame(self)
    frame.pack()
    Button(frame, text = "Load", command = self.load).pack(padx = 5, pady = 5, side = LEFT)
    Button(frame, text = "Save", command = self.save).pack(padx = 5, pady = 5, side = LEFT)
    self.area, self.pix = [], []
    self.w, self.h, self.l = W, H, (W+7)/8
    for y in xrange(H):
      for x in xrange(W):
        self.area.append(self.canvas.create_rectangle(x*7, y*7, x*7+6, y*7+6, fill = "white", width = 0))
        self.pix.append(0)

  def load(self):
    txt = self.text.get('1.0', END)
    txt = txt.strip()
    if not txt:
      return
    self.text.delete('1.0', END)
    try:
      txt += ","
      txt = eval("(%s)"%txt)
      txt = [bin(i)[2:].rjust(8, "0") for i in txt]
    except:
      print "wrong byte array format"
      return
    if len(txt) != self.h*self.l:
      print "wrong byte array lenght"
      return
    for x, y, xx, yy, index, tag in self.walk():
      bit = txt[yy*self.l+xx/8][xx%8]
      self.pix[index] = int(bit)
      color = "black" if self.pix[index] else "white"
      self.canvas.itemconfig(tag, state = NORMAL, fill = color)

  def walk(self):
    index = 0
    for y in xrange(H):
      for x in xrange(W):
        tag = self.area[index]
        if ((x < (W-self.w)/2.0) or (x >= (W-self.w)/2.0+self.w)) or ((y < (H-self.h)/2.0) or (y >= (H-self.h)/2.0+self.h)):
          self.canvas.itemconfig(tag, state = HIDDEN)
        else:
          xx, yy = x-int((W-self.w)/2.0+0.5), y-int((H-self.h)/2.0+0.5)
          yield x, y, xx, yy, index, tag
        index += 1


  def save(self):
    self.text.delete('1.0', END)
    txt = [["0", "0", "0", "0", "0", "0", "0", "0"] for i in xrange(self.h*self.l)]
    for x, y, xx, yy, index, tag in self.walk():
      txt[yy*self.l+xx/8][xx%8] = str(self.pix[index])
    txt = [int("".join(i), 2) for i in txt]
    txt = ["0x%s"%hexf(i) for i in txt]
    tmp = []
    for i in xrange(0, len(txt), self.l):
      tmp.append(", ".join(txt[i:i+self.l]))
    txt = ",\n".join(tmp)
    self.text.insert('1.0', txt)

  def resize(self):
    w, h = int(self.sw.get()), int(self.sh.get())
    if self.w == w and self.h == h:
      return
    self.w, self.h, self.l = w, h, (w+7)/8
    for x, y, xx, yy, index, tag in self.walk():
      self.canvas.itemconfig(tag, state = NORMAL, fill = "white")
      self.pix[index] = 0

  def click(self, event):
    tag = self.canvas.find_withtag(CURRENT)
    if not tag:return
    tag = tag[0]
    if self.canvas.type(tag) == "rectangle" and tag in self.area:
      index = self.area.index(tag)
      color = "white" if self.pix[index] else "black"
      self.canvas.itemconfig(tag, fill = color)
      self.pix[index] ^= 1


root = Tk()
app = Application(master = root)
app.master.title("Icon Editor")
app.master.resizable(width = FALSE, height = FALSE)
app.mainloop()