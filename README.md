# Учебное приложение на python (devops)
## Описание проекта
Элементарный сервер на python, который состоит из
1) Сервера на базе FastAPI, который
- предоставляет системную информацию о сервере
- логирует все входящие HTTP-запросы в файл `info_app.log`
2) Генератора нагрузки - имитирует поведение множества пользователей, отправляющих запросы к различным эндпоинтам сервера с разной интенсивностью
3) Дашборда с аналитикой - сервер на базе Flask, который анализирует и визуализирует результаты нагрузочного тестирования из CSV-файла

### Сервер
Запускается командой
```bash
python3 log-server.py
```
Лог-файл `info_app.log` создается в корневой директории проекта и имеет формат 
```log
YYYY-MM-DD HH:MM:SS - METHOD /path from IP - Status: CODE - TIMEs
```
Проверка работоспособности
```bash
curl http://localhost:9100
```
### Генератор нагрузки
Запускается командой
```bash
python load-generator.py http://localhost:9100 -r 1000 -c 50
```
Пример вывода
```bash
(.venv) anestesia@compute-vm-2-1-20-hdd-1749121410454:/opt/app$ python load-generator.py http://localhost:9100 -r 1000 -c 50

==================================================
🛠️ Settings:
  Target URL: http://localhost:9100
  Total requests: 1000
  Parallel requests: 50
==================================================


📊 Load testing results:
✅ Successful requests: 1000 (100.0%)
❌ Failure requests: 0 (0.0%)
⏱️ Total time: 110.94 s
⚡ Requests per second: 9.01
⏳ Average response time: 0.1109 s

🕒 Total test execution time: 2.37 s
```
Результат записывается в файл `results.csv` в корневой директории проекта (необходим для dashboard)
### Дашборд
Запускаетсяя командой
```bash
python3 dashboard.py
```
