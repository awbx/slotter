


install:
	touch .env && echo "INTRA_SESSION_ID=YOUR INTRA SESSION ID" > .env
	python3.9 -m pip install -r requirements.txt