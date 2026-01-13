# FastAPI + Kafka чат приложение.

Проект представляет собой базовый шаблон для FastAPI чат-сервера, использующего Kafka для асинхронной обработки сообщений и MongoDB для хранения данных.  Он предоставляет архитектурную основу, но требует дальнейшей разработки для полной функциональности.


## Зависимости

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## Установка

1. Клонируйте репозиторий:
    ```bash
        git clone https://github.com/your_username/your_repository.git
        cd your_repository
    ```

2. Установите все необходимые пакеты, указанные в разделе `Зависимости`.

### Make команды

* `make app` - запустить приложение и всю необходимую инфраструктуру.
* `make app-logs` - отслеживать логи приложения в контейнере.
* `make app-down` - остановить приложение и всю связанную с ним инфраструктуру.
