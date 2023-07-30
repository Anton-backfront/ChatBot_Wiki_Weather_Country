import requests
from pprint import pprint
from datetime import datetime
from countryinfo import CountryInfo

# --------------------- countryinfo --------------------------------



def get_country_info(country_request):

    country = CountryInfo(country_request)
    try:
        if country_request.lower() == '/stop':
            return ("Вы вышли из раздела country_info")

        else:
            return (f'''Столица {country_request}: {country.capital()}
Площадь: {country.area()} км.
Население: {country.population()} чел.
Язык: {country.languages()}
Телефонный код: {country.calling_codes()}
Название жителей: {country.demonym()}
Валюта: {country.currencies()}
Регион: {country.region()}
Провинции: {country.provinces()}
''')
    except:
        return ('Вы ввели не корректный город, попробуйте снова')