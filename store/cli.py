import os
import pickle
from store import Store, Product, Client

def main():
    if os.path.isfile('store.data'):
        # Ініціалізація з файлу
        with open('store.data', 'rb') as file:
            store = pickle.load(file)
        print("Дані успішно завантажено з файлу.")
    else:
        store = Store()
        
        store.add_product(Product(1, "Ноутбук", "Ігровий ноутбук", 25000.0))
        store.add_product(Product(2, "Миша", "Бездротова миша", 750.0))
        store.add_to_warehouse(1, 5)
        store.add_to_warehouse(2, 20)

        # Додаємо початкового клієнта
        store.add_client(Client(1, "Іван Петренко", "м. Київ, вул. Хрещатик 1", "+380501234567"))
        print("Створено новий магазин із початковими даними.")

    while True:
        print("\n=== Команди магазину ===")
        print(" * add_product")
        print(" * add_to_warehouse")
        print(" * add_client")
        print(" * create_order")
        print(" * get_products")
        print(" * get_warehouse")
        print(" * get_clients")
        print(" * q (вихід та збереження)")
        
        option = input('Enter comand: ').lower().strip()

        if option == 'q':
            with open('store.data', 'wb') as file:
                pickle.dump(store, file)
            print("Зміни збережено. Програму завершено.")
            break

        elif option == 'add_product':
            try:
                code = int(input("Введіть код товару: "))
                name = input("Введіть назву товару: ")
                desc = input("Введіть опис товару: ")
                price = float(input("Введіть вартість товару: "))
                
                store.add_product(Product(code, name, desc, price))
                print("Товар успішно додано!")
            except ValueError:
                print("Помилка введення даних. Спробуйте ще раз.")

        elif option == 'add_to_warehouse':
            try:
                p_code = int(input("Введіть код товару: "))
                qty = int(input("Введіть кількість для додавання: "))
                store.add_to_warehouse(p_code, qty)
                print("Склад оновлено!")
            except ValueError:
                print("Помилка введення даних.")

        elif option == 'add_client':
            try:
                code = int(input("Введіть код клієнта: "))
                fullname = input("Введіть ПІБ клієнта: ")
                address = input("Введіть адресу: ")
                phone = input("Введіть номер телефону: ")
                
                store.add_client(Client(code, fullname, address, phone))
                print("Клієнта успішно додано!")
            except ValueError:
                print("Помилка введення даних.")

        elif option == 'get_products':
            print("\n--- Список товарів ---")
            for prod in store.get_products():
                info = prod.get_info()
                print(f"Код: {info[0]} | Назва: {info[1]} | Опис: {info[2]} | Ціна: {info[3]} грн")

        elif option == 'get_warehouse':
            print("\n--- Наявність товарів на складі ---")
            for item in store.get_warehouse_info():
                print(f"Код товару: {item[0]} | Назва: {item[1]} | Кількість: {item[2]} од.")

        elif option == 'get_clients':
            print("\n--- Список клієнтів ---")
            for client in store.get_clients():
                info = client.get_info()
                print(f"Код: {info[0]} | ПІБ: {info[1]} | Адреса: {info[2]} | Тел: {info[3]}")

        elif option == 'create_order':
            try:
                client_code = int(input("Введіть код клієнта: "))
                items = []
                while True:
                    p_code = input("Введіть код товару (або 'done' для завершення вибору): ")
                    if p_code.lower() == 'done':
                        break
                    qty = int(input("Введіть кількість: "))
                    items.append((int(p_code), qty))
                
                if items:
                    order = store.create_order(client_code, items)
                    print(f"Замовлення №{order._order_number} успішно створено! Загальна вартість: {order._cost} грн")
                else:
                    print("Замовлення не містить товарів.")
            except Exception as e:
                print(f"Помилка при створенні замовлення: {e}")

        else:
            print("Невідома команда. Спробуйте знову.")

if __name__ == '__main__':
    main()