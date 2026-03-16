# Лабораторная работа №1 - Docker
## Вариант 2

## Ход выполнения
1. Создание *config.json*
2. Создание namespace
```
CLONE_NEWNS = 0x00020000   # Mount namespace
CLONE_NEWUTS = 0x04000000  # UTS namespace
CLONE_NEWPID = 0x20000000  # PID namespace
```
3. Контейнеры с идентификатором <id>
```
upper = base_path / "upper"
work = base_path / "work"
merged = base_path / "merged"
lower = "/tmp/alpine-rootfs" # Путь к вашей базовой ОС
```
4. Тестирование
```
ubuntu@container-dev:~/container-lab$ sudo python3 container_tool.py my-id-1
/ # ls -l
total 64
drwxr-xr-x    2 root     root          4096 Jan 26  2024 bin
drwxr-xr-x    2 root     root          4096 Jan 26  2024 dev
drwxr-xr-x   19 root     root          4096 Jan 26  2024 etc
drwxr-xr-x    2 root     root          4096 Jan 26  2024 home
drwxr-xr-x    7 root     root          4096 Jan 26  2024 lib
drwxr-xr-x    5 root     root          4096 Jan 26  2024 media
drwxr-xr-x    2 root     root          4096 Jan 26  2024 mnt
drwxr-xr-x    2 root     root          4096 Jan 26  2024 opt
dr-xr-xr-x  172 root     root             0 Mar 15 20:02 proc
drwx------    1 root     root          4096 Mar 15 20:02 root
drwxr-xr-x    2 root     root          4096 Jan 26  2024 run
drwxr-xr-x    2 root     root          4096 Jan 26  2024 sbin
drwxr-xr-x    2 root     root          4096 Jan 26  2024 srv
drwxr-xr-x    2 root     root          4096 Jan 26  2024 sys
drwxrwxrwt    2 root     root          4096 Jan 26  2024 tmp
drwxr-xr-x    7 root     root          4096 Jan 26  2024 usr
drwxr-xr-x   12 root     root          4096 Jan 26  2024 var
```
```
/ # echo "Hello from container" > /success.txt
/ # ls /
bin          home         mnt          root         srv          tmp
dev          lib          opt          run          success.txt  usr
etc          media        proc         sbin         sys          var
```
```
/ # hostname
artemij-container
```
```
/ # ps aux
PID   USER     TIME  COMMAND
    1 root      0:00 /bin/sh
    7 root      0:00 ps aux
```
## Поблемы, с которыми я столкнуля
1. Выполнение работы на macos

Пришлось устанавливать ВМ Multipass.

```
brew install multipass
multipass launch --name container-dev --cpus 2 --mem 2G --disk 10G
multipass shell container-dev
```
