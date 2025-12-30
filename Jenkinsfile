pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest
                '''
            }
        }
        stage('Build') {
            steps {
                sh '''
                    rm -rf dist
                    mkdir -p dist
                    cp app.py requirements.txt dist/
                '''
                archiveArtifacts artifacts: 'dist/**', fingerprint: true
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    nohup python3 app.py > flask_app.log 2>&1 &
                    sleep 2
                    curl http://127.0.0.1:5000/health
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'flask_app.log', allowEmptyArchive: true
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
