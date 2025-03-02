pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-django-app"
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
                    bat 'docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% .'
                }
            }
        }


        // stage('Run Tests') {
        //     steps {
        //         script {
        //             bat 'docker-compose -f docker-compose.yml up -d db'
        //             bat 'docker run --rm %DOCKER_IMAGE%:%DOCKER_TAG% pytest'
        //         }
        //     }
        // }

        stage('Push to DockerHub') {
            steps {
                script {
                    // Log in to Docker Hub securely
                    bat 'echo %DOCKERHUB_PASSWORD% | docker login -u %DOCKERHUB_USERNAME% --password-stdin'
                    
                    // Tag the image with the registry name
                    bat 'docker tag %DOCKER_IMAGE%:%DOCKER_TAG% %REGISTRY%/%DOCKER_IMAGE%:%DOCKER_TAG%'
                    
                    // Push the image to Docker Hub
                    bat 'docker push %REGISTRY%/%DOCKER_IMAGE%:%DOCKER_TAG%'
                }
            }
        }


        stage('Deploy to Kubernetes') {
            steps {
                script {
                    bat 'kubectl apply -f k8s/'
                }
            }
        }
    }
}
