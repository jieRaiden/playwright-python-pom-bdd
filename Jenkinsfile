pipeline {
  agent any
  options {
    ansiColor('xterm')
    timestamps()
  }

  environment {
    // 按你的机器实际路径改
    BASE_PY = 'C:\\Users\\Raiden\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
    VENV_PY = '.venv\\Scripts\\python.exe'
  }

  stages {
    stage('Print context') {
      steps {
        echo "Branch: ${env.BRANCH_NAME ?: 'N/A'}"
        bat 'ver'
      }
    }

    stage('Setup venv & deps') {
      steps {
        bat '''
          rem 1) 创建 venv（存在则跳过）
          if not exist .venv (
            "%BASE_PY%" -m venv .venv
          )

          rem 2) 升级 pip & 安装依赖（使用 venv 的 python）
          "%VENV_PY%" -m pip install --upgrade pip
          "%VENV_PY%" -m pip install -r requirements.txt

          rem 3) 安装/同步 Playwright 浏览器
          "%VENV_PY%" -m playwright install
        '''
      }
    }

    // 非 staging：只跑 API 快速集
    stage('Run tests - API (non-staging)') {
      when { not { branch 'staging' } }
      steps {
        bat '''
          if not exist test-results mkdir test-results
          "%VENV_PY%" -m pytest -m "api" -q ^
            --junitxml=test-results\\junit.xml ^
            --html=test-results\\report.html --self-contained-html
        '''
      }
    }

    // staging：跑全量（UI+API）
    stage('Run tests - Full (staging)') {
      when { branch 'staging' }
      steps {
        bat '''
          if not exist test-results mkdir test-results
          "%VENV_PY%" -m pytest -m "api" -q ^
            --junitxml=test-results\\junit.xml ^
            --html=test-results\\report.html --self-contained-html
        '''
      }
    }

    // staging：在 Jenkins 中发布 HTML 报告
    stage('Publish HTML (staging only)') {
      when { branch 'staging' }
      steps {
        publishHTML(target: [
          reportDir: 'test-results',
          reportFiles: 'report.html',
          reportName: 'Playwright Report',
          keepAll: true,
          alwaysLinkToLastBuild: true,
          allowMissing: true
        ])
      }
    }
  }

  post {
    always {
      // 收集 JUnit（失败也不会中断）
      junit allowEmptyResults: true, testResults: 'test-results/junit.xml'
      // 归档所有产物（便于下载/留存）
      archiveArtifacts artifacts: 'test-results/**', allowEmptyArchive: true
    }
  }
}
