Clone the project 

```bash
git clone https://github.com/hisafgit/carsproject.git 
```

Install poetry from [here](https://python-poetry.org/docs/#installation).

Make sure you are in the folder where pyproject.toml file exists
and to install the dependencies run

``` bash 
poetry install
```
To activate the environment created by poetry, run
```bash
poetry shell 
``` 


```bash 
cd ./project/backend
```
and run
```bash
python manage.py runserver 8080
```

Visit http://127.0.0.1:8080/cars/list in your webbrowser to use the API.

You will see the existing database populated with some data downloaded before.

To be able to filter the data, you can type query parameters such as 

http://127.0.0.1:8080/cars/list/?brand=jaguar&year=2023



## To delete the existing car data from the database you can run 
```bash
python manage.py shell
``` 
and within the shell

```python
from cars.models import Car
for car in Car.objects.all():
    car.delete()
```



Press Ctrl and D together to exit the shell.

Then to dowload some new data
```bash
cd ./project/downloader
```
and run downloader.py followed by number of pages you want to download e.g. 

```bash 
python downloader.py 10
```

You can find the new data downloaded using the API.
