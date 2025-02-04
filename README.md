# TGD (TeleGram Downloader) 🇺🇸
### Download all types of media from Telegram to your local system even if it is restricted
#### To get started, download binaries from the [Modified version](https://github.com/abortacc/TGD/releases/tag/v1.2.M) or [Original Releases Section](https://github.com/bipinkrish/tgd/releases). Supports [Windows](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd.exe) and [Linux](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd).
* If you do not have a Session String for your account, the program will ask for login credentials to generate one. The phone number should be in the format:
  `<countrycode><number>`
  Example: `910123456789` (here `91` is the code for India and `0123456789` is the number).у
* API ID and API HASH can be obtained from [my.telegram.org](https://my.telegram.org).
* All these details will be stored in `tgd.txt` for future use.
### New Features:
#### 1. **Loading from `links.txt`**
   - **Description**: The program now supports automatic loading of media files from a list of links specified in the `links.txt` file.
   - **Usage Instructions**:
     1. Enable `"enable_links_auto_read": true` in `config.json`.
     2. Create a `links.txt` file in the same directory as `tgd.exe`.
     3. Add links to Telegram messages or posts, one per line.
     4. Run the program, and it will automatically process the links from the file.

#### 2. **Simplified Exit Process**
   - **Description**: To exit the program, simply type `exit` at any time.

#### 3. **Advanced Logging**
   - **Description**: The program now supports advanced logging with detailed information about downloaded files, including file size, resolution, and metadata.
   - **Usage Instructions**:
     1. Enable logging by setting `"logging": true` in the `config.json` file.
     2. Upon enabling, the program will create a `logging.conf` configuration file and log all activities to `app.log`.
     3. Logs include:
        - Progress of downloads.
        - Detailed metadata of media files (e.g., file name, size, resolution, MIME type).
        - Errors and warnings during execution.
   - **Example Log Entry**:
     ```
     2023-10-05 12:00:06 - root - INFO - Media details for message 1423 (1/10): {
         'type': 'MessageMediaDocument',
         'file_name': 'example.jpg',
         'file_size': '1.23 MB',
         'mime_type': 'image/jpeg',
         'duration': 'N/A',
         'width': 1920,
         'height': 1080
     }
     ```

#### 4. **Detailed Metadata for Media Files**
   - **Description**: When downloading media files, the program logs detailed metadata such as file size, resolution (for images/videos), duration (for audio/video), and MIME type.
   - **Usage Instructions**:
     - Ensure logging is enabled (`"logging": true` in `config.json`).
     - Metadata will be automatically logged for each downloaded file.

![photo](https://github.com/bipinkrish/TGD/assets/87369440/af534efa-347e-4d23-9818-4b2c474dfb69)

---

# TGD (TeleGram Downloader) – 🇷🇺
### Загрузка всех типов медиафайлов из Telegram на ваш локальный компьютер, даже если они ограничены
#### Чтобы начать, скачайте файлы из [Модифицированной версии](https://github.com/abortacc/TGD/releases/tag/v1.2.M) или [Оригинального раздела Releases](https://github.com/bipinkrish/tgd/releases). Поддерживаются [Windows](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd.exe) и [Linux](https://github.com/bipinkrish/tgd/releases/download/v1.2/tgd).
* Если у вас нет Session String для вашего аккаунта, программа запросит данные для входа, чтобы сгенерировать его. Номер телефона должен быть в формате:
  `<код страны><номер>`
  Пример: `910123456789` (где `91` — код Индии, а `0123456789` — номер).
* API ID и API HASH можно получить на [my.telegram.org](https://my.telegram.org).
* Все эти данные будут сохранены в файле `tgd.txt` для дальнейшего использования.
### Новые функции:
#### 1. **Загрузка из `links.txt`**
   - **Описание**: Теперь программа поддерживает автоматическую загрузку медиафайлов из списка ссылок, указанных в файле `links.txt`.
   - **Инструкция по использованию**:
     1. Включите параметр `"enable_links_auto_read": true` в `config.json`.
     1. Создайте файл `links.txt` в той же директории, где находится `tgd.exe`.
     2. Добавьте ссылки на сообщения или посты Telegram, по одной на строку.
     3. Запустите программу, и она автоматически обработает ссылки из файла.

#### 2. **Упрощенный процесс выхода**
   - **Описание**: Для выхода из программы теперь достаточно ввести команду `exit` в любой момент.

#### 3. **Расширенное логирование**
   - **Описание**: Программа теперь поддерживает расширенное логирование с подробной информацией о скачиваемых файлах, включая размер, разрешение и метаданные.
   - **Инструкция по использованию**:
     1. Включите логирование, установив `"logging": true` в файле `config.json`.
     2. После включения программа создаст конфигурационный файл `logging.conf` и будет записывать все действия в файл `app.log`.
     3. Логи включают:
        - Прогресс скачивания.
        - Подробные метаданные медиафайлов (например, имя файла, размер, разрешение, MIME-тип).
        - Ошибки и предупреждения во время выполнения.
   - **Пример записи в логах**:
     ```
     2023-10-05 12:00:06 - root - INFO - Метаданные для сообщения 1423 (1/10): {
         'type': 'MessageMediaDocument',
         'file_name': 'example.jpg',
         'file_size': '1.23 MB',
         'mime_type': 'image/jpeg',
         'duration': 'N/A',
         'width': 1920,
         'height': 1080
     }
     ```

#### 4. **Подробные метаданные для медиафайлов**
   - **Описание**: При скачивании медиафайлов программа записывает подробные метаданные, такие как размер файла, разрешение (для изображений/видео), длительность (для аудио/видео) и MIME-тип.
   - **Инструкция по использованию**:
     - Убедитесь, что логирование включено (`"logging": true` в `config.json`).
     - Метаданные будут автоматически записываться для каждого скачанного файла.

![photo](https://github.com/bipinkrish/TGD/assets/87369440/af534efa-347e-4d23-9818-4b2c474dfb69)