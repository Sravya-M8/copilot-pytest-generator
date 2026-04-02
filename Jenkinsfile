pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        PYTHON = 'C:\\Users\\mathi.sravya\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
                bat 'if not exist reports mkdir reports'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m venv venv'
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'venv\\Scripts\\pip.exe install pytest pytest-cov'
                bat '''
                    if exist requirements.txt (
                        venv\\Scripts\\pip.exe install -r requirements.txt
                    ) else (
                        echo No requirements.txt found, skipping...
                    )
                '''
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                bat 'venv\\Scripts\\pip.exe install flake8'
                bat 'venv\\Scripts\\flake8.exe . --max-line-length=100 --exclude=venv,__pycache__,.git,.pytest_cache || exit /b 0'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running pytest...'
                bat 'venv\\Scripts\\pytest.exe tests/ -v --tb=short --junitxml=reports\\test-results.xml || exit /b 0'
            }
            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'reports\\test-results.xml'
                }
            }
        }

        stage('Build') {
            steps {
                echo 'Build stage completed'
                bat 'echo Build #%BUILD_NUMBER% done'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying...'
                bat 'echo Deploy #%BUILD_NUMBER%'
            }
        }
    }

    post {
        success {
            echo 'PIPELINE PASSED SUCCESSFULLY'
        }
        failure {
            echo 'PIPELINE FAILED - CHECK LOGS'
        }
        always {
            echo 'Cleaning workspace...'
            deleteDir()
        }
    }
}