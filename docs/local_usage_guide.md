# Локальный запуск

### 1. Клонирование и инициализация

NOTE: Вся модель + зависимости занимает 5 ГБ, поэтому если не хочется скачивать её,
можно протестировать всё без неё, запустив проект в режиме интеграционного тестирования.
Для этого нужно выставить переменную окружения `export ISEARCH_TEST=1` (запускать isearchd с таким флагом). 
Тогда достаточно будет на следующем шаге выполнить `pip install -r test.requirements.txt` (вместо всего `requirements.txt`) для `isearchd`. 
В таком случае в качестве эмбеддингов будут генерироваться рандомные векторы, но вся остальная (питоновская) часть проекта будет работать.

```bash
git clone 'github.com/k0marov/isearch' isearch 
cd isearch 
git checkout v0.1.0 

cd isearchcli 
python3 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt 

cd ../isearchctl   
python3 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt 

cd ../isearchd 
python3 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt  # or test.requirements.txt to skip ML model dependencies
```

### 2. Запуск isearchd

Создадим папку с изображениями, где будем проводить тесты.
```bash
mkdir ~/Images_test
````

Первый старт займёт долгое время, так как будет скачиваться ML модель. При последующих стартах она будет доставаться из кэша.


Запустим daemon `isearchd`, указав ему путь к этой тестовой папке.
```bash
cd isearchd 
source venv/bin/activate 

python3 main.py -h 
ISEARCHD_IMAGES_DIR=$HOME/Images_test python3 main.py 
```

Теперь этот демон будет прослушивать события
создания/перемещения/изменения/удаления файлов изображений в указанной директории,
и записывать данные в базу `~/.cache/isearch/db.sqlite3`.

Кроме того, он прослушивает подключения и запросы по сокету `~/.cache/isearch/isearchd.sock`.

Оба этих пути можно изменить через переменные окружения, см. [isearchd/README.md](../isearchd/README.md) или `python3 main.py -h`.

### 3. Использование isearchcli и isearchctl (в другом терминале)

Для начала переместим несколько тестовых изображений в папку. 
Для удобства их можно взять из [docs/sample_images/](../docs/sample_images/) 
(эта папка находится в ветке `extra/sample_images`, чтобы не захламлять ветки разработки):
```bash
git checkout extra/sample_images 
cp docs/sample_images/{dog1,dog2,human,cat,cat2,cat_meme,cat_meme2}.png ~/Images_test 
git checkout v0.1.0
```

Они должны проиндексироваться isearchd, это должно быть видно из логов.
Теперь выполним поиск:
```bash
cd isearchcli 
source venv/bin/activate 

python3 main.py -h 
python3 main.py 'котик'
python3 main.py -n 3 'человек'
```

Теперь проверим фичу реиндексации через isearchctl - 
это когда мы хотим за 1 команду рекурсивно переиндексировать всю выбранную папку (и не обязательно ту, которая прослушивается).

Для этого создадим новую папку, добавим пару картинок: 
```bash
mkdir ~/Images_test2 
cp ~/Images_test/* ~/Images_test2
``` 

Удалим картинки из нашей изначальной папки, `isearchd` должен удалить их из индекса, так как прослушивает события через `inotify`:
```bash 
rm ~/Images_test/dog{1,2}.png 
```

Запустим для новой папки `reindex`:
```bash
cd isearchctl 
source venv/bin/activate 
python3 main.py -h 
python3 main.py reindex ~/Images_test2 
```

Должен отображаться прогресс, получаемый в реалтайме из `isearchd` по сокету.

Теперь то, что изображения были проиндексированы, можно проверить через `isearchcli`. 