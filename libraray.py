"""
Library Management System
Built from specifications in the Excel file.
Requirements:
  - pip install tkcalendar
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import hashlib
import random

try:
    from tkcalendar import DateEntry
    HAS_CALENDAR = True
except ImportError:
    HAS_CALENDAR = False

# ─────────────────────────────────────────────
#  In-memory "database"
# ─────────────────────────────────────────────
USERS = {
    "adm":  {"password": hashlib.sha256("adm".encode()).hexdigest(),  "is_admin": True,  "active": True},
    "user": {"password": hashlib.sha256("user".encode()).hexdigest(), "is_admin": False, "active": True},
}

# category code → (from_code, to_code, category_label)
CATEGORIES = {
    "SC": ("SC(B/M)000001", "SC(B/M)000004", "Science"),
    "EC": ("EC(B/M)000001", "EC(B/M)000004", "Economics"),
    "FC": ("FC(B/M)000001", "FC(B/M)000004", "Fiction"),
    "CH": ("CH(B/M)000001", "CH(B/M)000004", "Children"),
    "PD": ("PD(B/M)000001", "PD(B/M)000004", "Personal Development"),
}

# ── CHANGE 1: Expanded book/movie catalogue ───────────────────────────────────
BOOKS = [
    # Science – Books
    {"serial": "SCB000001", "name": "Physics Fundamentals",      "author": "Halliday",      "category": "Science",             "type": "Book",  "status": "Available", "cost": 450, "procurement": "2022-01-10"},
    {"serial": "SCB000002", "name": "Chemistry Basics",          "author": "Atkins",        "category": "Science",             "type": "Book",  "status": "Available", "cost": 380, "procurement": "2022-03-15"},
    {"serial": "SCB000003", "name": "Biology Essentials",        "author": "Campbell",      "category": "Science",             "type": "Book",  "status": "Available", "cost": 420, "procurement": "2022-06-20"},
    {"serial": "SCB000004", "name": "Quantum Mechanics",         "author": "Griffiths",     "category": "Science",             "type": "Book",  "status": "Available", "cost": 510, "procurement": "2023-02-01"},
    # Economics – Books
    {"serial": "ECB000001", "name": "Microeconomics",            "author": "Mankiw",        "category": "Economics",           "type": "Book",  "status": "Available", "cost": 520, "procurement": "2021-07-20"},
    {"serial": "ECB000002", "name": "Macroeconomics",            "author": "Blanchard",     "category": "Economics",           "type": "Book",  "status": "Available", "cost": 490, "procurement": "2022-08-05"},
    {"serial": "ECB000003", "name": "Freakonomics",              "author": "Levitt",        "category": "Economics",           "type": "Book",  "status": "Available", "cost": 300, "procurement": "2021-11-12"},
    # Fiction – Books
    {"serial": "FCB000001", "name": "The Great Gatsby",          "author": "Fitzgerald",    "category": "Fiction",             "type": "Book",  "status": "Available", "cost": 250, "procurement": "2020-11-05"},
    {"serial": "FCB000002", "name": "1984",                      "author": "Orwell",        "category": "Fiction",             "type": "Book",  "status": "Available", "cost": 280, "procurement": "2021-04-18"},
    {"serial": "FCB000003", "name": "To Kill a Mockingbird",     "author": "Lee",           "category": "Fiction",             "type": "Book",  "status": "Available", "cost": 260, "procurement": "2021-09-30"},
    # Children – Books
    {"serial": "CHB000001", "name": "Harry Potter",              "author": "Rowling",       "category": "Children",            "type": "Book",  "status": "Available", "cost": 350, "procurement": "2019-06-01"},
    {"serial": "CHB000002", "name": "The Lion, the Witch & the Wardrobe", "author": "Lewis","category": "Children",            "type": "Book",  "status": "Available", "cost": 290, "procurement": "2020-03-22"},
    {"serial": "CHB000003", "name": "Charlotte's Web",           "author": "White",         "category": "Children",            "type": "Book",  "status": "Available", "cost": 220, "procurement": "2020-07-14"},
    # Personal Development – Books
    {"serial": "PDB000001", "name": "Atomic Habits",             "author": "Clear",         "category": "Personal Development","type": "Book",  "status": "Available", "cost": 410, "procurement": "2023-01-01"},
    {"serial": "PDB000002", "name": "The 7 Habits of Highly Effective People", "author": "Covey", "category": "Personal Development","type": "Book","status": "Available","cost": 390,"procurement": "2022-05-10"},
    {"serial": "PDB000003", "name": "Deep Work",                 "author": "Newport",       "category": "Personal Development","type": "Book",  "status": "Available", "cost": 370, "procurement": "2022-09-28"},
    # Science – Movies
    {"serial": "SCM000001", "name": "Interstellar",              "author": "Nolan",         "category": "Science",             "type": "Movie", "status": "Available", "cost": 200, "procurement": "2021-02-14"},
    {"serial": "SCM000002", "name": "The Martian",               "author": "Scott",         "category": "Science",             "type": "Movie", "status": "Available", "cost": 180, "procurement": "2021-08-19"},
    {"serial": "SCM000003", "name": "Contact",                   "author": "Zemeckis",      "category": "Science",             "type": "Movie", "status": "Available", "cost": 160, "procurement": "2020-10-05"},
    # Fiction – Movies
    {"serial": "FCM000001", "name": "The Dark Knight",           "author": "Nolan",         "category": "Fiction",             "type": "Movie", "status": "Available", "cost": 150, "procurement": "2020-08-08"},
    {"serial": "FCM000002", "name": "Inception",                 "author": "Nolan",         "category": "Fiction",             "type": "Movie", "status": "Available", "cost": 160, "procurement": "2021-01-25"},
    # Children – Movies
    {"serial": "CHM000001", "name": "Spirited Away",             "author": "Miyazaki",      "category": "Children",            "type": "Movie", "status": "Available", "cost": 140, "procurement": "2022-04-03"},
    {"serial": "CHM000002", "name": "The Lion King",             "author": "Allers",        "category": "Children",            "type": "Movie", "status": "Available", "cost": 130, "procurement": "2021-12-15"},
    # Personal Development – Movies
    {"serial": "PDM000001", "name": "The Pursuit of Happyness",  "author": "Muccino",       "category": "Personal Development","type": "Movie", "status": "Available", "cost": 170, "procurement": "2022-07-07"},
]

MEMBERSHIPS = [
    {"id": "MEM001", "first": "Alice",  "last": "Smith",   "contact": "9876543210", "address": "12 Main St",   "aadhar": "1234-5678-9012", "start": "2024-01-01", "end": "2024-12-31", "status": "Active",   "fine": 0},
    {"id": "MEM002", "first": "Bob",    "last": "Jones",   "contact": "9123456780", "address": "45 Park Ave",  "aadhar": "9876-5432-1098", "start": "2023-06-01", "end": "2024-05-31", "status": "Inactive", "fine": 50},
    {"id": "MEM003", "first": "Priya",  "last": "Sharma",  "contact": "9988776655", "address": "7 Lake View",  "aadhar": "2233-4455-6677", "start": "2024-03-01", "end": "2025-02-28", "status": "Active",   "fine": 0},
    {"id": "MEM004", "first": "Rohan",  "last": "Mehta",   "contact": "9871234560", "address": "23 MG Road",   "aadhar": "5566-7788-9900", "start": "2024-05-01", "end": "2025-04-30", "status": "Active",   "fine": 0},
]

# ── CHANGE 2: Pre-seeded ISSUES with 2 overdue + 1 current for Pay Fine demos ─
ISSUES = [
    {
        "serial":        "ECB000001",
        "name":          "Microeconomics",
        "membership_id": "MEM001",
        "issue_date":    str(date.today() - timedelta(days=20)),
        "return_date":   str(date.today() - timedelta(days=5)),   # 5 days overdue → ₹10 fine
    },
    {
        "serial":        "FCB000001",
        "name":          "The Great Gatsby",
        "membership_id": "MEM003",
        "issue_date":    str(date.today() - timedelta(days=18)),
        "return_date":   str(date.today() - timedelta(days=3)),   # 3 days overdue → ₹6 fine
    },
    {
        "serial":        "PDB000001",
        "name":          "Atomic Habits",
        "membership_id": "MEM004",
        "issue_date":    str(date.today() - timedelta(days=7)),
        "return_date":   str(date.today() + timedelta(days=8)),   # still within period, no fine
    },
]

# Mark pre-seeded issued books
_issued_serials = {i["serial"] for i in ISSUES}
for _b in BOOKS:
    if _b["serial"] in _issued_serials:
        _b["status"] = "Issued"

ISSUE_REQUESTS = []   # {membership_id, book_name, requested_date, fulfilled_date}

FINE_RATE = 2  # ₹ per day overdue

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
session = {"user": None, "is_admin": False}

# ─────────────────────────────────────────────
#  Helper widgets
# ─────────────────────────────────────────────

def make_date_entry(parent, **kwargs):
    if HAS_CALENDAR:
        return DateEntry(parent, date_pattern="yyyy-mm-dd", **kwargs)
    e = ttk.Entry(parent, **kwargs)
    e.insert(0, str(date.today()))
    return e

def get_date(widget):
    if HAS_CALENDAR and isinstance(widget, DateEntry):
        return widget.get_date()
    try:
        return date.fromisoformat(widget.get())
    except ValueError:
        return date.today()

def styled_frame(parent, **kwargs):
    f = ttk.Frame(parent, padding=10, **kwargs)
    return f

def heading(parent, text, size=14):
    ttk.Label(parent, text=text, font=("Arial", size, "bold")).pack(pady=(0, 10))

def nav_bar(parent, app, show_home=True, show_transactions=False, show_reports=False):
    bar = ttk.Frame(parent)
    bar.pack(fill="x", pady=(0, 6))
    if show_home:
        ttk.Button(bar, text="🏠 Home", command=app.go_home).pack(side="left", padx=2)
    if show_transactions:
        ttk.Button(bar, text="Transactions", command=app.show_transactions).pack(side="left", padx=2)
    if show_reports:
        ttk.Button(bar, text="Reports", command=app.show_reports).pack(side="left", padx=2)
    ttk.Button(bar, text="Log Out", command=app.logout).pack(side="right", padx=2)

def table(parent, columns, rows, heights=8):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, pady=4)
    tv = ttk.Treeview(frame, columns=columns, show="headings", height=heights)
    for c in columns:
        tv.heading(c, text=c)
        tv.column(c, width=max(80, len(c) * 9))
    for r in rows:
        tv.insert("", "end", values=r)
    sb = ttk.Scrollbar(frame, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=sb.set)
    tv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return tv

# ─────────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────────

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self._selected_book_serial = None
        self.show_main_page()

    # ── frame helpers ──────────────────────────

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def go_home(self):
        if session["is_admin"]:
            self.show_admin_home()
        else:
            self.show_user_home()

    def logout(self):
        session["user"] = None
        session["is_admin"] = False
        self.show_logout()

    # ══════════════════════════════════════════
    #  MAIN PAGE  (initial screen)
    # ══════════════════════════════════════════

    def show_main_page(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(expand=True)
        heading(f, "Library Management System", 16)
        ttk.Label(f, text="Welcome! Please select a login type.", font=("Arial", 11)).pack(pady=8)
        ttk.Button(f, text="Admin Login", width=20, command=lambda: self.show_login("admin")).pack(pady=6)
        ttk.Button(f, text="User Login",  width=20, command=lambda: self.show_login("user")).pack(pady=6)

    # ══════════════════════════════════════════
    #  LOGIN PAGES
    # ══════════════════════════════════════════

    def show_login(self, role="admin"):
        self.clear()
        f = styled_frame(self.container)
        f.pack(expand=True)
        heading(f, "Library Management System", 16)
        ttk.Label(f, text=f"{'Admin' if role == 'admin' else 'User'} Login",
                  font=("Arial", 12)).pack(pady=4)

        ttk.Label(f, text="User ID").pack()
        uid = ttk.Entry(f, width=30)
        uid.pack(pady=2)

        ttk.Label(f, text="Password").pack()
        pwd = ttk.Entry(f, width=30, show="*")
        pwd.pack(pady=2)

        def do_login():
            u = uid.get().strip()
            p = pwd.get().strip()
            hashed = hashlib.sha256(p.encode()).hexdigest()
            usr = USERS.get(u)
            if not usr or not usr["active"] or usr["password"] != hashed:
                messagebox.showerror("Error", "Invalid credentials.")
                return
            if role == "admin" and not usr["is_admin"]:
                messagebox.showerror("Error", "This account does not have admin rights.")
                return
            session["user"] = u
            session["is_admin"] = usr["is_admin"]
            if session["is_admin"]:
                self.show_admin_home()
            else:
                self.show_user_home()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Login",  command=do_login,           width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel", command=self.show_main_page, width=14).pack(side="left", padx=6)

    # ══════════════════════════════════════════
    #  HOME PAGES
    #  CHANGE 3: Back button removed from both
    #            Admin Home and User Home
    # ══════════════════════════════════════════

    def show_admin_home(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)   # Log Out available via nav bar; Back button removed

        heading(f, "Admin Home Page")

        btn_f = ttk.Frame(f)
        btn_f.pack(pady=10)
        ttk.Button(btn_f, text="Maintenance",  width=18, command=self.show_maintenance).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_f, text="Reports",      width=18, command=self.show_reports).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_f, text="Transactions", width=18, command=self.show_transactions).grid(row=0, column=2, padx=5, pady=5)

        heading(f, "Product Details", 11)
        rows = [(v[0], v[1], v[2]) for v in CATEGORIES.values()]
        table(f, ["Code No From", "Code No To", "Category"], rows, heights=6)

    def show_user_home(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)   # Log Out available via nav bar; Back button removed

        heading(f, "Home Page")

        btn_f = ttk.Frame(f)
        btn_f.pack(pady=10)
        ttk.Button(btn_f, text="Reports",      width=18, command=self.show_reports).grid(row=0, column=0, padx=5)
        ttk.Button(btn_f, text="Transactions", width=18, command=self.show_transactions).grid(row=0, column=1, padx=5)

        heading(f, "Product Details", 11)
        rows = [(v[0], v[1], v[2]) for v in CATEGORIES.values()]
        table(f, ["Code No From", "Code No To", "Category"], rows, heights=6)

    # ══════════════════════════════════════════
    #  TRANSACTIONS
    # ══════════════════════════════════════════

    def show_transactions(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "Transactions")

        ops = [
            ("Is Book Available?", self.show_book_available),
            ("Issue Book",         self.show_book_issue),
            ("Return Book",        self.show_return_book),
            ("Pay Fine",           self.show_pay_fine),
        ]
        for label, cmd in ops:
            ttk.Button(f, text=label, width=28, command=cmd).pack(pady=4)

        ttk.Button(f, text="← Back", command=self.go_home).pack(pady=10)

    # ── Book Available ─────────────────────────

    def show_book_available(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self, show_transactions=True)
        heading(f, "Book Availability")

        form = ttk.Frame(f)
        form.pack(pady=6)
        ttk.Label(form, text="Book Name").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        book_names = sorted({b["name"] for b in BOOKS})
        book_var = tk.StringVar()
        ttk.Combobox(form, textvariable=book_var, values=book_names, width=30).grid(row=0, column=1, padx=4)

        ttk.Label(form, text="Author").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        author_names = sorted({b["author"] for b in BOOKS})
        author_var = tk.StringVar()
        ttk.Combobox(form, textvariable=author_var, values=author_names, width=30).grid(row=1, column=1, padx=4)

        result_frame = ttk.Frame(f)
        result_frame.pack(fill="both", expand=True, pady=6)

        def search():
            for w in result_frame.winfo_children():
                w.destroy()
            bn, an = book_var.get().strip(), author_var.get().strip()
            if not bn and not an:
                ttk.Label(result_frame, text="Please enter a book name or author.", foreground="red").pack()
                return
            results = [b for b in BOOKS if
                       (not bn or bn.lower() in b["name"].lower()) and
                       (not an or an.lower() in b["author"].lower())]
            if not results:
                ttk.Label(result_frame, text="No books found.", foreground="red").pack()
                ttk.Button(result_frame, text="Cancel", command=self.show_book_available).pack(pady=4)
                return
            cols = ["Book Name", "Author", "Serial No", "Available", "Select"]
            tv = ttk.Treeview(result_frame, columns=cols, show="headings", height=8)
            for c in cols[:-1]:
                tv.heading(c, text=c); tv.column(c, width=130)
            tv.heading("Select", text="Select to Issue")
            tv.column("Select", width=100)
            for b in results:
                avail = "Y" if b["status"] == "Available" else "N"
                tv.insert("", "end", values=(b["name"], b["author"], b["serial"], avail,
                                              "◉" if avail == "Y" else ""), tags=(b["serial"],))
            tv.pack(fill="both", expand=True)

            def on_select(event):
                sel = tv.selection()
                if not sel:
                    return
                vals = tv.item(sel[0])["values"]
                if vals[3] == "Y":
                    self._selected_book_serial = vals[2]
                    messagebox.showinfo("Selected", f"Selected: {vals[0]}\nGo to Issue Book to proceed.")

            tv.bind("<<TreeviewSelect>>", on_select)
            ttk.Button(result_frame, text="Cancel", command=self.show_book_available).pack(pady=4)

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=4)
        ttk.Button(btn_row, text="Search", command=search).pack(side="left", padx=6)
        ttk.Button(btn_row, text="← Back", command=self.show_transactions).pack(side="left", padx=6)

    # ── Book Issue ─────────────────────────────

    def show_book_issue(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self, show_transactions=True)
        heading(f, "Book Issue")

        form = ttk.Frame(f)
        form.pack(pady=6)
        r = 0

        ttk.Label(form, text="Book Name *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        avail_books = [b for b in BOOKS if b["status"] == "Available"]
        book_var = tk.StringVar()
        book_cb = ttk.Combobox(form, textvariable=book_var, values=[b["name"] for b in avail_books], width=32)
        book_cb.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Author").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        author_var = tk.StringVar()
        ttk.Entry(form, textvariable=author_var, state="readonly", width=34).grid(row=r, column=1, padx=4); r += 1

        def on_book_select(event=None):
            sel = book_var.get()
            match = next((b for b in avail_books if b["name"] == sel), None)
            if match:
                author_var.set(match["author"])

        book_cb.bind("<<ComboboxSelected>>", on_book_select)

        ttk.Label(form, text="Membership ID *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        mem_var = tk.StringVar()
        mem_ids = [m["id"] for m in MEMBERSHIPS if m["status"] == "Active"]
        ttk.Combobox(form, textvariable=mem_var, values=mem_ids, width=32).grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Issue Date *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        issue_de = make_date_entry(form, width=16)
        if HAS_CALENDAR:
            issue_de.configure(mindate=date.today())
        issue_de.grid(row=r, column=1, sticky="w", padx=4); r += 1

        ttk.Label(form, text="Return Date *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        return_de = make_date_entry(form, width=16)
        if HAS_CALENDAR:
            return_de.set_date(date.today() + timedelta(days=15))
            return_de.configure(maxdate=date.today() + timedelta(days=15))
        else:
            return_de.delete(0, "end")
            return_de.insert(0, str(date.today() + timedelta(days=15)))
        return_de.grid(row=r, column=1, sticky="w", padx=4); r += 1

        ttk.Label(form, text="Remarks").grid(row=r, column=0, sticky="nw", padx=4, pady=3)
        remarks = tk.Text(form, width=34, height=3)
        remarks.grid(row=r, column=1, padx=4); r += 1

        def submit():
            bn = book_var.get().strip()
            mid = mem_var.get().strip()
            if not bn:
                messagebox.showerror("Error", "Please select a book."); return
            if not mid:
                messagebox.showerror("Error", "Please select a membership ID."); return
            idate = get_date(issue_de)
            rdate = get_date(return_de)
            if idate < date.today():
                messagebox.showerror("Error", "Issue date cannot be before today."); return
            delta = (rdate - idate).days
            if delta < 0 or delta > 15:
                messagebox.showerror("Error", "Return date must be within 15 days of issue date."); return
            book = next((b for b in BOOKS if b["name"] == bn), None)
            if book:
                book["status"] = "Issued"
                ISSUES.append({"serial": book["serial"], "name": bn, "membership_id": mid,
                                "issue_date": str(idate), "return_date": str(rdate)})
                ISSUE_REQUESTS.append({"membership_id": mid, "book_name": bn,
                                        "requested_date": str(date.today()), "fulfilled_date": str(date.today())})
            self.show_confirmation()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm Issue", command=submit, width=16).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",        command=self.show_transactions, width=16).pack(side="left", padx=6)

    # ── Return Book ────────────────────────────

    def show_return_book(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self, show_transactions=True)
        heading(f, "Return Book")

        form = ttk.Frame(f)
        form.pack(pady=6)
        r = 0

        issued_names = sorted({i["name"] for i in ISSUES})
        ttk.Label(form, text="Book Name *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        book_var = tk.StringVar()
        book_cb = ttk.Combobox(form, textvariable=book_var, values=issued_names, width=32)
        book_cb.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Author").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        author_var = tk.StringVar()
        ttk.Entry(form, textvariable=author_var, state="readonly", width=34).grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Serial No *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        serial_var = tk.StringVar()
        serial_cb = ttk.Combobox(form, textvariable=serial_var, width=32)
        serial_cb.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Issue Date").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        issue_var = tk.StringVar()
        ttk.Entry(form, textvariable=issue_var, state="readonly", width=34).grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Return Date").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        return_de = make_date_entry(form, width=16)
        return_de.grid(row=r, column=1, sticky="w", padx=4); r += 1

        ttk.Label(form, text="Remarks").grid(row=r, column=0, sticky="nw", padx=4, pady=3)
        remarks = tk.Text(form, width=34, height=3)
        remarks.grid(row=r, column=1, padx=4)

        def populate(issue):
            book = next((b for b in BOOKS if b["name"] == issue["name"]), None)
            if book:
                book_var.set(issue["name"])
                author_var.set(book["author"])
            serial_cb["values"] = [issue["serial"]]
            serial_var.set(issue["serial"])
            issue_var.set(issue["issue_date"])
            if HAS_CALENDAR:
                return_de.set_date(date.fromisoformat(issue["return_date"]))
            else:
                return_de.delete(0, "end")
                return_de.insert(0, issue["return_date"])

        def on_book_select(event=None):
            bn = book_var.get()
            issue = next((i for i in ISSUES if i["name"] == bn), None)
            if issue:
                populate(issue)

        book_cb.bind("<<ComboboxSelected>>", on_book_select)

        if ISSUES:
            populate(ISSUES[0])

        def submit():
            bn = book_var.get().strip()
            sn = serial_var.get().strip()
            if not bn:
                messagebox.showerror("Error", "Please select a book."); return
            if not sn:
                messagebox.showerror("Error", "Serial number is mandatory."); return
            self.show_pay_fine(prefill_book=bn, prefill_serial=sn,
                               actual_return=str(get_date(return_de)))

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm Return", command=submit, width=16).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",         command=self.show_transactions, width=16).pack(side="left", padx=6)

    # ── Pay Fine ───────────────────────────────
    # CHANGE 2: Full interactive dropdowns; all fields user-selectable

    def show_pay_fine(self, prefill_book=None, prefill_serial=None, actual_return=None):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self, show_transactions=True)
        heading(f, "Pay Fine")

        form = ttk.Frame(f)
        form.pack(pady=6)
        r = 0

        # ── Book Name dropdown ─────────────────
        ttk.Label(form, text="Book Name *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        issued_names = sorted({i["name"] for i in ISSUES})
        book_var = tk.StringVar()
        book_cb = ttk.Combobox(form, textvariable=book_var, values=issued_names, width=32, state="readonly")
        book_cb.grid(row=r, column=1, padx=4); r += 1

        # ── Author (read-only, auto-filled) ───
        ttk.Label(form, text="Author").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        author_var = tk.StringVar()
        ttk.Entry(form, textvariable=author_var, state="readonly", width=34).grid(row=r, column=1, padx=4); r += 1

        # ── Serial No dropdown ─────────────────
        ttk.Label(form, text="Serial No *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        serial_var = tk.StringVar()
        serial_cb = ttk.Combobox(form, textvariable=serial_var, width=32, state="readonly")
        serial_cb.grid(row=r, column=1, padx=4); r += 1

        # ── Issue Date (read-only, auto-filled) ─
        ttk.Label(form, text="Issue Date").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        issue_var = tk.StringVar()
        ttk.Entry(form, textvariable=issue_var, state="readonly", width=34).grid(row=r, column=1, padx=4); r += 1

        # ── Return Date (read-only, auto-filled) ─
        ttk.Label(form, text="Return Date").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        ret_var = tk.StringVar()
        ttk.Entry(form, textvariable=ret_var, state="readonly", width=34).grid(row=r, column=1, padx=4); r += 1

        # ── Actual Return Date (user-selectable) ─
        ttk.Label(form, text="Actual Return Date *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        act_de = make_date_entry(form, width=16)
        act_de.grid(row=r, column=1, sticky="w", padx=4); r += 1

        # ── Fine Calculated ────────────────────
        ttk.Label(form, text="Fine Calculated (₹)").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        fine_var = tk.StringVar(value="0")
        fine_entry = ttk.Entry(form, textvariable=fine_var, state="readonly", width=34)
        fine_entry.grid(row=r, column=1, padx=4); r += 1

        # ── Fine Paid checkbox ─────────────────
        fine_paid_var = tk.BooleanVar(value=True)
        ttk.Label(form, text="Fine Paid").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        ttk.Checkbutton(form, variable=fine_paid_var).grid(row=r, column=1, sticky="w", padx=4); r += 1

        # ── Remarks ───────────────────────────
        ttk.Label(form, text="Remarks").grid(row=r, column=0, sticky="nw", padx=4, pady=3)
        remarks = tk.Text(form, width=34, height=3)
        remarks.grid(row=r, column=1, padx=4); r += 1

        # ── internal state ─────────────────────
        _current_issue = {"rec": None}

        def recalc_fine(*_):
            """Recalculate fine whenever actual return date changes."""
            rec = _current_issue["rec"]
            if not rec:
                fine_var.set("0")
                return
            try:
                ret_date    = date.fromisoformat(rec["return_date"])
                actual_date = get_date(act_de)
                days_late   = max(0, (actual_date - ret_date).days)
                fine_var.set(str(days_late * FINE_RATE))
                fine_paid_var.set(days_late == 0)
            except Exception:
                fine_var.set("0")

        # Wire actual-return-date changes to recalc
        if HAS_CALENDAR:
            act_de.bind("<<DateEntrySelected>>", recalc_fine)
        else:
            act_de.bind("<FocusOut>", recalc_fine)

        def populate_from_issue(rec):
            """Fill all dependent fields once an issue record is chosen."""
            _current_issue["rec"] = rec
            book = next((b for b in BOOKS if b["serial"] == rec["serial"]), None)
            author_var.set(book["author"] if book else "")
            serial_cb["values"] = [rec["serial"]]
            serial_var.set(rec["serial"])
            issue_var.set(rec["issue_date"])
            ret_var.set(rec["return_date"])
            if HAS_CALENDAR:
                act_de.set_date(date.today())
            else:
                act_de.delete(0, "end")
                act_de.insert(0, str(date.today()))
            recalc_fine()

        def on_book_select(event=None):
            bn  = book_var.get()
            rec = next((i for i in ISSUES if i["name"] == bn), None)
            if rec:
                populate_from_issue(rec)

        book_cb.bind("<<ComboboxSelected>>", on_book_select)

        # ── Pre-fill if called from Return Book or pre-seed first overdue ──
        if prefill_book:
            book_var.set(prefill_book)
        else:
            # Default to first overdue issue so admin can act immediately
            today_str = str(date.today())
            overdue   = [i for i in ISSUES if i["return_date"] < today_str]
            first     = overdue[0] if overdue else (ISSUES[0] if ISSUES else None)
            if first:
                book_var.set(first["name"])
                prefill_book   = first["name"]
                prefill_serial = first["serial"]
                actual_return  = str(date.today())

        init_rec = next((i for i in ISSUES if i["name"] == prefill_book), None) if prefill_book else None
        if init_rec:
            populate_from_issue(init_rec)
            if actual_return:
                if HAS_CALENDAR:
                    act_de.set_date(date.fromisoformat(actual_return))
                else:
                    act_de.delete(0, "end")
                    act_de.insert(0, actual_return)
                recalc_fine()

        def confirm():
            rec = _current_issue["rec"]
            if not rec:
                messagebox.showerror("Error", "Please select a book first."); return
            fine = int(fine_var.get())
            if fine > 0 and not fine_paid_var.get():
                messagebox.showerror("Error", "Please mark fine as paid before confirming."); return
            ISSUES.remove(rec)
            book = next((b for b in BOOKS if b["serial"] == rec["serial"]), None)
            if book:
                book["status"] = "Available"
            self.show_confirmation()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm", command=confirm,               width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",  command=self.show_transactions, width=14).pack(side="left", padx=6)

    # ══════════════════════════════════════════
    #  REPORTS
    # ══════════════════════════════════════════

    def show_reports(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "Reports")

        reports = [
            ("Master List of Books",       self.show_books_report),
            ("Master List of Movies",      self.show_movies_report),
            ("Master List of Memberships", self.show_memberships_report),
            ("Active Issues",              self.show_active_issues),
            ("Overdue Returns",            self.show_overdue_returns),
            ("Pending Issue Requests",     self.show_issue_requests),
        ]
        for label, cmd in reports:
            ttk.Button(f, text=label, width=32, command=cmd).pack(pady=3)

        ttk.Button(f, text="← Back", command=self.go_home, width=20).pack(pady=10)

    def show_books_report(self):
        self._show_list_report(
            "Master List of Books",
            ["Serial No", "Name", "Author", "Category", "Status", "Cost", "Procurement Date"],
            [(b["serial"], b["name"], b["author"], b["category"], b["status"], b["cost"], b["procurement"])
             for b in BOOKS if b["type"] == "Book"],
            back_cmd=self.show_reports)

    def show_movies_report(self):
        self._show_list_report(
            "Master List of Movies",
            ["Serial No", "Name", "Director", "Category", "Status", "Cost", "Procurement Date"],
            [(b["serial"], b["name"], b["author"], b["category"], b["status"], b["cost"], b["procurement"])
             for b in BOOKS if b["type"] == "Movie"],
            back_cmd=self.show_reports)

    def show_memberships_report(self):
        self._show_list_report(
            "List of Active Memberships",
            ["ID", "Name", "Contact", "Address", "Aadhar", "Start", "End", "Status", "Fine (₹)"],
            [(m["id"], f"{m['first']} {m['last']}", m["contact"], m["address"],
              m["aadhar"], m["start"], m["end"], m["status"], m["fine"])
             for m in MEMBERSHIPS],
            back_cmd=self.show_reports)

    def show_active_issues(self):
        self._show_list_report(
            "Active Issues",
            ["Serial No", "Book/Movie Name", "Membership ID", "Issue Date", "Return Date"],
            [(i["serial"], i["name"], i["membership_id"], i["issue_date"], i["return_date"])
             for i in ISSUES],
            back_cmd=self.show_reports)

    def show_overdue_returns(self):
        today = str(date.today())
        overdue = [
            (i["serial"], i["name"], i["membership_id"], i["issue_date"], i["return_date"],
             f"₹{max(0,(date.today()-date.fromisoformat(i['return_date'])).days)*FINE_RATE}")
            for i in ISSUES if i["return_date"] < today
        ]
        self._show_list_report(
            "Overdue Returns",
            ["Serial No", "Book Name", "Membership ID", "Issue Date", "Return Date", "Fine"],
            overdue,
            back_cmd=self.show_reports)

    def show_issue_requests(self):
        self._show_list_report(
            "Pending Issue Requests",
            ["Membership ID", "Book/Movie Name", "Requested Date", "Fulfilled Date"],
            [(ir["membership_id"], ir["book_name"], ir["requested_date"], ir["fulfilled_date"])
             for ir in ISSUE_REQUESTS],
            back_cmd=self.show_reports)

    def _show_list_report(self, title, cols, rows, back_cmd=None):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self, show_reports=True)
        heading(f, title)
        table(f, cols, rows, heights=12)
        ttk.Button(f, text="← Back",
                   command=back_cmd if back_cmd else self.show_reports).pack(pady=6)

    # ══════════════════════════════════════════
    #  MAINTENANCE  (Admin only)
    # ══════════════════════════════════════════

    def show_maintenance(self):
        if not session["is_admin"]:
            messagebox.showerror("Access Denied", "Only admins can access Maintenance."); return
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "Maintenance")

        sections = [
            ("Membership – Add",      self.show_add_membership),
            ("Membership – Update",   self.show_update_membership),
            ("Books/Movies – Add",    self.show_add_book),
            ("Books/Movies – Update", self.show_update_book),
            ("User Management",       self.show_user_management),
        ]
        for label, cmd in sections:
            ttk.Button(f, text=label, width=30, command=cmd).pack(pady=4)

        ttk.Button(f, text="← Back", command=self.go_home, width=20).pack(pady=10)

    # ── Add Membership ─────────────────────────

    def show_add_membership(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "Add Membership")

        form = ttk.Frame(f)
        form.pack()
        fields = ["First Name", "Last Name", "Contact Number", "Contact Address", "Aadhar Card No"]
        entries = {}
        for i, field in enumerate(fields):
            ttk.Label(form, text=f"{field} *").grid(row=i, column=0, sticky="w", padx=4, pady=3)
            e = ttk.Entry(form, width=34)
            e.grid(row=i, column=1, padx=4)
            entries[field] = e

        r = len(fields)
        ttk.Label(form, text="Start Date *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        start_de = make_date_entry(form, width=16)
        start_de.grid(row=r, column=1, sticky="w", padx=4); r += 1

        ttk.Label(form, text="Membership *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        mem_var = tk.StringVar(value="6 months")
        mb_f = ttk.Frame(form)
        mb_f.grid(row=r, column=1, sticky="w")
        for opt in ["6 months", "1 year", "2 years"]:
            ttk.Radiobutton(mb_f, text=opt, variable=mem_var, value=opt).pack(side="left", padx=4)

        def submit():
            vals = {k: v.get().strip() for k, v in entries.items()}
            if any(not v for v in vals.values()):
                messagebox.showerror("Error", "All fields are required."); return
            durations = {"6 months": 182, "1 year": 365, "2 years": 730}
            sd = get_date(start_de)
            ed = sd + timedelta(days=durations[mem_var.get()])
            new_id = f"MEM{len(MEMBERSHIPS)+1:03d}"
            MEMBERSHIPS.append({
                "id": new_id, "first": vals["First Name"], "last": vals["Last Name"],
                "contact": vals["Contact Number"], "address": vals["Contact Address"],
                "aadhar": vals["Aadhar Card No"], "start": str(sd), "end": str(ed),
                "status": "Active", "fine": 0
            })
            messagebox.showinfo("Success", f"Membership {new_id} added.")
            self.show_confirmation()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm", command=submit,               width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",  command=self.show_maintenance, width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="← Back",  command=self.show_maintenance, width=14).pack(side="left", padx=6)

    # ── Update Membership ──────────────────────

    def show_update_membership(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "Update Membership")

        form = ttk.Frame(f)
        form.pack()
        ttk.Label(form, text="Membership Number *").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        mem_ids = [m["id"] for m in MEMBERSHIPS]
        mem_var = tk.StringVar()
        mem_cb = ttk.Combobox(form, textvariable=mem_var, values=mem_ids, width=30)
        mem_cb.grid(row=0, column=1, padx=4)

        info_var = tk.StringVar()
        ttk.Label(form, textvariable=info_var, foreground="blue").grid(row=1, column=0, columnspan=2, pady=4)

        ttk.Label(form, text="Extension").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        ext_var = tk.StringVar(value="6 months")
        ext_f = ttk.Frame(form)
        ext_f.grid(row=2, column=1, sticky="w")
        for opt in ["6 months", "1 year", "2 years"]:
            ttk.Radiobutton(ext_f, text=opt, variable=ext_var, value=opt).pack(side="left", padx=4)

        cancel_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(form, text="Cancel Membership", variable=cancel_var).grid(row=3, column=1, sticky="w", padx=4)

        def on_select(event=None):
            m = next((x for x in MEMBERSHIPS if x["id"] == mem_var.get()), None)
            if m:
                info_var.set(f"{m['first']} {m['last']} | Status: {m['status']} | Ends: {m['end']}")

        mem_cb.bind("<<ComboboxSelected>>", on_select)

        def submit():
            mid = mem_var.get()
            if not mid:
                messagebox.showerror("Error", "Membership number is required."); return
            m = next((x for x in MEMBERSHIPS if x["id"] == mid), None)
            if not m:
                messagebox.showerror("Error", "Membership not found."); return
            if cancel_var.get():
                m["status"] = "Inactive"
                messagebox.showinfo("Done", "Membership cancelled.")
            else:
                durations = {"6 months": 182, "1 year": 365, "2 years": 730}
                end = date.fromisoformat(m["end"]) + timedelta(days=durations[ext_var.get()])
                m["end"] = str(end)
                messagebox.showinfo("Done", f"Membership extended to {end}.")
            self.show_confirmation()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm", command=submit,               width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",  command=self.show_maintenance, width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="← Back",  command=self.show_maintenance, width=14).pack(side="left", padx=6)

    # ── Add Book/Movie ─────────────────────────

    def show_add_book(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "Add Book / Movie")

        form = ttk.Frame(f)
        form.pack()
        r = 0
        ttk.Label(form, text="Type *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        type_var = tk.StringVar(value="Book")
        tf = ttk.Frame(form)
        tf.grid(row=r, column=1, sticky="w")
        ttk.Radiobutton(tf, text="Book",  variable=type_var, value="Book").pack(side="left")
        ttk.Radiobutton(tf, text="Movie", variable=type_var, value="Movie").pack(side="left", padx=6); r += 1

        ttk.Label(form, text="Name *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        name_e = ttk.Entry(form, width=34); name_e.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Author/Director *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        auth_e = ttk.Entry(form, width=34); auth_e.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Category *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        cat_var = tk.StringVar()
        ttk.Combobox(form, textvariable=cat_var, values=[v[2] for v in CATEGORIES.values()], width=32).grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Cost *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        cost_e = ttk.Entry(form, width=34); cost_e.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Procurement Date *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        proc_de = make_date_entry(form, width=16); proc_de.grid(row=r, column=1, sticky="w", padx=4); r += 1

        ttk.Label(form, text="Quantity/Copies *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        qty_e = ttk.Entry(form, width=34); qty_e.insert(0, "1"); qty_e.grid(row=r, column=1, padx=4)

        def submit():
            name = name_e.get().strip()
            auth = auth_e.get().strip()
            cat  = cat_var.get().strip()
            cost = cost_e.get().strip()
            qty  = qty_e.get().strip()
            if not all([name, auth, cat, cost, qty]):
                messagebox.showerror("Error", "All fields are required."); return
            prefix = cat[:2].upper()
            typ    = type_var.get()
            suffix = "B" if typ == "Book" else "M"
            existing = [b for b in BOOKS if b["type"] == typ and b["category"] == cat]
            serial = f"{prefix}{suffix}{len(existing)+1:06d}"
            for _ in range(int(qty)):
                BOOKS.append({"serial": serial, "name": name, "author": auth, "category": cat,
                               "type": typ, "status": "Available", "cost": int(cost),
                               "procurement": str(get_date(proc_de))})
            self.show_confirmation()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm", command=submit,               width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",  command=self.show_maintenance, width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="← Back",  command=self.show_maintenance, width=14).pack(side="left", padx=6)

    # ── Update Book/Movie ──────────────────────

    def show_update_book(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "Update Book / Movie")

        form = ttk.Frame(f)
        form.pack()
        r = 0
        ttk.Label(form, text="Type").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        type_var = tk.StringVar(value="Book")
        tf = ttk.Frame(form)
        tf.grid(row=r, column=1, sticky="w")
        ttk.Radiobutton(tf, text="Book",  variable=type_var, value="Book").pack(side="left")
        ttk.Radiobutton(tf, text="Movie", variable=type_var, value="Movie").pack(side="left", padx=6); r += 1

        ttk.Label(form, text="Book/Movie Name *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        book_var = tk.StringVar()
        book_cb = ttk.Combobox(form, textvariable=book_var, values=sorted({b["name"] for b in BOOKS}), width=32)
        book_cb.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Serial No *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        serial_var = tk.StringVar()
        serial_cb = ttk.Combobox(form, textvariable=serial_var, width=32)
        serial_cb.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Status *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        status_var = tk.StringVar()
        ttk.Combobox(form, textvariable=status_var, values=["Available", "Issued", "Lost", "Damaged"], width=32).grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Date").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        date_de = make_date_entry(form, width=16); date_de.grid(row=r, column=1, sticky="w", padx=4)

        def on_book(event=None):
            bn = book_var.get()
            serials = [b["serial"] for b in BOOKS if b["name"] == bn]
            serial_cb["values"] = serials
            if serials:
                serial_var.set(serials[0])
                b = next((x for x in BOOKS if x["serial"] == serials[0]), None)
                if b:
                    status_var.set(b["status"])

        book_cb.bind("<<ComboboxSelected>>", on_book)

        def submit():
            bn = book_var.get().strip(); sn = serial_var.get().strip(); st = status_var.get().strip()
            if not all([bn, sn, st]):
                messagebox.showerror("Error", "All fields required."); return
            b = next((x for x in BOOKS if x["serial"] == sn), None)
            if b:
                b["status"] = st
                b["procurement"] = str(get_date(date_de))
            self.show_confirmation()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm", command=submit,               width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",  command=self.show_maintenance, width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="← Back",  command=self.show_maintenance, width=14).pack(side="left", padx=6)

    # ── User Management ────────────────────────

    def show_user_management(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(fill="both", expand=True)
        nav_bar(f, self)
        heading(f, "User Management")

        form = ttk.Frame(f)
        form.pack()
        r = 0
        ttk.Label(form, text="Mode").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        mode_var = tk.StringVar(value="New User")
        mf = ttk.Frame(form)
        mf.grid(row=r, column=1, sticky="w")
        ttk.Radiobutton(mf, text="New User",      variable=mode_var, value="New User").pack(side="left")
        ttk.Radiobutton(mf, text="Existing User", variable=mode_var, value="Existing User").pack(side="left", padx=6); r += 1

        ttk.Label(form, text="Username *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        uname_e = ttk.Entry(form, width=34); uname_e.grid(row=r, column=1, padx=4); r += 1

        ttk.Label(form, text="Password *").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        pwd_e = ttk.Entry(form, width=34, show="*"); pwd_e.grid(row=r, column=1, padx=4); r += 1

        active_var = tk.BooleanVar(value=True)
        admin_var  = tk.BooleanVar(value=False)
        ttk.Checkbutton(form, text="Active", variable=active_var).grid(row=r, column=1, sticky="w", padx=4); r += 1
        ttk.Checkbutton(form, text="Admin",  variable=admin_var).grid(row=r, column=1, sticky="w", padx=4); r += 1

        def submit():
            uname = uname_e.get().strip()
            pwd   = pwd_e.get().strip()
            if not uname:
                messagebox.showerror("Error", "Name is required."); return
            mode = mode_var.get()
            if mode == "New User":
                if not pwd:
                    messagebox.showerror("Error", "Password is required for new users."); return
                USERS[uname] = {"password": hashlib.sha256(pwd.encode()).hexdigest(),
                                 "is_admin": admin_var.get(), "active": active_var.get()}
                messagebox.showinfo("Success", f"User '{uname}' created.")
            else:
                if uname not in USERS:
                    messagebox.showerror("Error", "User not found."); return
                if pwd:
                    USERS[uname]["password"] = hashlib.sha256(pwd.encode()).hexdigest()
                USERS[uname]["is_admin"] = admin_var.get()
                USERS[uname]["active"]   = active_var.get()
                messagebox.showinfo("Success", f"User '{uname}' updated.")
            self.show_confirmation()

        btn_row = ttk.Frame(f)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirm", command=submit,               width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Cancel",  command=self.show_maintenance, width=14).pack(side="left", padx=6)
        ttk.Button(btn_row, text="← Back",  command=self.show_maintenance, width=14).pack(side="left", padx=6)

    # ══════════════════════════════════════════
    #  UTILITY SCREENS
    # ══════════════════════════════════════════

    def show_confirmation(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(expand=True)
        ttk.Label(f, text="✅ Transaction completed successfully.",
                  font=("Arial", 13), foreground="green").pack(pady=20)
        ttk.Button(f, text="Home",    command=self.go_home).pack(pady=4)
        ttk.Button(f, text="Log Out", command=self.logout).pack(pady=4)

    def show_logout(self):
        self.clear()
        f = styled_frame(self.container)
        f.pack(expand=True)
        ttk.Label(f, text="You have successfully logged out.",
                  font=("Arial", 13)).pack(pady=20)
        ttk.Button(f, text="Admin Login", command=lambda: self.show_login("admin")).pack(pady=4)
        ttk.Button(f, text="User Login",  command=lambda: self.show_login("user")).pack(pady=4)


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = LibraryApp(root)
    root.mainloop()