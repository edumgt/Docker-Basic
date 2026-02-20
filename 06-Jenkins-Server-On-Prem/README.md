# 06장 - Jenkins 서버 온프레미스 구축 (Dockerfile 기반)

## Jenkins 소개
Jenkins는 가장 널리 사용되는 오픈소스 CI 서버입니다.  
코드 빌드, 테스트, 배포 파이프라인을 자동화하고 수천 개의 플러그인을 통해 다양한 개발 도구와 통합할 수 있습니다.

## 이 장의 목표
- Dockerfile로 Jenkins 컨테이너 이미지를 직접 빌드
- 온프레미스 환경에서 Jenkins 마스터(컨트롤러) 컨테이너 기동
- 기본 포트/볼륨/초기 관리자 비밀번호 확인까지 실습

## Dockerfile
```dockerfile
FROM jenkins/jenkins:lts-jdk17

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io git curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
EXPOSE 8080 50000
```

### 구성 포인트
- `jenkins/jenkins:lts-jdk17`: 안정적인 LTS Jenkins + JDK17 베이스
- `docker.io`, `git`, `curl` 설치: 파이프라인 작업에서 자주 필요
- `8080`: Jenkins 웹 UI
- `50000`: 에이전트 연결 포트

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-jenkins:1.0 .

# 2) 데이터 보존용 볼륨 생성
docker volume create jenkins_home

# 3) 컨테이너 실행
docker run -d --name jenkins-server \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  onprem-jenkins:1.0
```

## 초기 접속
1. 브라우저에서 `http://localhost:8080` 접속
2. 초기 관리자 비밀번호 확인:
```bash
docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword
```

## 운영 팁
- Jenkins 홈(`/var/jenkins_home`)은 반드시 볼륨으로 분리
- 플러그인 버전은 주기적으로 검증 후 고정 관리
- 운영 환경에서는 리버스 프록시(Nginx) + TLS 적용 권장
