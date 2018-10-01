#! groovy
pipeline {
  agent none
  environment {
    DOCKER_HOST = 'unix:///var/run/docker.sock'
  }
  stages {
    stage("Python Testing") {
      parallel {
        stage("Testing Python 2.7") {
          agent {
            label 'python-docker-slave'
          }
          steps {
            sh('echo "#################################"')
            sh('echo "CWD: $(pwd)"')
            sh('echo "User: ${USER}"')
            sh('pip install --user -r requirements.txt')
          }
        }

        stage("Testing Python 3.7") {
          agent {
            label 'python-docker-slave'
          }
          steps {
            sh('echo "#################################"')
            sh('echo "CWD: $(pwd)"')
            sh('echo "User: ${USER}"')
            sh('pip install --user -r requirements.txt')
          }
        }
      }
    }
  }
}
