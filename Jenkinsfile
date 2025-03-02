pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my_django_app"
        DOCKER_TAG = "latest"
        REGISTRY = "docker.io/bannerroar"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'fix-functionality-of-evaluations', url: 'https://github.com/sean-meade/fund-frontier'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml up -d db'
                    sh 'docker run --rm $DOCKER_IMAGE:$DOCKER_TAG pytest'
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    sh 'docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_PASSWORD'
                    sh 'docker tag $DOCKER_IMAGE:$DOCKER_TAG $REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG'
                    sh 'docker push $REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh 'kubectl apply -f k8s/'
                }
            }
        }
    }
}
