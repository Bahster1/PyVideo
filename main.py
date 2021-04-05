from MainApplication import MainApplication
import tkinter as tk


def main():
    root = tk.Tk()
    app = MainApplication(root)
    app.configure(bg='black')
    root.wm_title('PyVideo')
    root.geometry('900x700')
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
