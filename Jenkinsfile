#! groovy

def shortcode(env) {
  return env.GIT_REV.substring(0, 8);
}

pipeline {
    agent any
    stages {
        stage("Setup") {
            steps {
                virtualenv /tmp/$shortcode
            }
        }
        parallel {
            stage("Testing Python 2.7") {
                agent {
                    label "linux"
                }
                steps {
                    virtualenv "/tmp/${shortcode}3.5" --python python2
                    source "/tmp/${shortcode}35/bin/activate"
                    pip install -r requirements.txt
                }
            }
            stage("Testing Python 3.5") {
                agent {
                    label "linux"
                }
                steps {
                    def shortCode = shortcode(env);
                    virtualenv "/tmp/${shortcode}3.5" --python python2
                    source "/tmp/${shortcode}35/bin/activate"
                    pip install -r requirements.txt
                }
            }
        }
    }
}
