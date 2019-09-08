# DRFtutorial
django rest framework drf tutorial


git clone https://github.com/zhaorch/DRFtutorial.git

mkvirtualenv tutorial

pip install -r requirements.txt

python manage.py runserver

## TEST
```python
class ZRCRateThrottle(UserRateThrottle):
    scope = 'zrc'
```
