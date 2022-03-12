# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* springstone/*.py

black:
	@black scripts/* springstone/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr springstone-*.dist-info
	@rm -fr springstone.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

run_api:
	uvicorn api.fast:app --reload  # load web server with code autoreload

# project id
PROJECT_ID=wagon-bootcamp-340323

# bucket name
BUCKET_NAME=wagon-data-716-el-merbouh

REGION=europe-west1

PROPHET_DOCKER_IMAGE_NAME=springstone_for_prophet_gcp
RNN_DOCKER_IMAGE_NAME=springstone_for_rnn_gcp

set_project:
	-@gcloud config set project ${PROJECT_ID}

create_bucket:
	-@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

gcp_build_prophet_docker:
	-@docker build -t eu.gcr.io/${PROJECT_ID}/${PROPHET_DOCKER_IMAGE_NAME} .

gcp_run_prophet_docker_locally:
	-@docker run -e PORT=8000 -p 8000:8000 eu.gcr.io/${PROJECT_ID}/${PROPHET_DOCKER_IMAGE_NAME}

gcp_push_prophet_docker:
	-@docker push eu.gcr.io/${PROJECT_ID}/${PROPHET_DOCKER_IMAGE_NAME}

gcp_deploy_prophet_docker:
	-@gcloud run deploy --image eu.gcr.io/${PROJECT_ID}/${PROPHET_DOCKER_IMAGE_NAME} --platform managed --region ${REGION}

gcp_build_rnn_docker:
	-@docker build -t eu.gcr.io/${PROJECT_ID}/${RNN_DOCKER_IMAGE_NAME} -f rnn_dockerfile .

gcp_run_rnn_docker_locally:
	-@docker run -e PORT=8000 -p 8000:8000 eu.gcr.io/${PROJECT_ID}/${RNN_DOCKER_IMAGE_NAME}

gcp_push_rnn_docker:
	-@docker push eu.gcr.io/${PROJECT_ID}/${RNN_DOCKER_IMAGE_NAME}

gcp_deploy_rnn_docker:
	-@gcloud run deploy --image eu.gcr.io/${PROJECT_ID}/${RNN_DOCKER_IMAGE_NAME} --platform managed --region ${REGION} --memory 4G

##### Training  - - - - - - - - - - - - - - - - - - - - - -

# will store the packages uploaded to GCP for the training
BUCKET_TRAINING_FOLDER = 'trainings'

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# not required here

### GCP AI Platform - - - - - - - - - - - - - - - - - - - -

##### Machine configuration - - - - - - - - - - - - - - - -

# REGION=europe-west1

PYTHON_VERSION=3.7
FRAMEWORK=scikit-learn
RUNTIME_VERSION=2.2

##### Package params  - - - - - - - - - - - - - - - - - - -

PACKAGE_NAME=springstone
FILENAME=trainer

JOB_NAME=springstone_RNN_pipeline_$(shell date +'%Y%m%d_%H%M%S')


run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--stream-logs
