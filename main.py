import speech_recognition as sr
from pynput import keyboard
from pynput.keyboard import Controller, Key

# Создаем объект Recognizer
recognizer = sr.Recognizer()

# Создаем объект Controller для эмуляции ввода
keyboard_controller = Controller()

# Устанавливаем начальное состояние - распознавание выключено
is_recognizing = False


def toggle_recognition(val):
    global is_recognizing
    is_recognizing = val
    print("Распознавание", "включено" if is_recognizing else "выключено")


def on_key_release(key):
    try:
        if key == Key.f9:
            toggle_recognition(False)

        if key == Key.f10:
            toggle_recognition(True)

        if key == Key.esc:
            print("Выход из программы")
            exit()
    except AttributeError:
        pass


# Слушатель для клавиш
keyboard_listener = keyboard.Listener(on_release=on_key_release)
keyboard_listener.start()


def type_with_keyboard(text):
    keyboard_controller.type(text)


with sr.Microphone() as source:
    while True:
        if is_recognizing:
            print("Скажите что-нибудь...")
            audio = recognizer.listen(source)
            try:
                recognized_text = recognizer.recognize_google(
                    audio, language="ru-RU")
                # Эмулируем ввод текста с клавиатуры
                type_with_keyboard(recognized_text)
                print("Произнесенный текст введен с клавиатуры:", recognized_text)
            except sr.UnknownValueError:
                print("Голос не распознан")
            except sr.RequestError as e:
                print("Ошибка сервиса распознавания: {0}".format(e))
