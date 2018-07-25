#d: ; docker build .
clitest:
	python -mdbc
#	python -mdbd
#xtest: test
all:
	@echo "try: install | clean"
install: realclean
	virtualenv -p python2 .ve2
	virtualenv -p python3 .ve3
	.ve2/bin/python setup.py install
	.ve3/bin/python setup.py install
test: ; @sh bin/test.sh
serve:; @sh bin/serve.sh
kill: ; @sh bin/kill.sh
realclean: clean ; rm -fr .ve?
clean:
	rm -fr build dist *.egg-info *.pid ?
	find . -name __pycache__ | xargs rm -fr
	find . -name '*.pyc'     | xargs rm -fr
	find . -name '*~'        | xargs rm -fr
