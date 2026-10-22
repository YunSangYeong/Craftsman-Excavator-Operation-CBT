import {describe, expect, it} from 'vitest';
import {BASE_BANK, createExam} from '../src/model';
// Independent path: derive results in SI units; do not import the Python generator.
const evaluate: Record<string,(v:number[])=>number> = {
  hydraulicForce: ([p,a]) => (p*1e6)*(a*1e-4)/1000,
  annularForce: ([p,a,r]) => (p*1e6)*((a-r)*1e-4)/1000,
  requiredPressure: ([f,a]) => (f*1000)/(a*1e-4)/1e6,
  pumpFlow: ([d,n,e]) => (d*1e-6)*(n/60)*(e/100)*60000,
  cylinderSpeed: ([q,a]) => (q/60000)/(a/10000),
  cylinderTime: ([s,a,q]) => (s*a/10000)/(q/60000),
  cylinderVolume: ([a,s]) => (a/10000)*(s/100)*1000,
  hydraulicPower: ([p,q]) => (p*1e6)*(q/60000)/1000,
  pumpInputPower: ([p,q,e]) => (p*1e6)*(q/60000)/(e/100)/1000,
  motorTorque: ([p,d,e]) => (p*1e6)*(d/1e6)/(2*3.14)*(e/100),
  motorSpeed: ([q,d,e]) => ((q/60000)*(e/100))/(d/1e6)*60,
  overallEfficiency: ([out,input]) => 100-(input-out)/input*100,
  engineDisplacement: ([b,s,n]) => 3.14*(b/2000)**2*(s/1000)*n*1e6,
  engineTorque: ([p,n]) => (p*1000)/(n/60*2*3.14),
  fuelRate: ([fuel,t]) => (fuel/1000)/(t*3600)*3600*1000,
  fuelEndurance: ([total,reserve,rate]) => ((total-reserve)/1000)/(rate/3600000)/3600,
  trenchVolume: ([l,w,d]) => (l*w)*d,
  looseVolume: ([v,k]) => v + v*(k-1),
  bucketOutput: ([v,fill,n]) => v*(fill/100)/(3600/n)*3600,
  cycleTime: v => v.reduce((sum,time)=>sum+time,0),
  truckTrips: ([v,c]) => Math.ceil(v/c),
  soilMass: ([v,rho]) => (rho*1000)*v/1000,
  groundPressure: ([w,a]) => (w*1000)/a/1000,
  gradePercent: ([h,l]) => Math.tan(Math.atan2(h,l))*100,
  travelDistance: ([v,t]) => (v/3.6)*(t*60)/1000,
  travelTime: ([s,v]) => s/(v/3.6)/60,
  loadMoment: ([m,r]) => (m*1000)*9.8*r/1000,
  mechanicalWork: ([f,s]) => (f*1000)*s/1000,
  averagePower: ([w,t]) => (w*1000)/t/1000,
  batteryEnergy: ([v,c]) => (v*(c*3600))/3600,
  electricalPower: ([v,a]) => v*a/1000,
  voltageDrop: ([a,r]) => a/(1/r),
};
function round(value:number) {
  return Math.round((value+Number.EPSILON*Math.max(1,Math.abs(value)))*100)/100;
}
const numeric = BASE_BANK.filter(q=>q.calculation);
describe('별도 SI 계산·해설·선택지 검증',()=>{
  it('반올림 경계와 정수 올림이 구분된다',()=>{
    expect(round(0.625)).toBe(0.63);
    expect(round(14.325)).toBe(14.33);
    expect(round(14.324)).toBe(14.32);
    expect(evaluate.truckTrips([91,6])).toBe(16);
    expect(evaluate.truckTrips([90,6])).toBe(15);
  });
  for (const q of numeric) it(`${q.id} ${q.calculation!.kind}`,()=>{
    const c=q.calculation!;
    const result=round(evaluate[c.kind](c.values));
    expect(result).toBe(c.result);
    const choices=q.choices.map(choice=>{
      const match=choice.match(/^([0-9]+(?:\.[0-9]+)?) (.+)$/);
      expect(match).not.toBeNull();
      expect(match![2]).toBe(c.unit);
      return Number(match![1]);
    });
    expect(new Set(choices).size).toBe(4);
    expect(choices.filter(v=>v===result)).toHaveLength(1);
    expect(choices[q.answer-1]).toBe(result);
    expect(q.explanation).toContain(q.choices[q.answer-1]);
    expect(q.question).toContain(c.kind==='truckTrips'?'올림한 정수':'소수 셋째 자리');
    expect(q.explanation).not.toMatch(/NaN|undefined|Infinity/);
    for(const value of c.values) expect(q.question).toContain(String(value));
    expect(q.reviewNote).toContain('계산 조건 변형');
    expect(q.year).toBeNull(); expect(q.session).toBeNull();
  });
  it('32유형마다 서로 다른 입력 29세트가 있다',()=>{
    expect(numeric).toHaveLength(928);
    expect(new Set(numeric.map(q=>q.family)).size).toBe(32);
    expect(new Set(numeric.map(q=>q.calculation!.kind))).toEqual(new Set(Object.keys(evaluate)));
    for(const kind of Object.keys(evaluate)) {
      const rows=numeric.filter(q=>q.calculation!.kind===kind);
      expect(rows).toHaveLength(29);
      expect(new Set(rows.map(q=>JSON.stringify(q.calculation!.values))).size).toBe(29);
      expect(new Set(rows.map(q=>q.question))).toHaveLength(29);
    }
  });
  it('60문항 시험은 숫자 변형 family를 최대 한 번만 사용한다',()=>{
    for(let i=0;i<20;i++) {
      const e=createExam(BASE_BANK,'main');
      const families=e.questions.flatMap(q=>q.family?[q.family]:[]);
      expect(new Set(families).size).toBe(families.length);
      expect(e.questions).toHaveLength(60);
    }
  });
});
