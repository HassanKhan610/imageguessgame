# A simple Image Guessing Game built on Django.

## Project Setup:
- Clone the repository
- Go to http://127.0.0.1:8000 to login/signup to play the game

## apply migration:
- python manage.py makemigrations
- python manage.py migrate

## create superuser:
python manage.py createsuperuser

## run the server:
python manage.py runserver

## Admin Dashboard:
- http://127.0.0.1:8000/admin/
- Add your google authentication credentials in admin site (social app model)
- move example.com to other table in (social app model)
- admin can upload multiple pictures for users to play the game with.

## User
- once user is logged in he can play the game, authentication is based on Google and Facebook.
- User statistics are displayed.
- Each image played by user is never displayed again.
