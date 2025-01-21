import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime, timedelta

class LibraryApp:

    # Constructor method
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")

        

        self.root.withdraw()

        self.user_id = None
        self.is_admin = False
        self.tab_control = None
        self.user_tab = None
        self.admin_tab = None

        self.login_window()

    # Differentiates user and admin tabs
    # If login is user only user tab is displayed
    # Else both user and admin tabs are displayed
    def setup_tabs(self):

        tab_control = ttk.Notebook(self.root)
        self.tab_control = tab_control

        self.user_tab = ttk.Frame(self.tab_control)
        self.admin_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.user_tab, text = "User")

        if self.is_admin:
            self.tab_control.add(self.admin_tab, text = "Admin")

        self.tab_control.pack(expand = 1, fill = "both")

        self.setup_user_tab()
        if self.is_admin:
            self.setup_admin_tab()

        

    #tkinter method for user tab
    #takes search_entry for search bar
    #initializes all buttons and listbox interfaces on user tab
    # calls display all books method to show books list
    def setup_user_tab(self):
        label = tk.Label(self.user_tab, text = "Welcome to the Library!", font = ("Arial", 16))
        label.pack(pady = 10)

        search_label = tk.Label(self.user_tab, text = "Search for a Book: ")
        
        search_label.pack()
        self.search_entry = tk.Entry(self.user_tab, width = 30)
        self.search_entry.pack(pady=5)

        search_button = tk.Button(self.user_tab, text = "Search", command = self.search_books)
        search_button.pack()

        self.favorites_label = tk.Label(self.user_tab, text ="Our Favorites", font = ("Arial", 14))
        self.favorites_label.pack(pady=10)


        self.search_results = tk.Listbox(self.user_tab, width = 50, height = 10)
        self.search_results.pack(pady=10)
        

        self.checkout_button = tk.Button(self.user_tab, text = "Checkout", command = self.checkout_book, state = tk.DISABLED)
        self.checkout_button.pack(pady = 5)

        my_books_label = tk.Label(self.user_tab, text = "My Checked Out Books: ")
        my_books_label.pack(pady=10)

        self.my_books_listbox = tk.Listbox(self.user_tab, width = 50, height = 10)
        self.my_books_listbox.pack(pady=5)

        self.search_results.bind('<<ListboxSelect>>', self.enable_checkout_button)

        self.return_button = tk.Button(self.user_tab, text = "Return Book", command = self.return_book, state = tk.DISABLED)
        self.return_button.pack(pady=5)

        self.my_books_listbox.bind('<<ListboxSelect>>', self.enable_return_button)

        self.display_all_books()
    


    # Initializes admin tab
    # Displays add book button, view books button and generate report button
    def setup_admin_tab(self):
        label = tk.Label(self.admin_tab, text = "Admin Panel", font = ("Arial", 16))
        label.pack(pady=10)

        add_book_button = tk.Button(self.admin_tab, text = "Add Book", command = self.add_book_window)
        add_book_button.pack(pady=5)

        view_books_button = tk.Button(self.admin_tab, text="View Books", command = self.view_books_window)
        view_books_button.pack(pady=5)

        generate_report_button = tk.Button(self.admin_tab, text = "Generate Report", command = self.generate_report)
        generate_report_button.pack(pady=5)


    #Initializes window to view all books available in Books table
    def view_books_window(self):
        self.books_window = tk.Toplevel(self.root)
        self.books_window.title("Book List")
        self.books_window.geometry("400x400")

        books_frame = tk.Frame(self.books_window)
        books_frame.pack(fill=tk.BOTH, expand = True)

        self.books_listbox = tk.Listbox(books_frame, width=50, height=20, selectmode=tk.SINGLE)
        self.books_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)

        books_scrollbar = tk.Scrollbar(books_frame)
        books_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_listbox.config(yscrollcommand=books_scrollbar.set)
        books_scrollbar.config(command=self.books_listbox.yview)

        self.fetch_books()

        delete_button = tk.Button(self.books_window, text="Delete Book", command=self.delete_selected_book)
        delete_button.pack(pady=5)


    # Queries Books table to return all books available
    def fetch_books(self):
        try:
            books = database.fetch_query("SELECT book_id, title, author FROM Books")
            self.books_listbox.delete(0,tk.END)
            for book_id, title, author in books:
                self.books_listbox.insert(tk.END, f"{book_id}: {title} by  {author}")
        except Exception as e:
            print(f"Error fetching books: {e}")
            messagebox.showerror("Error", "An unexpected error occured while fetching the book list")


    # Method to delete selected books in view books window
    # Only available in the admin tab
    def delete_selected_book(self):
        try:
            selection = self.books_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a book to delete")
                return
            selected_book = self.books_listbox.get(selection[0])
            book_id = selected_book.split(":")[0]

            database.execute_query("DELETE FROM Books WHERE book_id =?", (book_id,))
            messagebox.showinfo("Success", "Book deleted successfully")

            self.fetch_books()
        except Exception as e:
            print(f"Error deleting book: {e}")
            messagebox.showerror("Error", "An unexpected error occured while deleting the book.")


    # Selects searched books that are like a book in Books table
    # Displays searched book
    def search_books(self):
        if self.favorites_label.winfo_ismapped():
            self.favorites_label.pack_forget()


        query = self.search_entry.get().strip()
        results = database.fetch_query("SELECT book_id, title, author FROM Books WHERE title LIKE ?", ('%' + query + '%',))
        self.books = results
        self.search_results.delete(0,tk.END)



        for book_id, title, author in results:
            self.search_results.insert(tk.END, f"{title} by {author}")


    # Initializes login window
    # Has buttons to login and register
    # Register button launches the register window
    def login_window(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("Login")
        login_win.geometry("300x300")

        login_win.grab_set()

        tk.Label(login_win, text = "Username: ").pack(pady=5)
        username_entry = tk.Entry(login_win)
        username_entry.pack(pady=5)

        tk.Label(login_win, text = "Password: ").pack(pady=5)
        password_entry = tk.Entry(login_win, show = "*")
        password_entry.pack(pady=5)

        # Confirms that user information is correct in Users database
        def authenticate_user():
            username= username_entry.get().strip()
            password = password_entry.get().strip()

            user = database.fetch_query(
                "SELECT user_id, is_admin FROM Users WHERE username = ? AND password = ?",
                (username, password)
            )

            if user:
                user_id, is_admin = user[0]
                self.user_id = user_id
                self.is_admin = is_admin
                login_win.destroy()
                self.root.state("zoomed")
                self.root.deiconify()
                self.setup_tabs()
                self.fetch_checked_out_books()
                
            else:
                messagebox.showerror("Error", "Invalid username or password")
        tk.Button(login_win, text = "Login", command = authenticate_user).pack(pady=10)
        tk.Button(login_win, text="Register", command=self.register_window).pack(pady=5)

    # Helper method to hide admin tab from regular users
    def show_tabs_based_on_role(self):
        if self.is_admin:
            self.admin_tab.pack(fill="both", expand=1)
        else:
            self.tab_control.forget(self.admin_tab)

    # Displays books on user page
    # Queries Books table
    def display_all_books(self):

        books = database.fetch_query("SELECT book_id, title, author FROM Books")
        self.search_results.delete(0,tk.END)
        self.books= books

        for book_id, title, author in books:
            self.search_results.insert(tk.END, f"{title} by {author}" )


    # Intializes window to add a book in the admin tab
    # Allows admins to enter book title, author, isbn and number of copies
    def add_book_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Add Book")
        self.window.geometry("300x300")

        title_label = tk.Label(self.window, text = "Title: ")
        title_label.pack()
        self.title_entry = tk.Entry(self.window)
        self.title_entry.pack()

        author_label = tk.Label(self.window, text = "Author: ")
        author_label.pack()
        self.author_entry = tk.Entry(self.window)
        self.author_entry.pack()

        isbn_label = tk.Label(self.window, text = "ISBN: ")
        isbn_label.pack()
        self.isbn_entry = tk.Entry(self.window)
        self.isbn_entry.pack()

        copies_label = tk.Label(self.window, text = "Copies: ")
        copies_label.pack()
        self.copies_entry = tk.Entry(self.window)
        self.copies_entry.pack()

        # Saves added book within the Books table
        # Ensures that copies is a positive value
        def save_book():
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            isbn = self.isbn_entry.get().strip()
            copies = self.copies_entry.get().strip()
            if not title or not author or not isbn or not copies: 
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                copies = int(copies)
                if copies <= 0:
                    raise ValueError("Copies must be a postive integer.")
                
                database.execute_query(
                    "INSERT INTO Books (title, author, isbn, copies) VALUES (?,?,?,?)", 
                    (title, author, isbn, copies)
                )
                messagebox.showinfo("Success", "Book added successfully!")
                self.window.destroy()
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid inpur: {ve}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occured: {e}")
        
        submit_button = tk.Button(self.window, text = "Submit", command = save_book)
        submit_button.pack(pady = 10)
    
    # Generates report for admin
    # Checks Checkouts table to see if any overdue books
    def generate_report(self):
        try: 

            overdue_books = database.fetch_query("""
            SELECT Users.username, Books.title, Checkouts.fine
            FROM Checkouts
            JOIN Users ON Checkouts.user_id = Users.user_id
            Join Books ON Checkouts.book_id = Books.book_id
            Where Checkouts.return_date IS NULL AND Checkouts.fine > 0 
            """)

            if overdue_books:
                report = "\n".join([f"{user} - {book} - {fine:.2f}" 
                                    for user, book, fine in overdue_books])
            else:
                report = "No overdue books!"

            messagebox.showinfo("Overdue Report", report)
        except Exception as e:
            print(f"Error generating report: {e}")
            messagebox.showerror("Error", "An unexpected error occured while generating the report")

    # Enables checkout button when a selection is made in the Book list box
    def enable_checkout_button(self,event):
        selection = self.search_results.curselection()
        if selection:
            self.checkout_button.config(state = tk.NORMAL)
        else:
            self.checkout_button.config(state = tk.DISABLED)

    # Method to create a checkout 
    # Checks that copies are avaliable of the book
    # If copies available SQL method to insert user_id and book_id into Checkouts table
    # Displays checked out books in bottom list box
    def checkout_book(self):
        selection = self.search_results.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a book to checkout")
            return
        selected_index = selection[0]
        selected_book = self.books[selected_index]
        book_id = selected_book[0]

        try:

            available_copies = database.fetch_query(
                 """
                SELECT Books.copies - COUNT(Checkouts.book_id)
                FROM Books
                LEFT JOIN Checkouts
                ON Books.book_id = Checkouts.book_id
                AND Checkouts.return_date IS NULL
                WHERE Books.book_id = ?
                GROUP BY Books.book_id
                """,
                (book_id,)
            )

            if available_copies and available_copies[0][0] <= 0:
                messagebox.showerror("Unavailable", "No more copies of this book are available for checkout.")
                return

            database.execute_query(
                "INSERT INTO Checkouts (user_id, book_id) VALUES (?, ?)",
                (self.user_id, book_id)
            )

            database.execute_query(
                "UPDATE Books SET copies = copies - 1 WHERE book_id = ?", 
                (book_id,)
            )

            messagebox.showinfo("Success", "Book checked out successfully")
            self.checkout_button.config(state=tk.DISABLED)
            self.fetch_checked_out_books()
        except Exception as e:
            print(f"Error during checkout: {e}")
            messagebox.showerror("Error", "An unexpected error occured")


    # Calls Checkouts table to view checked out books by user
    # Initializes the checkout_date
    def fetch_checked_out_books(self):
        try:
            results = database.fetch_query(
                 """
            SELECT Books.book_id, Books.title, Books.author, Checkouts.checkout_date, Checkouts.fine
            FROM Checkouts
            JOIN Books ON Checkouts.book_id = Books.book_id
            WHERE Checkouts.user_id = ? AND Checkouts.return_date IS NULL
            """,
            (self.user_id,)
            )


            self.my_books_listbox.delete(0,tk.END)
            self.checked_out_books = []

            print(f"Fetched results: {results}")

            for book_id, title, author, checkout_date, current_fine in results:
                if checkout_date:
                    checkout_date_obj = datetime.strptime(checkout_date, "%Y-%m-%d").date()

                    new_fine = self.calculate_fine(checkout_date_obj)
                else:
                    checkout_date_obj = None
                    new_fine = 0

                if new_fine != current_fine:
                    database.execute_query(
                        """
                    UPDATE Checkouts
                    SET fine = ?
                    WHERE book_id = ? AND user_id = ? AND return_date IS NULL
                    """,
                    (new_fine, book_id, self.user_id)
                    )

                self.checked_out_books.append((book_id, title, author, checkout_date))
                fine_display = f"(${new_fine:.2f} fine)" if new_fine > 0 else ""
                self.my_books_listbox.insert(tk.END, f"{title} by {author} (Checked out on {checkout_date} {fine_display})")
                
        except Exception as e:
            print(f"Error fetching checked out books: {e}")
            messagebox.showerror("Error", "An unexpected error occured while fetching books")

    # Enables return button when selection is made in the Checked out books listbox
    def enable_return_button(self, event):
        selection = self.my_books_listbox.curselection()
        print(f"Selection: {selection}")
        if selection:
            self.return_button.config(state=tk.NORMAL)
        else:
            self.return_button.config(state=tk.DISABLED)


    # Allows users to return books that are checked out
    # Resets checked out books display box
    def return_book(self):
        selection = self.my_books_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a book to return")
            return
        selected_index = selection[0]
        selected_book = self.checked_out_books[selected_index]
        book_id = selected_book[0]

        try:
            database.execute_query(
                "UPDATE Checkouts SET return_date = CURRENT_DATE WHERE book_id = ? AND user_id = ? AND return_date IS NULL",
                (book_id, self.user_id)
            )

            database.execute_query(
                "UPDATE Books SET copies = copies + 1 WHERE book_id = ?",
                (book_id,)
            )

            messagebox.showinfo("Success", "Book returned successfully")
            self.return_button.config(state=tk.DISABLED)
            self.fetch_checked_out_books()
            self.display_all_books()


        except Exception as e:
            print(f"Error during return: {e}")
            messagebox.showerror("Error", "An unexpected error occured while returning")


    # Initializes user register window
    def register_window(self):
        register_win = tk.Toplevel(self.root)
        register_win.title("Register")
        register_win.geometry("300x300")

        register_win.grab_set()

        tk.Label(register_win, text="Create an Account", font=("Arial", 14)).pack(pady=10)

        tk.Label(register_win, text="Username: ").pack(pady=5)
        username_entry = tk.Entry(register_win)
        username_entry.pack(pady=5)

        tk.Label(register_win, text="Email").pack(pady=5)
        email_entry = tk.Entry(register_win)
        email_entry.pack(pady=5)

        tk.Label(register_win, text="Password: ").pack(pady=5)
        password_entry = tk.Entry(register_win, show="*")
        password_entry.pack(pady=5)

        tk.Label(register_win, text = "Confirm Password: ").pack(pady=5)
        confirm_password_entry = tk.Entry(register_win, show="*")
        confirm_password_entry.pack(pady=5)

        # If valid user then entered into Users table
        def register_user():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()

            if not username or not email or not password or not confirm_password:
                messagebox.showerror("Error", "All fields are required.")
                return
            
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            
            try:
                database.execute_query(
                    "INSERT INTO Users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password)
                )
                messagebox.showinfo("Success", "Account created successfully!")
                register_win.destroy()
            except Exception as e:
                print(f"Error during registration: {e}")
                messagebox.showerror("Error", "An error occured while creating account.")
        tk.Button(register_win, text="Register", command = register_user).pack(pady=10)


    # Method to calculate fines on overdue books
    # $10 after 2 weeks then $1 for every additional day late
    def calculate_fine(self, checkout_date, return_date = None):
        due_date = checkout_date + timedelta(weeks = 2)
        current_date = datetime.now().date()

        if return_date:
            effective_date = return_date
        else:
            effective_date = current_date

        if effective_date <= due_date:
            return 0
        
        overdue_days = (effective_date - due_date).days
        fine = 10 + (overdue_days - 1) * 1
        return max(fine, 0)




if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
