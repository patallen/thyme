#! groovy

def shortcode(env) {
  return env.GIT_REV.substring(0, 8);
}

pipeline {
    agent any
    stages {
        parallel {
            stage("Testing Python 2.7") {
                agent {
                    label "linux"
                }
                def code = shortcode(env);
                steps {
                    sh("virtualenv /tmp/${code}27 --python python2")
                    sh("source /tmp/${code}27/bin/activate")
                    sh("pip install -r requirements.txt")
                }
            }
            stage("Testing Python 3.5") {
                agent {
                    label "linux"
                }
                steps {
                    def code = shortcode(env);
                    steps {
                        sh("virtualenv /tmp/${code}35 --python python3.5")
                        sh("source /tmp/${code}35/bin/activate")
                        sh("pip install -r requirements.txt")
                    }
                    virtualenv "/tmp/${shortcode}3.5" --python python2
                    source "/tmp/${shortcode}35/bin/activate"
                    pip install -r requirements.txt
                }
            }
            stage("Complete") {
              sh('echo "$(tput setaf 2)All Done!$(tput sgr0)"')
            }
        }
    }
}
