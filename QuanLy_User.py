import json
import os
from DuLieu import User

class QuanLyUser:
    def __init__(self):
        self.UserList = []
        self.usersFile = 'users.json'
        self.loadData()
        
    def loadData(self):
        # Tạo file mặc định nếu chưa tồn tại
        if not os.path.exists(self.usersFile) or os.path.getsize(self.usersFile) == 0:
            admin_user = [{
                'username': 'admin',
                'password': 'admin',
                'role': 'Quản Lý',
                'permission': True
            }]
            with open(self.usersFile, "w", encoding="utf-8") as file:
                json.dump(admin_user, file, indent=4, ensure_ascii=False)
        
        # Load dữ liệu từ file
        try:
            with open(self.usersFile, "r", encoding="utf-8") as file:
                users_data = json.load(file)
                self.UserList = [User(user["username"], user["password"], user["role"], user["permission"]) for user in users_data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError(f"Lỗi khi đọc dữ liệu từ file JSON: {e}")
            self.UserList = []
        
        return self.UserList
    
    def saveData(self):
        try: 
            with open(self.usersFile, "w", encoding="utf-8") as file:
                users_data = [{"username": user.username, "password": user.password, "role": user.role, "permission": user.permission} for user in self.UserList]
                json.dump(users_data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Lỗi khi lưu dữ liệu vào file JSON: {e}")
    
    def addUser(self, user):
        # Kiểm tra trùng lặp
        for u in self.UserList:
            if u.username == user.username:
                raise ValueError("Tài khoản đã tồn tại.")
        
        self.UserList.append(user)
        self.saveData()
    
    def removeUser(self, username):
        original_count = len(self.UserList)
        self.UserList = [user for user in self.UserList if user.username != username]
        
        if len(self.UserList) == original_count:
            raise ValueError("Tài khoản không tồn tại.")
        
        self.saveData()
    
    def updateUser(self, username, new_data):
        found = False
        for user in self.UserList:
            if user.username == username:
                user.password = new_data.get("password", user.password)
                user.role = new_data.get("role", user.role)
                user.permission = new_data.get("permission", user.permission)
                found = True
                break
        
        if not found:
            raise ValueError("Tài khoản không tồn tại.")
        
        self.saveData()
    
    def getUser(self, username):
        for user in self.UserList:
            if user.username == username:
                return user
        return None
    
    def kiemTraQuyen(self, username, password, role):
        try:
            with open(self.usersFile, "r", encoding="utf-8") as f:
                users_data = json.load(f)
                for user in users_data:
                    if (user["username"] == username and 
                        user["password"] == password and 
                        user["role"] == role):
                        return User(user["username"], user["password"], user["role"], user.get("permission", False))
            return None
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Lỗi khi đọc file users: {e}")
            return None