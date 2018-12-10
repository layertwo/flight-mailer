PIP=`which pip3`
ZIP=`which zip`
PACKAGE=rssr

build: clean
	./bootstrap.sh

clean:
	rm -rf package/ function.zip

aws: build
	 aws lambda update-function-code --function-name $(PACKAGE) --zip-file fileb://function.zip

