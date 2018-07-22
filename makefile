
test: clean
	cd catcoin ; make test

clean:
	find . -name \*~    | xargs rm
	find . -name \*.pyc | xargs rm
	cd catcoin ; make clean
