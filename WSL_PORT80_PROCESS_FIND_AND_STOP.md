# WSL에서 80 포트 점유 프로세스 찾기 및 종료

## 1) 80 포트 점유 프로세스 찾기

```bash
# LISTEN 중인 80 포트 프로세스 확인
sudo ss -ltnp 'sport = :80'

# 프로세스/사용자/FD 상세 확인
sudo lsof -iTCP:80 -sTCP:LISTEN -n -P
```

## 2) 점유 프로세스 종료

### 방법 A: 서비스로 종료 (nginx 등)

```bash
sudo systemctl stop nginx 2>/dev/null || sudo service nginx stop
```

### 방법 B: PID로 강제 종료

```bash
# 예시: nginx master PID가 197인 경우
sudo kill -9 197
```

## 3) 종료 확인

```bash
sudo ss -ltnp 'sport = :80'
```

출력 결과에 `:80` LISTEN 항목이 없으면 해제 완료입니다.

