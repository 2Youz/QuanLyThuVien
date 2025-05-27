import json
import os
from DuLieu import ThuThu

class QuanLyThuThu:
    def __init__(self):
        self.ThuThuList = []
        self.thuthuFile = 'thuthu.json'
        self.loadData()
    
    def loadData(self):
        if not os.path.exists(self.thuthuFile) or os.path.getsize(self.thuthuFile) == 0:
            return
        try:
            with open(self.thuthuFile, "r", encoding="utf-8") as file:
                thuthuData = json.load(file)
                for tt in thuthuData:
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
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError(f"Lỗi khi đọc file: {e}")
            self.ThuThuList = []
    
    def saveData(self):
        try:
            with open(self.thuthuFile, "w", encoding="utf-8") as file:
                thuthuData = [tt.to_dict() for tt in self.ThuThuList]
                json.dump(thuthuData, file, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Lỗi khi lưu dữ liệu: {e}")
    
    def addThuThu(self, thuthu):
        for tt in self.ThuThuList:
            if tt.staffID == thuthu.staffID:
                raise ValueError("Mã thủ thư đã tồn tại.")
        self.ThuThuList.append(thuthu)
        self.saveData()
    
    def removeThuThu(self, staffID):
        before_count = len(self.ThuThuList)
        self.ThuThuList = [tt for tt in self.ThuThuList if tt.staffID != staffID]
        
        if len(self.ThuThuList) == before_count:
            raise ValueError("Mã thủ thư không tồn tại.")
        
        self.saveData()
    
    def updateThuThu(self, staffID, new_thuthu):
        for i, tt in enumerate(self.ThuThuList):
            if tt.staffID == staffID:
                self.ThuThuList[i] = new_thuthu
                self.saveData()
                return
        raise ValueError("Mã thủ thư không tồn tại.")
    
    def getThuThuByID(self, staffID):
        for tt in self.ThuThuList:
            if tt.staffID == staffID:
                return tt
        return None
    
    def searchThuThu(self, keyword):
        results = []
        keyword_lower = keyword.lower()
        for tt in self.ThuThuList:
            if (
                keyword_lower in tt.staffID.lower() or
                keyword_lower in tt.staffName.lower() or 
                keyword_lower in tt.address.lower() or
                keyword_lower in tt.shift.lower() or 
                keyword_lower in tt.phone or 
                keyword_lower in tt.email.lower() 
                ):
                results.append(tt)
        return results