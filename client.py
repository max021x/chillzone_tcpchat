import os
import socket
import threading
from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox 
from PIL import ImageTk , Image
from setting import Setting

class GuiApp(Setting):
  _client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
  _Host_ip = socket.gethostbyname(socket.gethostname())
  _Host_port = 12345
  def __init__(self):
    super().__init__()
    self.root = Window(themename=self.theme)
    try:
      GuiApp._client.connect((GuiApp._Host_ip , GuiApp._Host_port))
      self.root.geometry(f'{self.sc_width}x{self.sc_hieght}')
      ch_th = threading.Thread(target=self.recieve)
      ch_th.start()
    except:
      Messagebox.show_error('Server error 😂😂😂😂')
      os._exit(1)
    self.root.mainloop()



  # All methods 
# ===========================================================================
    
  def recieve(self):
    self.chat_layout = Chatapp(root=self.root)
    while True:       
        message = GuiApp._client.recv(self.BYTESIZE).decode(self.ENCODER)
        if message == 'cls':
          self.chat_layout.canvas.delete(1.0,END)
        self.chat_layout.ltext(message)


class Chatapp(Setting):
  def __init__(self , root):
    super().__init__()
    # ====== Main frame ======
    self.root = root
    self.frame = Frame(self.root)
    self.frame.columnconfigure((0,1,2,3,4,5,6) , uniform='a' , weight=1)
    self.frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10) , uniform='a' , weight=1)
    self.frame.pack(expand=True , fill='both')
  

    # ====== Chat canvas ======
    self.chat = LabelFrame(self.frame,style='primary.TLabelFrame' , borderwidth=20 ,relief='solid')
    self.chat.columnconfigure((0,1,2,3),weight=1 , uniform='a')
    self.chat.rowconfigure((0,1,2,3,4,5,6,7,8,9,10) , weight=1, uniform='a')
    self.canvas = Text(self.chat , font='arial 20' , undo=True)
    self.ftable = Frame(self.canvas)
    self.ftable.columnconfigure((0,1),weight=1 , uniform='a')
    self.verticalscorlbar = Scrollbar(self.frame)
    self.canvas.config(yscrollcommand=self.verticalscorlbar.set ,highlightthickness=0)
    self.verticalscorlbar.config(command=self.canvas.yview , orient=tk.VERTICAL)
    self.verticalscorlbar.grid(row=0 , column=10  , rowspan=10, sticky='ns')
    self.canvas.pack(expand=1 , fill='both')
    self.chat.grid(row=0 , column=1 , sticky='nswe' , columnspan=6 ,rowspan=10 , pady=3 ,padx=1)
    
    # ===== Text Box Style =====
    self.Text_box = Text(self.frame,font='arial 20',undo=True ,wrap='word')
    self.Text_box.grid(row=10,column=2 ,sticky='snew',columnspan=4)  
   
    # ==== Key events ===== 
    self.root.bind('<Return>',self.write_usingkey)
    self.root.bind('<Shift-Return>',self.shift_enter_pressed)
    self.root.bind('<F1>', lambda x : self.canvas.yview_moveto('1.0'))
    self.root.bind('<Destroy>',self.disconnected)

  def disconnected(self , event):
    if event !=self.root:
      os._exit(1)

  def shift_enter_pressed(self,event):
    self.shift_enter = True
  
  def rtext(self ,message):
    self.canvas.insert(END , message+"\n")
    # self.update()
    
  def ltext(self,message):
    self.canvas.insert(END, message+"\n")
    # self.update()

  def moveto_end_of_chat(self):
      self.canvas.yview_moveto('1.0')

  def write_usingkey(self,event):
      try:
        message = self.Text_box.get("1.0",'end-2c')
        self.Text_box.delete("1.0",END)
        GuiApp._client.send(message.encode(self.ENCODER))
        self.moveto_end_of_chat()
      except:
        message = 'error:cant Handel Unicode'
        GuiApp._client.send(message.encode(self.ENCODER))

GuiApp()
