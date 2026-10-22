"""32 explicit learning models × 29 input sets; not official exam questions.
Decimal is used here. Independent SI-unit evaluators live in tests/numeric.test.ts.
"""
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING, localcontext

D = lambda value: Decimal(str(value))
PI = D('3.14')
FAMILIES = []

def family(kind, topic, title, unit, inputs, prompt, evaluate, explanation):
    FAMILIES.append(dict(kind=kind, topic=topic, title=title, unit=unit,
        inputs=inputs, prompt=prompt, evaluate=evaluate, explanation=explanation))

family('hydraulicForce', '유압장치', '실린더 이론 추력', 'kN',
    lambda i: [10+i/2, 80+5*i],
    lambda p,a: f'굴착기 유압 실린더의 피스톤 유효 면적은 {a} cm², 공급 압력은 {p} MPa이다. 반대쪽 압력과 마찰을 무시할 때 이론 추력은?',
    lambda p,a: p*a/10,
    lambda p,a: f'F=pA. 1 MPa=10⁶ Pa, 1 cm²=10⁻⁴ m²이므로 kN 환산 시 F={p}×{a}/10이다. 이는 이론 실린더 힘이며 버킷 끝 굴착력이나 허용 인양하중이 아니다.')
family('annularForce', '유압장치', '로드측 환상 면적과 힘', 'kN',
    lambda i: [12+i/4, 120+4*i, 30+i],
    lambda p,a,r: f'복동 실린더의 피스톤 전체 면적은 {a} cm², 로드 단면적은 {r} cm²이다. 로드측에 {p} MPa를 공급하고 반대쪽 압력·마찰을 무시할 때 후퇴 방향 이론 힘은?',
    lambda p,a,r: p*(a-r)/10,
    lambda p,a,r: f'로드측 유효 면적 Aₑ=A피스톤−A로드={a}−{r} cm². 압력×면적을 kN으로 환산하면 F={p}×({a}−{r})/10이다. 로드 면적을 더하거나 전체 면적을 그대로 사용하지 않는다.')
family('requiredPressure', '유압장치', '필요 이론 압력', 'MPa',
    lambda i: [30+2*i, 100+3*i],
    lambda f,a: f'유효 면적 {a} cm²인 실린더로 {f} kN의 힘을 내려고 한다. 마찰과 반대쪽 압력을 무시할 때 필요한 이론 압력은?',
    lambda f,a: f*10/a,
    lambda f,a: f'p=F/A. 힘 {f} kN을 N으로, 면적 {a} cm²를 m²로 바꾸어 나누고 MPa로 환산하면 p=10×{f}/{a}이다. 실제 설정압력은 이 계산만으로 정하지 않는다.')
family('pumpFlow', '유압장치', '펌프 토출 유량', 'L/min',
    lambda i: [35+i, 1200+20*i, 85+i%10],
    lambda v,n,e: f'펌프의 1회전당 이론 토출량은 {v} cm³/rev, 회전수는 {n} rev/min, 체적효율은 {e}%이다. 실제 토출 유량은?',
    lambda v,n,e: v*n*e/100000,
    lambda v,n,e: f'실제 유량=회전당 토출량×회전수×체적효율. Q={v}×{n}×({e}/100) cm³/min이며 1,000으로 나누어 L/min으로 바꾼다. 체적효율은 유량 손실에만 적용한 조건이다.')
family('cylinderSpeed', '유압장치', '실린더 피스톤 속도', 'm/s',
    lambda i: [45+3*i, 120+5*i],
    lambda q,a: f'실린더 한쪽의 유효 면적은 {a} cm²이고 그쪽 유입 유량은 {q} L/min이다. 누설과 유체 압축을 무시할 때 피스톤의 일정 이동 속도는?',
    lambda q,a: q/(6*a),
    lambda q,a: f'속도 v=Q/A. Q={q}×10⁻³/60 m³/s, A={a}×10⁻⁴ m²를 대입하면 v={q}/(6×{a}) m/s이다. 유입측 유효 면적을 사용한다.')
family('cylinderTime', '유압장치', '실린더 행정 시간', 's',
    lambda i: [D('0.5')+D(i)/100, 160+5*i, 60+2*i],
    lambda s,a,q: f'유효 면적 {a} cm²인 실린더를 {s} m 전진시키려 한다. 일정 유입 유량은 {q} L/min이다. 누설·압축·가감속을 무시할 때 소요 시간은?',
    lambda s,a,q: s*a*6/q,
    lambda s,a,q: f'필요 체적 V=A×행정={a}×10⁻⁴×{s} m³. t=V/Q이며 유량 {q} L/min을 m³/s로 바꾸면 t=6×{a}×{s}/{q} s이다. 실제 가감속 시간은 포함하지 않는다.')
family('cylinderVolume', '유압장치', '실린더 충전 체적', 'L',
    lambda i: [90+4*i, 35+2*i],
    lambda a,s: f'실린더 유효 면적이 {a} cm²이고 행정이 {s} cm이다. 유체 압축과 배관 체적을 제외할 때 해당 행정에 필요한 유압유 체적은?',
    lambda a,s: a*s/1000,
    lambda a,s: f'체적=유효 면적×행정={a}×{s} cm³이다. 1 L=1,000 cm³이므로 V={a}×{s}/1,000 L. 면적과 길이의 단위를 맞춰야 한다.')
family('hydraulicPower', '유압장치', '유압 동력', 'kW',
    lambda i: [8+i/2, 70+3*i],
    lambda p,q: f'압력차가 {p} MPa, 유량이 {q} L/min인 회로의 유체 동력은? 회로 내부 손실은 계산에서 제외한다.',
    lambda p,q: p*q/60,
    lambda p,q: f'유체 동력 P=Δp×Q. {p}×10⁶ Pa와 {q}×10⁻³/60 m³/s를 곱한 뒤 W를 kW로 바꾸면 P={p}×{q}/60 kW이다. 펌프 축 입력동력과 구별한다.')
family('pumpInputPower', '유압장치', '펌프 축 입력동력', 'kW',
    lambda i: [10+i/4, 80+4*i, 75+i%15],
    lambda p,q,e: f'펌프가 압력차 {p} MPa에서 {q} L/min을 공급한다. 펌프 전체 효율이 {e}%일 때 필요한 축 입력동력은?',
    lambda p,q,e: p*q/60/(e/100),
    lambda p,q,e: f'유체 출력={p}×{q}/60 kW. 전체 효율 η=출력/입력이므로 입력=출력/({e}/100)이다. 효율이 100%보다 작으므로 입력이 유체 출력보다 커야 한다.')
family('motorTorque', '유압장치', '유압모터 축 토크', 'N·m',
    lambda i: [10+i/4, 80+5*i, 80+i%10],
    lambda p,v,e: f'유압모터 압력차는 {p} MPa, 1회전당 배제용적은 {v} cm³/rev, 기계효율은 {e}%이다. π=3.14일 때 축 출력 토크는?',
    lambda p,v,e: p*v*(e/100)/(2*PI),
    lambda p,v,e: f'1회전의 유체 일은 Δp×V이며 회전각은 2π rad이다. 이론 토크=ΔpV/(2π), 출력 토크에 기계효율을 곱한다. MPa×cm³는 N·m와 수치가 같아 T={p}×{v}×({e}/100)/(2×3.14) N·m이다.')
family('motorSpeed', '유압장치', '유압모터 실제 회전수', 'rev/min',
    lambda i: [45+2*i, 120+5*i, 85+i%10],
    lambda q,v,e: f'유압모터 유입 유량은 {q} L/min, 배제용적은 {v} cm³/rev, 체적효율은 {e}%이다. 누설을 체적효율로 반영한 실제 회전수는?',
    lambda q,v,e: q*1000/v*(e/100),
    lambda q,v,e: f'이론 회전수=유량/배제용적. 유량을 cm³/min으로 바꾸어 n={q}×1,000/{v}×({e}/100) rev/min이다. 모터에서는 체적효율을 곱해 실제 회전수를 계산한다.')
family('overallEfficiency', '유압장치', '기계 전체 효율', '%',
    lambda i: [40+2*i, 60+3*i+i%4],
    lambda out,inp: f'정상상태에서 장치의 유효 축 출력이 {out} kW, 축 입력이 {inp} kW로 측정되었다. 전체 효율은?',
    lambda out,inp: out/inp*100,
    lambda out,inp: f'효율 η=유효 출력/입력×100={out}/{inp}×100%이다. 입력과 출력 단위가 같아야 하며 이 조건에서 출력은 입력보다 작다. 손실률과 효율은 구별한다.')
family('engineDisplacement', '기관 기초', '기관 총 배기량', 'cm³',
    lambda i: [85+i, 90+i, 4],
    lambda b,s,n: f'다기통 기관의 실린더 지름은 {b} mm, 행정은 {s} mm, 기통 수는 {n}개이다. π=3.14일 때 총 행정체적(배기량)은?',
    lambda b,s,n: PI*b*b/4*s*n/1000,
    lambda b,s,n: f'한 기통 행정체적=πD²S/4이고 총 배기량은 이를 {n}배 한다. {b} mm와 {s} mm를 대입한 mm³ 값을 1,000으로 나누어 cm³로 바꾼다. 연소실의 틈새 체적은 배기량에 더하지 않는다.')
family('engineTorque', '기관 기초', '기관 출력과 회전 토크', 'N·m',
    lambda i: [40+2*i, 1500+25*i],
    lambda p,n: f'기관의 축 출력이 {p} kW이고 회전수가 {n} rev/min이다. π=3.14를 사용한 평균 축 토크는?',
    lambda p,n: p*1000*60/(2*PI*n),
    lambda p,n: f'P=Tω, ω=2πn/60 rad/s이다. {p} kW를 1,000배하여 W로 바꾼 뒤 T={p}×1,000×60/(2×3.14×{n}) N·m를 계산한다. 출력과 토크는 같은 물리량이 아니다.')
family('fuelRate', '기관 기초', '평균 연료 소비율', 'L/h',
    lambda i: [45+3*i, D('2.5')+D(i%7)/4],
    lambda fuel,t: f'굴착기가 일정 작업 구간 {t} h 동안 연료 {fuel} L를 소비했다. 그 구간의 평균 시간당 연료 소비량은?',
    lambda fuel,t: fuel/t,
    lambda fuel,t: f'평균 소비율=소비량/경과시간={fuel}/{t} L/h이다. 평균값이므로 부하나 공회전 비중이 달라진 다른 구간에도 같은 소비율이라고 단정하지 않는다.')
family('fuelEndurance', '기관 기초', '사용 가능 연료와 운전 시간', 'h',
    lambda i: [130+5*i, 20+i, 10+i/4],
    lambda total,reserve,rate: f'현재 연료는 {total} L이며 이 중 {reserve} L는 예비량으로 남긴다. 연료 소비율을 일정한 {rate} L/h로 가정할 때 예비량을 제외한 계산상 운전 가능 시간은?',
    lambda total,reserve,rate: (total-reserve)/rate,
    lambda total,reserve,rate: f'사용 가능 연료={total}−{reserve} L. 시간=(현재량−남길 양)/시간당 소비량=({total}−{reserve})/{rate} h이다. 예비량은 이 문항의 가정이며 법정 기준이나 실제 운전 보장이 아니다.')
family('trenchVolume', '조종·작업', '직육면체 굴착 체적', 'm³',
    lambda i: [12+i, D('0.8')+D(i%5)/10, D('1.1')+D(i%7)/10],
    lambda l,w,d: f'굴착 단면을 직사각형으로 단순화한다. 도랑 길이 {l} m, 폭 {w} m, 깊이 {d} m일 때 자연상태 굴착 체적은? 여굴·경사면·침하는 제외한다.',
    lambda l,w,d: l*w*d,
    lambda l,w,d: f'직육면체 체적 V=길이×폭×깊이={l}×{w}×{d} m³이다. 흙이 흐트러져 늘어나는 체적은 아직 반영하지 않은 자연상태의 기하학적 체적이다.')
family('looseVolume', '조종·작업', '흐트러진 흙의 체적', 'm³',
    lambda i: [35+3*i, D('1.1')+D(i%9)/100],
    lambda v,k: f'자연상태 토량이 {v} m³이다. 이 문항에서 흐트러진 체적/자연상태 체적 비를 {k}로 가정할 때 굴착 후 흐트러진 체적은?',
    lambda v,k: v*k,
    lambda v,k: f'정의된 체적비 k=흐트러진 체적/자연상태 체적이므로 흐트러진 체적={v}×{k} m³이다. 주어진 계수는 연습 조건이며 모든 토질에 공통인 값이 아니다.')
family('bucketOutput', '조종·작업', '버킷 기준 시간당 토량', 'm³/h',
    lambda i: [D('0.4')+D(i)/100, 70+i%20, 80+2*i],
    lambda v,e,n: f'버킷 공칭 체적은 {v} m³, 평균 채움률은 {e}%, 실제 1시간 작업 횟수는 {n}회이다. 공칭 체적과 채움률을 같은 흐트러진 상태 기준으로 볼 때 시간당 토량은?',
    lambda v,e,n: v*e/100*n,
    lambda v,e,n: f'1회 실토량=공칭 체적×채움률={v}×({e}/100) m³. 시간당 토량은 이를 {n}회 곱한다. 횟수는 이미 실제 작업 횟수이므로 별도 가동률을 중복 적용하지 않는다.')
family('cycleTime', '조종·작업', '굴착 적재 사이클 시간', 's',
    lambda i: [8+i/4, 5+i%5, 3+i%3, 4+i%4],
    lambda a,b,c,d: f'한 번의 작업은 굴착 {a} s, 적재 위치까지 선회 {b} s, 배토 {c} s, 원위치 복귀 {d} s로 이루어진다. 동작 겹침이나 대기 없이 순차 진행할 때 1사이클 시간은?',
    lambda a,b,c,d: a+b+c+d,
    lambda a,b,c,d: f'순차 동작의 사이클 시간은 각 시간의 합이다. T={a}+{b}+{c}+{d} s. 동시 동작과 대기 시간이 없다는 조건이므로 합산하며 현장 평균 사이클과 같다고 단정하지 않는다.')
family('truckTrips', '조종·작업', '체적 제한 운반 횟수', '회',
    lambda i: [90+7*i, 6+i%5],
    lambda v,c: f'흐트러진 흙 {v} m³를 운반한다. 차량 1회 운반 가능 체적을 {c} m³로 제한하고 마지막 일부 적재도 1회로 셀 때 필요한 최소 운반 횟수는? 중량 제한은 별도로 충족된다고 가정한다.',
    lambda v,c: (v/c).to_integral_value(rounding=ROUND_CEILING),
    lambda v,c: f'횟수={v}/{c}를 올림한 정수이다. 남는 흙이 있으면 추가 1회가 필요하므로 일반 반올림을 쓰지 않는다. 차량 대수나 법정 적재한도를 묻는 문제가 아니라 제시된 체적 조건의 운반 횟수이다.')
family('soilMass', '조종·작업', '흙의 체적과 질량', 't',
    lambda i: [6+i/2, D('1.4')+D(i%8)/20],
    lambda v,rho: f'운반할 흙의 체적이 {v} m³이고 해당 상태에서 측정한 평균 밀도가 {rho} t/m³이다. 질량은?',
    lambda v,rho: v*rho,
    lambda v,rho: f'질량 m=밀도×체적={rho}×{v} t이다. 밀도의 체적 상태와 토량의 상태가 같다는 조건이며, 자연상태 밀도를 흐트러진 체적에 그대로 적용하지 않는다.')
family('groundPressure', '현장 안전', '평균 정적 접지압', 'kPa',
    lambda i: [140+5*i, D('2.8')+D(i%7)/10],
    lambda w,a: f'수평면에서 장비 전체 중량은 {w} kN, 양쪽 트랙의 총 접지면적은 {a} m²이다. 하중이 균등 분포한다고 단순화할 때 평균 정적 접지압은?',
    lambda w,a: w/a,
    lambda w,a: f'평균 압력=중량/총 접지면적={w}/{a} kN/m². 1 kN/m²=1 kPa이다. 평균 정적 값만으로 지반의 허용 지지력이나 전도 안전성을 판단할 수 없다.')
family('gradePercent', '현장 안전', '경사율의 기하학적 계산', '%',
    lambda i: [D('0.5')+D(i)/20, 8+i/2],
    lambda h,l: f'경사면의 높이 차는 {h} m, 수평거리는 {l} m이다. 높이 차/수평거리×100으로 정의한 경사율은? 장비의 주행 허용 경사각을 묻는 것은 아니다.',
    lambda h,l: h/l*100,
    lambda h,l: f'경사율={h}/{l}×100%이다. 분모는 경사면 길이가 아니라 수평거리이며, 경사율(%)과 경사각(도)은 서로 다른 값이다. 이 계산이 주행 안전을 보장하지 않는다.')
family('travelDistance', '현장 안전', '일정 속도 이동 거리', 'km',
    lambda i: [D('2.1')+D(i)/20, 6+i],
    lambda v,t: f'닫힌 시험 구간에서 평균 속도 {v} km/h로 {t} min 동안 이동했다고 가정한다. 이동 거리는? 가감속 구간은 이 평균 속도에 포함한다.',
    lambda v,t: v*t/60,
    lambda v,t: f'거리=속도×시간. {t} min={t}/60 h이므로 s={v}×{t}/60 km이다. 이 속도는 문제의 계산 조건일 뿐 현장 허용속도나 도로 운행 규칙이 아니다.')
family('travelTime', '현장 안전', '이동 거리와 소요 시간', 'min',
    lambda i: [120+15*i, D('2')+D(i%8)/5],
    lambda s,v: f'장비가 거리 {s} m를 평균 속도 {v} km/h로 이동한다고 단순화한다. 정차 시간을 제외한 소요 시간은? 실제 현장 주행 허용 여부는 별도로 판단한다.',
    lambda s,v: s/1000/v*60,
    lambda s,v: f'시간=거리/속도. 거리를 {s}/1,000 km로 바꾸고 h를 min으로 바꾸면 t={s}/1,000/{v}×60 min이다. 단위 변환을 생략하면 1,000배 또는 60배 오류가 생긴다.')
family('loadMoment', '작업장치·점검', '단순 하중 모멘트', 'kN·m',
    lambda i: [D('0.5')+D(i)/20, D('2')+D(i%7)/4],
    lambda m,r: f'단순 정역학 모형에서 질량 {m} t인 하중의 수평거리가 기준점에서 {r} m이다. 중력가속도 9.8 m/s²일 때 이 하중만의 모멘트 크기는? 장비 허용 인양하중을 구하는 문제가 아니다.',
    lambda m,r: m*D('9.8')*r,
    lambda m,r: f'질량 {m} t는 중력가속도 9.8에서 중량 {m}×9.8 kN이다. 모멘트=힘×수직거리이므로 M={m}×9.8×{r} kN·m. 장비 자중·자세·동적 하중·제조사 하중표를 반영하지 않아 인양 안전 판단에 사용할 수 없다.')
family('mechanicalWork', '작업장치·점검', '일정 힘의 기계적 일', 'kJ',
    lambda i: [20+i, D('0.4')+D(i)/50],
    lambda f,s: f'일정한 힘 {f} kN이 이동 방향과 나란히 작용하여 부품이 {s} m 이동했다. 이 힘이 한 기계적 일은? 마찰과 가감속은 제외한다.',
    lambda f,s: f*s,
    lambda f,s: f'일 W=F×s. {f} kN×{s} m={f}×{s} kJ이다. 1 kN·m=1 kJ이며 힘이 이동 방향과 나란하다는 조건이 필요하다.')
family('averagePower', '작업장치·점검', '일과 평균 동력', 'kW',
    lambda i: [180+12*i, 6+i%7],
    lambda w,t: f'작업장치가 {t} s 동안 유효한 기계적 일 {w} kJ를 수행했다. 이 구간의 평균 유효 동력은?',
    lambda w,t: w/t,
    lambda w,t: f'평균 동력=일/시간={w}/{t} kJ/s. 1 kJ/s=1 kW이다. 이는 유효 작업 동력으로, 손실을 포함한 기관 입력동력과 같다고 할 수 없다.')
family('batteryEnergy', '전기·동력전달', '축전지 명목 에너지', 'Wh',
    lambda i: [24, 60+5*i],
    lambda v,c: f'장비 축전지의 명목 전압은 {v} V, 정격 용량은 {c} Ah이다. 전압이 일정하다고 단순화할 때 명목 전기 에너지는? 실제 방전 가능 에너지와는 구별한다.',
    lambda v,c: v*c,
    lambda v,c: f'명목 에너지=전압×전하 용량={v}×{c} Wh이다. Ah는 전하량 단위이고 Wh는 에너지 단위다. 실제 방전량은 온도·방전율·노화·종지전압 등에 따라 달라진다.')
family('electricalPower', '전기·동력전달', '직류 전장품 소비전력', 'kW',
    lambda i: [24, 15+i],
    lambda v,a: f'직류 전장품 양단 전압은 {v} V, 흐르는 전류는 {a} A이다. 정상상태의 입력 전력은?',
    lambda v,a: v*a/1000,
    lambda v,a: f'직류 전력 P=VI={v}×{a} W이며 1,000으로 나누어 kW로 바꾼다. 이는 전기 입력으로 전동기 등의 기계 출력과는 효율만큼 차이가 날 수 있다.')
family('voltageDrop', '전기·동력전달', '직류 배선 전압강하', 'V',
    lambda i: [20+i, D('0.01')+D(i%9)/1000],
    lambda a,r: f'장비 직류회로에서 왕복 배선 전체 저항은 {r} Ω이고 전류는 {a} A이다. 배선 전체에 생기는 전압강하는? 접촉저항도 제시된 전체 저항에 포함한다.',
    lambda a,r: a*r,
    lambda a,r: f'옴의 법칙 ΔV=IR={a}×{r} V이다. 이미 왕복 전체 저항이 주어졌으므로 길이를 두 배로 보아 저항을 다시 두 배 하지 않는다. 기기 단자전압을 묻는 것이 아닌 배선 강하량이다.')


def rounded(value):
    return D(value).quantize(D('0.01'), rounding=ROUND_HALF_UP)


def text(value):
    # Inputs are finite Decimal values. Never truncate them before evaluation.
    return format(value, 'f').rstrip('0').rstrip('.') if '.' in format(value, 'f') else str(value)


def build_numeric_bank():
    questions = []
    assert len(FAMILIES) == 32
    with localcontext() as ctx:
        ctx.prec = 36
        for number, spec in enumerate(FAMILIES, 1):
            for index in range(29):
                values = [D(v) for v in spec['inputs'](index)]
                result = rounded(spec['evaluate'](*values))
                # Deliberate arithmetic distractors. Same units and precision, never alternate correct values.
                options = [result, rounded(result*D('0.5')), rounded(result*D('1.25')), rounded(result*2)]
                assert len(set(options)) == 4 and min(options) > 0
                rotation = (number+index) % 4
                options = options[rotation:] + options[:rotation]
                units = spec['unit']
                unit_string = lambda value: f'{text(value)} {units}'
                displayed = [text(v) for v in values]
                # Explicit Korean rounding instruction; truckTrips uses a discrete ceiling instead.
                rounding_note = '횟수는 올림한 정수로 구한다.' if spec['kind']=='truckTrips' else '최종값은 소수 셋째 자리에서 반올림한다.'
                question = spec['prompt'](*displayed)+' '+rounding_note
                rationale = spec['explanation'](*displayed)
                explanation = f"{rationale} 계산 결과는 {unit_string(result)}이다. {rounding_note} 제시한 단순화 조건의 연습 계산이며 실제 장비의 작업 허용값은 제조사 자료와 작업계획으로 별도 확인한다."
                questions.append(dict(
                    id=f'EXC-N-{number:02}-{index+1:02}', subject='굴착기 조종, 점검 및 안전관리',
                    topic=spec['topic'], question=question,
                    choices=[unit_string(v) for v in options], answer=options.index(result)+1,
                    explanation=explanation, difficulty='중', year=None, session=None,
                    type='original', sourceUrl='https://github.com/YunSangYeong/Craftsman-Excavator-Operation-CBT/blob/main/docs/calculation-review.md',
                    verificationStatus='reviewed',
                    reviewNote=f"자체 제작 계산 조건 변형 · {spec['title']} · 동일 family 29문항 중 {index+1}번. AI 일반 지식의 기본 물리식과 단위 정의로 작성. 유형별 문장·가정 내부 검토 및 별도 SI 계산 테스트 수행. 외부 전문가 검수·공식 출제기준 대조 미완료.",
                    version='main', rights='자체 제작 원고: CC BY 4.0, Craftsman-Excavator-Operation-CBT contributors. 공식 기출·복원 아님.',
                    family=f'EXC-{spec["kind"]}',
                    calculation=dict(kind=spec['kind'], values=[float(v) for v in values], result=float(result), unit=units, precision=2)))
    return questions
