# Учебный проект YAtube
## Описание
Учебный проект для отработки навыков работы с **Django Flamework** в рамках финального задания спринта 6.
Создавался на Python 3.9
## Функционал
Сайт-социальная сеть, имеется возможность зарегистрироваться, писать посты, к постам прикладывать фото. Пост можно поместить в группу (список групп создаётся админом). К посту зарегистрированные пользователи могут писать комментарии.

## Установка
### Клонировать репозиторий с github:
```
git clone https://github.com/lorpaxx/hw05_final.git
```
### Перейти в склонированный каталог
```
cd hw05_final
```
### Создать и активировать виртуальное окружение, обновить pip
windows
```
python -m venv venv

source venv/Scripts/activate

python -m pip install --upgrade pip
```
linux
```
python3 -m venv venv

source venv/bin/activate

python3 -m pip install --upgrade pip
```
### C помощью pip доустановить остальные необходимые пакеты
```
pip install -r requirements.txt
```
### Перейти в католог yatube, выполнить миграции, запустить проект
```
cd yatube
python manage.py migrate
python manage.py runserver
```