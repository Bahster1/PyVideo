from app import App
import tkinter as tk


def main():
    root = tk.Tk()
    app = App(root)
    app.configure(bg='black')
    root.wm_title('PyVideo')
    root.geometry('900x700')
    root.mainloop()


if __name__ == '__main__':
    main()
