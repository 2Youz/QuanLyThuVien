import tkinter as tk
from tkinter import messagebox, ttk
from GiaoDien_User import GiaoDienUser
from GiaoDien_API import GiaoDienAPI
from GiaoDien_TongHop import GiaoDienSachVaThuThu as GiaoDienTongHop
class GiaoDienChinh(tk.Frame):
    def __init__(self, master, user_login, on_logout_callback=None):
        super().__init__(master)
        self.master = master
        self.user_login = user_login
        self.on_logout_callback = on_logout_callback  # Callback để xử lý đăng xuất
        self.master.title("Quản Lý Thư Viện")
        self.master.geometry("1200x700")
        self.pack(fill="both", expand=True)

        # Sidebar trái
        self.sidebar = tk.Frame(self, bg="#2c3e50", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # chuyển đổi chuỗi thành hoa
        def to_uppercase(s):
            return s.upper() if isinstance(s, str) else s
        
        # Label chào mừng
        welcome_label = tk.Label(
            self.sidebar,
            text=f"CHÀO MỪNG {to_uppercase(self.user_login.username)}!",
            bg="#2c3e50", fg="white",
            font=("Arial", 12, "bold"),
            anchor="center",
            pady=20
        )
        welcome_label.pack(fill="x", pady=(20, 10))
        
        # Tạo Khung chính
        self.khungChinh = tk.Frame(self, bg="white", relief="ridge", bd=2)
        self.khungChinh.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.button_QuanLy()  # Gọi hàm để tạo nút Quản lý User
    
    # Tạo các nút trong sidebar
    def button_QuanLy(self):
        # Nút quản lý người dùng chỉ hiển thị nếu người dùng có quyền
        if self.user_login.permission:
            btn_user = tk.Button(
                self.sidebar,
                text = "Quản lý User",
                command = self.open_UserQuanLy,
                bg="#e74c3c",
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                pady=10
            )
            btn_user.pack(fill="x", padx=10, pady=5)
        # Nút tìm kiếm sách qua API chỉ hiển thị nếu người dùng có quyền
        btn_API = tk.Button(
            self.sidebar,
            text="Tìm Kiếm Sách Qua API",
            command= self.open_BookAPI,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=10
        )
        btn_API.pack(fill="x", padx=10, pady=5)
        # Nút quản lý sách và thủ thư
        btn_tonghop = tk.Button(
            self.sidebar,
            text="Quản lý Tổng hợp",
            command= self.open_TongHop,
            bg="#16a085",  # Màu xanh lá đậm
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=10 
        )
        btn_tonghop.pack(fill="x", padx=10, pady=5)
        # Nút đăng xuất - Sửa đổi command
        btn_logout = tk.Button(
            self.sidebar,
            text="Đăng Xuất",
            command=self.dang_xuat,  # Gọi hàm đăng xuất mới
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=10
        )
        btn_logout.pack(fill="x", padx=10, pady=5, side="bottom")
    
    # Hàm xử lý đăng xuất
    def dang_xuat(self):
        if self.on_logout_callback:
            self.on_logout_callback()  # Gọi callback để quay về màn hình đăng nhập
        else:
            self.master.quit()  # Fallback nếu không có callback

    # Xóa tất cả widget trong khung chính
    def xoa_KhungChinh(self):
        for widget in self.khungChinh.winfo_children():
            widget.destroy() 

    # Mở giao diện quản lý người dùng
    def open_UserQuanLy(self):
        # Xóa khung chính hiện tại
        win = tk.Toplevel(self.master)
        win.title("Quản Lý Người Dùng")
        win.geometry("480x450")
        win.configure(bg="white")
        win.transient(self.master)
        win.grab_set()
        GiaoDienUser(win)
        GiaoDienUser(win).pack(fill="both", expand=True)

    # Mở giao diện tìm kiếm sách qua API
    def open_BookAPI(self):
        win = tk.Toplevel(self.master)
        win.title("Tìm Kiếm Sách Qua API")
        win.geometry("700x400")
        win.configure(bg="white")
        win.transient(self.master)
        win.grab_set()
        GiaoDienAPI(win)
    # Mở giao diện quản lý sách và thủ thư
    def open_TongHop(self):
        self.xoa_KhungChinh()
        app_tonghop = GiaoDienTongHop(self.khungChinh, self.user_login)
        app_tonghop.pack(fill="both", expand=True)
        
# Chạy thử giao diện
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x700")  # Kích thước cửa sổ chính
    user_login = type('User', (object,), {
        'username': 'admin',
        'permission': True
    })()  # Tạo đối tượng người dùng giả lập
    app = GiaoDienChinh(root, user_login)
    app.pack(fill="both", expand=True)  # Hiển thị giao diện
    root.mainloop()  # Bắt đầu vòng lặp sự kiện của Tkinter