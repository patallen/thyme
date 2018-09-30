#! groovy
pipeline {
  agent any
  stages {
    stage('Run Python Tests') {
      parallel {
        stage("Testing Python 2.7") {
          agent {
            label "linux"
          }
          steps {
            sh("virtualenv /tmp/${env.GIT_REV}27 --python python2")
            sh("source /tmp/${env.GIT_REV}27/bin/activate")
            sh("pip install -r requirements.txt")
          }
        }
        stage("Testing Python 3.5") {
          agent {
            label "linux"
          }
          steps {
            sh("virtualenv /tmp/${env.GIT_REV}35 --python python3.5")
            sh("source /tmp/${env.GIT_REV}35/bin/activate")
            sh("pip install -r requirements.txt")
          }
        }
      }
    }
  }
  post {
    always {
      sh('echo "$(tput setaf 2)All Done!$(tput sgr0)"')
    }
  }
}
