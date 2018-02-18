.PHONY: all
all: test

.PHONY: test
test:
	tox

# Runs the program
.PHONY: sync
sync:
	gsutil rsync -R static/ gs://mediblock-static/static

# Deploys package to the App Engine
.PHONY: deploy
deploy:
	gcloud app --project mediblock-195521 deploy

# Runs the program
.PHONY: run
run:
	db_proxy.sh & runserver.sh; fg

.PHONY: clean
clean:
	@find . -name '*.pyc' -delete
