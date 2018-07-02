all: ; @make -C ws
clean:
	find . -name \*~    | xargs rm
	find . -name \*.pyc | xargs rm
