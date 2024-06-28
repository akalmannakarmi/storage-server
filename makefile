init:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	mkdir -p static/bootstrap
	cd static/bootstrap && curl -L -O https://github.com/twbs/bootstrap/releases/download/v5.3.3/bootstrap-5.3.3-dist.zip
	cd static/bootstrap && unzip bootstrap-5.3.3-dist.zip
	rm static/bootstrap/bootstrap-5.3.3-dist.zip

run:
	. venv/bin/activate && python run.py

clean:
	rm -rf venv
	rm -rf static/bootstrap
	find . -type d -name "__pycache__" -exec rm -rf {} +


