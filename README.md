# BaseHabilis


#### Инструкция для запуска приложения в случае переноса на другой сервер, если его будет поддерживать не автор кода

1. Проект необходимо устанавливать на сервере под управлением Linux, также на него необходимо установить [Docker Engine](https://docs.docker.com/engine/install/) и плагин [Docker Compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository)

2. Скачайте исходный код из репозитория:

```git clone https://github.com/Strokman/architecture_archaeology_ia_ras.git ```

3. В корневой папке проекта нужно создать файл ```.env```. Содержимое предоставлю по запросу.

4. В корневую папку также необходимо переместить директорию ```postgres-data```, в которой содержится база данных. Либо восстановить базу из файла дампа. Предоставлю по запросу.

5. Запустить проект командой 
```sudo docker compose up --build```

