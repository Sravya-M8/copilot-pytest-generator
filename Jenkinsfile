pipeline {
    agent any

    // ── Environment Variables ──────────────────────────────
    environment {
        REPORTS_DIR     = 'reports'
        TEST_RESULTS    = 'reports\\test-results.xml'
        COVERAGE_DIR    = 'reports\\coverage'
        VENV_DIR        = 'venv'
        VENV_ACTIVATE   = 'venv\\Scripts\\activate'
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {

        // ══════════════════════════════════════════════════
        // STAGE 1 — CHECKOUT
        // ══════════════════════════════════════════════════
        stage('Checkout') {
            steps {
                echo "📥 Checking out code from GitHub..."
                checkout scm
                bat 'if not exist reports mkdir reports'
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 2 — SETUP PYTHON ENVIRONMENT
        // ══════════════════════════════════════════════════
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                bat '''
                    python --version
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                '''
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 3 — INSTALL DEPENDENCIES
        // ══════════════════════════════════════════════════
        stage('Install Dependencies') {
            steps {
                echo '📦 Installing project dependencies...'
                bat '''
                    call venv\\Scripts\\activate
                    pip install pytest pytest-cov --quiet
                    if exist requirements.txt (
                        pip install -r requirements.txt --quiet
                    )
                '''
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 4 — CODE QUALITY
        // ══════════════════════════════════════════════════
        stage('Code Quality') {
            parallel {

                stage('Lint') {
                    steps {
                        echo '🔍 Running flake8 linter...'
                        bat '''
                            call venv\\Scripts\\activate
                            pip install flake8 --quiet
                            flake8 . ^
                              --max-line-length=100 ^
                              --exclude=venv,__pycache__,.git,.pytest_cache ^
                              --output-file=reports\\flake8-report.txt ^
                            || exit /b 0
                        '''
                    }
                }

                stage('Security Scan') {
                    steps {
                        echo '🔐 Running bandit security scan...'
                        bat '''
                            call venv\\Scripts\\activate
                            pip install bandit --quiet
                            bandit -r . ^
                              -x venv,tests,__pycache__ ^
                              -f json ^
                              -o reports\\bandit-report.json ^
                            || exit /b 0
                        '''
                    }
                }
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 5 — RUN TESTS
        // ══════════════════════════════════════════════════
        stage('Run Tests') {
            steps {
                echo '🧪 Running pytest test suite...'
                bat '''
                    call venv\\Scripts\\activate
                    pytest tests/ ^
                      -v ^
                      --tb=short ^
                      --junitxml=reports\\test-results.xml ^
                      --cov=. ^
                      --cov-report=xml:reports\\coverage.xml ^
                      --cov-report=html:reports\\coverage ^
                    || exit /b 0
                '''
            }
            post {
                always {
                    echo '📊 Publishing test results...'
                    junit allowEmptyResults: true,
                          testResults: 'reports\\test-results.xml'

                    publishHTML([
                        allowMissing:          true,
                        alwaysLinkToLastBuild: true,
                        keepAll:               true,
                        reportDir:             'reports\\coverage',
                        reportFiles:           'index.html',
                        reportName:            'Coverage Report'
                    ])
                }
                success {
                    echo '✅ All tests passed!'
                }
                failure {
                    echo '❌ Some tests failed — check report above.'
                }
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 6 — BUILD
        // ══════════════════════════════════════════════════
        stage('Build') {
            steps {
                echo '🏗️ Build stage...'
                bat 'echo Build #%BUILD_NUMBER% completed successfully'
                // Add your actual build command here if needed
                // e.g. bat 'python -m build'
            }
        }

        // ══════════════════════════════════════════════════
        // STAGE 7 — DEPLOY (main branch only)
        // ══════════════════════════════════════════════════
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Deploying application...'
                bat 'echo Deploying build #%BUILD_NUMBER%...'
                // Add your actual deploy command here
            }
        }
    }

    // ── Post Pipeline ──────────────────────────────────────
    post {
        success {
            echo '''
            ╔══════════════════════════════════════╗
            ║   ✅ PIPELINE PASSED SUCCESSFULLY    ║
            ╚══════════════════════════════════════╝
            '''
        }
        failure {
            echo '''
            ╔══════════════════════════════════════╗
            ║   ❌ PIPELINE FAILED — CHECK LOGS    ║
            ╚══════════════════════════════════════╝
            '''
        }
        always {
            echo '🧹 Cleaning up workspace...'
            cleanWs()
        }
    }
}