import json
import os
from DuLieu import User

class QuanLyUser:
    def __init__(self):
        self.UserList = [] #Danh sách người dùng
        self.usersFile = 'users.json' #Tên file lưu trữ danh sách người dùng
        self.loadData() #Tải dữ liệu từ file JSON vào danh sách người dùng
    def loadData(self):
        if not os.path.exists(self.usersFile) or os.path.getsize(self.usersFile) == 0:
            admin_user = [{
                'username': 'admin',
                'password': 'admin',
                'role': 'Quản Lý',
                'permission': True
            }]
            with open(self.usersFile, "w", encoding = "utf-8") as file:
                json.dump(admin_user, file, indent = 4,ensure_ascii= False)
        # load dữ liệu từ file JSON
        if os.path.exists(self.usersFile):
            try:
                with open(self.usersFile, "r", encoding= "utf-8") as file:
                    UsersData = json.load(file)
                    self.UserList = [User(user["username"], user["password"], user["role"], user["permission"]) for user in UsersData]
            except json.JSONDecodeError as e:
                print(f"Lỗi khi đọc dữ liệu từ file JSON: {e}")
                self.UserList = []
        else:
            print(f"File {self.usersFile} không tồn tại.")
            self.UserList = []
        return self.UserList
    def saveData(self):
        # Lưu dữ liệu vào file users.json
        try: 
            with open(self.usersFile, "w", encoding= "utf-8") as file:
                usersData = [{"username": user.username, "password": user.password, "role": user.role, "permission": user.permission} for user in self.UserList]
                json.dump(usersData, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào file JSON: {e}")
    # Thêm người dùng mới
    def addUser(self, user):
        users = self.loadData()
        for u in users:
            if u.username == user.username:
                raise ValueError("Tài khoản đã tồn tại.")
        self.UserList.append(user)
        self.saveData()
    # Xóa người dùng theo tên đăng nhập
    def removeUser(self, username):
        users = self.loadData()
        new_users = [user for user in users if user.username != username]
        if len(new_users) == len(users):
            raise ValueError("Tài khoản không tồn tại.")
        self.UserList = new_users
        self.saveData()
    # Cập nhật thông tin người dùng
    def updateUser(self, username, new_user):
        users = self.loadData()
        found = False
        for u in users:
            if u.username == username:
                u.password = new_user.get("password", u.password)
                u.role = new_user.get("role", u.role)
                u.permission = new_user.get("permission", u.permission)
                found = True
                break
        if not found:
            raise ValueError("Tài khoản không tồn tại.")
        self.UserList = users
        self.saveData()
    # Lấy thông tin người dùng theo tên đăng nhập
    def getUser(self, username):
        users = self.loadData()
        for u in users:
            if u.username == username:
                return u
        return None
    # Kiểm tra quyền truy cập của người dùng
    def kiemTraQuyen(self, username, password, role):
        try:
            with open(self.usersFile, "r", encoding="utf-8") as f:
                ds_user = json.load(f)
                for u in ds_user:
                    if (u["username"] == username and 
                        u["password"] == password and 
                        u["role"] == role):
                        quyen = u.get("permission", False)
                        return User(u["username"], u["password"], u["role"], quyen)
            return None
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Lỗi khi đọc file users: {e}")
            return None
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            return None