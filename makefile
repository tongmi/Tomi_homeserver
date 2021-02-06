compile: compile.py
	./compile.py
	chmod 777 Tomi_homeserver.pyc
clean: Tomi_homeserver.pyc
	rm -rf Tomi_homeserver.pyc