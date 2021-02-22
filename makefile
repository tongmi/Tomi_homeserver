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
pull:
	git pull
login:
	bash .git_login.sh
push:
	git push
github:
	git remote set-url origin https://github.com/tongmi/Tomi_homeserver
gitee:
	git remote set-url origin https://gitee.com/tongmi/Tomi_homeserver
help:
	#compile (1)
	#clean
	#install
	#uninstall
	#debug
	#reinstall
	#pull
	#login
	#push
	#github
	#gitee
	#help
