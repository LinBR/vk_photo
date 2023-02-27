# -*- coding: utf-8 -*-
import os
import time
import sqlite3
import requests
import vk_api
from python3_anticaptcha import ImageToTextTask


# вход, редактирование, создание, инфо, настройки
class Config:
    # приветствие пользователя
    def intro(self):
        print("\033[H\033[J")
        print("_____________________________________________________________\n  _    _   _    _   ____     _     _     "
              "__   ______     __  \n  |   /    /  ,'    /    )   /    /    /    )   /      /    )\n--|--/----/_.'-----"
              "/____/---/___ /----/----/---/------/----/-\n  | /    /  \\     /        /    /    /    /   /      /    /"
              "  \n__|/____/____\\___/________/____/____(____/___/______(____/___\n")
        print(f'''Скрипт который накручивает фото в альбом\n\n''')
        # переводим пользователя на авторизацию
        self.autorization()

    def autorization(self):
        while True:
            try:
                print('Выберите способ авторизации:\n[1] Через пароль и логин\n[2] Через токен \n[3] У меня есть ко'
                      'нфиг с данными моего аккаунта\n[4] Я хочу редактировать свой конфиг\n[5] Создать конфиг с данным'
                      'и моего аккаунта\n[6] Инфо\n[7] Настройка скрипта\n')
                self.authorization_method = int(input('Введите цифру: '))
                self.number_autorization()
                break
            # обрабатываем ошибки
            except ValueError:
                print('\n\nВведите число!\n\n')
            except Exception as e:
                print(f'\n\nПроизошла ошибка:\n{e}\n\n')

    def number_autorization(self):
        # авторизация через логин или пароль
        if self.authorization_method == 1:
            self.autorization_logpass()
        # авторизация через токен
        elif self.authorization_method == 2:
            self.autorization_token()
        # авторизация через конфиг
        elif self.authorization_method == 3:
            self.autorization_conf()
        # редактируем конфиг
        elif self.authorization_method == 4:
            self.edit_conf()
        # создаем конфиг
        elif self.authorization_method == 5:
            self.create_conf()
        # информация
        elif self.authorization_method == 6:
            self.info()
        # настройки, которых нет
        elif self.authorization_method == 7:
            self.settings()
        # че ввел мудак иди обратно подумай над своими цифрами
        else:
            print('\n\nВведите число от 1 до 7!\n\n')
            self.autorization()

    def autorization_logpass(self):
        while True:
            try:
                number = input('\nВведите номер: ')
                password = input('Введите пароль: ')
                url = f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB" \
                      f"1inYsH&username={number}&password={password}"
                ke = requests.get(url).json()
                self.token = ke['access_token']     # получаем токен
                vk = vk_api.VkApi(token=self.token)     # авторизовываемся в вк для получения айди и имени
                info_account = vk.method('users.get', {})   # получаем инфу об акке
                imya = info_account[0]["first_name"]   # получаем имя
                familiya = info_account[0]["last_name"]   # получаем фамилию
                id = info_account[0]["id"]   # получаем айди
                print(f'Аккаунт {imya} {familiya}(id{id}) был успешно авторизован!')
                if self.authorization_method == 4:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                    conn = sqlite3.connect('conf.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET token_vk="%s"' % (self.token))
                    conn.commit()
                    conn.close()
                    print('Токен успешно сменён!')
                    self.edit_conf()
                    break
                else:
                    self.anticaptcha()
                    break
            except Exception as e:
                print(f'Произшла ошибка:\n{e}')

    def autorization_token(self):
        while True:
            try:
                self.token = input('\nВведите токен:\n')
                if len(self.token) == 85 or len(self.token) == 198:
                    vk = vk_api.VkApi(token=self.token)     # авторизовываемся в вк для получения айди и имени
                    info_account = vk.method('users.get', {})   # получаем инфу об акке
                    imya = info_account[0]["first_name"]   # получаем имя
                    familiya = info_account[0]["last_name"]   # получаем фамилию
                    id = info_account[0]["id"]   # получаем айди
                    print(f'Аккаунт {imya} {familiya}(id{id}) был успешно авторизован!')
                    if self.authorization_method == 4:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                        conn = sqlite3.connect('conf.db')
                        cur = conn.cursor()
                        cur.execute('UPDATE info SET token_vk="%s"' % (self.token))
                        conn.commit()
                        conn.close()
                        print('Токен успешно сменён!')
                        self.edit_conf()
                        break
                    else:
                        self.anticaptcha()
                        break
                else:
                    print(f'Ваш токен содержит {len(self.token)} символов, а должен 85 или 198. Повторите попытку.')
            except Exception as e:
                print(f'Произошла ошибка:\n{e}')

    def anticaptcha(self):
        while True:
            try:
                print('\nХотите ли вы добавить антикапчу?\n[1] Ввести ключ антикапчи\n[2] Я буду вводить капчу вручную'
                      '\n[3] Если возникнет капча, взять перерыв')
                self.number_anticaptcha = int(input('Выберите вариант: '))

                # задаем переменным кодовое имя чтобы в будущем ссылаться на них
                if self.number_anticaptcha == 1:
                    self.captcha = 'Введите ваш токен https://anti-captcha.com/:\n'
                elif self.number_anticaptcha == 2:
                    self.captcha = 'ARMS'
                elif self.number_anticaptcha == 3:
                    self.captcha = 'TIME'
                else:
                    print('\n\nВведите число от 1 до 3!\n')
                    continue

                if self.authorization_method == 4:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                    conn = sqlite3.connect('conf.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET token_captcha="%s"' % (self.captcha))
                    conn.commit()
                    conn.close()
                    print('Значение было успешно изменено!')
                    self.edit_conf()
                    break
                else:
                    self.path_file()
                    break
            except ValueError:
                print('\n\nВведите число!\n')
            except Exception as e:
                print(f'\n\nПроизошла ошибка:\n{e}\n')

    def path_file(self):
        while True:
            try:
                self.path = input('\nВведите путь на файл(пример C:\\photo\\minecraft.jpg или если файл лежит в папке с'
                                  'о скриптом просто его название)\n')
                # проверка существования файла
                if os.path.isfile(self.path):
                    if self.authorization_method == 4:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                        conn = sqlite3.connect('conf.db')
                        cur = conn.cursor()
                        cur.execute('UPDATE info SET path="%s"' % (self.path))
                        conn.commit()
                        conn.close()
                        print('Файл был успешно сменён!')
                        self.edit_conf()
                        break
                    else:
                        self.count_photo()
                        break
                else:
                    print('\n\nТакого файла/пути нет!\n')
            except Exception as e:
                print(f'\n\nПроизошла ошибка:\n{e}\n')

    def count_photo(self):
        while True:
            try:
                self.count = int(input('\nСколько фоток будем накручивать?\n'))
                if self.authorization_method == 4:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                    conn = sqlite3.connect('conf.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET count="%s"' % (self.count))
                    conn.commit()
                    conn.close()
                    print('Количество накруток было успешно изменено!')
                    self.edit_conf()
                    break
                else:   # иначе переходим к другой функции
                    self.id_album()
                    break
            except ValueError:
                print('\n\nВведите число!\n')
            except Exception as e:
                print(f'\n\nПроизошла ошибка:\n{e}\n')

    def id_album(self):
        while True:
            try:
                album_id = input('\nВведите ссылку на альбом\nПример https://vk.com/album555034297_285590862\n\n')
                self.id = album_id[album_id.find('_')+1:]
                if self.authorization_method == 4:  # редактируем конфиг
                    conn = sqlite3.connect('conf.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET id="%s"' % (self.id))
                    conn.commit()
                    conn.close()
                    print('Альбом был успешно сменён!')
                    self.edit_conf()
                    break
                elif self.authorization_method == 5:    # заполняем наш конфиг данными которые вводили
                    conn = sqlite3.connect('conf.db')
                    cur = conn.cursor()
                    cur.execute('INSERT INTO info VALUES("%s", "%s", "%s", "%s", "%s")'
                                % (self.token, self.captcha, self.path, self.id, self.count))
                    conn.commit()
                    conn.close()
                    print('\n\nКонфиг был успешно создан!\n\n')
                    self.autorization()
                    break
                else:   # если пользователь выбрал вход через токен или лог/пасс запускаем ему накрутку
                    Nakrutka().data(self.token, self.captcha, self.path, self.id, self.count)
                    break
            except Exception as e:
                print(f'\n\nПроизошла ошибка!\n{e}\n')

    # берем всю инфу из конфига и отправляем в другой класс
    def autorization_conf(self):
        conn = sqlite3.connect('conf.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM info")
        data = cur.fetchall()[0]
        conn.commit()
        conn.close()
        Nakrutka().data(data[0], data[1], data[2], data[3], data[4])

    def edit_conf(self):
        while True:
            try:
                print('\nЧто будем редактировать:\n[1] Токен вк\n[2] Токен антикапчи\n[3] Файл\n[4] Айди альбома\n[5] К'
                      'оличество фоток\n[6] Удалить конфиг\n[7] Выйти\n')
                self.edit_num = int(input('Введите число:\n'))
                if self.edit_num == 1:
                    num_auth = int(input('Введите способ авторизации:\n[1] Через пароль и логин\n[2] Через токен\n'))
                    if num_auth == 1:
                        self.autorization_logpass()
                        break
                    elif num_auth == 2:
                        self.autorization_token()
                        break
                    else:
                        print('Ок. Пон.')
                elif self.edit_num == 2:
                    self.anticaptcha()
                    break
                elif self.edit_num == 3:
                    self.path_file()
                    break
                elif self.edit_num == 4:
                    self.id_album()
                    break
                elif self.edit_num == 5:
                    self.count_photo()
                    break
                elif self.edit_num == 6:
                    os.remove('conf.db')
                    print('\nКонфиг был успешно удален!\nВозвращаю вас назад\n')
                    self.autorization()
                    break
                elif self.edit_num == 7:
                    self.autorization()
                    break
                else:
                    print('\n\nВведите число от 1 до 5!\n')
            except ValueError:
                print('\n\nВведите число!\n')
            except Exception as e:
                print(f'\n\nПроизошла ошибка:\n{e}\n')

    def create_conf(self):
        # создаем базу
        conn = sqlite3.connect('conf.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE info(
                        token_vk TEXT,
                        token_captcha TEXT,
                        path TEXT,
                        id INTEGER,
                        count INTEGER
        )""")
        conn.commit()
        conn.close()

        # и заполняем
        while True:
            try:
                print('\nВыберите способ авторизации:\n[1] Через пароль и логин\n[2] Через токен')
                self.method_autorization_db = int(input('Введите число: '))
                if self.method_autorization_db == 1:
                    self.autorization_logpass()
                    break
                elif self.method_autorization_db == 2:
                    self.autorization_token()
                    break
                else:
                    print("\n\nВведите 1 или 2!\n")
            except ValueError:
                print('\n\nВведите число!\n')
            except Exception as e:
                print(f'\n\nПроизошла ошибка:\n{e}\n')

    def info(self):
        print('\nСкрипт для накрутки фотографий в альбом. Советую создать конфиг и не мучиться с постоянной настройкой'
              '\nСледи за моим гитхабом в скором времени обновлю этот скрипт, да и добавлю еще несколько.')
        input('\nВведи че-нить чтобы выйти отсюда')
        self.autorization()

    def settings(self):
        print('Потом добавлю, мужик, даааа')
        self.autorization()


# тут вся работа накрутки
class Nakrutka:
    # переводим полученные данные в переменные для всего класса
    def data(self, token, captcha, path, id, count):
        self.vktoken = token
        self.captchatoken = captcha
        self.path = path
        self.album_id = id
        self.count = count
        self.authorization()

    # метод для ввода вручную капчи
    def enter_arms(self, captcha):
        key = input(f"Введите капчу {captcha.get_url()}:\n").strip()
        return captcha.try_again(key)

    # метод позволяющий решать капчу при помощи антикапчи
    def captcha_handler(self, captcha):
        key = ImageToTextTask.ImageToTextTask(anticaptcha_key=self.captchatoken, save_format='const').\
            captcha_handler(captcha_link=captcha.get_url())
        return captcha.try_again(key['solution']['text'])

    def authorization(self):
        # проверяем какой ввод капчи выбрал пользователь
        if self.captchatoken == 'TIME':
            self.vk = vk_api.VkApi(token=self.vktoken)
        elif self.captchatoken == 'ARMS':
            self.vk = vk_api.VkApi(token=self.vktoken, captcha_handler=self.enter_arms)
        else:
            self.vk = vk_api.VkApi(token=self.vktoken, captcha_handler=self.captcha_handler)
        self.upload = vk_api.VkUpload(self.vk)

        print("\033[H\033[J")   # чистка консоли
        print('\nРабота скрипта запущена!')

        # загружаем фото в альбом
        for i in range(self.count):
            try:
                link = self.upload.photo(self.path, album_id=self.album_id, )
                print(f'Фото №{i + 1} загружено\nСсылка на фото: https://vk.com/photo{link[0]["owner_id"]}_'
                      f'{link[0]["id"]}\n')
            except Exception as e:
                print(f'Произошла ошибка:\n{e}')
                if self.captchatoken == 'TIME':
                    print('Беру перерыв 15 секунд')
                    time.sleep(15)


if __name__ == '__main__':
    Config().intro()
