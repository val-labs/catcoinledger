
test:
	cd catcoin ; make

clean:
	find . -name \*~    | xargs rm
	find . -name \*.pyc | xargs rm
