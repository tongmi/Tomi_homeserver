compile:
	./compile.py
	chmod 777 Tomi_homeserver.pyc
clean: Tomi_homeserver.pyc
	rm -rf Tomi_homeserver.pyc
install:
	./compile.py
	chmod 777 Tomi_homeserver.pyc
	mkdir outfile
	mv ./Tomi_homeserver.pyc ./outfile/.
	mkdir outfile/plugins
	cp plugins/* outfile/plugins/.
uninstall:
	rm -rf ./outfile
debug:
	bash debug.sh
reinstall:
	rm -rf ./outfile
	./compile.py
	chmod 777 Tomi_homeserver.pyc
	mkdir outfile
	mv ./Tomi_homeserver.pyc ./outfile/.
	mkdir outfile/plugins
	cp plugins/* outfile/plugins/.
help:
	#compile (1)
	#clean
	#install
	#uninstall
	#debug
	#reinstall
	#help