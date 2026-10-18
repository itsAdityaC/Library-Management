pipeline {
    agent any

    environment {
        IMAGE_NAME = 'library-app'
        CONTAINER_NAME = 'library-container'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'venv\\Scripts\\python -m pytest'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Deploy') {
            steps {
                bat(returnStatus: true, script: 'docker rm -f %CONTAINER_NAME%')
                bat 'docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%:latest'
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded. App is live on port 5000.' }
        failure { echo 'Pipeline failed. Check the console output.' }
    }
}