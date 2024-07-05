class RestaurantSystem:
    def __init__(self):
        self.orders = {}
        self.tables = [0] * 10  
        self.order_id = 1

    def reserve_table(self, num_people):
        # Partición de equivalencias y valores límite
        if not (1 <= num_people <= 10):
            return "Error: Invalid number of people. Must be between 1 and 10."
        for i in range(len(self.tables)):
            if self.tables[i] == 0:
                self.tables[i] = num_people
                return f"Table {i + 1} reserved for {num_people} people."
        return "Error: No tables available."

    def create_order(self, table_number, order_details):
        if table_number < 1 or table_number > 10 or self.tables[table_number - 1] == 0:
            return "Error: Invalid or unreserved table."
        order = {
            'table': table_number,
            'details': order_details,
            'state': 'CREATED'
        }
        self.orders[self.order_id] = order
        self.order_id += 1
        return f"Order {self.order_id - 1} created."

    def update_order_state(self, order_id, new_state):
        # Transición de Estado
        valid_transitions = {
            'CREATED': ['PREPARING', 'CANCELLED'],
            'PREPARING': ['SERVED', 'CANCELLED'],
            'SERVED': ['PAID'],
            'CANCELLED': [],
            'PAID': []
        }
        if order_id not in self.orders:
            return "Error: Invalid order ID."
        current_state = self.orders[order_id]['state']
        if new_state in valid_transitions[current_state]:
            self.orders[order_id]['state'] = new_state
            return f"Order {order_id} state updated to {new_state}."
        else:
            return f"Error: Invalid state transition from {current_state} to {new_state}."

    def apply_discount(self, order_id, discount_code):
        # Tablas de decisiones
        discount_rates = {
            'WELCOME10': 0.10,
            'SUMMER20': 0.20,
            'VIP30': 0.30
        }
        if order_id not in self.orders:
            return "Error: Invalid order ID."
        if discount_code not in discount_rates:
            return "Error: Invalid discount code."
        order = self.orders[order_id]
        original_price = sum(item['price'] for item in order['details'])
        discount_rate = discount_rates[discount_code]
        discounted_price = original_price * (1 - discount_rate)
        return f"Original price: ${original_price:.2f}, Discounted price: ${discounted_price:.2f}"


restaurant_system = RestaurantSystem()

# Reservar una mesa
print(restaurant_system.reserve_table(4))  
print(restaurant_system.reserve_table(11))  

# Crear una orden
order_details = [{'item': 'Pizza', 'price': 10}, {'item': 'Soda', 'price': 2}]
print(restaurant_system.create_order(1, order_details))  

# Actualizar estado de la orden
print(restaurant_system.update_order_state(1, 'PREPARING'))  
print(restaurant_system.update_order_state(1, 'PAID'))  

# Aplicar descuento a la orden
print(restaurant_system.apply_discount(1, 'WELCOME10'))  
print(restaurant_system.apply_discount(1, 'INVALIDCODE'))  