from gui import LibraryApp
import tkinter as tk
import database

def main():
    database.initialize_db()

    root = tk.Tk()
    
    app = LibraryApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()
 