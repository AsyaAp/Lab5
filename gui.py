import tkinter as tk
from tkinter import ttk
import random
from game_data import *

class BartenderGameGUI:
    def __init__(self, root, game_logic):
        self.root = root
        self.game = game_logic
        self.setup_gui()
        
    def setup_gui(self):
        self.root.title("Bartender Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#4a1c6b")
        
        # Создаем фреймы для разных экранов
        self.start_frame = tk.Frame(self.root, bg="#4a1c6b")
        self.tutorial_frame = tk.Frame(self.root, bg="#4a1c6b") 
        self.game_frame = tk.Frame(self.root, bg="#4a1c6b")
        self.end_frame = tk.Frame(self.root, bg="#4a1c6b")
        
        self.setup_start_screen()
        self.setup_tutorial_screen()
        self.setup_game_screen()
        self.setup_end_screen()
        
        self.show_screen("start")
        
    def setup_start_screen(self):
        self.start_frame.pack(fill="both", expand=True)
        
        title_label = tk.Label(self.start_frame, text="BARTENDER SIMULATOR", 
                              font=("Courier New", 36, "bold"), fg="white", bg="#4a1c6b")
        title_label.pack(pady=100)
        
        start_btn = tk.Button(self.start_frame, text="ИГРАТЬ", command=self.start_game,
                             font=("Courier New", 20), bg="#4cc9f0", fg="white",
                             relief="raised", bd=5, width=15, height=2)
        start_btn.pack(pady=50)
        
    def setup_tutorial_screen(self):
        # Этот фрейм будет заполнен когда потребуется
        pass
        
    def setup_game_screen(self):
        # Этот фрейм будет заполнен когда потребуется
        pass
        
    def setup_end_screen(self):
        # Этот фрейм будет заполнен когда потребуется
        pass
        
    def show_screen(self, screen_name):
        # Скрыть все экраны
        for frame in [self.start_frame, self.tutorial_frame, self.game_frame, self.end_frame]:
            frame.pack_forget()
        
        # Показать нужный экран
        if screen_name == "start":
            self.start_frame.pack(fill="both", expand=True)
        elif screen_name == "tutorial":
            if not hasattr(self, 'tutorial_initialized'):
                self.create_tutorial_screen()
                self.tutorial_initialized = True
            self.tutorial_frame.pack(fill="both", expand=True)
        elif screen_name == "game":
            if not hasattr(self, 'game_initialized'):
                self.create_game_screen()
                self.game_initialized = True
            self.game_frame.pack(fill="both", expand=True)
        elif screen_name == "end":
            self.end_frame.pack(fill="both", expand=True)
            
    def create_tutorial_screen(self):
        # Очистить фрейм обучения
        for widget in self.tutorial_frame.winfo_children():
            widget.destroy()
            
        tutorial_container = tk.Frame(self.tutorial_frame, bg="#16213e", padx=20, pady=20)
        tutorial_container.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Заголовок обучения
        day_label = tk.Label(tutorial_container, text="День 0 - Обучение", 
                            font=("Courier New", 14, "bold"), fg="white", bg="#0f3460")
        day_label.pack(pady=10, fill="x")
        
        # Персонаж
        character_frame = tk.Frame(tutorial_container, bg="#0f3460")
        character_frame.pack(pady=10, fill="x")
        
        character_circle = tk.Canvas(character_frame, width=60, height=60, bg="#4cc9f0", 
                                   highlightthickness=0)
        character_circle.pack(side="left", padx=10, pady=10)
        
        character_name = tk.Label(character_frame, text="Бармен", 
                                 font=("Courier New", 14, "bold"), fg="white", bg="#0f3460")
        character_name.pack(side="left", padx=10)
        
        # Текст обучения
        tutorial_text = """Приветствую! Сегодня твой первый день работы в нашем баре. 
Прежде чем начать, нужно прочесть инструктаж, который выдали при устройстве на работу."""
        
        dialog_text = tk.Text(tutorial_container, wrap="word", font=("Courier New", 12),
                             bg="black", fg="white", padx=15, pady=15, height=4)
        dialog_text.insert("1.0", tutorial_text)
        dialog_text.config(state="disabled")
        dialog_text.pack(fill="x", pady=10)
        
        # Книга рецептов (сворачиваемая)
        self.instructions_collapsed = True
        self.instructions_frame = tk.Frame(tutorial_container, bg="#0f3460")
        self.instructions_header = tk.Frame(self.instructions_frame, bg="#0f3460", cursor="hand2")
        self.instructions_header.pack(fill="x")
        
        instructions_title = tk.Label(self.instructions_header, text="📖 Инструкция для бармена", 
                                     font=("Courier New", 12, "bold"), fg="white", bg="#0f3460")
        instructions_title.pack(side="left", padx=10, pady=5)
        
        arrow_label = tk.Label(self.instructions_header, text="▼", 
                              font=("Courier New", 12), fg="white", bg="#0f3460")
        arrow_label.pack(side="right", padx=10, pady=5)
        
        self.instructions_content = tk.Frame(self.instructions_frame, bg="#0f3460")
        
        # Содержание инструкции
        instructions_text = """
Как смешивать напитки:
Клиенты заказывают напитки по названию или типу. Используй ингредиенты для создания напитков согласно рецептам. Следи за правильным порядком и количеством ингредиентов.

Учет состояния клиентов:
Обращай внимание на настроение клиентов. Грустным клиентам добавь Эликсир или Сироп для поднятия настроения. Взволнованным - Жидкую мяту или Сияющую шипучку для успокоения.

Способы приготовления:
Не забудь выбрать правильный способ приготовления: Лёд, Фламбирование или Взболтать. Это важно для правильного вкуса напитка.

Совет от опытного бармена:
Старайся внимательно слушать клиентов и учитывай их настроение. Правильно приготовленный напиток может изменить чей-то день! Ты справишься - я в тебе уверен!
"""
        
        content_text = tk.Text(self.instructions_content, wrap="word", font=("Courier New", 11),
                              bg="#0f3460", fg="white", padx=10, pady=10, height=10)
        content_text.insert("1.0", instructions_text)
        content_text.config(state="disabled")
        content_text.pack(fill="both", expand=True)
        
        self.instructions_frame.pack(fill="x", pady=10)
        self.instructions_content.pack_forget()  # Сворачиваем по умолчанию
        
        # Обработчик клика для сворачивания/разворачивания
        def toggle_instructions(event):
            if self.instructions_collapsed:
                self.instructions_content.pack(fill="both", expand=True)
                arrow_label.config(text="▲")
                self.instructions_collapsed = False
            else:
                self.instructions_content.pack_forget()
                arrow_label.config(text="▼")
                self.instructions_collapsed = True
                
        self.instructions_header.bind("<Button-1>", toggle_instructions)
        instructions_title.bind("<Button-1>", toggle_instructions)
        arrow_label.bind("<Button-1>", toggle_instructions)
        
        # Кнопка продолжения
        next_btn = tk.Button(tutorial_container, text="Начать работу →", 
                            command=self.start_main_game, font=("Courier New", 14),
                            bg="#4cc9f0", fg="white", padx=20, pady=10)
        next_btn.pack(pady=20)
        
    def create_game_screen(self):
        # Очистить фрейм игры
        for widget in self.game_frame.winfo_children():
            widget.destroy()
            
        # Основной контейнер игры
        game_container = tk.Frame(self.game_frame, bg="#4a1c6b")
        game_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Сетка для разделения на две колонки
        left_frame = tk.Frame(game_container, bg="#4a1c6b")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(game_container, bg="#4a1c6b")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Левая колонка - диалоги
        self.create_dialog_section(left_frame)
        
        # Правая колонка - бар
        self.create_bar_section(right_frame)
        
    def create_dialog_section(self, parent):
        dialog_section = tk.Frame(parent, bg="#16213e", padx=15, pady=15)
        dialog_section.pack(fill="both", expand=True)
        
        # Информация о дне
        self.day_label = tk.Label(dialog_section, text="День 1 из 3", 
                                 font=("Courier New", 12, "bold"), fg="white", bg="#0f3460")
        self.day_label.pack(pady=(0, 10), fill="x")
        
        # Контейнер персонажа
        character_container = tk.Frame(dialog_section, bg="#16213e")
        character_container.pack(fill="x", pady=10)
        
        # Информация о персонаже
        character_info = tk.Frame(character_container, bg="#0f3460")
        character_info.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.character_circle = tk.Canvas(character_info, width=60, height=60, bg="#4cc9f0", 
                                        highlightthickness=0)
        self.character_circle.pack(side="left", padx=10, pady=10)
        
        self.character_name = tk.Label(character_info, text="Бармен", 
                                      font=("Courier New", 14, "bold"), fg="white", bg="#0f3460")
        self.character_name.pack(side="left", padx=10)
        
        # Удовлетворенность клиента
        self.customer_satisfaction = tk.Label(character_info, text="...", 
                                            font=("Courier New", 12), fg="#e6e6e6", bg="#0f3460")
        self.customer_satisfaction.pack(side="right", padx=10)
        
        # Мысли бармена
        self.bartender_thoughts = tk.Text(dialog_section, wrap="word", font=("Courier New", 11),
                                         bg="black", fg="white", padx=10, pady=8, height=3)
        self.bartender_thoughts.pack(fill="x", pady=5)
        self.bartender_thoughts.config(state="disabled")
        
        # Диалоговое окно
        self.dialog_text = tk.Text(dialog_section, wrap="word", font=("Courier New", 12),
                                  bg="black", fg="white", padx=15, pady=15, height=6)
        self.dialog_text.pack(fill="both", expand=True, pady=5)
        self.dialog_text.config(state="disabled")
        
        # Управление диалогом
        dialog_controls = tk.Frame(dialog_section, bg="#16213e")
        dialog_controls.pack(fill="x", pady=10)
        
        self.next_btn = tk.Button(dialog_controls, text="Далее →", command=self.game.next_dialog,
                                 font=("Courier New", 12), bg="#4cc9f0", fg="white", padx=20)
        self.next_btn.pack(side="right")
        
        # Прогресс истории
        story_progress = tk.Frame(dialog_section, bg="#0f3460", padx=10, pady=8)
        story_progress.pack(fill="x", pady=10)
        
        progress_title = tk.Label(story_progress, text="Прогресс:", 
                                 font=("Courier New", 11, "bold"), fg="white", bg="#0f3460")
        progress_title.pack(anchor="w")
        
        self.story_progress_label = tk.Label(story_progress, 
                                           text="День: 1/3 | Клиенты: 0/3 | Историй: 0/3",
                                           font=("Courier New", 10), fg="white", bg="#0f3460")
        self.story_progress_label.pack(anchor="w")
        
    def create_bar_section(self, parent):
        bar_section = tk.Frame(parent, bg="#16213e", padx=15, pady=15)
        bar_section.pack(fill="both", expand=True)
        
        title = tk.Label(bar_section, text="🎮 Барная стойка", 
                        font=("Courier New", 16, "bold"), fg="white", bg="#16213e")
        title.pack(pady=(0, 15))
        
        # Текущий заказ
        current_drink_frame = tk.Frame(bar_section, bg="#16213e")
        current_drink_frame.pack(fill="x", pady=5)
        
        order_title = tk.Label(current_drink_frame, text="Текущий заказ:", 
                              font=("Courier New", 12, "bold"), fg="white", bg="#16213e")
        order_title.pack(anchor="w")
        
        self.current_order_label = tk.Label(current_drink_frame, text="Ожидаем клиента...", 
                                          font=("Courier New", 11), fg="white", bg="#16213e")
        self.current_order_label.pack(anchor="w")
        
        # Текущий состав
        self.current_composition_label = tk.Label(bar_section, text="Состав: пусто", 
                                                font=("Courier New", 10), fg="white", bg="#16213e")
        self.current_composition_label.pack(anchor="w", pady=5)
        
        # Книга рецептов
        self.recipes_collapsed = True
        self.recipes_frame = tk.Frame(bar_section, bg="#0f3460")
        self.recipes_header = tk.Frame(self.recipes_frame, bg="#0f3460", cursor="hand2")
        self.recipes_header.pack(fill="x")
        
        recipes_title = tk.Label(self.recipes_header, text="📖 Книга рецептов", 
                               font=("Courier New", 12, "bold"), fg="white", bg="#0f3460")
        recipes_title.pack(side="left", padx=10, pady=5)
        
        self.recipes_arrow = tk.Label(self.recipes_header, text="▼", 
                                    font=("Courier New", 12), fg="white", bg="#0f3460")
        self.recipes_arrow.pack(side="right", padx=10, pady=5)
        
        self.recipes_content = tk.Frame(self.recipes_frame, bg="#0f3460")
        
        # Контент рецептов
        self.recipes_text = tk.Text(self.recipes_content, wrap="word", font=("Courier New", 10),
                                   bg="#0f3460", fg="white", padx=10, pady=10, height=8)
        self.recipes_text.pack(fill="both", expand=True)
        self.recipes_text.config(state="disabled")
        
        self.recipes_frame.pack(fill="x", pady=10)
        self.recipes_content.pack_forget()
        
        # Обработчик для рецептов
        def toggle_recipes(event):
            if self.recipes_collapsed:
                self.recipes_content.pack(fill="both", expand=True)
                self.recipes_arrow.config(text="▲")
                self.recipes_collapsed = False
            else:
                self.recipes_content.pack_forget()
                self.recipes_arrow.config(text="▼")
                self.recipes_collapsed = True
                
        self.recipes_header.bind("<Button-1>", toggle_recipes)
        recipes_title.bind("<Button-1>", toggle_recipes)
        self.recipes_arrow.bind("<Button-1>", toggle_recipes)
        
        # Бокал для напитка
        glass_frame = tk.Frame(bar_section, bg="black", relief="sunken", bd=2, height=120)
        glass_frame.pack(fill="x", pady=10)
        glass_frame.pack_propagate(False)
        
        self.glass_content = tk.Frame(glass_frame, bg="black")
        self.glass_content.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.glass_label = tk.Label(self.glass_content, text="Бокал пуст", 
                                   font=("Courier New", 11), fg="#666", bg="black")
        self.glass_label.pack(expand=True)
        
        # Действия приготовления
        prep_frame = tk.Frame(bar_section, bg="#16213e")
        prep_frame.pack(fill="x", pady=10)
        
        prep_actions = [
            ("❄️ Лёд", "Лёд"),
            ("🔥 Фламбировать", "Фламбирование"), 
            ("🔄 Взболтать", "Взболтать")
        ]
        
        for text, action in prep_actions:
            btn = tk.Button(prep_frame, text=text, 
                          command=lambda a=action: self.game.add_preparation(a),
                          font=("Courier New", 11), bg="#9d4edd", fg="white",
                          relief="raised", padx=10, pady=8)
            btn.pack(side="left", expand=True, fill="x", padx=2)
        
        # Сетка ингредиентов
        ingredients_frame = tk.Frame(bar_section, bg="#16213e")
        ingredients_frame.pack(fill="both", expand=True, pady=10)
        
        self.ingredient_buttons = []
        for i, ingredient in enumerate(ingredients):
            color = ingredient["color"]
            btn = tk.Button(ingredients_frame, 
                          text=f"{ingredient['name']}\n{ingredient['description']}",
                          command=lambda ing=ingredient: self.game.add_ingredient(ing),
                          font=("Courier New", 9), bg="black", fg="white",
                          relief="raised", bd=2, padx=5, pady=5,
                          highlightbackground=color, highlightcolor=color, 
                          highlightthickness=2)
            row, col = i // 3, i % 3
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            self.ingredient_buttons.append(btn)
            
        # Настройка веса строк и колонок
        for i in range(2):
            ingredients_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            ingredients_frame.grid_columnconfigure(i, weight=1)
        
        # Кнопки управления
        controls_frame = tk.Frame(bar_section, bg="#16213e")
        controls_frame.pack(fill="x", pady=10)
        
        self.serve_btn = tk.Button(controls_frame, text="🍸 Подать напиток", 
                            command=self.game.serve_drink,
                            font=("Courier New", 12), bg="#4cc9f0", fg="white",
                            padx=20, pady=10)
        self.serve_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        self.clear_btn = tk.Button(controls_frame, text="🚰 Очистить", 
                            command=self.game.clear_drink,
                            font=("Courier New", 12), bg="#e94560", fg="white",
                            padx=20, pady=10)
        self.clear_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))
        
    def create_end_screen(self, title, text, stats):
        # Очистить фрейм конца игры
        for widget in self.end_frame.winfo_children():
            widget.destroy()
            
        self.end_title = tk.Label(self.end_frame, text=title, 
                                 font=("Courier New", 36, "bold"), fg="#9d4edd", bg="#4a1c6b")
        self.end_title.pack(pady=50)
        
        self.end_text = tk.Label(self.end_frame, text=text, wraplength=600,
                               font=("Courier New", 14), fg="white", bg="#4a1c6b", justify="center")
        self.end_text.pack(pady=20, padx=50)
        
        self.end_stats = tk.Label(self.end_frame, text=stats, 
                                font=("Courier New", 12), fg="white", bg="#4a1c6b")
        self.end_stats.pack(pady=20)
        
        restart_btn = tk.Button(self.end_frame, text="НАЧАТЬ ЗАНОВО", 
                               command=self.restart_game,
                               font=("Courier New", 16), bg="#4cc9f0", fg="white",
                               padx=30, pady=15)
        restart_btn.pack(pady=30)
        
    def start_game(self):
        self.show_screen("tutorial")
        
    def start_main_game(self):
        self.show_screen("game")
        self.game.init_game()
        
    def restart_game(self):
        # Перезапуск игры
        self.game.__init__()
        self.show_screen("start")
        
    def update_dialog(self, text):
        self.dialog_text.config(state="normal")
        self.dialog_text.delete("1.0", "end")
        self.dialog_text.insert("1.0", text)
        self.dialog_text.config(state="disabled")
        
    def update_thoughts(self, text):
        self.bartender_thoughts.config(state="normal")
        self.bartender_thoughts.delete("1.0", "end")
        if text:
            self.bartender_thoughts.insert("1.0", text)
            self.bartender_thoughts.pack(fill="x", pady=5)
        else:
            self.bartender_thoughts.pack_forget()
        self.bartender_thoughts.config(state="disabled")
        
    def update_character(self, name, color):
        self.character_name.config(text=name)
        self.character_circle.config(bg=color)
        
    def update_order(self, text):
        self.current_order_label.config(text=text)
        
    def update_composition(self, text):
        self.current_composition_label.config(text=text)
        
    def update_progress(self, text):
        self.story_progress_label.config(text=text)
        
    def update_day_info(self, text):
        self.day_label.config(text=text)
        
    def update_satisfaction(self, text, color):
        self.customer_satisfaction.config(text=text, fg=color)
        
    def update_recipes(self):
        recipes_text = ""
        for name, info in drinks.items():
            prep_text = f" → {info['preparation']}" if info['preparation'] != "Нормальный" else ""
            temp_symbol = " ❄️" if info['temperature'] == "холодный" else " 🔥" if info['temperature'] == "горячий" else ""
            recipes_text += f"{name}: {', '.join(info['ingredients'])}{prep_text}\n"
            recipes_text += f"   {info['type']} - {info['description']}{temp_symbol}\n\n"
        
        self.recipes_text.config(state="normal")
        self.recipes_text.delete("1.0", "end")
        self.recipes_text.insert("1.0", recipes_text)
        self.recipes_text.config(state="disabled")
        
    def update_glass(self, drink_layers):
        # Очистить бокал
        for widget in self.glass_content.winfo_children():
            widget.destroy()
            
        if not drink_layers:
            self.glass_label = tk.Label(self.glass_content, text="Бокал пуст", 
                                       font=("Courier New", 11), fg="#666", bg="black")
            self.glass_label.pack(expand=True)
        else:
            total_layers = len(drink_layers)
            for i, ingredient_name in enumerate(drink_layers):
                ingredient = next((ing for ing in ingredients if ing["name"] == ingredient_name), None)
                if ingredient:
                    layer_height = max(10, 80 // total_layers)
                    layer = tk.Frame(self.glass_content, bg=ingredient["color"], 
                                   height=layer_height)
                    layer.pack(fill="x", pady=1)
                    layer.pack_propagate(False)
                    
    def show_served_drink(self):
        for widget in self.glass_content.winfo_children():
            widget.destroy()
        served_label = tk.Label(self.glass_content, text="🍸", font=("Courier New", 48), 
                               bg="black", fg="white")
        served_label.pack(expand=True)
        
    def show_ending(self, title, text, stats):
        self.create_end_screen(title, text, stats)
        self.show_screen("end")