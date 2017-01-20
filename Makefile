lint:
	flake8 code/*.py


data1:
	mkdir -p data
	python code/get_package_list_from_cran_task_view.py
	python code/get_package_repo_urls.links.py

data2:
	python code/get_github_stars.py
	python code/get_cran_downloads.py
	python code/get_stack_overflow_data.py

help:
	@echo "    NOTE: Run all scripts from here. EG: `python code/get_cran_metadata.py`"
	@echo "    "
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    data1"
	@echo "        (Needed for `make data2`)"
	@echo "        Scrape list of R packages for analysis."
	@echo "    data2"
	@echo "        Obtain social metrics using APIs, for a list of packages from data1."

