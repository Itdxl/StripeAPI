# StripeAPI

## Запуск проекта на своем устройстве:

Разверните проект:

```
git clone git@github.com:Itdxl/StripeAPI.git
```

```
python3 -m venv env
```

```
source venv/scripts/activate
```


```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В директории infra:

Создайте env с переменными:
```
STRIPE_SECRET_KEY = 'Ваш ключ'
SECRET_KEY = 'Ваш ключ'
PUBLIC_STRIPE_KEY = ''Ваш ключ''
```

В директории infra:


```
docker-compose up -d --build
```

```
docker-compose exec backend python manage.py createsuperuser
```

```
docker-compose exec backend python manage.py loaddata backup
```

Альетернативный вариант развертывания проекта:

```
развернуть все руками из папки stripe_project
```


Откройте в бразуере:

```
127.0.0./api/
```

```
127.0.0./api/item/int:pk/ - Предмет
```

```
127.0.0./api/welcome/ - Привественная страница

```


```
127.0.0./api/сart/ - Корзина drf формат```

```
Остальные эндпойнты технические/по результам действий.
```
