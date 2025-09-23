# Лабораторная работа №1

## Задание:
Настроить nginx по заданному тз:
Должен работать по https c сертификатом
Настроить принудительное перенаправление HTTP-запросов (порт 80) на HTTPS (порт 443) для обеспечения безопасного соединения.
Использовать alias для создания псевдонимов путей к файлам или каталогам на сервере.
Настроить виртуальные хосты для обслуживания нескольких доменных имен на одном сервере.
Что угодно еще под требования проекта
## Результат:
Предположим, что у вас есть два пет проекта на одном сервере, которые должны быть доступны по https. Настроенный вами веб сервер умеет работать по https, относить нужный запрос к нужному проекту, переопределять пути исходя из требований пет проектов.
В качестве пет проектов можете использовать что-то свое, можете что-то опенсорсное, можете просто код из трех строчек как например здесь

## Ход работы:
### 1. Установка необходимых пакетов

`sudo apt update && sudo apt install nginx openssl -y`

Проверяем, что сервер запущен успешно: 

<img width="762" height="309" alt="изображение(1)1" src="https://github.com/user-attachments/assets/4f7a955f-f29a-4c95-b5cc-56967d306ae4" />

### 2. Создаем струтуру каталогов 

`sudo mkdir -p /etc/nginx/sites-available`

`sudo mkdir -p /etc/nginx/sites-enabled`

`sudo mkdir -p /var/www/project1/assets`

`sudo mkdir -p /var/www/project2/data`

где:

-sites-available - доступные конфигурации

-sites-enabled - активные конфигурации

-/var/www/ - корневые каталоги проектов
Что это делает?

/etc/nginx/sites-available/ —  каталог, где  хранятся конфигурационные файлы для всех виртуальных хостов 

/etc/nginx/sites-enabled/ —  каталог, где хранятся сссылки на конфиги из sites-available, а nginx cчитывает оттуда конфиги.

/var/www/project1/assets и /var/www/project2/data —  корневые каталоги, которые хранят HTML, CSS, JS и другие файлы

<img width="576" height="427" alt="изображение (3)3" src="https://github.com/user-attachments/assets/d7141e5d-7715-4944-896d-4f5833d37483" />


### 3. Генерируем SSL-сертификата

`sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt`

где:

-req -x509 - создание самоподписанного сертификата

-nodes - не шифровать приватный ключ

-days 365 - срок действия сертификата

-newkey rsa:2048 - генерация RSA-ключа 2048 бит

-keyout - путь сохранения приватного ключа

-out - путь сохранения сертификата

<img width="1280" height="547" alt="изображение (5)5" src="https://github.com/user-attachments/assets/a8809562-a9dc-42c9-b252-d3e548cc3151" />


### 4. Настройка конфигурационных файлов

`sudo nano /etc/nginx/nginx.conf`

<img width="1280" height="800" alt="Снимок экрана от 2025-09-11 22-23-31" src="https://github.com/user-attachments/assets/6f1aad01-3319-47cb-8d69-33a056af011a" />


`sudo nano /etc/nginx/sites-available/project1.conf`

<img width="501" height="451" alt="изображение (7)" src="https://github.com/user-attachments/assets/71945014-b273-4605-8d22-63e3672caabb" />

Т.е первый блок server слушает http-запросы на порту 80, отвечает на запросы к домену и перенаправляет все http-запросы на https. Второй блок server слушает hhtps-запросы на порту 443, указывает пути к SSl-сертификату и ключу, определяет корневую директорию и обрабатывает все запросы к сайту

`sudo nano /etc/nginx/sites-available/project2.conf`

<img width="1280" height="800" alt="изображение (9)" src="https://github.com/user-attachments/assets/0e393905-ec1f-4782-a85b-38b9db376213" />

Аналогичный файл был создан для project2.conf, где server_name был project2.local, а root и alias вели на соответствующие каталоги /var/www/project2.

### 5. Активация виртуальных хостов

`sudo ln -s /etc/nginx/sites-available/project1.conf /etc/nginx/sites-enabled/`
`sudo ln -s /etc/nginx/sites-available/project2.conf /etc/nginx/sites-enabled/`

Применяем систему разделения конфигураций на директории sites-available и sites-enabled, чтобы обеспечить гибкое и безопасное управление виртуальными хостами.

### 6 Создaние страниц и тестовых файлов

`sudo nano /var/www/project1/index.html`

<img width="1280" height="800" alt="Снимок экрана от 2025-09-11 22-46-17" src="https://github.com/user-attachments/assets/3e20907a-bf1d-472a-a9e3-4c751c874d57" />


`sudo nano /var/www/project1/assets/test.html`

`sudo nano /var/www/project1/assets/image.txt`

`sudo nano /var/www/project2/index.html`

`sudo nano /var/www/project2/data/data.json`

`sudo nano /var/www/project2/data/config.txt`

Т.е мы создали главную страницу index.html и файлы разных типов, чтобы проверить alias

Также мы настроили права доступа для лучшей работоспособности и отсутсивя ошибок при переходе по ссылкам:

`sudo chown -R www-data:www-data /var/www/project1/`

`sudo chown -R www-data:www-data /var/www/project2/`

`sudo chmod -R 755 /var/www/project1/`

`sudo chmod -R 755 /var/www/project2/`

### 7 Настройка доменов 

`sudo nano /etc/hosts`

<img width="1280" height="800" alt="Снимок экрана от 2025-09-11 22-48-3811" src="https://github.com/user-attachments/assets/d7a57530-4f51-42c3-913c-ddb2c70dab75" />

Мы добавили строчки: `127.0.0.1   project1.local` и
`127.0.0.1   project2.local` для того, чтобы браузер понимал, что по адресу progect1.local находится наш сервер и не искал его в интеренете.

### 8 Проверка конфигураций и конфликтов 

`sudo nginx -t `

<img width="879" height="125" alt="Снимок экрана от 2025-09-11 22-55-11(1)" src="https://github.com/user-attachments/assets/d8e887d9-980e-4d48-97de-e19a5829063b" />

Nginx работает корректно, а предупреждения не мешают ходу работы и вполне ожидаемы, тк мы перенаправляем порты.
### 9 Тестирование
1. `curl -I http://project1.local`
<img width="607" height="152" alt="ббббб(1)1111" src="https://github.com/user-attachments/assets/b690bf26-b52d-4a4c-a035-689e7712ccc7" />

Мы делаем запрос по http, nginx получает запрос на порт 80, сервер видит правило и отправляет запрос с кодом 301 -> браузер автоматически переходит на https:/project1.local.

Основное, что мы тут видим, что клиент будет перенаправлен на https версию (Location: https:/project1.local/)

2. `curl -I http://project2.local`

<img width="490" height="151" alt="Снимок экрана от 2025-09-11 23-04-054444(1)" src="https://github.com/user-attachments/assets/6114fef5-c157-4907-bd65-f5ce885fa208" />

Тут аналогично пункту 1

3. Тестируем HTTPS соединение:

`curl -k https://project1.local`

<img width="795" height="491" alt="нов" src="https://github.com/user-attachments/assets/102363be-fabd-44b3-9d27-50db4a4dd35c" />

`curl -k https://project2.local`

<img width="652" height="489" alt="новнов" src="https://github.com/user-attachments/assets/2ef17e03-07dc-4ddb-b71f-a1e522a46704" />

Эти тесты подтверждают, что HTTPS соединение установлено успешно

4. Проверяем api через alias:

`curl -k https://project2.local/api/test.html`

<img width="645" height="235" alt="мурмур" src="https://github.com/user-attachments/assets/640a4a4b-6a70-4a16-a05f-346a9e65d627" />

Тест подтвержает, что  запрос к https://project2.local/api/test.html будет обслуживаться из файла /var/www/project2/data/test.html. Т.е мы обращаемся к URL `/api/test.html` и nginx через alias перенаправляет запрос

5. Тестирование в браузере

<img width="1280" height="800" alt="Снимок экрана от 2025-09-11 23-38-06" src="https://github.com/user-attachments/assets/71fc88b0-adfd-480a-9af5-f7bfcff96017" />

<img width="1280" height="800" alt="Снимок экрана от 2025-09-11 23-37-56" src="https://github.com/user-attachments/assets/2b4cfb34-430e-44a5-9fb3-8a0a28a781da" />

<img width="1280" height="800" alt="Снимок экрана от 2025-09-12 01-05-04" src="https://github.com/user-attachments/assets/b90458ce-7f2b-42f8-92b6-5221f9efac05" />


<img width="1280" height="800" alt="Снимок экрана от 2025-09-12 01-05-22" src="https://github.com/user-attachments/assets/63eff26d-a0ea-4030-ae63-c8c598394251" />

## Вывод

В ходе работы был успешно настроен веб-сервер Nginx для обслуживания двух проектов с полным соблюдением требований технического задания. Реализовано  перенаправление HTTP на HTTPS с использованием самоподписанного SSL-сертификата, что обеспечивает безопасное соединение. Настроены виртуальные хосты для раздельного обслуживания доменов project1.local и project2.local на одном сервере, а также применены alias для организации псевдонимов путей.
