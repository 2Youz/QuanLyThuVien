import tkinter as tk
from tkinter import messagebox, ttk
from DuLieu import User
from QuanLy_User import QuanLyUser
import re
class GiaoDienUser(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Quản Lý Người Dùng")
        self.ql_user = QuanLyUser() 
        self.GiaoDien()
        self.tailaiDuLieu()
        
    def GiaoDien(self):
        tk.Label(self, text="Tên đăng nhập:").place(x=20, y=20)
        tk.Label(self, text="Mật khẩu:").place(x=20, y=60)
        tk.Label(self, text="Chức vụ:").place(x=20, y=100)
    
        self.tenDN = tk.StringVar()
        self.matKhau = tk.StringVar()
        self.chucVu = tk.StringVar()
    
        tk.Entry(self, textvariable=self.tenDN).place(x=120, y=20, width=200)
        tk.Entry(self, textvariable=self.matKhau, show="*").place(x=120, y=60, width=200)
    
        self.cbChucVu = ttk.Combobox(self, textvariable=self.chucVu, values=["Thủ Thư", "Quản Lý"], state="readonly")
        self.cbChucVu.place(x=120, y=100, width=200)
        self.cbChucVu.set("Thủ Thư")
    
        tk.Button(self, text="Thêm", command=self.add).place(x=350, y=20, width=100)
        tk.Button(self, text="Sửa", command=self.update).place(x=350, y=50, width=100)
        tk.Button(self, text="Xóa", command=self.remove).place(x=350, y=80, width=100)
        tk.Button(self, text="Làm mới", command=self.clear).place(x=350, y=110, width=100)
    
        self.tree = ttk.Treeview(self, columns=("username", "password", "role"), show="headings")
        self.tree.heading("username", text="Tên đăng nhập")
        self.tree.column("username", width=150)
        self.tree.heading("password", text="Mật khẩu")
        self.tree.column("password", width=150)
        self.tree.heading("role", text="Chức vụ")
        self.tree.column("role", width=100)
        self.tree.place(x=20, y=150, width=430, height=250)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
    def tailaiDuLieu(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for user in self.ql_user.UserList:
            self.tree.insert("", "end", values=(user.username, user.password, user.role))
            
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.tenDN.set(values[0])
            self.matKhau.set(values[1])
            self.chucVu.set(values[2])
            
    def add(self):
        try:
            username = self.tenDN.get().strip()
            password = self.matKhau.get().strip()
            role = self.chucVu.get()
            
            if not username:
                messagebox.showerror("Lỗi","Tên đăng nhập không được để trống.")
                return
            if not password:
                messagebox.showerror("Lỗi","Mật khẩu không được để trống.")
                return
            if len(password) < 6:
                messagebox.showerror("Lỗi","Mật khẩu phải có ít nhất 6 ký tự")
                return
            if not re.match(r"^[a-zA-Z0-9_]+$", username):
                messagebox.showerror("Lỗi", "Tên đăng nhập không được chứa ký tự đặc biệt")
                return
            if len(username) < 6:
                messagebox.showerror("Lỗi", "Tên đăng nhập phải có ít nhất 6 ký tự")
                return
            user = User(username, password, role, role == "Quản Lý")
            self.ql_user.addUser(user)
            messagebox.showinfo("Thông báo", "Thêm người dùng thành công!")
            self.clear()
            self.tailaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

            
    def remove(self):
        username = self.tenDN.get().strip()
        if not username:
            messagebox.showerror("Lỗi", "Vui lòng chọn người dùng để xóa.")
            return
            
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa người dùng '{username}'?"):
            try:
                self.ql_user.removeUser(username)
                messagebox.showinfo("Thông báo", "Xóa người dùng thành công!")
                self.clear()
                self.tailaiDuLieu()
            except Exception as e:
                raise ValueError(f"Lỗi: {e}")
                
    def update(self):
        username = self.tenDN.get().strip()
        if not username:
            messagebox.showerror("Lỗi", "Vui lòng chọn người dùng để cập nhật.")
            return
            
        try:
            self.ql_user.updateUser(username, {
                "password": self.matKhau.get().strip(),
                "role": self.chucVu.get(),
                "permission": self.chucVu.get() == "Quản Lý"
            })
            messagebox.showinfo("Thông báo", "Cập nhật người dùng thành công!")
            self.clear()
            self.tailaiDuLieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            
    def clear(self):
        self.tenDN.set("")
        self.matKhau.set("")
        self.chucVu.set("Thủ Thư")