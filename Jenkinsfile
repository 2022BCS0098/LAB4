pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "kushal2022bcs0098/wine-inference"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python scripts/train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def metrics = readJSON file: 'app/artifacts/metrics.json'
                    env.CURRENT_ACCURACY = metrics.accuracy.toString()
                    echo "Current Accuracy: ${env.CURRENT_ACCURACY}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_ACC')]) {
                        if (env.CURRENT_ACCURACY.toFloat() > BEST_ACC.toFloat()) {
                            env.IS_BETTER = "true"
                            echo "New model is better!"
                        } else {
                            env.IS_BETTER = "false"
                            echo "Model did not improve."
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.IS_BETTER == "true" }
            }
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.IS_BETTER == "true" }
            }
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
    }
}
