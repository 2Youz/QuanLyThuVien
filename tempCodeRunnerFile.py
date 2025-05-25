import tkinter as tk
from tkinter import messagebox, ttk
from DuLieu import User
from GiaoDien_Chinh import GiaoDienChinh
from QuanLy_User import QuanLyUser
class GiaoDienDangNhap(tk.Frame):
    def __init__(self, master, kiemTraQuyen):
        super().__init__(master)
        self.master = master
        self.kiemTraQuyen = kiemTraQuyen
        self.master.title("Đăng Nhập")
        self.GiaoDien()

    def GiaoDien(self):
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        # Căn giữa cửa sổ
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - 400) // 2
        y = (sh - 400) // 2
        self.master.geometry(f"400x400+{x}+{y}")

        self.pack(fill="both", expand=True)

        startX, startY = 50, 50

        tk.Label(self, text="Đăng Nhập", font=("Arial", 20, "bold")).place(x=0, y=startY, width=400, height=40)

        # Tên đăng nhập
        tk.Label(self, text="Tên đăng nhập:", anchor="w").place(x=startX, y=startY + 60)
        self.ten_dn = tk.StringVar()
        self.entry_ten_dn = tk.Entry(self, textvariable=self.ten_dn)
        self.entry_ten_dn.place(x=startX, y=startY + 85, width=300, height=30)

        # Mật khẩu
        tk.Label(self, text="Mật khẩu:", anchor="w").place(x=startX, y=startY + 125)
        self.mat_khau = tk.StringVar()
        self.entry_mat_khau = tk.Entry(self, textvariable=self.mat_khau, show="*")
        self.entry_mat_khau.place(x=startX, y=startY + 150, width=300, height=30)

        # Chức vụ
        tk.Label(self, text="Chức vụ:", anchor="w").place(x=startX, y=startY + 190)
        self.chuc_vu = tk.StringVar()
        self.combo_chuc_vu = ttk.Combobox(self, textvariable=self.chuc_vu, values=["Thủ Thư", "Quản Lý"], state="readonly")
        self.combo_chuc_vu.place(x=startX, y=startY + 215, width=300, height=30)
        self.combo_chuc_vu.set("Thủ Thư")

        # Nút đăng nhập
        tk.Button(self, text="Đăng nhập", command=self.DangNhap, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")
        ).place(x=startX + 50, y=startY + 270, width=200, height=40)

        # Tự động focus
        self.entry_ten_dn.focus_set()

        # Phím tắt chuyển focus
        self.entry_ten_dn.bind("<Return>", lambda e: self.entry_mat_khau.focus_set())
        self.entry_mat_khau.bind("<Return>", lambda e: self.DangNhap())  # <-- sửa dòng này
        self.combo_chuc_vu.bind("<Return>", lambda e: self.DangNhap())
        

    def DangNhap(self):
        username = self.ten_dn.get().strip()
        password = self.mat_khau.get().strip()
        role = self.chuc_vu.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        user = self.kiemTraQuyen(username, password, role)

        if user:
            messagebox.showinfo("Thành công", f"Đăng nhập thành công với vai trò: {role}")
            self.master.withdraw()

            new_win = tk.Toplevel(self.master)
            new_win.geometry("1000x600")
            new_win.title("Giao diện chính")

            app = GiaoDienChinh(new_win, user)
            app.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập, mật khẩu hoặc vai trò không đúng.")

# ======================
# Hàm kiểm tra mẫu
# ======================
def kiemTraQuyenMau(username, password, role):
    if username == "admin" and password == "admin" and role in ["Quản Lý"]:
        return User(username, password, role)
    return None

# ======================
# Chạy thử
# ======================
if __name__ == "__main__":
    ql = QuanLyUser()  # Tải dữ liệu người dùng từ file JSON
    root = tk.Tk()
    app = GiaoDienDangNhap(root, ql.kiemTraQuyen)
    app.pack(fill="both", expand=True)
    root.resizable(False, False)
    root.mainloop()
    
