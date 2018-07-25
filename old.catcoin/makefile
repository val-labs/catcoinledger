all:
	cd .. ; python -mcatcoin.client
test:
	@echo TESTING
	[ ! -e ../test.data ]
	@cd .. ; PATH=$$PATH:/usr/local/bin python -um catcoin.test
clean:
	@echo CLEANING
	cd .. ; rm -fr test.data
	ls -la ..
