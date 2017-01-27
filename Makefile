lint:
	flake8 code/*.py


r-data:
	mkdir -p data
	python code/get_package_list_from_cran_task_view.py
	python code/get_package_repo_urls.py
	python code/get_github_stars.py
	python code/get_cran_downloads.py
	python code/get_stack_overflow_data.py

python-data:
	@echo "See code/make-python-data.ipynb"

help:
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    r-data"
	@echo "        Scrape list of R packages for analysis and obtain all metrics."
	@echo "    python-data"
	@echo "        See code/make-python-data.ipynb"


