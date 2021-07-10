import tkinter as tk

class PopupWindow(tk.Frame):
    def __init__(self, master):
        super(PopupWindow, self).__init__(master)
        self.pack()

'''
window=tk.Tk()
window.title('alarm')
window.geometry()
window.resizable(False, False)

#1. 눈깜빡임 횟수가 1분에 15회 이하면 알람띄워주기

blink_alarm_text=tk.Label(window, text='Blink_alarm : ')
blink_alarm=tk.Label(window, text='Blinks too few times!\nBlink more often:)', fg='red')
blink_alarm.place(x=0,y=0)
blink_alarm.place(x=100, y=0)
blink_alarm.after(1000, blink_alarm.destroy)

#2. 자세 알람

#3. 작업시간측정

window.mainloop()
'''