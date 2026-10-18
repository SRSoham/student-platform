pipeline {
    agent any
    environment {
        IMAGE = "student-platform:v1.0.0"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Lint') {
            steps { sh '. venv/bin/activate && flake8 app tests --max-line-length=120' }
        }
        stage('Test') {
            steps { sh '. venv/bin/activate && pytest --cov=app --cov-fail-under=85 --junitxml=report.xml' }
            post { always { junit 'report.xml' } }
        }
        stage('Docker Build') {
            steps {
                sh 'eval $(minikube docker-env) && docker build -t $IMAGE .'
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh 'kubectl apply -f k8s/'
                sh 'kubectl rollout status deployment/student-platform --timeout=90s'
            }
        }
    }
    post {
        failure { echo 'Pipeline failed - check the failing stage.' }
    }
}
