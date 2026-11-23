# TOKER CONTROL Demo

Безопасный прототип статуса устройств. Клиент подключается только после явного нажатия владельцем кнопки «Подключить». Нет скрытого доступа, удалённого управления, записи экрана, клавиатуры, мыши или файлов.

## Локальный запуск
`pip install -r requirements.txt`
Задайте `ENROLLMENT_TOKEN` и `ADMIN_TOKEN`, затем: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Render
Build: `pip install -r requirements.txt`
Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
Добавьте `ENROLLMENT_TOKEN` и `ADMIN_TOKEN` в Environment.

Клиент: `python client/client.py` (после `pip install -r requirements.txt`).