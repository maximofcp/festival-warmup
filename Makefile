init:
	make initial-setup
	make spotify-user

clear:
	@find ./spotify ./fwu -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@find . -name "db.sqlite3" -delete

update:
	@pip install --upgrade pip
	@pip install -r requirements.txt

initial-setup:
	make clear
	make update
	make migrations
	make migrate
	make fixtures

run:
	 @python manage.py runserver

migrate:
	@python manage.py migrate

migrations:
	@python manage.py makemigrations

fixtures:
	@python manage.py loaddata fwu/fixtures/users.json
	@python manage.py loaddata fwu/fixtures/festivals.json

spotify-user:
	@python manage.py create_spotify_user

playlists:
	@python manage.py create_playlists

tunnel:
	@ssh -p 443 -R0:localhost:8000 a.pinggy.io

show-redirect-uri:
	@python manage.py shell -c "from django.conf import settings;print(settings.REDIRECT_URI)"
