init:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

bootstrap:
	mkdir -p static/bootstrap
	cd static/bootstrap && curl -L -O https://github.com/twbs/bootstrap/releases/download/v5.3.3/bootstrap-5.3.3-dist.zip
	cd static/bootstrap && unzip bootstrap-5.3.3-dist.zip
	rm static/bootstrap/bootstrap-5.3.3-dist.zip

run:
	. venv/bin/activate && python run.py

dock:
	@docker volume create storage-server-auth
	@docker volume create storage-server-data
	@docker stop storage-server || true
	@docker rm storage-server || true
	@docker rmi storage-server || true
	@docker build -t storage-server .
	@docker run -d -p 9876:5000\
		-v storage-server-auth:/storage-server/instance \
		-v storage-server-data:/storage-server/data \
		--name storage-server storage-server 

clean:
	rm -rf venv
	rm -rf static/bootstrap
	find . -type d -name "__pycache__" -exec rm -rf {} +
