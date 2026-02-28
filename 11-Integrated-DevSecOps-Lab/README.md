# 11. Integrated DevSecOps Lab (보안/관측성/트래픽/거버넌스)

요청하신 A~D 항목을 한 번에 실습할 수 있도록 `docker-compose` 기반 통합 실습 예제를 추가했습니다.

## 구성 요소

### A. 보안/접근제어
- **Keycloak**: 중앙 인증(SSO) 실습용 IdP
- **Vault**: 비밀정보 중앙 관리(Dev 모드)
- **Trivy**: 컨테이너 이미지 취약점 스캔

### B. 관측성(Observability)
- **Prometheus**: 메트릭 수집
- **Grafana**: 대시보드
- **Loki + Promtail**: 로그 수집/분석
- **Alertmanager**: 알림 라우팅

### C. 네트워크/트래픽
- **Traefik**: 리버스 프록시 + 라우팅
- **사설 CA 대체 전략**: `step-ca`를 profile(`private-ca`)로 제공

### D. 이미지 거버넌스
- **Harbor 대안 검토 실습용 구성**: `harbor` profile로 DB/Redis/Registry 샘플 포함
  - 실제 Harbor 풀스택 배포 전 개념검증(PoC)용
  - 기존 Nexus와 병행 운영 전략 검토 시, registry endpoint 분리 실습 가능

---

## 빠른 시작

```bash
cd 11-Integrated-DevSecOps-Lab
docker compose up -d
```

### 선택 프로파일 실행

```bash
# 사설 CA(step-ca) 포함 실행
docker compose --profile private-ca up -d

# Harbor 관련 샘플 컴포넌트 포함 실행
docker compose --profile harbor up -d
```

---

## 접속 URL (hosts 기반 라우팅)

Traefik 라우팅 테스트를 위해 `/etc/hosts`에 아래를 추가하세요.

```text
127.0.0.1 keycloak.localhost vault.localhost prometheus.localhost grafana.localhost harbor-registry.localhost
```

접속 주소:
- Keycloak: `http://keycloak.localhost`
- Vault: `http://vault.localhost`
- Prometheus: `http://prometheus.localhost`
- Grafana: `http://grafana.localhost`
- Traefik Dashboard: `http://localhost:8088`

---

## Trivy 실습

샘플 Dockerfile(`dockerfiles/vuln-demo`)을 빌드 후 Trivy로 스캔합니다.

```bash
./scripts/run-trivy-scan.sh
```

> 파이프라인에 연결할 때는 Jenkins/Drone job에서 동일 스크립트를 실행하면 됩니다.

---

## 운영 전환 시 권장사항

- Keycloak/Vault는 반드시 외부 DB + HA 구성을 사용
- Vault는 Dev 모드 대신 Raft/Auto-Unseal(KMS/HSM) 적용
- Traefik HTTPS는 step-ca 연동(ACME internal) 또는 조직 표준 PKI와 통합
- Harbor는 공식 `harbor.yml` 기반 설치(Chart/Installer)로 전환
- Alertmanager webhook을 Slack/Teams/사내 알림 시스템으로 연결
