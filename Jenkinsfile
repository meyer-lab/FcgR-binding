pipeline {
    agent any
    environment {
        PATH = "/bin:/usr/sbin:/usr/bin:/usr/local/bin"
    }
    stages {
        stage('Build') {
            steps {
                sh 'make'
            }
        }
        stage('Test'){
            steps {
                sh 'make test'
            }
        }
        stage('Deploy') {
            when { currentBuild.result == 'SUCCESS' }
            steps {
                sh 'make upload'
            }
        }
    }
}
