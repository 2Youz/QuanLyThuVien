import tkinter as tk
from QuanLy_User import QuanLyUser
from GiaoDien_DangNhap import GiaoDienDangNhap
if __name__ == "__main__":
    ql = QuanLyUser()
    root = tk.Tk()
    app = GiaoDienDangNhap(root, ql.kiemTraQuyen)
    app.pack(fill="both", expand=True)
    root.resizable(False, False)
    root.mainloop()