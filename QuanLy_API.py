import requests
from tkinter import messagebox

class APIBook:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def tim_kiem_sach(self, keyword, max_results=20):
        try:
            params = {
                'q': keyword,
                'maxResults': max_results,
                'printType': 'books'
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [self.extract_book_info(item) for item in data.get('items', []) if self.extract_book_info(item)]
            else:
                messagebox.showerror("Lỗi API", f"Mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Lỗi kết nối", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi không xác định", str(e))
        return []

    def extract_book_info(self, item):
        try:
            vi = item.get('volumeInfo', {})
            return {
                'id': item.get('id', ''),
                'title': vi.get('title', 'Không có tiêu đề'),
                'author': ', '.join(vi.get('authors', ['Không rõ tác giả'])),
                'category': vi.get('categories', ['Chung'])[0],
                'published_date': vi.get('publishedDate', 'Không rõ'),
                'isbn': next((i.get('identifier') for i in vi.get('industryIdentifiers', [])
                              if i.get('type') in ['ISBN_13', 'ISBN_10']), '')
            }
        except:
            return None

    def get_book_detail(self, book_id):
        try:
            response = requests.get(f"{self.base_url}/{book_id}", timeout=10)
            if response.status_code == 200:
                return self.extract_book_info(response.json())
            else:
                messagebox.showerror("Lỗi API", f"Lấy chi tiết thất bại: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Lỗi lấy chi tiết sách", str(e))
        return None
