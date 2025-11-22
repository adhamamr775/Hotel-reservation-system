import random
from abc import ABC, abstractmethod

# Abstract class for different payment methods
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# Represents a customer using the system
class Customer:
    def __init__(self, name, email, phone):
        self.__id = id(self)
        self.__name = name
        self.__email = email
        self.__phone = phone

    def get_details(self):
        return f"Customer: {self.__name}, Email: {self.__email}, Phone: {self.__phone}"

    def __str__(self):
        return f"{self.__name} | Email: {self.__email} | Phone: {self.__phone}"

# Represents a hotel room
class Room:
    def __init__(self, room_number, price, room_type):
        self.room_number = room_number
        self.price = price
        self.room_type = room_type
        self.is_booked = False

    def get_room_info(self):
        return f"Room {self.room_number} ({self.room_type}): ${self.price}/night"

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type}) - ${self.price}/night"

# A subclass for VIP rooms, with added features
class VIPRoom(Room):
    def __init__(self, room_number, price):
        super().__init__(room_number, price, "VIP")


    def get_room_info(self):
        return super().get_room_info()

# Payment using credit card
class CreditCardPayment(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processed ${amount} via Credit Card"

# Payment using cash
class CashPayment(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processed ${amount} via Cash"

# Represents a booking made by a customer
class Booking:
    def __init__(self, customer, room, days, payment_processor):
        self.customer = customer
        self.room = room
        self.days = days
        self.payment_processor = payment_processor
        self.total_amount = self.calculate_amount()

    def calculate_amount(self):
        return self.days * self.room.price

    def confirm_booking(self):
        if not self.room.is_booked:
            self.room.is_booked = True
            payment_result = self.payment_processor.process_payment(self.total_amount)
            return f"\nBooking Confirmed!\n{self.customer}\n{self.room}\nDays: {self.days}\nTotal: ${self.total_amount}\n{payment_result}"
        return "Room is already booked"

    def __str__(self):
        return f"Booking for {self.customer} in {self.room} for {self.days} days. Total = ${self.total_amount}"

# Represents a hotel with rooms and bookings
class Hotel:
    def __init__(self, name, room_prices):
        self.name = name
        self.rooms = []
        self.bookings = []
        self.room_prices = room_prices
        self.add_rooms()

    def add_rooms(self):
        room_types = ['Single', 'Double', 'Standard', 'VIP']
        for room_type in room_types:
            price = self.room_prices[room_type]
            room_number = random.randint(1, 200)
            if room_type == "VIP":
                self.rooms.append(VIPRoom(room_number, price))
            else:
                self.rooms.append(Room(room_number, price, room_type))

    def find_available_room(self, room_type):
        for room in self.rooms:
            if room.room_type.lower() == room_type.lower() and not room.is_booked:
                return room
        return None

    def create_booking(self, customer, room_type, days, payment_type):
        room = self.find_available_room(room_type)
        if not room:
            return "No available rooms of this type."

        payment_processor = CreditCardPayment() if payment_type.lower() == "visa" else CashPayment()
        booking = Booking(customer, room, days, payment_processor)
        self.bookings.append(booking)
        return booking.confirm_booking()

# Main program starts here
if __name__ == "__main__":
    hotels_info = {
        "Marriott Mena House Cairo": {'Single': 299, 'Double': 349, 'Standard': 399, 'VIP': 499},
        "Four Seasons Hotel Cairo": {'Single': 365, 'Double': 415, 'Standard': 465, 'VIP': 565},
        "Sofitel Old Cataract Aswan": {'Single': 446, 'Double': 490, 'Standard': 525, 'VIP': 600},
        "Steigenberger Alcazar": {'Single': 149, 'Double': 179, 'Standard': 199, 'VIP': 249},
        "Kempinski Nile Hotel": {'Single': 174, 'Double': 204, 'Standard': 234, 'VIP': 284},
        "Sofitel Winter Palace Luxor": {'Single': 379, 'Double': 429, 'Standard': 459, 'VIP': 519},
    }

    hotels = [Hotel(name, prices) for name, prices in hotels_info.items()]

    print("\n🏨 Welcome to Egypt Hotel Booking System 🏨")

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    customer = Customer(name, email, phone)

    print("\nAvailable Hotels:")
    for idx, hotel in enumerate(hotels):
        print(f"{idx+1}. {hotel.name}")

    hotel_choice = int(input("Choose a hotel (1-6): ")) - 1
    selected_hotel = hotels[hotel_choice]

    print("\nAvailable Room Types:")
    print("1. Single")
    print("2. Double")
    print("3. Standard")
    print("4. VIP")

    room_choice = int(input("Choose a room type (1-4): "))
    room_types = ["Single", "Double", "Standard", "VIP"]
    room_type = room_types[room_choice - 1]

    days = int(input("Enter the number of days: "))

    print("\nPayment Methods:")
    print("1. Visa")
    print("2. Cash")

    payment_choice = int(input("Choose payment method (1 for Visa, 2 for Cash): "))
    payment_type = "visa" if payment_choice == 1 else "cash"

    print("\nProcessing your booking...")
    result = selected_hotel.create_booking(customer, room_type, days, payment_type)
    print(result)
