import datetime

class Product:
    def __init__(self, code: int, name: str, description: str, price: float):
        self._code = code
        self._name = name
        self._description = description
        self._price = price

    def get_info(self):
        return (self._code, self._name, self._description, self._price)


class Warehouse:
    def __init__(self, product_code: int, quantity: int):
        self._product_code = product_code
        self._quantity = quantity

    def get_info(self):
        return (self._product_code, self._quantity)


class Client:
    def __init__(self, code: int, fullname: str, address: str, phone: str):
        self._code = code
        self._fullname = fullname
        self._address = address
        self._phone = phone

    def get_info(self):
        return (self._code, self._fullname, self._address, self._phone)


class Order:
    def __init__(self, order_number: int, date_time: str, client_code: int, items: list, cost: float):
        self._order_number = order_number
        self._date_time = date_time
        self._client_code = client_code
        self._items = items  
        self._cost = cost

    def get_info(self):
        return (self._order_number, self._date_time, self._client_code, self._items, self._cost)


class Store:
    def __init__(self):
        self._products = {}     
        self._warehouse = {}    
        self._clients = {}      
        self._orders = []       

    def add_product(self, product: Product):
        self._products[product._code] = product
        if product._code not in self._warehouse:
            self._warehouse[product._code] = Warehouse(product._code, 0)

    def add_to_warehouse(self, product_code: int, quantity: int):
        if product_code in self._warehouse:
            self._warehouse[product_code]._quantity += quantity
        else:
            self._warehouse[product_code] = Warehouse(product_code, quantity)

    def add_client(self, client: Client):
        self._clients[client._code] = client

    def get_products(self):
        return self._products.values()

    def get_warehouse_info(self):
        result = []
        for p_code, wh in self._warehouse.items():
            product = self._products.get(p_code)
            product_name = product._name if product else "Невідомий товар"
            result.append((p_code, product_name, wh._quantity))
        return result

    def get_clients(self):
        return self._clients.values()

    def create_order(self, client_code: int, items: list):
        total_cost = 0.0
        
        for p_code, qty in items:
            if p_code not in self._warehouse or self._warehouse[p_code]._quantity < qty:
                raise ValueError(f"Немає або недостатньо товару з кодом {p_code} на складі!")
            product = self._products[p_code]
            total_cost += product._price * qty


        for p_code, qty in items:
            self._warehouse[p_code]._quantity -= qty

        order_number = len(self._orders) + 1
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        new_order = Order(order_number, date_time, client_code, items, total_cost)
        self._orders.append(new_order)
        return new_order