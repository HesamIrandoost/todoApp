exersise8
- 127.0.0.1:8000/weather/  

caching for api
- in todo.api.v1.views already cashing for api 

and syntax:
- from django.views.decorators.cache import cache_page
- from django.views.decorators.vary import vary_on_headers
- - @method_decorator(cache_page(60 * 13))
- - @method_decorator(vary_on_headers("Authorization")) * optinal

repo addres
- https://github.com/HesamIrandoost/todoApp/


a todo project with django, drf, bootstrap