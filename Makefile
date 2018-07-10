xall: ; @make -C ws ; python ty.py
clean:
	find . -name \*~    | xargs rm
	find . -name \*.pyc | xargs rm
