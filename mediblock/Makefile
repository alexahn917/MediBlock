.PHONY: all
all: test

.PHONY: test
test:
	tox

# Setup or update virtualenv for development
.PHONY: update-virtualenv
update-virtualenv:
	bin/update-virtualenv.sh

# Runs the program
.PHONY: sync
sync:
	gsutil rsync -R static/ gs://mediblock/static

# Deploys package to the App Engine
.PHONY: deploy
deploy:
	gcloud app --project mediblock-195521 deploy

# Runs the program
.PHONY: run
run:
	bin/db_proxy.sh & bin/runserver.sh; fg

.PHONY: clean
clean:
	@find . -name '*.pyc' -delete
