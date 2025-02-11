# TGD (TeleGram Downloader) - 🇺🇸
### Download all types of media from Telegram to your local system even if it is restricted
#### To get started, download binaries from the [Modified version](https://github.com/abortacc/TGD/releases/tag/v1.4.M) or [Original Releases Section](https://github.com/bipinkrish/tgd/releases). Supports [Windows](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd.exe) and [Linux](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd).
TeleGram Downloader (TGD) is a tool for automatically downloading messages and media files from Telegram (Including from closed channels).

## How to start using the software

If you don't have a Session String for your account, the program will automatically request login details to generate one.

1. Enter your phone number in the format: `<country code><number>`.
   - For example, for India: `910123456789` (where `91` is the country code and `0123456789` is the phone number).
2. Enter the API ID and API HASH, which can be obtained from [my.telegram.org](https://my.telegram.org/).
3. All this data is stored in `config.json` and is used for subsequent runs of the program.

## Configuration

The application uses the `config.json` file to configure parameters. The following is a description of the available parameters:

```json
{
    "api_id": "API ID",
    "api_hash": "API HASH",
    "session_string": "SESSION STRING",
    "settings": {
        "enable_links_auto_read": false,
        "logging": false,
        "wait_seconds": 0,
        "post_step": 1,
        "max_requests_per_second": 5,
        "random_delay_min": 1,
        "random_delay_max": 5
    }
}
```

### Description of `settings` parameters

- **enable\_links\_auto\_read** *(bool)* - enables or disables automatic reading of links from `links.txt` file. If `true`, the program automatically loads links from the specified file.
- **logging** *(bool)* - enables or disables logging of the program. It is useful for debugging and monitoring the work.

- **wait\_seconds** *(int)* - sets the delay (in seconds) between downloading groups of messages. It is recommended to set it to 1-3 seconds if the Telegram server limits requests.
- **post\_step** *(int)* - defines the number of messages downloaded per step. The higher the value, the faster the download, but the higher the load on Telegram API.
[![Help](https://github.com/abortacc/TGD/blob/main/assets/post_wait.png)]
[![Help](https://github.com/abortacc/TGD/blob/main/assets/post_wait2.png)]

- **max\_requests\_per/second** *(int)* - the maximum number of requests to the Telegram API per second. The optimal value is 5 to avoid temporary blocking.
- **random\_delay\_min** *(int)* and **random\_delay\_max** *(int)* - set the minimum and maximum random delay time before each API request. Used to mimic natural behavior.

## Using the `links.txt` file

The `links.txt` file is used to store a list of links to messages or ranges of messages to be loaded. Each line must contain one link. For example:

```
https://t.me/xxxx/1423
https://t.me/c/xxxx/10
https://t.me/xxxx/1001-1010
https://t.me/c/xxxx/101-120
```

This file is handy if you need to download many links without manual input.

## Downloading and organizing files

After starting the program, it will automatically create a `downloads` folder in the root directory. All downloaded files will be sorted into subfolders named after the channels from which they were downloaded. For example:

```
downloads/
    ├── channel_name1/
    │ ├─── file.mp4
    ├─── channel_name2/
    │ ├─── file.jpg
```

This structure helps you easily navigate through the loaded data.

## Logging

If logging is enabled (`logging: true`), log files are saved to `app.log`. Example contents:

```
2025-02-10 17:57:23 - root - INFO - Handling link: https://t.me/channel_name/1254
2025-02-10 17:57:24 - root - INFO - API Request: Fetching message, Chat ID: channel_name, Message ID: 1254
2025-02-10 17:57:34 - root - INFO - Media details for message 1254 (1/1): {'type': 'Video', 'file_name': None, 'file_size': '13.00 MB', 'mime_type': 'video/mp4', 'duration': 30, 'width': 720, 'height': 1280}
2025-02-10 17:57:34 - root - INFO - API Request: Downloading media, Chat ID: channel_name, Message ID: 1254
2025-02-10 17:57:40 - root - INFO - File saved at: downloads\channel_name\1254_video.mp4
```

The `logging.conf` file allows you to customize the logging settings.

## Usage

1. Enter a message link or range of messages manually or download them from `links.txt`.
2. Follow the instructions in the console.

## Developer

Author: [abortacc] Version: 1.4.M


![photo](https://github.com/bipinkrish/TGD/assets/87369440/af534efa-347e-4d23-9818-4b2c474dfb69)

---

# TGD (TeleGram Downloader) – 🇷🇺
### Загрузка всех типов медиафайлов из Telegram на ваш локальный компьютер, даже если они ограничены
#### Чтобы начать, скачайте файлы из [Модифицированной версии](https://github.com/abortacc/TGD/releases/tag/v1.4.M) или [Оригинального раздела Releases](https://github.com/bipinkrish/tgd/releases). Поддерживаются [Windows](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd.exe) и [Linux](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd).

TeleGram Downloader (TGD) - это инструмент для автоматического скачивания сообщений и медиафайлов из Telegram (В том числе и из закрытых каналов).

## Как начать пользоваться софтом

Если у вас нет Session String для вашего аккаунта, программа автоматически запросит данные для входа, чтобы сгенерировать его.

1. Введите номер телефона в формате: `<код страны><номер>`.
   - Например, для Индии: `910123456789` (где `91` — код страны, а `0123456789` — номер телефона).
2. Введите API ID и API HASH, которые можно получить на [my.telegram.org](https://my.telegram.org/).
3. Все эти данные сохраняются в `config.json` и используются для последующих запусков программы.

## Конфигурация

Приложение использует файл `config.json` для настройки параметров. Ниже приведено описание доступных параметров:

```json
{
    "api_id": "Ваш API ID",
    "api_hash": "Ваш API HASH",
    "session_string": "Строка сессии",
    "settings": {
        "enable_links_auto_read": false,
        "logging": false,
        "wait_seconds": 0,
        "post_step": 1,
        "max_requests_per_second": 5,
        "random_delay_min": 1,
        "random_delay_max": 5
    }
}
```

### Описание параметров `settings`

- **enable\_links\_auto\_read** *(bool)* — включает или отключает автоматическое чтение ссылок из файла `links.txt`. Если `true`, программа автоматически загружает ссылки из указанного файла.
- **logging** *(bool)* — включает или отключает ведение логов работы программы. Полезно для отладки и мониторинга работы.

- **wait\_seconds** *(int)* — задает задержку (в секундах) между скачиванием групп сообщений. Рекомендуется устанавливать в 1-3 секунды, если сервер Telegram ограничивает запросы.
- **post\_step** *(int)* — определяет количество сообщений, скачиваемых за один шаг. Чем выше значение, тем быстрее скачивание, но выше нагрузка на API Telegram.
[![Help](https://github.com/abortacc/TGD/blob/main/assets/post_wait.png)]
[![Help](https://github.com/abortacc/TGD/blob/main/assets/post_wait2.png)]

- **max\_requests\_per\_second** *(int)* — максимальное количество запросов в API Telegram в секунду. Оптимальное значение — 5, чтобы избежать временных блокировок.
- **random\_delay\_min** *(int)* и **random\_delay\_max** *(int)* — задают минимальное и максимальное случайное время задержки перед каждым API-запросом. Используются для имитации естественного поведения.

## Использование файла `links.txt`

Файл `links.txt` предназначен для хранения списка ссылок на сообщения или диапазоны сообщений, которые необходимо загрузить. Каждая строка должна содержать одну ссылку. Например:

```
https://t.me/xxxx/1423
https://t.me/c/xxxx/10
https://t.me/xxxx/1001-1010
https://t.me/c/xxxx/101-120
```

Этот файл удобен, если нужно загрузить много ссылок без ручного ввода.

## Скачивание и организация файлов

После запуска программа автоматически создаст папку `downloads` в корневой директории. Все загруженные файлы будут сортироваться по подпапкам, названным в честь каналов, из которых они были скачаны. Например:

```
downloads/
    ├── channel_name1/
    │   ├── file.mp4
    ├── channel_name2/
    │   ├── file.jpg
```

Эта структура помогает легко ориентироваться в загруженных данных.

## Логирование

Если включено логирование (`logging: true`), файлы логов сохраняются в `app.log`. Пример содержимого:

```
2025-02-10 17:57:23 - root - INFO - Handling link: https://t.me/channel_name/1254
2025-02-10 17:57:24 - root - INFO - API Request: Fetching message, Chat ID: channel_name, Message ID: 1254
2025-02-10 17:57:34 - root - INFO - Media details for message 1254 (1/1): {'type': 'Video', 'file_name': None, 'file_size': '13.00 MB', 'mime_type': 'video/mp4', 'duration': 30, 'width': 720, 'height': 1280}
2025-02-10 17:57:34 - root - INFO - API Request: Downloading media, Chat ID: channel_name, Message ID: 1254
2025-02-10 17:57:40 - root - INFO - File saved at: downloads\channel_name\1254_video.mp4
```

Файл `logging.conf` позволяет настраивать параметры логирования.

## Использование

1. Введите ссылку на сообщение или диапазон сообщений вручную или загрузите их из `links.txt`.
2. Следуйте инструкциям в консоли.

## Разработчик

Автор: [abortacc] Версия: 1.4.M


![photo](https://github.com/bipinkrish/TGD/assets/87369440/af534efa-347e-4d23-9818-4b2c474dfb69)