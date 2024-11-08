# isearch 

## Общее описание 

Система для семантического поиска по картинкам, сохранённым в папках на ПК пользователя. 

У многих людей есть папка "Изображения" на компьютере, в которой тысячи файлов с бесполезными названиями, по которым невозможно ориентироваться, поэтому при надобности достать нужный файл очень проблематично. 

Поэтому предлагается разработать систему Daemon+CLI, с помощью которой можно будет выполнять быстрый семантический поиск по картинкам в любой из выбранных директорий. 

Пример использования: 
```bash 
$ isearch 'мемы с котиками' 

/Users/roshi/Pictures/pic-full-210626-1542-58.png
/Users/roshi/Pictures/pic-full-210306-2218-27.png
/Users/roshi/Pictures/pic-selected-200611-2059-42.png
/Users/roshi/Pictures/pic-selected-211031-1421-57.png
/Users/roshi/Pictures/Screenshot 2022-06-05 at 08.40.30.png
```

## Итоги разработки первой версии 

### Модули 

Были разработаны 3 приложения: 

- `isearchd` - Linux-демон, который работает с ML моделью, обрабатывает запросы клиентов, подписывается на события файловой системы, поддерживает индекс изображений в БД 
- `isearchcli` - главный клиент, через который происходит использование системы поиска. Подключается к `isearchd` через Unix-сокет и запрашивает поиск. 
- `isearchctl` - дополнительный клиент-конфигуратор, через который пользователи могут конфигурировать систему и вызывать весь функционал кроме поиска. В данной версии это команда `reindex`, с помощью которой можно вызывать реиндексацию изображений в произвольной директории.
 
Были написаны интеграционные тесты для всей системы (кроме ML-модели) и настроены в [CI Github Actions](https://github.com/k0marov/isearch/actions). 

### Технологии

Были использованы следующие технологии: 
- Python3 
- SQLite3 для персистентного хранения эмбеддингов. Расширение [sqlite-vec](https://github.com/asg017/sqlite-vec) для векторного поиска. 
- [CLIP](https://github.com/openai/CLIP) - ML модель для генерации эмбеддингов. 
- `inotify` для получения ивентов файловой систему через пакет [watchdog](https://pypi.org/project/watchdog/)
- Unix-sockets. Сервер и клиенты через биндинги либы `asyncio`

### Ограничения 

#### ML 

Baseline модель CLIP, используемая в проекте - сравнительно небольшая по размеру и потребляемым ресурсам (чтобы проще было запускать локально) 
и в какой-то мере недостаточно умная для реального использования. 

Она отлично справляется с семантическим поиском, если на картинке 1-2 главных объекта, тогда поисковые запросы выдают верные результаты. 
Но если использовать сложные изображения, особенно с текстом, она может выдавать неверные результаты. Это логично, ведь в эмбеддинг из 640 чисел невозможно поместить столько данных. 

Поэтому в [docs/sample_images/](docs/sample_images/) используются простые изображения: кошечки, собачки и тд. Для более реалистичного использования нужно провести дополнительную работу по ML части (в проект интегрировать это будет легко). 

#### Прослушивание нескольких папок 

Допзадача - прослушивание нескольких папок не была реализована. Поскольку SQLite не поддерживает асихронные write, эта фича может сильно усложнить проект, поэтому в данной версии она опущена. Но доп папки можно индексировать с помощью `isearchctl reindex`. 

#### Linux 

Проект изначально предполагал запуск на ОС Linux, потому что интерес был в реализации "системной проги" в виде коммуникации через Unix-сокеты. 

На Windows проект не тестировался. 

### Локальный запуск 

Гайд по локальному запуску находится здесь [docs/local_usage_guide.md](docs/local_usage_guide.md). 

## Реализация 

В качестве модели используется CLIP: эта мультимодальная модель может получать на вход как текст, так и изображения, и возвращать векторные эмбеддинги для них, которые потом можно сравнивать. В этом и заключается суть семантического поиска.  

Крутится демон isearchd, который подписан на события в папках через inotify, при появлении нового файла он генерирует для него эмбеддинг через CLIP и записывает в SQLite вместе с путём к файлу. 

Когда приходит запрос из isearch, для текстового запроса генерируется эмбеддинг через CLIP и затем происходит векторный поиск по самым совпадающим эмбеддингам из БД. 

## Диаграммы 

### Диаграмма C1 
![](docs/diagram_c1.png)

### Диаграмма C2 
![](docs/diagram_c2.png)

[Ссылка на диаграммы](https://drive.google.com/file/d/1ZRCyDkhljztHS2Crj0z7jfxlvnq18PN3/view?usp=sharing)

## Задачи 

- [x] Документация, диаграммы 
- [x] isearch CLI  
- [x] Интеграция isearch и isearchd через Unix-сокет
- [x] isearchd: прослушивание ивентов из inotify 
- [x] isearchd: обёртка для CLIP 
- [x] isearchd: обёртка для бд и поиска 

### Допзадачи 
- [x] isearch: команда reindex
- [x] isearchctl: realtime отображение прогресса для reindex через сокеты
- [x] isearchd: корректная обработка удаления и изменения файлов
- [x] isearch: аргумент для кол-ва картинок 
- [x] интеграционные тесты для isearchd, isearchctl, isearchcli
- [ ] isearchctl - добавление нескольких папок для индексирования
- [ ] isearchd: прослушивание нескольких папок 
- [ ] isearchd: отдельный поиск по папкам
