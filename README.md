# Docker Fundamentals

## StackSimplify 의 Docker 교육 Repo 를 복제하여 빌드업한 Docker 교육용 Repo 입니다.

## Docker Fundamentals에서 다루는 내용
1. Docker 소개
2. Docker 설치
3. 흐름-1: Docker Hub에서 이미지 내려받아 로컬에서 실행
4. 흐름-2: 새 Docker 이미지 빌드 → 로컬 실행 → Docker Hub에 푸시
5. 핵심 Docker 명령어
6. Jenkins 서버 온프레미스 구축
7. GitLab CE 온프레미스 구축
8. SonarQube 온프레미스 구축
9. Nexus Repository 온프레미스 구축
10. Drone CI 온프레미스 구축

## 사용되는 Docker 이미지
| 애플리케이션 이름 | Docker 이미지 이름 |
| --- | --- |
| Nginx | nginx |
| 커스텀 Nginx | stacksimplify/mynginx_image1 |
| 간단한 SpringBoot HelloWorld | stacksimplify/dockerintro-springboot-helloworld-rest-api |
| Jenkins LTS | jenkins/jenkins:lts-jdk17 |
| GitLab CE | gitlab/gitlab-ce:17.5.2-ce.0 |
| SonarQube Community | sonarqube:community |
| Nexus Repository OSS | sonatype/nexus3:3.70.1 |
| Drone CI | drone/drone:2 |
