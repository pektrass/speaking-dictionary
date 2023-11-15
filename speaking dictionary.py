# Импорт необходимых библиотек
import pyttsx3
from PyDictionary import PyDictionary
import speech_recognition as spr
from gtts import gTTS
import os

# Класс для озвучивания
class Speak:
    def SpeakWord(self, audio):
        # Инициализация движка pyttsx3
        pSpeakEngine = pyttsx3.init('sapi5')
        pVoices = pSpeakEngine.getProperty('voices')

        # Установка параметров голоса
        pSpeakEngine.setProperty('voices', pVoices[0].id)
        
        # Произнесение предоставленного аудио
        pSpeakEngine.say(audio)
        pSpeakEngine.runAndWait()

# Создание экземпляра Recognizer, Microphone
sRecog = spr.Recognizer()
sMic = spr.Microphone()

# Захват голоса с микрофона
with sMic as source:
    print("Скажите 'Привет', чтобы запустить говорящий словарь!")
    print("----------------------------------------------")

    # Настройка для окружающего шума и захват аудио
    sRecog.adjust_for_ambient_noise(source, duration=.2)
    rAudio = sRecog.listen(source)

    # Распознавание сказанного слова с использованием Google Speech Recognition
    szHello = sRecog.recognize_google(rAudio, language='ru-RU') 
    szHello = szHello.lower()

# Если пользователь сказал 'Привет', инициализировать говорящий словарь
if 'привет' in szHello:
    sSpeak = Speak()
    pDict = PyDictionary()

    print("Какое слово вы хотите найти? Говорите медленно.")
    sSpeak.SpeakWord("Какое слово вы хотите найти? Говорите медленно")
    
    try:
        sRecog2 = spr.Recognizer()
        sMic2 = spr.Microphone()

        # Захват слова, которое пользователь хочет найти значение 
        with sMic2 as source2:
            sRecog2.adjust_for_ambient_noise(source2, duration=.2)
            rAudio2 = sRecog2.listen(source2)
                
            szInput = sRecog2.recognize_google(rAudio2, language='ru-RU')
            
            try:
                # Убедитесь, что распознаватель получил правильное слово
                print("Вы сказали " + szInput + "? Ответьте да или нет.")
                sSpeak.SpeakWord("Вы сказали " + szInput + "? Ответьте да или нет")
                
                sRecog2.adjust_for_ambient_noise(source2, duration=.2)
                rAudioYN = sRecog2.listen(source2)

                szYN = sRecog2.recognize_google(rAudioYN)
                szYN = szYN.lower()

                # Если пользователь сказал 'да' (когда распознаватель получил правильное слово)
                if 'да' in szYN:
                    szMeaning = pDict.meaning(szInput)

                    print("Значение: ", end="")
                    for i in szMeaning:
                        print(szMeaning[i])
                        sSpeak.SpeakWord("Значение: " + str(szMeaning[i]))

                # Когда распознаватель получил неправильное слово
                else:
                    sSpeak.SpeakWord("Извините. Пожалуйста, попробуйте еще раз")

            # Когда распознаватель не смог понять ответ (да или нет)
            except spr.UnknownValueError:
                sSpeak.SpeakWord("Не удалось понять ввод. Пожалуйста, попробуйте еще раз")
            except spr.RequestError as e:
                sSpeak.SpeakWord("Не удалось предоставить необходимый вывод")

    # Когда распознаватель не смог понять слово
    except spr.UnknownValueError:
        sSpeak.SpeakWord("Не удалось понять ввод. Пожалуйста, попробуйте еще раз")
    except spr.RequestError as e:
        sSpeak.SpeakWord("Не удалось предоставить необходимый вывод")