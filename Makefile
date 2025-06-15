tailwind-watch:
	npm run tailwind:watch

django-runserver:
	python manage.py runserver 8080

dev:
	make -j 2 tailwind-watch django-runserver