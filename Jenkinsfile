pipeline {
    agent any

    environment {
        VENV = ".venv"
        APP_PORT = "5000"
    }

    stages {
        stage('Clone Repo (GitHub)') {
            steps {
                echo "Cloning repository from GitHub..."
                checkout scm
            }
        }

        stage('Install Dependencies (requirements.txt)') {
            steps {
                bat '''
                    py --version
                    py -m venv %VENV%
                    call %VENV%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests (pytest)') {
            steps {
                bat '''
                    call %VENV%\\Scripts\\activate
                    pytest -q
                '''
            }
        }

        stage('Build Application (Package Artifact)') {
            steps {
                bat '''
                    if exist dist rmdir /s /q dist
                    mkdir dist
                    copy app.py dist\\
                    copy requirements.txt dist\\
                    dir dist
                '''
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/**', fingerprint: true
                }
            }
        }

        stage('Deploy (Run Flask App)') {
            steps {
                bat '''
                    call %VENV%\\Scripts\\activate
                    start /B python app.py > flask_app.log 2>&1
                    timeout /t 2 /nobreak
                    powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:%APP_PORT%/health).Content } catch { 'HEALTHCHECK_FAILED' }"
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'flask_app.log', allowEmptyArchive: true
        }
        failure {
            echo "Pipeline failed."
        }
    }
}
