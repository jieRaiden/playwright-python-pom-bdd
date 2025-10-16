pipeline {
  agent any
  environment {
    PYTHON = 'C:\\Users\\Raiden\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
  }

  stages {
    stage('Setup Environment') {
      steps {
        bat '''
          "%PYTHON%" -m venv .venv
          call .venv\\Scripts\\activate
          "%PYTHON%" -m pip install --upgrade pip
          pip install -r requirements.txt
          "%PYTHON%" -m playwright install
        '''
      }
    }

    stage('Run Tests') {
      steps {
        bat '''
          call .venv\\Scripts\\activate
          pytest tests/ --maxfail=1 --disable-warnings -q --junitxml=test-results\\junit.xml
        '''
      }
    }
  }

  post {
    always {
      junit 'test-results/junit.xml'
    }
  }
}
