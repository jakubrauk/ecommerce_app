# Procedura uruchomienia docker-compose
```bash
docker compose up -d --build
```
Powinna stworzyć się baza danych i migracje powinny się automatycznie uruchomić.

do utworzenia superusera:
```bash
docker ps  # znajdź kontener ecommerce_project-web
docker exec -it kontener_id /bin/bash
python manage.py createsuperuser
```


# Procedura uruchomienia

Python w wersji 3.8.10
Serwer redis 5.0.7

instalacja wymaganych zależności
```bash
pip install -r requirements.txt
```

Wygenerowanie SECRET_KEY, do umieszczenia w zmiennych środowiskowych lub do ustawienia na sztywno w ecommerce_project.settings.SECRET_KEY
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Pierwsze utworzenie bazy danych, migracje, stworzenie grup Customer oraz Salesman i przypisanie im uprawnień
```bash
python manage.py migrate
```

Uruchomienie serwera django
```bash
python manage.py runserver
```

Uruchomienie redis
```bash
redis-server
```

Uruchomienie celery
```bash
python -m celery -A ecommerce_project worker -l info -B
```

### Spełnione obowiązkowe funkcjonalności oraz przypomnienie o terminie płatności

## Zadanie
Napisz niewielką aplikację wykorzystując co najmniej Django 4, Django REST Framework oraz bazę
SQLite. Powinna ona udostępniać RESTowe API pokrywające funkcjonalności opisane poniżej. Do
projektu dołącz koniecznie plik requirements.txt zwierający wszystkie pythonowe zależności oraz
krótkie readme opisujące sposób uruchomienia aplikacji.
Ocenie podlega przede wszystkim jakość napisanego kodu, jego wydajność i poprawność, a także
odpowiednie wykorzystanie wbudowanych w Django oraz Django REST Framework narzędzi jak klasy
bazowe czy funkcje.

## Temat: Aplikacja e-commerce

## Główne założenia:
1. W bazie danych należy przechowywać co najmniej:
    - Kategoria produktów:
        - Nazwa
    - Produkt
      - Nazwa
      - Opis
      - Cena
      - Kategoria (relacja do kategorii produktów)
      - Zdjęcie
      - Zdjęcie miniaturka
    - Zamówienie
      - Klient (relacja do auth_user)
      - Adres dostawy
      - Lista produktów wraz z ich liczebnością
      - Data zamówienia
      - Termin płatności
      - Sumaryczna cena
    - Do Przechowywania podstawowych danych użytkownika aplikacji wykorzystaj tabelę auth_user generowaną przez Django
2. Obowiązkowe funkcjonalności
    - Wyświetlanie listy wszystkich produktów:
      - Dostęp: Wszyscy użytkownicy, nawet niezalogowani
      - Obsługa paginacji
      - Filtrowanie po polach:
        - Nazwa
        - kategoria
        - Opis
        - Cena
      - Sortowanie po polach:
        - Nazwa
        - Kategoria
        - Cena
    - Wyświetlanie szczegółów wskazanego produktu
      - Dostęp: wszyscy użytkownicy, nawet niezalogowani
    - Dodawanie, modyfikowanie i usuwanie produktu:
      - Dostęp: sprzedawca
      - Miniaturka zdjęcia powinna generować się automatycznie
        - Maksymalna szerokość to 200px
    - Składanie zamówienia
      - Dostęp: Klient
      - Dane wejściowe:
        - Imię i nazwisko klienta
        - Adres dostawy
        - Lista produktów wraz z ich liczebnością
      - Dane wyjściowe:
        - Sumaryczna cena produktów
        - Termin płatności (załóżmy, że to data złożenia zamówienia +5 dni)
      - Po złożeniu zamówienia klient powinien otrzymać maila z potwierdzeniem (możesz użyć django.core.mail.backends.console.EmailBackend)
    - Statystyka najczęściej zamawianych produktów
      - Dostęp: sprzedawca
      - Dane wejściowe:
        - Data od
        - Data do
        - Liczba produktów (wskazuje ile produktów chcemy otrzymać w wyniku)
      - Dane wyjściowe:
        - Lista najczęściej zamawianych produktów wraz z liczbą sztuk
3. Opcjonalne funkcjonalności na dodatkowe punkty:
    - Wysyłanie do klienta przypomnienia e-mailowego o płatności na dzień przed jej terminem:
      - Zadanie należy zrealizować za pomocą biblioteki Celery
