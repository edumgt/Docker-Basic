# 09장 - Nexus Repository 온프레미스 구축 (Dockerfile 기반)

## Nexus Repository 소개
Nexus Repository OSS는 Maven, npm, Docker Registry 프록시/호스팅 등 다양한 아티팩트 저장소를 제공하는 오픈소스 도구입니다.
CI 빌드 산출물을 중앙 저장소로 관리하여 배포 추적성과 재현성을 높일 수 있습니다.

## 이 장의 목표
- Dockerfile로 Nexus Repository 이미지 생성
- 온프레미스 아티팩트 저장소를 컨테이너로 운영
- 사내 CI/CD 파이프라인의 패키지 허브 역할 구성

## Dockerfile
```dockerfile
FROM sonatype/nexus3:3.70.1

EXPOSE 8081
```

### 구성 포인트
- `sonatype/nexus3` 공식 이미지 사용
- `8081` 포트로 Nexus UI 및 Repository API 제공

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-nexus:1.0 .

# 2) 볼륨 생성
docker volume create nexus_data

# 3) 컨테이너 실행
docker run -d --name nexus3 \
  -p 8082:8081 \
  -v nexus_data:/nexus-data \
  onprem-nexus:1.0
```

## 초기 관리자 비밀번호 확인
```bash
docker exec nexus3 cat /nexus-data/admin.password
```

## 운영 팁
- Blob Store 백업 정책을 별도로 구성
- Docker Hosted/Proxy repository를 분리해 캐시와 사설 이미지를 함께 운영
- 정기적인 컴포넌트 정리(Cleanup Policy)로 저장소 비대화 방지
