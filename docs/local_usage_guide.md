# Локальный запуск

### 1. Клонирование и инициализация
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
pip install -r requirements.txt 
```

### 2. Запуск isearchd

Создадим папку с изображениями, где будем проводить тесты. 

Запустим daemon `isearchd`, указав ему путь к этой тестовой папке.
```bash
mkdir ~/Images_test
cd isearchd 
source venv/bin/activate 

python3 main.py -h 
ISEARCHD_IMAGES_DIR=$HOME/Images_test python3 main.py 
```

Первый старт займёт долгое время, так как будет скачиваться ML модель. При последующих стартах она будет доставаться из кэша.

Теперь этот демон будет прослушивать события
создания/перемещения/изменения/удаления файлов изображений в указанной директории,
и записывать данные в базу `~/.cache/isearch/db.sqlite3`.

Кроме того, он прослушивает подключения и запросы по сокету `~/.cache/isearch/isearchd.sock`.

Оба этих пути можно изменить через переменные окружения, см. [isearchd/README.md]().

#### 4. Использование isearchcli и isearchctl (в другом терминале)

Для начала перместим несколько тестовых изображений в папку (их можно взять из [docs/sample_images]()):
```bash
cp docs/sample_images/{dog1,dog2,human,cat,cat2,cat_meme1,cat_meme2}.png ~/Images_test 
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

Теперь проверим фичу реиндексации через isearchctl - это когда мы хотим за 1 команду переиндексировать выбранную папку (и не обязательно ту, которая прослушивается).

Удалим несколько картинок из нашей папки, `isearchd` должен удалить их из индекса, так как прослушивает события через `inotify`:
```bash 
rm ~/Images_test/dog{1,2}.png 
```
Теперь создадим новую папку, добавим пару картинок и запустим для неё `reindex`.
```bash
mkdir ~/Images_test2 
cp docs/sample_images/* ~/Images_test2

cd isearchctl 
source venv/bin/activate 
python3 main.py -h 
python3 main.py reindex ~/Images_test2 
```

Должен отображаться прогресс, получаемый в реалтайме из `isearchd` по сокету.

Теперь то, что изображения были проиндексированы, можно проверить через `isearchcli`. 

