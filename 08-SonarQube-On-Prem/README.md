# 08장 - SonarQube 온프레미스 구축 (Dockerfile 기반)

## SonarQube 소개
SonarQube는 코드 품질과 보안 취약점을 정적 분석으로 점검하는 대표 오픈소스 플랫폼입니다.
CI 파이프라인에 연동하여 코드 스멜, 버그, 취약점을 Pull Request 단계에서 조기 탐지할 수 있습니다.

## 이 장의 목표
- SonarQube 컨테이너 이미지를 Dockerfile로 구성
- 코드 품질 대시보드를 온프레미스에서 운영
- Jenkins/GitLab CI와 연계 가능한 기본 환경 준비

## Dockerfile
```dockerfile
FROM sonarqube:community

ENV SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true

EXPOSE 9000
```

### 구성 포인트
- `sonarqube:community`: 무료 커뮤니티 에디션
- `9000`: SonarQube 웹 UI/REST API 포트
- 단일 노드 실습 환경을 위한 최소 설정 적용

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-sonarqube:1.0 .

# 2) 볼륨 생성
docker volume create sonarqube_data
docker volume create sonarqube_extensions
docker volume create sonarqube_logs

# 3) 컨테이너 실행
docker run -d --name sonarqube \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  -v sonarqube_extensions:/opt/sonarqube/extensions \
  -v sonarqube_logs:/opt/sonarqube/logs \
  onprem-sonarqube:1.0
```

## 초기 접속
- URL: `http://localhost:9000`
- 기본 계정: `admin / admin` (최초 로그인 시 비밀번호 변경)

## 운영 팁
- 운영 환경은 외부 PostgreSQL 연동 권장
- 품질 게이트를 CI 파이프라인 실패 조건으로 연동하면 효과적
