import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.animation import Animation

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        welcome_label = Label(text="Welcome to the Guess the Number Game!", font_size='32sp', bold=True, color=(1, 1, 0, 1))
        layout.add_widget(welcome_label)

        self.difficulty = 'easy'

        difficulty_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50sp', spacing=20)
        self.easy_button = Button(text="Easy", font_size='18sp', background_color=(0, 0.7, 0, 1))
        self.easy_button.bind(on_press=lambda x: self.set_difficulty('easy'))
        difficulty_layout.add_widget(self.easy_button)
        self.medium_button = Button(text="Medium", font_size='18sp', background_color=(0.7, 0.7, 0, 1))
        self.medium_button.bind(on_press=lambda x: self.set_difficulty('medium'))
        difficulty_layout.add_widget(self.medium_button)
        self.hard_button = Button(text="Hard", font_size='18sp', background_color=(1, 0, 0, 1))
        self.hard_button.bind(on_press=lambda x: self.set_difficulty('hard'))
        difficulty_layout.add_widget(self.hard_button)
        layout.add_widget(difficulty_layout)

        start_button = Button(text="Start Game", font_size='24sp', size_hint_y=None, height='50sp', background_color=(0, 0.7, 0, 1))
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        quit_button = Button(text="Quit Game", font_size='24sp', size_hint_y=None, height='50sp', background_color=(1, 0, 0, 1))
        quit_button.bind(on_press=self.quit_game)
        layout.add_widget(quit_button)

        self.add_widget(layout)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.easy_button.background_color = (0, 0.7, 0, 1) if difficulty == 'easy' else (0.7, 0.7, 0.7, 1)
        self.medium_button.background_color = (0.7, 0.7, 0, 1) if difficulty == 'medium' else (0.7, 0.7, 0.7, 1)
        self.hard_button.background_color = (1, 0, 0, 1) if difficulty == 'hard' else (0.7, 0.7, 0.7, 1)

    def start_game(self, instance):
        if self.difficulty == 'easy' or self.difficulty == 'medium' or self.difficulty == 'hard':
            self.manager.current = 'game'
            self.manager.get_screen('game').set_difficulty(self.difficulty)
        else:
            self.show_popup("Error", "Please select a difficulty level.")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, font_size='18sp')
        popup_button = Button(text="OK", size_hint_y=None, height='50sp')

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

    def quit_game(self, instance):
        App.get_running_app().stop()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.difficulty = 'easy'
        self.number_to_guess = None
        self.attempts = 0
        self.max_attempts = 10

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='80sp', padding=10)
        header_label = Label(text="Guess the Number Game", font_size='32sp', bold=True, color=(1, 1, 0, 1))
        header_layout.add_widget(header_label)
        main_layout.add_widget(header_layout)

        self.layout = GridLayout(cols=1, padding=20, spacing=20)

        self.instruction_label = Label(text="I am thinking of a number. Try to guess it!", font_size='18sp', color=(1, 1, 1, 1))
        self.layout.add_widget(self.instruction_label)

        self.guess_input = TextInput(hint_text="Enter your guess", multiline=False, input_filter='int', font_size='18sp', foreground_color=(0, 0, 0, 1), background_color=(1, 1, 1, 1))
        self.guess_input.bind(on_text_validate=self.check_guess)
        self.layout.add_widget(self.guess_input)

        self.submit_button = Button(text="Submit Guess", font_size='18sp', size_hint_y=None, height='50sp', background_color=(0, 0.7, 0, 1))
        self.submit_button.bind(on_press=self.check_guess)
        self.layout.add_widget(self.submit_button)

        self.result_label = Label(text="", font_size='18sp', color=(1, 0, 0, 1))
        self.layout.add_widget(self.result_label)

        self.attempts_label = Label(text=f"Attempts left: {self.max_attempts}", font_size='18sp', color=(1, 1, 1, 1))
        self.layout.add_widget(self.attempts_label)

        button_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=20)
        self.restart_button = Button(text="Restart Game", font_size='18sp', background_color=(0, 0.5, 1, 1))
        self.restart_button.bind(on_press=self.reset_game)
        button_layout.add_widget(self.restart_button)

        self.home_button = Button(text="Home", font_size='18sp', background_color=(0.5, 0.5, 1, 1))
        self.home_button.bind(on_press=self.go_home)
        button_layout.add_widget(self.home_button)

        self.quit_button = Button(text="Quit Game", font_size='18sp', background_color=(1, 0, 0, 1))
        self.quit_button.bind(on_press=self.quit_game)
        button_layout.add_widget(self.quit_button)

        self.layout.add_widget(button_layout)
        main_layout.add_widget(self.layout)
        self.add_widget(main_layout)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 'easy':
            self.number_to_guess = random.randint(1, 50)
            self.max_attempts = 10
        elif difficulty == 'medium':
            self.number_to_guess = random.randint(1, 100)
            self.max_attempts = 8
        else:
            self.number_to_guess = random.randint(1, 200)
            self.max_attempts = 5
        self.reset_game()

    def check_guess(self, instance):
        try:
            user_guess = int(self.guess_input.text)
            self.attempts += 1

            if user_guess > self.number_to_guess:
                self.result_label.text = "Your guess is too high."
                self.animate_result(self.result_label, correct=False)
            elif user_guess < self.number_to_guess:
                self.result_label.text = "Your guess is too low."
                self.animate_result(self.result_label, correct=False)
            else:
                self.result_label.text = "You guessed it right!"
                self.animate_result(self.result_label, correct=True)
                self.show_popup("Congratulations", f"You guessed the number {self.number_to_guess} in {self.attempts} attempts!")
                return

            if self.attempts < self.max_attempts:
                self.attempts_label.text = f"Attempts left: {self.max_attempts - self.attempts}"
                self.guess_input.text = ""
                self.guess_input.focus = True
            else:
                self.result_label.text = f"Sorry, you've reached the maximum number of attempts. The number was {self.number_to_guess}."
                self.show_popup("Game Over", f"The number was {self.number_to_guess}. Better luck next time!")
                self.reset_game()
        except ValueError:
            self.result_label.text = "Invalid input! Please enter a number."
            self.guess_input.text = ""
            self.guess_input.focus = True

    def animate_result(self, label, correct=False):
        if correct:
            animation = Animation(color=(0, 1, 0, 1), duration=0.5) + Animation(color=(1, 0, 0, 1), duration=0.5)
        else:
            animation = Animation(color=(1, 0.5, 0.5, 1), duration=0.5) + Animation(color=(1, 0, 0, 1), duration=0.5)
        animation.start(label)

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, font_size='18sp')
        popup_button = Button(text="OK", size_hint_y=None, height='50sp')

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

    def reset_game(self, instance=None):
        self.attempts = 0
        self.attempts_label.text = f"Attempts left: {self.max_attempts}"
        self.result_label.text = ""
        self.guess_input.text = ""
        self.guess_input.focus = True

    def quit_game(self, instance):
        App.get_running_app().stop()

    def go_home(self, instance):
        self.manager.current = 'start'

class NumberGuessingGame(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    NumberGuessingGame().run()