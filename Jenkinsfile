pipeline {
    agent any
    options { ansiColor('xterm'); timestamps() }

    stages {
        stage('Prepare Environment') {
            steps {
                bat '''
                    echo ===== Checking Python version =====
                    py -3 --version

                    if not exist .venv (
                        echo 🟡 Creating virtual environment...
                        py -3 -m venv .venv
                        call .venv\\Scripts\\activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        python -m playwright install
                    ) else (
                        echo 🟢 Using existing virtual environment...
                        call .venv\\Scripts\\activate
                        pip install -r requirements.txt --quiet
                    )
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call .venv\\Scripts\\activate
                    echo ===== Running pytest-bdd =====
                    pytest --maxfail=1 --disable-warnings -q --junitxml=test-results\\junit.xml
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results/junit.xml'
            archiveArtifacts artifacts: 'test-results/**', allowEmptyArchive: true
        }
        success { echo '✅ All tests passed successfully!' }
        failure { echo '❌ Some tests failed — check Console Output.' }
    }
}
