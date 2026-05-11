# ML CI/CD — Blue-Green Deployment

RandomForest-классификатор на датасете Iris с полным CI/CD-пайплайном через GitLab и GitHub Actions.

## Стратегия деплоя

Выбрана **Blue-Green Deployment**. Обоснование — в [ADR](doc/architecture/decisions/0001-deployment-strategy.md).

Кратко: отсутствие обработки ошибок в сервисе требует возможности мгновенного отката. Blue-Green обеспечивает атомарное переключение трафика и полную изоляцию версий.

## Структура проекта

```
.
├── ml_pipeline.py                          # обучение модели, сохранение артефактов
├── app.py                                  # FastAPI-сервис (/health, /predict)
├── ab_test.py                              # планирование A/B-теста
├── Dockerfile
├── requirements.txt
├── switch.sh                               # переключение трафика blue ↔ green
├── docker-compose.blue.yml                 # blue-окружение (v1.0.0)
├── docker-compose.green.yml                # blue + green (v1.0.0 + v1.1.0)
├── nginx/
│   ├── nginx.blue.conf                     # трафик → blue
│   └── nginx.green.conf                    # трафик → green
├── doc/architecture/decisions/
│   └── 0001-deployment-strategy.md         # ADR
└── .github/workflows/
    ├── ci.yml                              # CI: обучение + воспроизводимость
    └── deploy.yml                          # CD: сборка образа + деплой
```

## Запуск локально

### 1. Только blue (v1.0.0)

```bash
docker compose -f docker-compose.blue.yml up -d --build
curl http://localhost/health
curl http://localhost/predict -H "Content-Type: application/json" -d '{"x": [5.1, 3.5, 1.4, 0.2]}'
```

### 2. Деплой green (v1.1.0) без переключения трафика

```bash
docker compose -f docker-compose.green.yml up -d --build
curl http://localhost:8002/health
```

### 3. Переключить трафик на green

```bash
chmod +x switch.sh
./switch.sh green
```

### 4. Откат на blue

```bash
./switch.sh rollback
```

### 5. Статус обоих сервисов

```bash
./switch.sh status
```

## Ожидаемые ответы

```json
// GET /health
{"status": "ok", "version": "v1.0.0"}

// POST /predict
{"prediction": 0, "version": "v1.0.0"}
```

## A/B-тест

```bash
pip install scipy
python ab_test.py
```

## GitHub Actions

Добавить в Settings → Secrets and variables → Actions:

| Secret | Описание |
|--------|----------|
| `CLOUD_TOKEN` | токен облачного провайдера |
| `MODEL_VERSION` | например `v1.1.0` |

`GITHUB_TOKEN` добавляется автоматически.
