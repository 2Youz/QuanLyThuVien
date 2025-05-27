import json
import os
from DuLieu import ThuThu

class QuanLyThuThu:
    def __init__(self):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha
        # Danh sách thủ thư
        self.ThuThuList = []  # Danh sách thủ thư
        self.thuthuFile = 'thuthu.json'  # Tên file lưu trữ danh sách thủ thư
        self.loadData()  # Tải dữ liệu từ file JSON vào danh sách thủ thư
    
    def loadData(self):
        if not os.path.exists(self.thuthuFile) or os.path.getsize(self.thuthuFile) == 0:
            self.ThuThuList = []
            return
        try:
            with open(self.thuthuFile, "r", encoding="utf-8") as file:
                thuthuData = json.load(file)
                self.ThuThuList = []  # Clear existing data
                for tt in thuthuData:
                    # Validate required fields
                    required_fields = ['staffID', 'staffName', 'phone', 'email', 'address', 'shift', 'salary']
                    if not all(field in tt for field in required_fields):
                        print(f"Dữ liệu thiếu trường bắt buộc: {tt}")
                        continue
                
                    t = ThuThu(
                        tt['staffID'],
                        tt['staffName'],
                        tt['phone'],
                        tt['email'],
                        tt['address'],
                        tt['shift'],
                        tt['salary']
                    )
                    self.ThuThuList.append(t)
            print(f"Đã tải {len(self.ThuThuList)} thủ thư từ file.")
        except json.JSONDecodeError as e:
            print(f"Lỗi khi đọc dữ liệu từ file JSON: {e}")
            self.ThuThuList = []
        except FileNotFoundError:
            print(f"File {self.thuthuFile} không tồn tại, tạo danh sách mới.")
            self.ThuThuList = []
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            self.ThuThuList = []
    
    def saveData(self):
        try:
        # Tạo thư mục nếu chưa tồn tại
            dir_path = os.path.dirname(self.thuthuFile) 
            if dir_path:  # Chỉ tạo nếu có đường dẫn thư mục
                os.makedirs(dir_path, exist_ok=True)
        
            with open(self.thuthuFile, "w", encoding="utf-8") as file:
                thuthuData = [tt.to_dict() for tt in self.ThuThuList]
                json.dump(thuthuData, file, indent=4, ensure_ascii=False)
            print(f"Đã lưu {len(self.ThuThuList)} thủ thư vào file.")
        except PermissionError:
            print("Không có quyền ghi file.")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào file JSON: {e}")
    
    # Thêm thủ thư mới
    def addThuThu(self, thuthu):
        for tt in self.ThuThuList:
            if tt.staffID == thuthu.staffID:
                raise ValueError("Mã thủ thư đã tồn tại.")
        self.ThuThuList.append(thuthu)
        self.saveData()
        print("Thêm thủ thư thành công!")
    
    # Xóa thủ thư theo mã thủ thư
    def removeThuThu(self, staffID):
        before_count = len(self.ThuThuList)
        self.ThuThuList = [tt for tt in self.ThuThuList if tt.staffID != staffID]
        
        if len(self.ThuThuList) == before_count:
            raise ValueError("Mã thủ thư không tồn tại.")
        
        self.saveData()
        print("Xóa thủ thư thành công!")
    
    # Cập nhật thông tin thủ thư
    def updateThuThu(self, staffID, new_thuthu):
        for i, tt in enumerate(self.ThuThuList):
            if tt.staffID == staffID:
                self.ThuThuList[i] = new_thuthu
                self.saveData()
                print("Cập nhật thủ thư thành công!")
                return
        raise ValueError("Mã thủ thư không tồn tại.")
    
    # Lấy thủ thư theo mã thủ thư
    def getThuThuByID(self, staffID):
        for tt in self.ThuThuList:
            if tt.staffID == staffID:
                return tt
        return None  # Trả về None thay vì raise Exception
    
    # Lấy tất cả thủ thư
    def getAllThuThu(self):
        return self.ThuThuList
    
    # Tìm kiếm thủ thư theo từ khóa
    def searchThuThu(self, keyword):
        if not keyword or not keyword.strip():
            return []
    
        keyword_lower = keyword.lower().strip()
        results = []
        for tt in self.ThuThuList:
            # Tìm kiếm trong nhiều trường - có xử lý safe hơn
            search_fields = [
                str(tt.staffName).lower(),
                str(tt.staffID).lower(), 
                str(tt.phone),  # Không cần lower vì phone là số
                str(tt.email).lower()
            ]
            if any(keyword_lower in field for field in search_fields):
                results.append(tt)
        return results
    
    # Đếm tổng số thủ thư
    def countThuThu(self):
        return len(self.ThuThuList)
    
    # Lấy danh sách thủ thư theo ca làm việc
    def getThuThuByShift(self, shift):
        return [tt for tt in self.ThuThuList if tt.shift.lower() == shift.lower()]