


install:
	touch .env && echo "INTRA_SESSION_ID=YOUR INTRA SESSION ID" > .env # TODO check if .env file exists to avoid overwriting.
	python3.9 -m pip install -r requirements.txt