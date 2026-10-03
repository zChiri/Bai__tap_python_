import csv
import json 
from datetime import datetime

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
        
        if not config:
            raise ValueError
        return config
    
    except FileNotFoundError:
        print("[ERROR-01] Không tìm thấy file 'config.json'.")
        return None
    except (json.JSONDecodeError, ValueError, KeyError):
        print("[ERROR-02] File 'config.json' rỗng hoặc sai định dạng.")
        return None

def load_menu(filename):
    menu = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            if not reader.fieldnames:
                raise ValueError
        
            required_columns = ["id", "name", "category", "price"]
            for column in required_columns:
                if column not in reader.fieldnames:
                    raise ValueError
            
            for row in reader:
                if not row["id"] or not row["name"] or not row["category"]:
                    raise ValueError
            
                price = int(row["price"])
                if price < 0:
                    raise ValueError
            
                item = {
                    "id": row["id"],
                    "name": row["name"],
                    "category": row["category"],
                    "price": price
                }
                menu.append(item)
        
            if len(menu) == 0:
                raise ValueError
        
        return menu

    except FileNotFoundError:
        print(f"[ERROR-01] Không tìm thấy file '{filename}'.")
        return None
    except (ValueError, KeyError):
        print(f"[ERROR-02] File '{filename}' rỗng hoặc sai định dạng.")
        return None 
    
def load_orders(filename):
    orders = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                
                if len(parts) != 4:
                    continue
                
                try:
                    order = {
                        "time": parts[0].strip(),
                        "order_id": parts[1].strip(),
                        "items": parts[2].strip(),
                        "total": int(parts[3].strip())
                    }
                    
                    if order["order_id"] == "" or order["items"] == "":
                        continue
                    
                    orders.append(order)
                except ValueError:
                    continue
    
    except FileNotFoundError:
        pass
    return orders

def show_menu(menu):
    print("\n" + "=" * 58)
    print(f"{'MÃ':<8}{'TÊN MÓN':<25}{'NHÓM':<12}{'ĐƠN GIÁ':>13}")
    print("-" * 58)

    for item in menu:
        print(f"{item['id']:<8}{item['name']:<25}{item['category']:<12}{item['price']:>13,}")

    print("-" * 58)
    print("Tổng số món:", len(menu))
           

def main():
    config = load_config()

    if config is None:
        return

    try:
        menu_filename = config["files"]["menu"]
        orders_filename = config["files"]["orders"]

        menu = load_menu(menu_filename)
        if menu is None:
            return

        orders = load_orders(orders_filename)

    except KeyError:
        print("[ERR-02] File 'config.json' rỗng hoặc sai định dạng.")
        return

    while True:
        print("\n==========", config["shop_name"].upper(), "==========")
        print("1. Xem thực đơn")
        print("2. Tìm món theo mã")
        print("3. Tạo đơn hàng")
        print("4. Xem lịch sử đơn hàng")
        print("5. Xuất báo cáo doanh thu")
        print("0. Thoát")
        print("=" * 40)

        try:
            choice = int(input("Chọn chức năng: "))
        except ValueError:
            print("[ERR-03] Dữ liệu nhập không hợp lệ. Vui lòng nhập số nguyên.")
            continue

        if choice == 1:
            show_menu(menu)
        
        elif choice == 0:
            print("Cảm ơn bạn đã sử dụng chương trình!")
            break
        else:
            print("[ERR-03] Dữ liệu nhập không hợp lệ. Vui lòng chọn từ 0 đến 5.")                