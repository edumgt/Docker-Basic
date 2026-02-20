# 07장 - GitLab CE 온프레미스 구축 (Dockerfile 기반)

## GitLab CE 소개
GitLab CE는 소스코드 관리(Git), 이슈 관리, CI/CD 파이프라인을 한 번에 제공하는 DevOps 통합 플랫폼입니다.
온프레미스 환경에서 코드 저장소와 파이프라인을 내부망에서 독립적으로 운영할 때 많이 사용됩니다.

## 이 장의 목표
- Dockerfile 기반 GitLab CE 커스텀 이미지 준비
- 컨테이너 단일 노드로 GitLab 서비스 기동
- 데이터/로그/설정 디렉터리 영속화

## Dockerfile
```dockerfile
FROM gitlab/gitlab-ce:17.5.2-ce.0

ENV GITLAB_OMNIBUS_CONFIG="external_url 'http://gitlab.local'; gitlab_rails['gitlab_shell_ssh_port'] = 2222;"

EXPOSE 80 443 22
```

### 구성 포인트
- `gitlab/gitlab-ce` 공식 이미지 사용
- `GITLAB_OMNIBUS_CONFIG`로 초기 환경값 주입
- HTTP/HTTPS/SSH 포트 노출

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-gitlab:1.0 .

# 2) 볼륨 생성
docker volume create gitlab_config
docker volume create gitlab_logs
docker volume create gitlab_data

# 3) 컨테이너 실행
docker run -d --name gitlab-ce \
  --hostname gitlab.local \
  -p 8081:80 -p 8443:443 -p 2222:22 \
  -v gitlab_config:/etc/gitlab \
  -v gitlab_logs:/var/log/gitlab \
  -v gitlab_data:/var/opt/gitlab \
  --shm-size 256m \
  onprem-gitlab:1.0
```

## 초기 루트 비밀번호 확인
```bash
docker exec -it gitlab-ce grep 'Password:' /etc/gitlab/initial_root_password
```

## 운영 팁
- 메모리 최소 4GB 이상 권장
- 사내 DNS 또는 `/etc/hosts`에 `gitlab.local` 등록
- GitLab Runner는 별도 컨테이너로 분리 운영 권장
