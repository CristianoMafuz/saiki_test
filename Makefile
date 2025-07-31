# Makefile at <saiki/src/backend>
# ==============================
# @saiki
# Last update: 2025-06-23
# -----------------------

.PHONY: run-django run-uvicorn django-migrate

#
# Handles the backend settings.
#

# Structure
# ---------

dir_backend 			:= src/backend/
DJANGO_MANAGE			:= $(dir_backend)manage.py
DJANGO_MANAGE_MODULE	:= src.backend.manage



# Running the server
# ------------------

# Running the FastAPI server application
run-uvicorn:
	uvicorn src.backend.main:app

# Running the Django server
run-django:
	@$(PYTHON) -m $(DJANGO_MANAGE_MODULE) runserver
# @$(PYTHON) $(DJANGO_MANAGE) runserver

# Run migrations: makemigrations + migrate
django-migrate:
	$(PYTHON) $(DJANGO_MANAGE) makemigrations
	$(PYTHON) $(DJANGO_MANAGE) migrate

