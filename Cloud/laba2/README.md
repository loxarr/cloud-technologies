# Лабораторная работа 2
# Сравнение сервисов Amazon Web Services и Microsoft Azure. Создание единой кросс-провайдерной сервисной модели.


Кросс-провайдерная сервисная модель — это единая система классификации облачных сервисов, которая позволяет:
Сравнивать аналогичные сервисы разных провайдеров (например, Amazon EC2 и Azure Virtual Machines), анализировать общие расходы на облачные услуги, оптимизировать облачные расходы на уровне всей компании.​

## Ход работы

### 1. Сравнение AWS и Azure

В отличие от AWS, где мы смотрели на Product Code, в Azure данные представлены по-другому:

Ключевые поля в Azure:
- Meter Category — аналог Product Code в AWS
- Meter Sub-Category — дополнительная детализация
- Meter Name — конкретное название или тип использования
- Consumed Service — указывает принадлежность к сервису Azure

По какому алгоритму заполняли:
- Смотрим на Meter Category — определяем основной тип сервиса
- Ищем аналог в AWS — находим похожий сервис из ЛР1
- Берем IT Tower и Service Family из аналога в AWS
- Service Type — пишем название сервиса Azure
- Service Sub Type и Service Usage Type — берем из Meter Sub-Category и Meter Name
- 
Например:
 
Amazon EC2(Сервис AWS)	→	Azure Virtual Machines(Сервис Azure)	→	Compute → Compute (Классификация)

### 2. Импорт 11 таблиц Azure и их заполнение
Заполняем первые 5 пустых столбцов. Логика заполнения:
- Смотрим на Meter Category (аналог ProductCode в AWS) — это основной идентификатор сервиса в Azure
- Ищем функциональный аналог в AWS из ЛР1:

Например:

Virtual Machines в Azure → Amazon EC2 в AWS

SQL Database в Azure → Amazon RDS в AWS

Data Factory в Azure → AWS Glue в AWS
- Берем IT Tower и Service Family из аналога в AWS:

если в AWS аналог был Compute → Compute, то и для Azure ставим Compute → Compute; 

если в AWS аналог был Cloud Services → Analytics, то и для Azure ставим Cloud Services → Analytics
- Service Type — пишем название сервиса Azure с префиксом "Azure":

Virtual Machines → Azure Virtual Machines; 

SQL Database → Azure SQL Database; 

Data Factory → Azure Data Factory
- Service Sub Type и Service Usage Type — берем из Meter Sub-Category и Meter Name:

Meter Sub-Category: D% → Service Sub Type: D-Series

Meter Name: Compute Hours → Service Usage Type: Compute Hours

Meter Sub-Category: Tabular → Service Sub Type: Tabular Model

Meter Name: Standard S% → Service Usage Type: Standard Tier Compute

### Что получилось в итоге

В итоге получаем заполненные таблицы, как в примере

Это позволяет анализировать оба провайдера вместе: теперь видно, какие сервисы AWS и Azure являются аналогами, также можно сравнивать стоимоти аналогичных услуг

В [файле](lab2.xlsm) находится полностью заполненные таблицы.

