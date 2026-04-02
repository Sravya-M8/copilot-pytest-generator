pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // ══════════════════════════════════════════════════
        // STAGE 1 — CHECKOUT
        // ══════════════════════════════════════════════════
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
                bat 'if not exist reports mkdir reports'
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 2 — SETUP PYTHON
        // ══════════════════════════════════════════════════
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat 'python --version'
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 3 — INSTALL DEPENDENCIES
        // ══════════════════════════════════════════════════
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

        // ══════════════════════════════════════════════════
        // STAGE 4 — CODE QUALITY
        // ══════════════════════════════════════════════════
        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                bat 'venv\\Scripts\\pip.exe install flake8'
                bat 'venv\\Scripts\\flake8.exe . --max-line-length=100 --exclude=venv,__pycache__,.git,.pytest_cache || exit /b 0'
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 5 — RUN TESTS
        // ══════════════════════════════════════════════════
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

        // ══════════════════════════════════════════════════
        // STAGE 6 — BUILD
        // ══════════════════════════════════════════════════
        stage('Build') {
            steps {
                echo 'Build stage completed'
                bat 'echo Build #%BUILD_NUMBER% done'
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 7 — DEPLOY
        // ══════════════════════════════════════════════════
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

    // ── Post Pipeline ──────────────────────────────────────
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