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
           
def find_item(menu):
    code = input("Nhập mã món: ").strip().upper()

    for item in menu:
        if item["id"] == code:
            print(
                f"Mã: {item['id']} | Tên: {item['name']} | "
                f"Nhóm: {item['category']} | Giá: {item['price']:,} VND"
            )
            return

    print(f"[ERROR-04] Không tìm thấy món có mã '{code}'.")

def create_order(menu, config, orders):
    chosen_items = []
    subtotal = 0

    while True:
        code = input("Nhập mã món (Enter để kết thúc): ").strip().upper()

        if code == "":
            break

        found_item = None
        for item in menu:
            if item["id"] == code:
                found_item = item
                break

        if found_item is None:
            print(f"[ERROR-04] Không tìm thấy món có mã '{code}'.")
            continue

        # Nhap so luong va kiem tra du lieu
        while True:
            try:
                quantity = int(input("Số lượng: "))

                if quantity <= 0:
                    print("[ERROR-05] Số lượng phải là số nguyên dương. Vui lòng nhập lại.")
                else:
                    break
            except ValueError:
                print("[ERROR-05] Số lượng phải là số nguyên dương. Vui lòng nhập lại.")

        line_total = found_item["price"] * quantity
        subtotal += line_total

        chosen_items.append({
            "id": found_item["id"],
            "name": found_item["name"],
            "quantity": quantity
        })

        print(f"  + {found_item['name']} x{quantity} = {line_total:,}")

    if len(chosen_items) == 0:
        print("[ERROR-05] Đơn hàng chưa có món nào.")
        return

    # Tinh giam gia va VAT theo config.json
    discount = 0
    if subtotal >= config["discount_threshold"]:
        discount = round(subtotal * config["discount_rate"])

    after_discount = subtotal - discount
    vat = round(after_discount * config["vat_rate"])
    total = round(after_discount + vat)

    print("-" * 32)
    print(f"Tạm tính : {subtotal:>18,}")
    print(f"Giảm giá : {discount:>18,}")
    print(f"VAT ({config['vat_rate'] * 100:g}%) : {vat:>17,}")
    print(f"TỔNG CỘNG : {total:>17,} VND")

    # Tao ma don hang tiep theo
    order_number = len(orders) + 1
    order_id = f"HD{order_number:03d}"
    order_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Luu cac mon theo dang CF02x2, TR01x1
    item_text_list = []
    for item in chosen_items:
        item_text_list.append(f"{item['id']}x{item['quantity']}")
    item_text = ", ".join(item_text_list)

    # Ghi noi tiep vao file TXT
    order_line = f"{order_time} | {order_id} | {item_text} | {total}\n"

    try:
        with open(config["files"]["orders"], "a", encoding="utf-8") as file:
            file.write(order_line)
    except (OSError, KeyError):
        print("[ERROR-02] Không thể ghi file lịch sử đơn hàng.")
        return

    # Them vao danh sach trong bo nho
    new_order = {
        "time": order_time,
        "order_id": order_id,
        "items": item_text,
        "total": total
    }
    orders.append(new_order)

    print(f"[OK] Đã lưu đơn {order_id} vào {config['files']['orders']}")

def show_history(config, orders):
    # Doc lai file de cap nhat lich su moi nhat
    orders[:] = load_orders(config["files"]["orders"])

    if len(orders) == 0:
        print("[ERROR-06] Chưa có đơn hàng nào trong lịch sử.")
        return

    print("\n" + "-" * 62)
    print(f"{'MÃ ĐƠN':<10}{'THỜI GIAN':<24}{'CÁC MÓN':<20}{'TỔNG TIỀN':>12}")
    print("-" * 62)

    for order in orders:
        print(
            f"{order['order_id']:<10}{order['time']:<24}"
            f"{order['items']:<20}{order['total']:>12,}"
        )

    print("-" * 62)

def export_report(config, menu, orders):
    # Doc lai file de thong ke du lieu moi nhat
    orders = load_orders(config["files"]["orders"])

    if len(orders) == 0:
        print("[ERROR-06] Chưa có đơn hàng nào trong lịch sử.")
        return

    items_sold = {}

    # Dem so luong tung mon tu cac don hang
    for order in orders:
        item_parts = order["items"].split(",")

        for part in item_parts:
            part = part.strip()

            try:
                code, quantity_text = part.split("x")
                quantity = int(quantity_text)

                if quantity > 0:
                    if code not in items_sold:
                        items_sold[code] = 0
                    items_sold[code] += quantity
            except ValueError:
                # Bo qua mon co dinh dang sai
                continue

    # Tim mon ban nhieu nhat
    best_seller = None

    if len(items_sold) > 0:
        best_code = max(items_sold, key=items_sold.get)

        for item in menu:
            if item["id"] == best_code:
                best_seller = {
                    "id": item["id"],
                    "name": item["name"],
                    "quantity": items_sold[best_code]
                }
                break

    report = {
        "shop_name": config["shop_name"],
        "total_orders": len(orders),
        "total_revenue": sum(order["total"] for order in orders),
        "items_sold": items_sold,
        "best_seller": best_seller
    }

    try:
        with open(config["files"]["report"], "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2, ensure_ascii=False)

        print(
            f"[OK] Đã xuất báo cáo ra {config['files']['report']} "
            f"({report['total_orders']} đơn, doanh thu {report['total_revenue']:,} VND)"
        )
    except (OSError, KeyError):
        print("[ERROR-02] Không thể ghi file báo cáo.")


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
        print("[ERROR-02] File 'config.json' rỗng hoặc sai định dạng.")
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
            print("[ERROR-03] Dữ liệu nhập không hợp lệ. Vui lòng nhập số nguyên.")
            continue

        if choice == 1:
            show_menu(menu)
        elif choice == 2:
            find_item(menu)
        elif choice == 3:
            create_order(menu, config, orders)
        elif choice == 4:
            show_history(config, orders)
        elif choice == 5:
            export_report(config, menu, orders)
        elif choice == 0:
            print("Cảm ơn bạn đã sử dụng chương trình!")
            break
        else:
            print("[ERROR-03] Dữ liệu nhập không hợp lệ. Vui lòng chọn từ 0 đến 5.")                
if __name__ == "__main__":
   main()
