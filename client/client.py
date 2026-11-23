import platform,socket,threading,tkinter as tk
from tkinter import messagebox
import requests
class Client:
 def __init__(self,root):
  self.root=root;root.title("TOKER CONTROL — клиент");root.geometry("420x290");self.running=False;self.session=requests.Session()
  tk.Label(root,text="TOKER CONTROL",fg="#ff4fa3",font=("Consolas",18,"bold")).pack(pady=15)
  tk.Label(root,text="Видимый клиент статуса устройства").pack()
  tk.Label(root,text="URL сервера").pack();self.url=tk.Entry(root,width=48);self.url.insert(0,"https://your-service.onrender.com");self.url.pack()
  tk.Label(root,text="Токен подключения").pack(pady=(10,0));self.token=tk.Entry(root,width=48,show="*");self.token.pack()
  self.status=tk.Label(root,text="Отключён",fg="red");self.status.pack(pady=12)
  self.btn=tk.Button(root,text="Подключить",command=self.connect);self.btn.pack()
  tk.Label(root,text="Отправка статуса начинается только после нажатия кнопки.").pack(pady=12)
  root.protocol("WM_DELETE_WINDOW",self.close)
 def connect(self):
  base=self.url.get().strip().rstrip("/");secret=self.token.get().strip()
  if not base.startswith(("http://","https://")) or not secret: messagebox.showerror("Ошибка","Укажите URL и токен.");return
  try:
   r=self.session.post(base+"/api/register",headers={"X-Enrollment-Token":secret},json={"name":socket.gethostname(),"platform":platform.system()},timeout=10);r.raise_for_status()
   self.device_id=r.json()["device_id"];self.base=base;self.running=True;self.btn.config(text="Отключить",command=self.disconnect);self.status.config(text="Подключён",fg="green");threading.Thread(target=self.loop,daemon=True).start()
  except Exception as e: messagebox.showerror("Ошибка подключения",str(e))
 def loop(self):
  while self.running:
   try:
    self.session.post(self.base+"/api/heartbeat",json={"device_id":self.device_id},timeout=10).raise_for_status();self.root.after(0,lambda:self.status.config(text="Подключён — связь активна",fg="green"))
   except Exception: self.root.after(0,lambda:self.status.config(text="Нет связи — повторная попытка",fg="orange"))
   for _ in range(20):
    if not self.running:break
    threading.Event().wait(1)
 def disconnect(self):
  self.running=False;self.status.config(text="Отключён",fg="red");self.btn.config(text="Подключить",command=self.connect)
 def close(self): self.disconnect();self.root.destroy()
if __name__=="__main__":
 root=tk.Tk();Client(root);root.mainloop()
