import tkinter as tk
import random
from game_data import *
from gui import BartenderGameGUI

class BartenderGame:
    def __init__(self):
        self.current_day = 1
        self.current_customer_index = 0
        self.correct_drinks = 0
        self.special_drinks = 0
        self.stories_heard = 0
        self.current_dialog_step = 0
        self.current_dialogue = []
        self.drink_served = False
        self.current_customer = None
        self.current_drink = []
        self.current_order = None
        self.current_preparation = "Нормальный"
        self.game_state = "start"
        self.day_correct_drinks = 0
        self.used_characters_today = []
        self.day_customers = []
        self.customer_state = "normal"
        self.order_type = "specific"
        self.last_drink_success = False
        
    def init_game(self):
        self.update_recipes_display()
        self.update_progress()
        self.update_day_info()
        self.start_day_intro()
        
    def start_day_intro(self):
        self.current_customer = None
        self.game_state = "bartender_intro"
        self.current_dialog_step = 0
        self.day_correct_drinks = 0
        self.used_characters_today = []
        self.day_customers = []
        
        self.show_bartender_character()
        self.current_dialogue = bartenderDayThoughts.get(self.current_day, bartenderDayThoughts[1])
        self.next_dialog()
        
    def show_bartender_character(self):
        if hasattr(self, 'gui'):
            self.gui.update_character("Бармен", "#4cc9f0")
            self.gui.update_satisfaction("...", "#e6e6e6")
        
    def next_dialog(self):
        if self.current_dialog_step < len(self.current_dialogue):
            dialog_text = self.current_dialogue[self.current_dialog_step]
            if hasattr(self, 'gui'):
                self.gui.update_dialog(dialog_text)
            self.current_dialog_step += 1
            
            if self.game_state == "customer_order":
                self.update_order_display()
        else:
            self.handle_dialog_complete()
            
    def update_order_display(self):
        if self.game_state == "customer_order" and self.current_customer:
            if self.order_type == "specific":
                drink = drinks[self.current_order["drink"]]
                temp_symbol = " ❄️" if drink["temperature"] == "холодный" else " 🔥" if drink["temperature"] == "горячий" else ""
                order_text = f"{self.current_order['drink']} - {drink['type']}{temp_symbol}"
                
                thoughts_text = f"Клиент точно знает, что хочет - {self.current_order['drink']}."
                if self.customer_state == "sad":
                    thoughts_text += " Выглядит грустным, возможно, дополнительный Эликсир или Сироп поднимет настроение."
                elif self.customer_state == "excited":
                    thoughts_text += " Выглядит взбудораженным, освежающий ингредиент поможет успокоиться."
                    
            else:
                possible_drinks = drinksByType.get(self.current_order["drinkType"], [self.current_order["drink"]])
                drink = drinks[self.current_order["drink"]]
                temp_symbol = " ❄️" if drink["temperature"] == "холодный" else " 🔥" if drink["temperature"] == "горячий" else ""
                order_text = f"Любой {self.current_order['drinkType']} напиток{temp_symbol}"
                
                thoughts_text = f"Клиент не уверен в выборе. Подойдут: {', '.join(possible_drinks)}."
                if self.customer_state == "sad":
                    thoughts_text += " Выглядит грустным, возможно, дополнительный Эликсир или Сироп поднимет настроение."
                elif self.customer_state == "excited":
                    thoughts_text += " Выглядит взбудораженным, освежающий ингредиент поможет успокоиться."
            
            if hasattr(self, 'gui'):
                self.gui.update_order(order_text)
                self.gui.update_thoughts(thoughts_text)
                self.gui.next_btn.config(state="normal")
        
    def handle_dialog_complete(self):
        if self.game_state == "bartender_intro":
            self.next_customer()
        elif self.game_state == "customer_greeting":
            self.game_state = "customer_order"
            self.order_type = "specific" if random.random() < 0.5 else "vague"
            
            if self.order_type == "specific":
                self.current_dialogue = [self.current_customer["dialogues"]["specificOrder"].replace("[drink]", self.current_order["drink"])]
            else:
                self.current_dialogue = [self.current_customer["dialogues"]["vagueOrder"]]
                vague_order_text = self.current_customer["dialogues"]["vagueOrder"].lower()
                found_type = "крепкий"
                
                for key, value in orderTypesMapping.items():
                    if key in vague_order_text:
                        found_type = value
                        break
                        
                self.current_order["drinkType"] = found_type
                possible_drinks = drinksByType.get(found_type, [])
                if possible_drinks:
                    self.current_order["drink"] = random.choice(possible_drinks)
                    
            self.current_dialog_step = 0
            self.next_dialog()
            
        elif self.game_state == "customer_order":
            self.game_state = "customer_welcome"
            if hasattr(self, 'gui'):
                self.gui.next_btn.config(state="disabled")
                
        elif self.game_state == "drink_served":
            result = self.check_recipe()
            self.last_drink_success = result["success"]
            
            if result["success"]:
                self.game_state = "story"
                self.current_dialogue = [
                    self.current_customer["dialogues"]["stories"][self.current_day],
                    self.current_customer["dialogues"]["followUp"][self.current_day],
                    self.current_customer["dialogues"]["response"][self.current_day]
                ]
                self.stories_heard += 1
            else:
                self.game_state = "goodbye"
                self.current_dialogue = [self.current_customer["dialogues"]["goodbye"]]
                
            self.current_dialog_step = 0
            if hasattr(self, 'gui'):
                self.gui.next_btn.config(state="normal")
            self.next_dialog()
            
        elif self.game_state == "story":
            self.game_state = "goodbye"
            self.current_dialogue = [
                self.current_customer["dialogues"]["goodbye"],
                self.current_customer["dialogues"]["bartenderGoodbye"]
            ]
            self.current_dialog_step = 0
            self.next_dialog()
            
        elif self.game_state == "goodbye":
            self.game_state = "bartender_after_customer"
            self.current_dialog_step = 0
            self.show_bartender_character()
            
            if self.last_drink_success:
                self.current_dialogue = [self.current_customer["dialogues"]["bartender_thoughts"][self.current_day]]
            else:
                wrong_thoughts = self.current_customer["dialogues"].get("bartender_wrong_thoughts", [
                    "Неловко вышло... Надеюсь, клиент вернётся.",
                    "Жаль, что не угодил... В следующий раз постараюсь лучше.",
                    "Не самый удачный заказ... Надо быть внимательнее к пожеланиям клиентов."
                ])
                self.current_dialogue = [random.choice(wrong_thoughts)]
                
            if hasattr(self, 'gui'):
                self.gui.update_thoughts("")
            self.next_dialog()
            
        elif self.game_state == "bartender_after_customer":
            self.current_customer_index += 1
            if self.current_customer_index < CUSTOMERS_PER_DAY:
                self.next_customer()
            else:
                self.show_day_results()
                
        elif self.game_state == "day_results":
            self.show_day_statistics()
            
        elif self.game_state == "day_statistics":
            self.current_day += 1
            self.current_customer_index = 0
            self.update_day_info()
            if self.current_day > TOTAL_DAYS:
                self.show_ending()
            else:
                self.start_day_intro()
                
    def next_customer(self):
        available_characters = [char for char in characters.keys() if char not in self.used_characters_today]
        if not available_characters:
            self.show_day_results()
            return
            
        random_character = random.choice(available_characters)
        self.current_customer = characters[random_character]
        self.used_characters_today.append(random_character)
        
        self.customer_state = "normal"
        if random.random() < 0.3:
            self.customer_state = "sad" if random.random() < 0.5 else "excited"
            
        ordered_drink = self.current_customer["dayDrinks"][self.current_day]
        self.current_order = {"drink": ordered_drink, "hint": drinks[ordered_drink]["type"]}
        
        self.game_state = "customer_greeting"
        self.current_dialog_step = 0
        self.drink_served = False
        
        if hasattr(self, 'gui'):
            self.gui.update_character(self.current_customer["name"], self.current_customer["color"])
            self.gui.update_satisfaction("⏳ Ожидает напиток", "#e6e6e6")
            self.gui.next_btn.config(state="normal")
            self.gui.update_thoughts("")
            
        self.clear_drink()
        self.current_dialogue = self.current_customer["dialogues"]["greeting"]
        self.next_dialog()
        
    def add_ingredient(self, ingredient):
        if self.drink_served or len(self.current_drink) >= MAX_INGREDIENTS:
            return
            
        self.current_drink.append(ingredient["name"])
        self.update_current_composition()
        self.update_glass_display()
        
    def add_preparation(self, prep):
        if self.drink_served:
            return
            
        self.current_preparation = prep
        self.update_current_composition()
        
    def clear_drink(self):
        self.current_drink = []
        self.current_preparation = "Нормальный"
        self.update_current_composition()
        self.update_glass_display()
        
    def update_current_composition(self):
        composition = "Состав: "
        if self.current_drink:
            composition += " + ".join(self.current_drink)
            if self.current_preparation != "Нормальный":
                composition += f" → {self.current_preparation}"
        else:
            composition += "пусто"
            
        if hasattr(self, 'gui'):
            self.gui.update_composition(composition)
            
    def serve_drink(self):
        if not self.current_drink or self.drink_served:
            return
            
        result = self.check_recipe()
        self.drink_served = True
        
        if hasattr(self, 'gui'):
            self.gui.update_thoughts("")
            self.show_served_drink_display()
            
        self.day_customers.append({
            "name": self.current_customer["name"],
            "status": "special" if result["special"] else "correct" if result["success"] else "wrong",
            "storyHeard": result["success"]
        })
        
        if result["success"]:
            self.correct_drinks += 1
            self.day_correct_drinks += 1
            if result["special"]:
                self.special_drinks += 1
                dialogues = self.current_customer["dialogues"]["special"]
            else:
                dialogues = self.current_customer["dialogues"]["correct"]
            self.current_dialogue = [random.choice(dialogues)]
        else:
            dialogues = self.current_customer["dialogues"]["wrong"]
            self.current_dialogue = [random.choice(dialogues)]
            
        self.game_state = "drink_served"
        self.current_dialog_step = 0
        if hasattr(self, 'gui'):
            self.gui.next_btn.config(state="normal")
            
        satisfaction_text = "..."
        satisfaction_color = "#e6e6e6"
        if result["success"]:
            if result["special"]:
                satisfaction_text = "✨ В восторге"
                satisfaction_color = "#9d4edd"
            else:
                satisfaction_text = "✓ Доволен"
                satisfaction_color = "#4ade80"
        else:
            satisfaction_text = "✗ Недоволен"
            satisfaction_color = "#e94560"
            
        if hasattr(self, 'gui'):
            self.gui.update_satisfaction(satisfaction_text, satisfaction_color)
            
        self.next_dialog()
        self.update_progress()
        
    def check_recipe(self):
        target_drink = drinks[self.current_order["drink"]]
        target_ingredients = target_drink["ingredients"]
        
        if self.order_type == "vague":
            possible_drinks = drinksByType.get(self.current_order["drinkType"], [self.current_order["drink"]])
            success = False
            special = False
            
            for drink_name in possible_drinks:
                drink = drinks[drink_name]
                current_drink_copy = self.current_drink.copy()
                has_all_ingredients = all(
                    ingredient in current_drink_copy and 
                    current_drink_copy.remove(ingredient) or True
                    for ingredient in drink["ingredients"]
                )
                
                preparation_match = self.current_preparation == drink["preparation"]
                
                if has_all_ingredients and preparation_match:
                    success = True
                    has_special_ingredient = self.check_special_ingredient()
                    special = has_special_ingredient and self.customer_state in ["sad", "excited"]
                    break
                    
            return {"success": success, "special": special}
            
        current_drink_copy = self.current_drink.copy()
        has_all_ingredients = all(
            ingredient in current_drink_copy and 
            current_drink_copy.remove(ingredient) or True
            for ingredient in target_ingredients
        )
        
        preparation_match = self.current_preparation == target_drink["preparation"]
        success = has_all_ingredients and preparation_match
        
        has_special_ingredient = self.check_special_ingredient()
        special = success and has_special_ingredient and self.customer_state in ["sad", "excited"]
        
        return {"success": success, "special": special}
        
    def check_special_ingredient(self):
        if self.customer_state == "sad":
            return "Эликсир" in self.current_drink or "Сироп" in self.current_drink
        elif self.customer_state == "excited":
            return "Жидкая мята" in self.current_drink or "Сияющая шипучка" in self.current_drink
        return False
        
    def show_day_results(self):
        self.game_state = "day_results"
        self.current_dialog_step = 0
        
        success_rate = (self.day_correct_drinks / CUSTOMERS_PER_DAY) * 100
        if success_rate == 100:
            results = dayResults["perfect"]
        elif success_rate >= 50:
            results = dayResults["good"]
        else:
            results = dayResults["bad"]
            
        self.show_bartender_character()
        self.current_dialogue = [
            "Похоже, клиентов на сегодня не будет, нужно закрывать смену.",
            *results
        ]
        self.next_dialog()
        
    def show_day_statistics(self):
        self.game_state = "day_statistics"
        self.current_dialog_step = 0
        
        stats_text = f"Статистика за день {self.current_day}\n"
        stats_text += f"Правильных напитков: {self.day_correct_drinks} из {CUSTOMERS_PER_DAY}\n"
        stories_count = len([c for c in self.day_customers if c["storyHeard"]])
        stats_text += f"Собранных историй: {stories_count} из {len(self.day_customers)}\n"
        stats_text += "Обслужено клиентов:\n"
        
        for customer in self.day_customers:
            status_text = "✓ Правильно" if customer["status"] == "correct" else "✨ Идеально" if customer["status"] == "special" else "✗ Ошибка"
            stats_text += f"- {customer['name']}: {status_text}\n"
            
        self.show_bartender_character()
        self.current_dialogue = [stats_text]
        self.next_dialog()
        
    def show_ending(self):
        total_customers = TOTAL_DAYS * CUSTOMERS_PER_DAY
        success_rate = (self.correct_drinks / total_customers) * 100
        stats_text = f"Статистика: {self.correct_drinks}/{total_customers} правильных напитков ({success_rate:.0f}%) | {self.stories_heard}/{total_customers} историй | {self.special_drinks} специальных приготовлений"
        
        if self.special_drinks == total_customers and self.stories_heard == total_customers:
            title = "ЛЕГЕНДАРНЫЙ БАРМЕН"
            text = "Вы не просто приготовили все напитки правильно - вы почувствовали души своих клиентов. Каждый дополнительный ингредиент был идеальным жестом заботы. Вы услышали все истории и помогли каждому клиенту. Ваш бар стал легендой города!"
        elif success_rate == 100 and self.stories_heard == total_customers:
            title = "МАСТЕР СВОЕГО ДЕЛА"
            text = "Идеальная неделя! Все клиенты получили именно то, что заказывали и рассказали все свои истории. Ваш бар славится надежностью и качеством. Вы доказали, что являетесь настоящим профессионалом!"
        elif success_rate >= 50:
            title = "НАДЕЖНЫЙ БАРМЕН"
            text = "Хорошая работа! Большинство клиентов остались довольны. Кое-где были небольшие ошибки, но в целом вы справились хорошо. Бар продолжает работать, клиенты возвращаются."
        else:
            title = "НОВИЧОК"
            text = "Эта неделя была не самой удачной... Слишком много ошибок в заказах. Клиенты уходили недовольными. Возможно, стоит повторить рецепты и больше практиковаться. Каждый мастер когда-то начинал - не сдавайтесь!"
            
        if hasattr(self, 'gui'):
            self.gui.show_ending(title, text, stats_text)
            
    def update_progress(self):
        total_stories = TOTAL_DAYS * CUSTOMERS_PER_DAY
        progress_text = f"День: {self.current_day}/{TOTAL_DAYS} | Клиенты: {self.current_customer_index}/{CUSTOMERS_PER_DAY} | Историй: {self.stories_heard}/{total_stories}"
        if hasattr(self, 'gui'):
            self.gui.update_progress(progress_text)
            
    def update_day_info(self):
        day_text = f"День {self.current_day} из {TOTAL_DAYS}"
        if hasattr(self, 'gui'):
            self.gui.update_day_info(day_text)
            
    def update_recipes_display(self):
        if hasattr(self, 'gui'):
            self.gui.update_recipes()
            
    def update_glass_display(self):
        if hasattr(self, 'gui'):
            self.gui.update_glass(self.current_drink)
            
    def show_served_drink_display(self):
        if hasattr(self, 'gui'):
            self.gui.show_served_drink()

def main():
    root = tk.Tk()
    game = BartenderGame()
    gui = BartenderGameGUI(root, game)
    game.gui = gui
    root.mainloop()

if __name__ == "__main__":
    main()