# 로컬 검증 기록

2026-10-21 한국 시간, `/workspace/Craftsman-Excavator-Operation-CBT`.
Node 24.19.0, npm 11.9.0, Chromium 154.0.8037.57 (Debian).

| 검사 | 결과 |
| --- | --- |
| npm ci --cache /workspace/.npm-cache --no-audit --no-fund | exit 0、lockfile 설치 |
| npm test | exit 0、18 passed / 0 failed / 0 skipped |
| PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e | exit 0、26 passed / 0 failed / 0 skipped、34.1초 |
| 위 test:e2e의 npm run build | exit 0、TypeScript + Vite 프로덕션 빌드 |
| python3 scripts/audit-bank.py | exit 0、72문항 구조·중복·원고 재현 확인 |

초기 설치는 기본 `/home/agent/.npm/_cacache` 쓰기 실패로 중단됐으며 작업 공간 캐시로 바꿔 정상 설치했다. TLS/무결성 검증을 끄지 않았다. 초기 단위 검사에서 기존 과목별 20문항 기대값 하나가 남아 실패해 통합 과목 60문항으로 수정한 뒤 최종 18개가 통과했다. 이는 로컬 개발 중 수정이며 배포 재시도가 아니다.

브라우저 검사는 13개 시나리오 × desktop / Pixel 7 모바일 에뮬레이션이다. 설치된 Chromium을 직접 구동했다. 실제 휴대전화·Safari·Firefox·블로그 iframe은 미실행이다.

- 두 모드 시작, 답변·변경·북마크·새로고침 복원, 합격 경계의 결과와 오답 복습.
- 실제 clock으로 만료 전후 이동, 자동 제출, 만료 재접속, 중복 제출 방지, 타이머 콜백 전 만료 후 답안 차단.
- 실전과 랜덤의 실제 Space keydown/keyup, 문제 본문 포커스, 미응답·반복·수정키·버튼·컨트롤·대화상자 보호, 마지막 문항 자동 제출 방지.
- 등록·중복 제거·검증 대기·근거와 확인 후 로컬 승인·CSV 등록·원자적 오류·초기화.
- 손상 저장 원본 보존, 저장 실패 경고, 실제 JSON 백업 다운로드.
- 학습 기준 메뉴 없음, 상단 criteria-note 없음, 주요 화면 이동, 가로 넘침 없음.
- 메뉴 390×480 / 740×360 / 390×480 글자150%에서 실제 휠 아래·위 입력. 하단 초기화 도구를 클릭하고 확인창 취소 후 위로 돌아와 대시보드를 클릭함.
- 모바일 3조건은 위 휠 검사와 별도로 CDP `Input.dispatchTouchEvent`의 touchStart/move/end 스와이프로 아래·위 이동. 하단 도구 탭과 상단 대시보드 접근 검증. 프로그램으로 scrollTop을 설정하지 않음. 메뉴 애니메이션 종료 및 배경 스크롤 전파 방지도 확인.

채점·추출·시간·가져오기·복원·72문항 구조 테스트는 환경과 앱 로직의 증거다. 공식 규칙·전문가 검수·문항 정확성에 관한 외부 검증을 대신하지 않는다. 1,000문항 수량 기준은 미충족(928 부족)이다.

배포 사전 확인: Git 원격 main 읽기 성공. 이후 GitHub 저장소 API 요청 `Forbidden`으로 차단. main push·CI·Pages 실행은 하지 않았다. API 상태 재조회·재배포·공개 주소 조회도 하지 않았으며 공개 화면 확인 미실행이다. 자세한 오류와 최소 사용자 조치는 README에 기록했다.

클라우드 dev 서버도 `npm run dev -- --port 5173 --strictPort`로 시작하고 기본 경로의 HTML을 HTTP 성공 응답과 한국어 제목으로 확인했다. 공개 Pages 주소에 대한 검증이 아니다. 스킬 폴더 전체는 원본 최신 main 사본과 `diff -qr`로 동일함을 확인했다. 클라우드 설정 초안의 install_script·start_skill과 `api.github.com`, `www.q-net.or.kr` 도메인 요구를 저장했으며, 현재 런타임 적용·게시·GitHub 재시도는 하지 않았다.
