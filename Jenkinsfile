pipeline {
  agent any
  options { ansiColor('xterm'); timestamps() }

  environment {
    // 你的本机 Python 可执行文件（用你刚才能成功的那条）
    BASE_PY = 'C:\\Users\\Raiden\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
    VENV_PY = '.venv\\Scripts\\python.exe'   // venv 里的 python
  }

  stages {
    stage('Setup venv & deps') {
      steps {
        bat '''
          rem 1) 创建虚拟环境（若已存在则跳过）
          if not exist .venv (
            "%BASE_PY%" -m venv .venv
          )

          rem 2) 用 venv 里的 python 安装一切（不要用 activate）
          "%VENV_PY%" -m pip install --upgrade pip
          "%VENV_PY%" -m pip install -r requirements.txt

          rem 3) 用同一个 venv 安装/同步浏览器
          "%VENV_PY%" -m playwright install
        '''
      }
    }

    stage('Run tests') {
      steps {
        bat '''
          "%VENV_PY%" -m pytest -q --junitxml=test-results\\junit.xml
        '''
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'test-results/junit.xml'
      archiveArtifacts artifacts: 'test-results/**', allowEmptyArchive: true
    }
  }
}
