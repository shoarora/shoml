PROJECT_NAME=shoml
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh; conda init; conda activate

setup: create-env

create-env:
  # Create a local python environment on top of conda.
	conda env create -f environment.yml -n $(PROJECT_NAME)
	$(CONDA_ACTIVATE) $(PROJECT_NAME) && pip install -r requirements.txt

update-env:
  # Update the local python environment.
	conda env update -f environment.yml -n $(PROJECT_NAME)
	$(CONDA_ACTIVATE) $(PROJECT_NAME) && pip install -r requirements.txt

lint:
	flake8
