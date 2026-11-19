import random

class MazeGame:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.player_pos = [0, 0]
        self.maze = self.generate_maze()
        self.visited = [[False] * m for _ in range(n)]
        self.revealed = [[None] * m for _ in range(n)]
        self.game_over = False
        self.shield_active = False  # активен ли щит
        
        # Стартовая комната
        self.maze[0][0] = 'empty'
        self.visited[0][0] = True
        self.revealed[0][0] = 'empty'
    
    def generate_maze(self):
        #Генерация лабиринта
        maze = []
        for i in range(self.n):
            row = []
            for j in range(self.m):
                row.append('empty')
            maze.append(row)
        
        maze[self.n-1][self.m-1] = 'exit'
        
        cells = [(i, j) for i in range(self.n) for j in range(self.m) 
                 if (i, j) != (0, 0) and (i, j) != (self.n-1, self.m-1)]
        random.shuffle(cells)
        
        elements = ['chest'] * 4 + ['trap'] * 3 + ['key'] * 2 + ['portal'] * 1
        for element, (i, j) in zip(elements, cells):
            maze[i][j] = element
            
        return maze
    
    def display_maze(self):
        #Отображение лабиринта 
        print("\n" + "="*50)
        shield_status = "ЩИТ АКТИВЕН" if self.shield_active else "нет"
        print(f"Здоровье: {self.health}/{self.max_health} | Щит: {shield_status}")
        print(f"Позиция: ({self.player_pos[0]}, {self.player_pos[1]})")
        print(f"Инвентарь: {self.inventory if self.inventory else 'пусто'}")
        print("="*50)
        
        symbols = {'empty': "⬜", 'chest': "📦", 'trap': "💀", 'key': "🔑", 'portal': "🌀", 'exit': "🚪"}
        
        for i in range(self.n):
            for j in range(self.m):
                if [i, j] == self.player_pos:
                    print("🧑", end=" ")
                elif not self.visited[i][j]:
                    print("⬛", end=" ")
                else:
                    print(symbols.get(self.revealed[i][j], "⬜"), end=" ")
            print()
        print("="*50)
        print("⬛ неизвестно | ⬜ пусто | 📦 сундук | 💀 ловушка")
        print("🔑 ключ | 🌀 портал | 🚪 выход")
        print("="*50)
    
    def move_player(self, direction):
        #Перемещение игрока
        new_pos = self.player_pos.copy()
        
        if direction == 'w':
            new_pos[0] -= 1
        elif direction == 's':
            new_pos[0] += 1
        elif direction == 'a':
            new_pos[1] -= 1
        elif direction == 'd':
            new_pos[1] += 1
        
        if 0 <= new_pos[0] < self.n and 0 <= new_pos[1] < self.m:
            self.player_pos = new_pos
            self.handle_room()
        else:
            print("Нельзя выйти за границы лабиринта")
    
    def handle_room(self):
        #Текущая комната
        i, j = self.player_pos
        
        if self.visited[i][j]:
            room = self.maze[i][j]
            print(f"\nВы вернулись в знакомую комнату: {self.room_name(room)}")
            return
        
        self.visited[i][j] = True
        room = self.maze[i][j]
        self.revealed[i][j] = room
        
        if room == 'chest':
            self.open_chest()
        elif room == 'trap':
            self.trigger_trap()
        elif room == 'key':
            self.pick_key()
        elif room == 'portal':
            self.use_portal()
        elif room == 'exit':
            self.reach_exit()
        else:
            print("\nПустая комната. Ничего интересного")
    
    def room_name(self, room):
        names = {'empty': 'пустая комната ⬜', 'chest': 'сундук 📦', 'trap': 'ловушка 💀', 'key': 'ключ 🔑', 'portal': 'портал 🌀', 'exit': 'выход 🚪'
        }
        return names.get(room, 'неизвестно')
    
    def open_chest(self):
        #Сундук
        items = ['зелье здоровья', 'щит']
        #Случайное количество предметов: 1 или 2
        count = random.randint(1, 2)
        found_items = [random.choice(items) for _ in range(count)]
        
        print(f"\nВы нашли сундук! Внутри: {', '.join(found_items)}")
        self.inventory.extend(found_items)
        print("Предметы добавлены в инвентарь")
        
        self.maze[self.player_pos[0]][self.player_pos[1]] = 'empty'
        self.revealed[self.player_pos[0]][self.player_pos[1]] = 'empty'
    
    def trigger_trap(self):
        #Ловушка
        base_damage = random.randint(15, 30)
        
        if self.shield_active:
            actual_damage = base_damage // 2  # щит уменьшает урон вдвое
            print(f"\n💀 Вы попали в ловушку! Урон: {base_damage}, но щит поглотил половину")
            print(f"Потеряно {actual_damage} здоровья (вместо {base_damage})")
            self.shield_active = False  # щит тратится
            print("Щит использован и больше не активен")
        else:
            actual_damage = base_damage
            print(f"\n💀 Вы попали в ловушку! Потеряно {actual_damage} здоровья")
        
        self.health -= actual_damage
        
        if self.health <= 0:
            print("☠️ Вы погибли!")
            self.game_over = True
        
        self.maze[self.player_pos[0]][self.player_pos[1]] = 'empty'
        self.revealed[self.player_pos[0]][self.player_pos[1]] = 'empty'
    
    def pick_key(self):
        #ключ
        print("\nВы нашли ключ!")
        self.inventory.append('ключ')
        print("Ключ добавлен в инвентарь")
        
        self.maze[self.player_pos[0]][self.player_pos[1]] = 'empty'
        self.revealed[self.player_pos[0]][self.player_pos[1]] = 'empty'
    
    def use_portal(self):
        #Портал
        print("\nВы нашли портал. Телепортация в случайное место...")
        
        empty_cells = [(i, j) for i in range(self.n) for j in range(self.m) 
                      if self.maze[i][j] == 'empty']
        
        if empty_cells:
            self.player_pos = list(random.choice(empty_cells))
            print(f"Вы телепортированы в позицию ({self.player_pos[0]}, {self.player_pos[1]})")
            self.handle_room()
    
    def reach_exit(self):
        #Выход
        if 'ключ' in self.inventory:
            print("\nПоздравляю! Вы нашли выход и у вас есть ключ!")
            print("🏆 Вы победили!")
            self.game_over = True
        else:
            print("\nВы нашли выход, но у вас нет ключа!")
            print("Найдите ключ, чтобы открыть дверь.")
    
    def use_health_potion(self):
        #Использование зелья здоровья
        if 'зелье здоровья' not in self.inventory:
            print("У вас нет зелья здоровья!")
            return False
        
        if self.health >= self.max_health:
            print("У вас уже максимальное здоровье!")
            return False
        
        heal_amount = 30
        old_health = self.health
        self.health = min(self.max_health, self.health + heal_amount)
        actual_heal = self.health - old_health
        
        self.inventory.remove('зелье здоровья')
        print(f"Вы выпили зелье здоровья. Восстановлено {actual_heal} HP")
        print(f"Здоровье: {self.health}/{self.max_health}")
        return True
    
    def use_shield(self):
        #Использование щита
        if 'щит' not in self.inventory:
            print("У вас нет щита!")
            return False
        
        if self.shield_active:
            print("Щит уже активен!")
            return False
        
        self.inventory.remove('щит')
        self.shield_active = True
        print("Вы активировали щит! Следующая ловушка нанесёт вдвое меньше урона.")
        return True
    
    def manage_inventory(self):
        #Управление инвентарём
        while True:
            print("\n" + "="*50)
            print("УПРАВЛЕНИЕ ИНВЕНТАРЁМ")
            print("="*50)
            print(f"Здоровье: {self.health}/{self.max_health}")
            shield_status = "ЩИТ АКТИВЕН" if self.shield_active else "нет"
            print(f"Щит: {shield_status}")
            print(f"Текущий инвентарь: {self.inventory if self.inventory else 'пусто'}")
            print("\n--- ИСПОЛЬЗОВАНИЕ ---")
            print("1. Выпить зелье здоровья 🧪")
            print("2. Активировать щит 🛡️")
            print("\n--- УПРАВЛЕНИЕ ---")
            print("3. Выбросить предмет (remove)")
            print("4. Выбросить последний предмет (pop)")
            print("5. Отсортировать инвентарь (sort)")
            print("6. Перевернуть инвентарь (reverse)")
            print("7. Найти предмет (index)")
            print("8. Проверить наличие предмета (in)")
            print("9. Выход")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == '1':
                self.use_health_potion()
            elif choice == '2':
                self.use_shield()
            elif choice == '3':
                if self.inventory:
                    item = input("Какой предмет выбросить? ").strip()
                    try:
                        self.inventory.remove(item)
                        print(f"✅ Предмет '{item}' выброшен")
                    except ValueError:
                        print(f"❌ Предмет '{item}' не найден в инвентаре")
                else:
                    print("❌ Инвентарь пуст")
            elif choice == '4':
                if self.inventory:
                    item = self.inventory.pop()
                    print(f"✅ Выброшен последний предмет: '{item}'")
                else:
                    print("❌ Инвентарь пуст")
            elif choice == '5':
                self.inventory.sort()
                print("✅ Инвентарь отсортирован")
            elif choice == '6':
                self.inventory.reverse()
                print("✅ Инвентарь перевёрнут")
            elif choice == '7':
                if self.inventory:
                    item = input("Какой предмет найти? ").strip()
                    try:
                        index = self.inventory.index(item)
                        print(f"✅ Предмет '{item}' найден на позиции {index}")
                    except ValueError:
                        print(f"❌ Предмет '{item}' не найден")
                else:
                    print("❌ Инвентарь пуст")
            elif choice == '8':
                item = input("Какой предмет проверить? ").strip()
                if item in self.inventory:
                    print(f"✅ Предмет '{item}' есть в инвентаре")
                else:
                    print(f"❌ Предмет '{item}' отсутствует в инвентаре")
            elif choice == '9':
                break
            else:
                print("❌ Неверный выбор")
    
    def play(self):
        #Сама игра
        print("\n" + "="*50)
        print("ДОБРО ПОЖАЛОВАТЬ В ЛАБИРИНТ!")
        print("="*50)
        print("\nЦель: найти выход и ключ")
        print("\nОбозначения:")
        print("🧑 вы | ⬛ неизвестно | ⬜ пусто | 📦 сундук")
        print("💀 ловушка | 🔑 ключ | 🌀 портал | 🚪 выход")
        print("\nПредметы:")
        print("🧪 зелье здоровья — восстанавливает 30 HP")
        print("🛡️ щит — уменьшает урон от следующей ловушки вдвое")
        print("\nУправление:")
        print("w/a/s/d — движение | i — инвентарь | q — выход")
        
        while not self.game_over:
            self.display_maze()
            
            command = input("\nВаше действие (w/a/s/d/i/q): ").strip().lower()
            
            if command in ['w', 'a', 's', 'd']:
                self.move_player(command)
            elif command == 'i':
                self.manage_inventory()
            elif command == 'q':
                print("\n👋 Игра завершена!")
                break
            else:
                print("❌ Неверная команда!")

def main():
    #Главная функция
    print("="*50)
    print("НАСТРОЙКА ЛАБИРИНТА")
    print("="*50)
    
    while True:
        try:
            n = int(input("Введите количество строк (минимум 3): "))
            m = int(input("Введите количество столбцов (минимум 3): "))
            
            if n >= 3 and m >= 3:
                break
            else:
                print("❌ Размер должен быть не менее 3x3")
        except ValueError:
            print("❌ Введите корректное число")
    
    game = MazeGame(n, m)
    game.play()

if __name__ == "__main__":
    main()