#! groovy
pipeline {
  agent none
  stages {
    stage("Python Testing") {
      parallel {
        stage("Testing Python 2.7") {
          agent {
            docker {
              image 'python:2.7.15'
              label 'python-2.7'
              args  '-v /tmp:/tmp'
            }
          }
          steps {
              sh("virtualenv /tmp/${env.GIT_REV}27 --python python2")
              sh("source /tmp/${env.GIT_REV}27/bin/activate")
              sh("pip install -r requirements.txt")
          }
        }
        stage("Testing Python 3.5") {
          agent {
            docker {
              image 'python:3.7'
              label 'python-3.7'
              args  '-v /tmp:/tmp'
            }
          }
          steps {
            sh("virtualenv /tmp/${env.GIT_REV}35 --python python3.7")
            sh("source /tmp/${env.GIT_REV}35/bin/activate")
            sh("pip install -r requirements.txt")
          }
        }
        post {
          always {
            sh('echo "$(tput setaf 2)All Done!$(tput sgr0)"')
          }
        }
      }
    }
  }
}
