# Sprinkle

Some stuff to get a CI environment configured quicker. Configuration is driven by yaml, on startup its dumped into a consul k/v store & the rest of the setup references it from there. Primary objects propagated throughout the system are Users, Groups, Roles, Services, and Projects. The same data constructs are just remapped as necessary for each service in the pipeline.

## Python bindings & stuff

- pyyaml <http://pyyaml.org/>
- consulate <https://github.com/gmr/consulate>
- python-gitlab <https://github.com/gpocentek/python-gitlab>
- python-jenkins <https://git.openstack.org/cgit/openstack/python-jenkins>
- pycrypto <https://www.dlitz.net/software/pycrypto/>

## Service API docs

- GitLab <http://docs.gitlab.com/ce/api/>
- Jenkins <https://wiki.jenkins-ci.org/display/JENKINS/Remote+access+API>
- Artifactory <https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API>
- Jira <https://docs.atlassian.com/jira/REST/latest/>

## Python shit I'm gonna forget

- Create: virtualenv -p /usr/bin/python3.4 .env
- Start: source .env/bin/activate
- Stop: deactivate
- pip freeze > requirements.txt
- pip install -r requirements.txt
