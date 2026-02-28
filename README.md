# Docker Fundamentals

## StackSimplify 의 Docker 교육 Repo 를 복제하여 빌드업한 Docker 교육용 Repo 입니다.

이 저장소는 **Docker 기본기 학습(1~5번)**과 **온프레미스 DevSecOps 오픈소스 연동(6~10번)**을 한 흐름으로 다루는 실습형 레포지토리입니다.

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

---

## Solution Architect 관점의 전체 기술 스택

### 1) 핵심 플랫폼 레이어
- **Container Runtime**: Docker Engine
- **이미지 배포/저장**: Docker Hub + Nexus Repository OSS(사내 프록시/호스팅)
- **CI 서버**: Jenkins, Drone CI
- **SCM/코드협업**: GitLab CE
- **코드 품질/정적분석**: SonarQube
- **애플리케이션 런타임 예시**: Nginx, Spring Boot

### 2) 현재 레포 기준 역할 분리
- **개발자 경험(Developer Experience)**: Docker 기본 학습 + 이미지 빌드/실행/배포
- **플랫폼 운영(Platform Ops)**: 사내 CI/CD 도구와 아티팩트 저장소 구축
- **품질 게이트(Quality Gate)**: SonarQube 연계로 코드 품질 기준 수립

### 3) 컴포넌트 간 관계(Reference Flow)
1. 개발자가 GitLab CE에 코드 Push
2. Jenkins 또는 Drone CI가 빌드 파이프라인 수행
3. 테스트/분석 단계에서 SonarQube 품질 검사 수행
4. Docker 이미지 빌드 후 Nexus Repository(또는 Docker Hub)에 푸시
5. 운영 서버에서 해당 이미지를 Pull하여 배포

> 즉, **GitLab(소스) → Jenkins/Drone(CI) → SonarQube(품질) → Nexus(아티팩트) → Docker Runtime(배포)** 의 체인으로 이해할 수 있습니다.

---

## 온프레미스 운영 시 추가하면 좋은 오픈소스(권장)

현재 구성은 학습/기본 운영에 적합하며, 실제 운영 안정성을 높이려면 아래 스택을 확장하는 것을 권장합니다.

### A. 보안/접근제어
- **Keycloak**: SSO 및 중앙 인증( GitLab/Jenkins/Sonar/Nexus 통합)
- **HashiCorp Vault**: 비밀정보(토큰/패스워드/인증서) 중앙관리
- **Trivy**: 이미지 취약점 스캔(파이프라인 내 자동화)

### B. 관측성(Observability)
- **Prometheus + Grafana**: 메트릭 수집/대시보드
- **Loki + Promtail** 또는 **EFK/ELK**: 로그 수집 및 분석
- **Alertmanager**: 장애 알림 자동화

### C. 네트워크/트래픽
- **Traefik / Nginx Proxy Manager**: 리버스 프록시, HTTPS/TLS 종료, 라우팅
- **cert-manager 대체 운영방안(사설 CA)**: 폐쇄망 인증서 자동갱신 전략 수립

### D. 이미지 거버넌스
- **Harbor(대안)**: 사내 컨테이너 레지스트리 + 취약점 스캔 + 서명정책
  - Nexus를 쓰는 경우에도 Harbor를 병행 검토 가능

### E. 백업/DR(재해복구)
- GitLab, SonarQube, Nexus 볼륨 및 DB 정기 백업
- 오브젝트 스토리지(MinIO 등) 기반 백업 보관 전략

---

## 권장 아키텍처(온프레미스 중소~중견 조직 기준)

- **Zone 1 - Dev Zone**: 개발자 PC, 로컬 Docker, 개발 테스트
- **Zone 2 - CI Zone**: GitLab, Jenkins/Drone, SonarQube
- **Zone 3 - Artifact Zone**: Nexus(또는 Harbor), 패키지/이미지 저장
- **Zone 4 - Runtime Zone**: 서비스 컨테이너 실행 노드
- **Zone 5 - Ops Zone**: 모니터링, 로깅, 백업, 보안 시스템

네트워크는 최소한 다음 정책을 권장합니다.
- CI Zone → Artifact Zone: Push 허용
- Runtime Zone → Artifact Zone: Pull 허용
- Dev Zone → Runtime Zone: 직접 접근 제한(배포는 CI 통해서만)

---

## 단계별 도입 로드맵 제안

1. **Phase 1 (기본기/PoC)**
   - 현재 레포의 1~10 단계 실습 완료
   - Jenkins/Drone 중 1개를 표준 CI로 선정
2. **Phase 2 (표준화)**
   - Git 브랜치 전략, 파이프라인 템플릿, Sonar 품질 게이트 표준화
   - Nexus 저장소 구조(팀/환경별) 정리
3. **Phase 3 (운영 안정화)**
   - 모니터링/로그/알림 연계
   - 백업/복구 리허설 및 장애 대응 Runbook 작성
4. **Phase 4 (보안 고도화)**
   - SSO, 비밀정보 중앙관리, 이미지 스캔/서명 정책 도입

---

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

## 이 레포 활용 대상
- Docker를 처음 학습하는 엔지니어
- 온프레미스 DevOps/Platform 구축을 시작하는 팀
- Solution Architect 관점에서 도구 간 연결 구조를 빠르게 파악하려는 실무자
