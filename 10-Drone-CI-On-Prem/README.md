# 10장 - Drone CI 온프레미스 구축 (Dockerfile 기반)

## Drone CI 소개
Drone CI는 컨테이너 기반 파이프라인을 간결하게 구성할 수 있는 오픈소스 CI/CD 도구입니다.
`.drone.yml` 선언형 파이프라인으로 빌드/테스트/배포 단계를 빠르게 자동화할 수 있습니다.

## 이 장의 목표
- Dockerfile 기반 Drone 서버 이미지 구성
- 온프레미스에서 경량 CI 서버 실행
- GitHub/Gitea/GitLab OAuth 연동을 위한 기본 환경 변수 확인

## Dockerfile
```dockerfile
FROM drone/drone:2

ENV DRONE_SERVER_HOST=drone.local \
    DRONE_SERVER_PROTO=http \
    DRONE_RPC_SECRET=change-me

EXPOSE 80
```

### 구성 포인트
- `drone/drone:2` 공식 이미지 사용
- `DRONE_RPC_SECRET`: Drone 서버/러너 인증에 필수
- 실제 운영 시 OAuth 관련 ENV는 외부 주입 권장

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-drone:1.0 .

# 2) 볼륨 생성
docker volume create drone_data

# 3) 컨테이너 실행
docker run -d --name drone-server \
  -p 8083:80 \
  -v drone_data:/data \
  -e DRONE_GITEA_SERVER=http://gitea.local \
  -e DRONE_GITEA_CLIENT_ID=your-client-id \
  -e DRONE_GITEA_CLIENT_SECRET=your-client-secret \
  -e DRONE_RPC_SECRET=change-me \
  -e DRONE_USER_CREATE=username:admin,admin:true \
  onprem-drone:1.0
```

## 운영 팁
- Drone Runner는 서버와 분리하여 독립 배포 권장
- `DRONE_RPC_SECRET`는 강력한 랜덤 값으로 교체
- 사내 Git 서버(Gitea/GitLab)와 SSO/OAuth 통합 권장
