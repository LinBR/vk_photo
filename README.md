# vk_photo
Скрипт для накрутки фотокарточек в альбом вк  

![screenshot of sample](https://sun9-78.userapi.com/impg/3fFqGVqtcWoOssZsWX7Pu2E0dKqY96dCyMBdEA/3VZiTrYm28I.jpg?size=630x407&quality=96&sign=332158e957417ca1f68a117ec7190a2e&type=album)  
## Как пользоваться?
Запускаем скрипт и выбираем возможность входа(рекомендую создать конфиг и заходить с него, чтобы лишний раз не вводить буковки и цифорки при запуске, а в случае чего отредачить конфиг). Выбираем сколько фоток надо накрутить и также вводим путь на файл, который будем загружать(путь вводить не надо если файлик лежит в папке со скриптом, вводим просто его название) и все. Дальше просто ждем и наблюдаем за скачкой фоток в альбом.  
## Как скачать?
### TERMUX
При первом использовании термукса вводим  
apt update && apt upgrade -y  
termux-setup-storage  
Перезапускаем  
1. Для скрипта нужен питон, скачиваем  
pkg install python 
2. Чтобы скачать скрипт, нужен гит, его тоже скачиваем  
pkg install git
3. Теперь скачиваем сам скрипт  
git clone https://github.com/LinBR/vk_photo  
4. Переходим в папку со скриптом  
cd vk_photo
5. Скачиваем модули, что использует скрипт  
pip install -r requirements.txt
6. Запуск скрипта  
python main.py  
7. Если файл находится в загрузках, то колдуем следующее:  
../storage/shared/Download/имяфайла.срасширением
### Linux
1. Скачиваем скрипт  
git clone https://github.com/LinBR/vk_photo
3. Переходим в папку со скриптом  
cd vk_photo
4. Скачиваем все зависимости, которые использует бот  
pip install -r requirements.txt
5. Запуск скрипта  
python main.py
### Windows
1. Скачиваем питон  
[Ссылка на видео где показывают как это делается](https://www.youtube.com/watch?v=swZA4EJnsG0&ab_channel=MRSpace)
2. пишем в консольке  
pip install python3-anticaptcha   
pip install requests  
pip install vk-api  
3. Скачиваем мое творение из гитхаба (находим зеленую кнопку Code, кликаем на нее->Download zip->распаковываем)
4. переходим по пути где находится код в консольке и вводим  
python main.py  
