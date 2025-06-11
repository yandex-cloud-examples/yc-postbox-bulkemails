# Отправка писем из Yandex Cloud Postbox (postbox-sender.py)

1. Используйте следующие переменные окружения Yandex Cloud:
   - `AWS_ACCESS_KEY_ID` — статический ключ доступа сервисного аккаунта Yandex Cloud.
   - `AWS_SECRET_ACCESS_KEY` — секретная часть статического ключа доступа сервисного аккаунта Yandex Cloud.
   - `FROM` — адрес электронной почты, зарегистрированный в подтвержденном домене Yandex Postbox.
   - `LIST_ID` — идентификатор списка, который соответствует стандарту [RFC2919](https://datatracker.ietf.org/doc/html/rfc2919). 
   - `UNSUBSCRIBE_LINK` — ссылка на функцию Yandex Cloud для отписки.
   - `UNSUBSCRIBE_MAIL` — триггер электронной почты Yandex Cloud для отписки.
2. Подключите хранилище Object Storage к функции Cloud Functions с точкой монтирования **bucket** (или измените пути к файлам либо имена файлов внутри кода).
3. Используйте файл `bulkemail.xlsx` для адресов массовой рассылки, а файл `blacklist.xlsx` для адресов отписавшихся пользователей.

# Функция отписки Cloud Functions (`postbox-unsubscribe.py`)
Эта функция добавляет адреса электронной почты отписавшихся пользователей в файл `blacklist.xlsx`. 
1. Подключите хранилище Object Storage к функции Cloud Functions с точкой монтирования **bucket** (или измените пути к файлам либо имена файлов внутри кода) и **отключите режим read-only**.
2. Выполните функцию со следующими параметрами URL: `email` (добавляемый адрес) и `l` (список адесов для рассылки). Пример: https://functions.yandexcloud.net/d4sdxfer4243sdxfcvfr?email=a@example.com&l=demolist.example.com.

Видеоинструкцию по использованию сервиса см. [здесь](https://yandex.cloud/ru/events/878).
