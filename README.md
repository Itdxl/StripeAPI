# StripeAPI

## Запуск проекта на своем устройстве:

Разверние проект:

```
git clone git@github.com:Itdxl/foodgram-project-react.git
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
docker-compose exec -T backend python manage.py migrate
```


```
docker-compose exec -T backend python manage.py collectstatic --no-input
```


```
Имопртируйте : python3 manage.py import_data
```

```
В админке добвьте Теги
```


Откройте в бразуере:

```
127.0.0./api/
```
