## SecretsManager to env vars

### Requirements
docker (https://get.docker.com/)
python3.7 (https://www.python.org/downloads/)
define AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_REGION environment variables (and also in the Dockerfile if using it)

### Implementation
A simple app.py has been created to read any environment variable that has the "replaceme" value and actually replace it by the real value from AWS Secrets Manager using boto3. For this approach, i've also added a simple tweak, print the export of the actual variables and then run an eval, to actually export the variables to the container/host.

### Running it
Untar the file provided
Assign an environment variable that actually the KV exists on secrets manager with the value replaceme
```shell
export TEST=replaceme
```
run (using a virtualenv):
```shell
python3 -m venv testapp
source testapp/bin/activate
pip install -r requirements.txt
eval $(./app.py)
deactivate
```
Check if the variable was correctly replaced:
```shell
env | grep TEST
```

### Running it with docker
Assign correct variables for AWS in the Dockerfile, the same as the test vars that will be replaced
Build it
```shell
docker build -t testapp .
```
Run it
```shell
docker run testapp
```
The docker file has an entrypoint that will first run the vars assignment, and after it I just execute an env, to actually show those vars are changed in the container (but anything can be run afterwards)

### Tests
Just run:
```shell
tox
```
Tests will run with a coverage report. For this I've used moto and pytest.
