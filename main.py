import tkinter as tk
from app import WhiteNoiseApp


def main():
    root = tk.Tk()
    app = WhiteNoiseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
