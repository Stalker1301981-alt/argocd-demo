pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "docker.io/stalker1301981"
        APP_NAME = "arbitrage-bot"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit tests') {
            steps {
                sh 'pip install -r arbitrage-bot/requirements.txt'
                sh 'python -m pytest arbitrage-bot/tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('Lint') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 arbitrage-bot/src/ --max-line-length=120'
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t $DOCKER_REGISTRY/$APP_NAME:$BUILD_NUMBER arbitrage-bot/'
            }
        }

        stage('Security scan') {
            steps {
                sh 'docker scout quickview $DOCKER_REGISTRY/$APP_NAME:$BUILD_NUMBER'
            }
        }

        stage('Push image') {
            steps {
                withDockerRegistry(registry: "$DOCKER_REGISTRY") {
                    sh 'docker push $DOCKER_REGISTRY/$APP_NAME:$BUILD_NUMBER'
                    sh 'docker tag $DOCKER_REGISTRY/$APP_NAME:$BUILD_NUMBER $DOCKER_REGISTRY/$APP_NAME:latest'
                    sh 'docker push $DOCKER_REGISTRY/$APP_NAME:latest'
                }
            }
        }

        stage('Update Git manifests') {
            steps {
                sh '''
                    sed -i "s/tag:.*/tag: $BUILD_NUMBER/" helm-chart/values.yaml
                    git config user.name "Jenkins CI"
                    git config user.email "ci@company.com"
                    git add helm-chart/values.yaml
                    git commit -m "Update image tag to $BUILD_NUMBER"
                    git push
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed. ArgoCD will auto-deploy."
            slackSend(color: "good", message: "✅ ${APP_NAME} deployed (build #${BUILD_NUMBER})")
        }
        failure {
            echo "❌ Pipeline failed."
            slackSend(color: "danger", message: "❌ ${APP_NAME} build #${BUILD_NUMBER} failed")
        }
    }
}
