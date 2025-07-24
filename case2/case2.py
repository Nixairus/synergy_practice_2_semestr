class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def make_sound(self):
        return "Какой-то звук"
    
    def get_info(self):
        return f"Имя: {self.name}, Возраст: {self.age}"
    
    def sleep(self):
        return f"{self.name} спит"

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    
    def make_sound(self):
        return "Гав-гав!"
    
    def fetch_ball(self):
        return f"{self.name} принес мячик"
    
    def get_info(self):
        return f"{super().get_info()}, Порода: {self.breed}"

class Cat(Animal):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    def make_sound(self):
        return "Мяу-мяу!"
    
    def climb_tree(self):
        return f"{self.name} залез на дерево"
    
    def get_info(self):
        return f"{super().get_info()}, Цвет: {self.color}"

# Демонстрация работы
if __name__ == "__main__":
    print("=== Демонстрация работы классов ===")
    
    # Создаем объекты
    animal = Animal("Животное", 5)
    dog = Dog("Бобик", 3, "Лабрадор")
    cat = Cat("Мурзик", 2, "Рыжий")
    
    # Тестируем методы базового класса
    print("\n--- Базовый класс Animal ---")
    print(animal.get_info())
    print(animal.make_sound())
    print(animal.sleep())
    
    # Тестируем методы производного класса Dog
    print("\n--- Производный класс Dog ---")
    print(dog.get_info())
    print(dog.make_sound())
    print(dog.sleep())
    print(dog.fetch_ball())
    
    # Тестируем методы производного класса Cat
    print("\n--- Производный класс Cat ---")
    print(cat.get_info())
    print(cat.make_sound())
    print(cat.sleep())
    print(cat.climb_tree()) 