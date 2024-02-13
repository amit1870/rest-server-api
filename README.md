# Install pip, venv, subversion
>$ sudo apt-get install python3-pip python3-venv subversion

# Create Virtual Environment
>$ python3 -m venv <virual_env>

# Activate Virtual Environment
>$ cd <virual_env>
>$ source bin/activate

# Set svn ignore home dir
>$ svn propset svn:ignore -RF .svnignore .

# Check which files will be ignored
>$ svn status --no-ignore

# export PYTHONPATH to make pylint work
> For ex. if you have checkout your project in /home/apatel/
> Then export the PYTHONPATH with following
> $ export PYTHONPATH=${HOME}/{path}

# Set FLASK_CONFIG=production to skip test and other things
> Available configurations are [production, testing, development, local]
> $ export FLASK_CONFIG=production

# Install invoke-1.2.0
> $ pip install invoke==1.2.0

# Invoke run from task dir/
> $ invoke run

# Inoke run with --no-install to skip dependencies installation
> $ invoke run --no-install

# Create a file inside app directory
> $ cp app/signup.py app/<file_name>.py

# Edit <file_name>.py as per required and run it in background
> $ python app/<file_name>.py &

# To cancel the running file
> $ fg
> $ Ctrl^C

# Test api POST Method
> $ curl --data {} http://172.xx.xx.xx:8089/testapi/

# Test api GET Method
> $ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://xx.xx.xx.xx:8089/testapi/

# To run functional test cases
> $ locust -f functional.py --host=xx.xx.xx.xx 2>/dev/null &
