import os
import socket
import threading
from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox 
from PIL import ImageTk , Image
from pygame import mixer
from setting import Setting

class GuiApp(Setting):
  _client = None
  _Host_ip = None
  _Host_port = None
  _username = ''
  _password = ''

  def __init__(self ,condition,root):
    super().__init__()
    self.root = root
    self.music = MusicPlayer()
    self.frame = Frame(self.root)
    self.frame.pack()
    
    if condition == 'login':
      self.login()

    try:
      self.frame.pack(expand=1 , fill='both')
    except:
      os._exit(1)

  def login(self):
    # ==== Connect to The Server ====
    try:
      GuiApp._client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
      GuiApp._client.connect((GuiApp._Host_ip,GuiApp._Host_port))
      self.root.geometry('1400x900')
    except:
      Messagebox.show_error('Wrong Host_ip or Port')
      Server_Config(self.root)
      return
    self.root.bind('<Destroy>',self.disconnected)

    # ====== login thread =====
    login_thread = threading.Thread(target=self.recieve)
    login_thread.start()
  
  
  # All methods 
# ===========================================================================
  
  def disconnected(self , event):
    if event !=root:
      os._exit(1)
  

  
  def username_clicked(self,*args):
    if self.username_entry.get() == 'Enter Username':
      self.username_entry.config(state=tk.NORMAL,foreground='#fff')
      self.username_entry.delete(0,END)

  def password_clicked(self,*args):
    if self.password_entry.get() == 'Enter Password':
      self.password_entry.config(show='*' ,state=tk.NORMAL , foreground='#fff')
      self.password_entry.delete(0,END)
    

  def username_leave(self,*args):
    if self.username_entry.get() == '':
      self.username_entry.delete(0,END)
      self.username_entry.insert(0,'Enter Username')
      self.username_entry.config(state=tk.DISABLED, foreground='#a8a7a7')
    else:
      username = self.username_entry.get()
      self.username_entry.delete(0,END)
      self.username_entry.insert(0,username) 

  def password_leave(self,*args):
    if self.password_entry.get() == 'Enter Password' or self.password_entry.get() == '':
      self.password_entry.delete(0,END)
      self.password_entry.insert(0,'Enter Password')
      self.password_entry.config(show='' ,state=tk.DISABLED ,foreground='#a8a7a7')
      
    else:
      password = self.password_entry.get()
      self.password_entry.delete(0,END)
      self.password_entry.config(show='*' ,state=tk.NORMAL)
      self.password_entry.insert(0,password)


  def recieve(self):
    while True:
        message = GuiApp._client.recv(self.BYTESIZE).decode(self.ENCODER)
        if message == 'info':
          print(message)
          GuiApp._username = 'saeed'
          GuiApp._password = 'loopc'
          GuiApp._client.send(f"{GuiApp._username}:{GuiApp._password}".encode(self.ENCODER))
        elif message == 'enter':
          break
    self.frame.pack_forget()
    self.chat_layout = Chatapp(condition='chatapp' ,root=self.root)
    alert_message = f'{GuiApp._username}:joined the chat'
    GuiApp._client.send(alert_message.encode(self.ENCODER))
    while True:
      try:
        message = GuiApp._client.recv(self.BYTESIZE).decode(self.ENCODER)
        newmessage = message.split(":")
        if newmessage[0] != GuiApp._username:
          self.chat_layout.ltext(message)
        if int(self.chat_layout.verticalscorlbar.get()[1]) >= 0.8 :
          self.chat_layout.moveto_end_of_chat()
      except:
        message = 'error:Cant Handel Unicode'
        self.chat_layout.rtext(message)
        self.chat_layout.moveto_end_of_chat()



class Chatapp(GuiApp):
  def __init__(self,condition,root):
    GuiApp.__init__(self,condition,root)
    self.music = MusicPlayer()
    # ====== Main frame ======
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
    
    # ===== Send Button Style ====
    self.sendbtn_style = Style()
    self.sendbtn_style.configure('success.Outline.TButton',font=("arila",20),anchor='center')
    self.send_btn = Button(self.frame,text=f'📩',style='success.Outline.TButton',command=self.write_usingbtn)
    self.send_btn.grid(row=10 , column=6 ,sticky='nswe')
    
    # ===== Text Box Style =====
    self.Text_box = Text(self.frame,font='arial 20',undo=True ,wrap='word')
    self.Text_box.grid(row=10,column=2 ,sticky='snew',columnspan=4)  

    # ===== Mute Button Style ====
    self.mute_style = Style()
    self.mute_style.configure('danger.Outline.TButton',font=("arila",20),anchor='center')
    self.isclicked = False
    self.mute_button = Button(self.frame , text='🔊' , style='danger.Outline.TButton' , command= lambda:self.mute_btn(self.mute_button))
    self.mute_button.grid(row=10,column=1,sticky='nswe')
    
    # ==== Mouse-Wheel event and Updating Canvas width ===
    # self.canvas.bind('<Configure>' , self.width)
    # self.canvas.bind_all('<MouseWheel>',lambda event :self.canvas.yview_scroll(-int(event.delta/60),"units"))
    
    # ==== Key events ===== 
    self.root.bind('<Return>',self.write_usingkey)
    self.root.bind('<Shift-Return>',self.shift_enter_pressed)
    self.root.bind('<F1>', lambda x : self.canvas.yview_moveto('1.0'))
    self.root.bind('<Destroy>',self.disconnected)


  def mute_btn(self, button):
    if self.isclicked == False:
      self.isclicked = True
      mixer.music.set_volume(0)
      button.configure(text='🔇')
    else:
      self.isclicked = False
      mixer.music.set_volume(1)
      button.configure(text='🔊')


  def shift_enter_pressed(self,event):
    self.shift_enter = True

  def width(self,event):
    cc_width = event.width
    self.canvas.create_window(0,0,window=self.ftable , width=cc_width, anchor=tk.NW)
  
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
        GuiApp._client.send(f'{GuiApp._username}:{message}'.encode(self.ENCODER))
        self.rtext(message=message)
        self.moveto_end_of_chat()
      except:
        message = 'error:cant Handel Unicode'
        GuiApp._client.send(message.encode(self.ENCODER))
      

  def write_usingbtn(self):
    message = self.Text_box.get("1.0",'end-1c')
    self.Text_box.delete("1.0",END)
    GuiApp._client.send(f'{GuiApp._username}:{message}'.encode(self.ENCODER))
    self.rtext(message=message)
    self.moveto_end_of_chat()

  # def update(self):
  #   self.canvas.update_idletasks()
  #   self.canvas.config(scrollregion=self.ftable.bbox('all'))


class MusicPlayer:
  def __init__(self) -> None:
    self.mixer = mixer.init()
    self.all_musics =  []
    self.send_music = r'musics\tap-notification-180637.mp3'
    self.recieve_music = r'musics\livechat-129007.mp3'
    mixer.music.set_volume(1)

  def notif_sound(self,type):
    if type == 'send':
      mixer.music.load(self.send_music)
      mixer.music.play()
    else:
      mixer.music.load(self.recieve_music)
      mixer.music.play()



class Server_Config:
  def __init__(self , root) -> None:
    self.root = root
    self.root.geometry('500x300')
    self.host_port_ui()
    self.root.mainloop()


  def host_port_ui(self):
    self.config_frame = Frame(self.root)
    self.config_frame.columnconfigure((0,1,2,3),weight=1 , uniform='a')
    self.config_frame.rowconfigure((0,1,2,3),weight=1 , uniform='a')
    
    self.host_lbl = Label(self.config_frame , text='Host_name:' , font='arial 15')
    self.host_lbl.grid(row=0 ,column=0)

    self.ip_entry = Entry(self.config_frame ,font='15')
    self.ip_entry.grid(row=0 ,column=1 ,columnspan=2 ,sticky='ew')  
    
    self.port_lbl = Label(self.config_frame , text='Host_port:', font='aril 15')
    self.port_lbl.grid(row=1 , column=0)
    
    self.port_entry = Entry(self.config_frame ,font='15')
    self.port_entry.grid(row=1 ,column=1 ,columnspan=2 , sticky='ew')

    self.connect_btn = Button(self.config_frame , text='Connect' , padding=(10,10) ,command=self.connect)
    self.connect_btn.grid(row=2,column=1 ,columnspan=2)

    self.config_frame.pack(expand=1 , fill='both')


  def connect(self):
    self.ip = self.ip_entry.get()
    self.port = None
    try:
      self.port = int(self.port_entry.get())
    except:
      Messagebox.show_error('Please enter Integer like : 5050 for Port')

    if self.ip !=None and self.port !=None:
      GuiApp._Host_ip = self.ip
      GuiApp._Host_port = self.port
      self.config_frame.pack_forget()
      GuiApp(condition='login' , root=self.root)

    else:
      Messagebox.show_error('No valid HostIP or Port')
    


root = Window(themename='darkly')
app = Server_Config(root=root)
root.mainloop()
