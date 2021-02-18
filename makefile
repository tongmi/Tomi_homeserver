compile: compile.py
	./compile.py
	chmod 777 Tomi_homeserver.pyc
clean: Tomi_homeserver.pyc
	rm -rf Tomi_homeserver.pyc
install:
	./compile.py
	chmod 777 Tomi_homeserver.pyc
	mkdir outfile
	mv ./Tomi_homeserver.pyc ./outfile/.
uninstall:
	rm -rf ./outfile
	rm config.json
	rm -rf ./logs
debug:
	python3 ./outfile/Tomi_homeserver.pyc -s
	rm ./config.json
	rm -rf ./logs
help:
	#compile
	#clean
	#install
	#uninstall
	#debug
	#help