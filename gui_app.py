import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

#SQL Server connection settings 

SERVER = r"ALVIN"  
DRIVER = "{ODBC Driver 17 for SQL Server}"  

DATABASES = [
    ("Store_UnitedStates", "USA"),
    ("Store_UK", "United Kingdom"),
    ("Store_Japan", "Japan"),
]

TABLES = ["Customers", "Products", "Orders", "OrderItems", "Payments"]


USE_BOOTSTRAP = True
try:
    if USE_BOOTSTRAP:
        import ttkbootstrap as tb
        TKBase = tb.Window
    else:
        raise ImportError
except Exception:
    tb = None
    TKBase = tk.Tk


def connect(dbname: str):
    return pyodbc.connect(
        f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={dbname};Trusted_Connection=yes;"
    )


class App(TKBase):
    def __init__(self):
        super().__init__(themename="superhero" if tb else None) if tb else super().__init__()
        self.title("Global Store — DB Viewer")
        self.geometry("1120x720")
        self.minsize(960, 620)

        # state
        self.conn = None
        self.current_db = None
        self.current_table = None

        # UI
        self._build_header()
        self._build_db_cards()
        self._build_table_row()
        self._build_grid()
        self._build_update_bar()
        self._build_statusbar()

    #Header 
    def _build_header(self):
        wrap = ttk.Frame(self, padding=(18, 16, 18, 8))
        wrap.pack(fill="x")
        ttk.Label(wrap, text="Global Store", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=12, pady=(8, 8))

    #Database cards
    def _build_db_cards(self):
        row = ttk.Frame(self, padding=(14, 0, 14, 4))
        row.pack(fill="x")

        for db_name, region_label in DATABASES:
            card = ttk.Frame(row, padding=12, relief="ridge", borderwidth=2)
            card.pack(side="left", expand=True, fill="x", padx=8)

            title = ttk.Label(card, text=db_name, font=("Segoe UI", 12, "bold"))
            subtitle = ttk.Label(card, text=f"Region: {region_label}")
            title.pack(anchor="w")
            subtitle.pack(anchor="w")

          
            for w in (card, title, subtitle):
                w.bind("<Button-1>", lambda e, db=db_name: self.on_connect(db))

            
            card.bind("<Enter>", lambda e, c=card: c.configure(relief="solid"))
            card.bind("<Leave>", lambda e, c=card: c.configure(relief="ridge"))

    #Table buttons 
    def _build_table_row(self):
        r = ttk.Frame(self, padding=(18, 8, 18, 6))
        r.pack(fill="x")
        ttk.Label(r, text="Tables:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 10))

        for t in TABLES:
            if tb:
                b = ttk.Button(r, text=t, command=lambda tbl=t: self.on_load_table(tbl), bootstyle="secondary-outline")
            else:
                b = ttk.Button(r, text=t, command=lambda tbl=t: self.on_load_table(tbl))
            b.pack(side="left", padx=6)

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=12, pady=(6, 6))

    #Data grid 
    def _build_grid(self):
        container = ttk.Frame(self, padding=(12, 0, 12, 6))
        container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(container, columns=(), show="headings")
        self.tree.pack(fill="both", expand=True)

        vs = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        hs = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vs.set, xscroll=hs.set)
        vs.pack(side="right", fill="y")
        hs.pack(side="bottom", fill="x")

    #Update Product Price 
    def _build_update_bar(self):
        bar = ttk.Frame(self, padding=(18, 6, 18, 6))
        bar.pack(fill="x")

        ttk.Label(bar, text="Update Product Price:", font=("Segoe UI", 10, "bold"))\
            .pack(side="left", padx=(0, 12))

        ttk.Label(bar, text="product_id").pack(side="left")
        self.ent_pid = ttk.Entry(bar, width=8)
        self.ent_pid.pack(side="left", padx=(4, 14))

        ttk.Label(bar, text="new price").pack(side="left")
        self.ent_price = ttk.Entry(bar, width=10)
        self.ent_price.pack(side="left", padx=(4, 14)),

        if tb:
            btn = ttk.Button(bar, text="Update", command=self.on_update_price, bootstyle="success")
        else:
            btn = ttk.Button(bar, text="Update", command=self.on_update_price)
        btn.pack(side="left", padx=(0, 10))

    #Status bar
    def _build_statusbar(self):
        self.status = tk.StringVar(value="Ready")
        self.conn_text = tk.StringVar(value="Not connected")

        s = ttk.Frame(self, padding=(18, 0, 18, 12))
        s.pack(fill="x")
        ttk.Label(s, textvariable=self.status, anchor="w").pack(side="left")
        ttk.Label(s, textvariable=self.conn_text, anchor="e").pack(side="right")

    #Actions
    def on_connect(self, dbname):
        try:
            if self.conn:
                try:
                    self.conn.close()
                except Exception:
                    pass

            self.conn = connect(dbname)
            self.current_db = dbname
            self.conn_text.set(f"Connected: {dbname}")
            self.status.set(f"Connected to {dbname}. Choose a table.")
          
        except Exception as e:
            self.conn_text.set("Not connected")
            self.status.set("Connection error")
            messagebox.showerror("Connection error", str(e))

    def on_load_table(self, table):
        if not self.conn:
            messagebox.showwarning("Not connected", "Click a database card first.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT TOP 100 * FROM dbo.{table}")
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Load error", str(e))
            return

        # Fill table grid
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, stretch=True)

        for r in rows:
            self.tree.insert("", "end", values=[str(x) for x in r])

        self.current_table = table
        self.status.set(f"{self.current_db} → {table} ({len(rows)} rows)")

    def on_update_price(self):
        if not self.conn:
            messagebox.showwarning("Not connected", "Connect to a database first.")
            return

        pid = self.ent_pid.get().strip()
        price = self.ent_price.get().strip()

        try:
            pid_i = int(pid)
        except ValueError:
            messagebox.showwarning("Input error", "product_id must be an integer.")
            return

        try:
            price_f = float(price)
        except ValueError:
            messagebox.showwarning("Input error", "price must be a number.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE dbo.Products SET price = ? WHERE product_id = ?", (price_f, pid_i))
            self.conn.commit()

            cur.execute("SELECT product_id, sku, name, price FROM dbo.Products WHERE product_id = ?", (pid_i,))
            row = cur.fetchone()

            if row:
                messagebox.showinfo("Success", "Product price updated successfully.")
                self.status.set(f"Updated product_id={pid_i} → price={price_f}")
                if self.current_table == "Products":
                    self.on_load_table("Products")
            else:
                messagebox.showwarning("Not found", f"No product with product_id={pid_i}")
        except Exception as e:
            messagebox.showerror("Update error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()
