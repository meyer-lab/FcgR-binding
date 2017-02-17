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
        echo currentBuild.result
      }
    }
    stage('Deploy') {
      when { expression { currentBuild.result == 'SUCCESS' } }
      steps {
        sh 'make upload'
      }
    }
  }
}
