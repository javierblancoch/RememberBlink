from win10toast import ToastNotifier
from threading import Thread
import tkinter as tk
import schedule
import random
import signal
import time
import os


messages = [
	"No olvides papadear", "Recuerda parpadear", "Paradea un momento"
]


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('RememberBlink')
		self.geometry('300x200')
		self.run = True
		self.limit = 3600

		self.label1 = tk.Label(self, text="Recordarme cada")
		self.label1.pack(pady=(20, 0))

		self.spinbox1 = tk.Spinbox(self, from_=1, to=self.limit, width=10)
		self.spinbox1["state"] = "readonly"
		self.spinbox1.pack(pady=(5, 5))

		self.label2 = tk.Label(self, text="segundos")
		self.label2.pack(pady=(0, 10))

		self.button1 = tk.Button(self, text='Iniciar')
		self.button1['command'] = self.start
		self.button1.pack(pady=(10, 10))

		self.button2 = tk.Button(self, text='Detener')
		self.button2['command'] = self.stop
		self.button2["state"] = tk.DISABLED
		self.button2.pack(pady=(0, 10))

	def start(self):
		self.run = True
		self.button1["state"] = tk.DISABLED
		self.button2["state"] = tk.NORMAL
		Thread(target=self.event).start()

	def event(self):
		val = int(self.spinbox1.get())
		schedule.every(val).seconds.do(notification)
		while self.run:
			schedule.run_pending()
			time.sleep(1)

	def stop(self):
		schedule.clear()
		self.run = False
		self.button1["state"] = tk.NORMAL
		self.button2["state"] = tk.DISABLED

def notification():
    toaster = ToastNotifier()
    toaster.show_toast("RememberBlink", random.choice(messages), duration=5)

def close():
	os.kill(os.getpid(), signal.SIGTERM)


if __name__ == "__main__":
	app = App()
	app.protocol("WM_DELETE_WINDOW", close)
	app.eval('tk::PlaceWindow . center')
	app.mainloop()