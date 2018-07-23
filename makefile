
test: clean
	cd catcoin ; make test

clean:
	find . -name \*~    | xargs rm
	find . -name \*.pyc | xargs rm
	cd catcoin ; make clean

qwert:
	python -um catcoin.node erase
	python -um catcoin.node init
	python -um catcoin.node start

client:
	python -um catcoin.node client

clientx:
	python -um catcoin.node client <client.convo


