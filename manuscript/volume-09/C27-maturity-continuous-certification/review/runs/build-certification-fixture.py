#!/usr/bin/env python3
"""Build deterministic C24 v2.7 causal-DAG certification fixtures."""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path

HERE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location('c24_v24_builder_runner',HERE/'run-certification-harness.py')
runner=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(runner)
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=True)
def sha(x): return 'sha256:'+hashlib.sha256(canon(x).encode()).hexdigest()
def seal(x,field='record_digest'):
    y=copy.deepcopy(x); y[field]=sha({k:v for k,v in y.items() if k!=field}); return y
def principal(pid,kind,roles,aliases=None): return seal({'principal_id':pid,'kind':kind,'status':'ACTIVE','roles':roles,'aliases':aliases or [],'valid_from':'2026-09-01T00:00:00Z','expires_at':'2026-12-31T00:00:00Z','record_digest':''})
def evidence(eid,kind,app,subject,obj,version,scope,owner,content,status='PASS',source='independent-synthetic-registry'):
    return seal({'evidence_id':eid,'kind':kind,'application_id':app,'subject_id':subject,'object_id':obj,'object_version':version,'scope':scope,'status':status,'source':source,'owner':owner,'issued_at':'2026-09-30T11:00:00Z','expires_at':'2026-10-30T00:00:00Z','content_digest':content,'record_digest':''})
def authority(aid,actor,action,stype,sid,obj,scope): return seal({'authority_id':aid,'actor':actor,'action':action,'subject_type':stype,'subject_id':sid,'object_digest':obj,'scope':scope,'status':'ACTIVE','issued_at':'2026-09-30T09:00:00Z','not_before':'2026-09-30T09:00:00Z','expires_at':'2026-10-30T00:00:00Z','record_digest':''})
def signature_payload(a):
    return {k:a[k] for k in ('subject_id','scope','release','task_id','platform','model','tools','data','budget','risk','environment','expires_at','exclusions')}
def change_payload(a,ch):
    return {'change_id':ch['change_id'],'application_id':ch['application_id'],'release':a['release'],'material':ch['material'],'kind':ch['kind'],'impact_review':ch['impact_review'],'retest':ch['retest'],'owner':ch['owner'],'issued_at':ch['issued_at'],'affected_scopes':ch['affected_scopes'],'post_change_release':ch['post_change_release'],'retest_trial_refs':ch['retest_trial_refs'],'retest_evidence_refs':ch['retest_evidence_refs'],'retest_review_ref':ch['retest_review_ref'],'retest_manifest':ch['retest_manifest']}
def lifecycle_payload(life):
    return {k:life[k] for k in ('event_id','certificate_id','previous','current','kind','occurred_at')}
def event(eid,app,kind,subject,when,sequence,predecessors):
    return seal({'event_id':eid,'application_id':app,'kind':kind,'subject_ref':subject,'occurred_at':when,'sequence':sequence,'predecessor_refs':predecessors,'record_digest':''})

def make_state(i,lifecycle='LIMITED'):
    suf=f'{i:03d}'; app=f'APP-{suf}'; subject=f'SUB-{suf}'; task=f'TASK-{suf}'; cert=f'CERT-{suf}'; scope='research-draft'; release='openclaw@eb377ac'
    ids={k:f'{k.upper()}-{suf}' for k in ('author','controller','certifier','reviewer','expert','appeal','custodian','lifeowner','changeowner','changeapprover','exceptionowner','orgowner')}
    ps={subject:principal(subject,'agent',['subject']),ids['author']:principal(ids['author'],'human',['author']),ids['controller']:principal(ids['controller'],'human',['controller']),ids['certifier']:principal(ids['certifier'],'human',['certifier']),ids['reviewer']:principal(ids['reviewer'],'human',['reviewer']),ids['expert']:principal(ids['expert'],'human',['domain_expert']),ids['appeal']:principal(ids['appeal'],'human',['appeal_reviewer']),ids['custodian']:principal(ids['custodian'],'human',['evidence_custodian']),ids['lifeowner']:principal(ids['lifeowner'],'human',['lifecycle_owner']),ids['changeowner']:principal(ids['changeowner'],'human',['change_owner']),ids['changeapprover']:principal(ids['changeapprover'],'human',['change_approver']),ids['exceptionowner']:principal(ids['exceptionowner'],'human',['conflict_exception_approver']),ids['orgowner']:principal(ids['orgowner'],'human',['organization_owner'])}
    application=seal({'application_id':app,'subject_id':subject,'subject_kind':'individual_agent','controller':ids['controller'],'author':ids['author'],'scope':scope,'release':release,'task_id':task,'platform':'openclaw','model':'provider/model@snapshot-202609','tools':['read_synthetic'],'data':'synthetic-v1','budget':100.0,'risk':'R2','environment':'isolated-copy','expires_at':'2026-10-30T00:00:00Z','exclusions':['external_send','payment','delete','production_change'],'requested_mat':'MAT-L2','requested_au':'AU-L1','requested_decision':'PASS','namespace_id':f'NS-{suf}','certificate_id':cert,'manifest_ref':f'EV-MANIFEST-{suf}','change_id':f'CHANGE-{suf}','appeal_id':f'APPEAL-{suf}','application_digest':''},'application_digest')
    auths={f'AUTH-ISSUE-{suf}':authority(f'AUTH-ISSUE-{suf}',ids['certifier'],'issue_synthetic_assessment','application',app,application['application_digest'],scope),f'AUTH-OPERATE-{suf}':authority(f'AUTH-OPERATE-{suf}',ids['controller'],'operate_synthetic_scope','application',app,application['application_digest'],scope),f'AUTH-APPEAL-{suf}':authority(f'AUTH-APPEAL-{suf}',ids['appeal'],'decide_appeal','appeal',f'APPEAL-{suf}',application['application_digest'],scope),f'AUTH-LIFE-{suf}':authority(f'AUTH-LIFE-{suf}',ids['lifeowner'],'change_certificate_lifecycle','certificate',cert,application['application_digest'],scope),f'AUTH-CHANGE-{suf}':authority(f'AUTH-CHANGE-{suf}',ids['changeapprover'],'approve_material_change','change',f'CHANGE-{suf}',application['application_digest'],scope)}
    ev={}
    def add(tag,kind,obj,ver,content,status='PASS',source='independent-synthetic-registry'):
        eid=f'EV-{tag}-{suf}'; ev[eid]=evidence(eid,kind,app,subject,obj,ver,scope,ids['custodian'],content,status,source); return eid
    signature=add('SIGN','application_signature',app,application['application_digest'],sha(signature_payload(application)))
    holdout=add('HOLDOUT','holdout_lineage',task,release,sha({'sealed':'holdout-v1','task':task,'release':release}),source='sealed-independent-holdout')
    grader=add('GRADER','grader_preregistration',task,release,sha({'grader':'blind-v1','task':task}),source='preregistered-blind-grader')
    trial_ids=[]
    trials={}
    for j,layer in enumerate(('training','regression','holdout'),1):
        tid=f'TRIAL-{suf}-{j}'; out=add(f'OUTPUT-{j}','trial_output',tid,release,sha({'trial':tid,'result':'completed'})); trial_ids.append(tid)
        trials[tid]=seal({'trial_id':tid,'application_id':app,'subject_id':subject,'task_id':task,'release':release,'layer':layer,'status':'COMPLETED','cost':float(j),'completed_at':f'2026-09-30T11:{10+j:02d}:00Z','output_ref':out,'holdout_ref':holdout,'grader_ref':grader,'record_digest':''})
        ev[out]['issued_at']=f'2026-09-30T11:{11+j:02d}:00Z'; ev[out]=seal(ev[out])
    failure=add('FAILURES','failure_archive',task,release,sha([])); cost=add('COST','cost_ledger',task,release,sha({'trial_count':3,'cost':6.0})); artifact=add('ARTIFACT','artifact',task,release,sha({'task':task,'release':release}))
    d21={face:add('D21-'+face.upper(),'d21_'+face,task,release,sha({'face':face,'task':task})) for face in ('technical','delivery','business_environment')}
    dimensions={}
    for d in ('quality','generalization','safety','stability','efficiency','collaboration','governability'):
        status='NOT_APPLICABLE' if d=='collaboration' else 'PASS'; ref=add('DIM-'+d.upper(),'dimension_'+d,app,application['application_digest'],sha({'dimension':d,'status':status}),status); dimensions[d]={'status':status,'evidence_ref':ref}
    change_ev=add('CHANGE','change_review',f'CHANGE-{suf}',release,sha('pending-change-review'))
    claim_text={'LIMITED':'synthetic limited assessment','ACTIVE':'synthetic active assessment','EXPIRED':'synthetic assessment expired','SUSPENDED':'synthetic assessment suspended','REVOKED':'synthetic assessment revoked'}[lifecycle]
    claim=add('CLAIM','public_claim',cert,application['application_digest'],sha(claim_text))
    life_ev=add('LIFE','lifecycle_event',cert,application['application_digest'],sha('pending-lifecycle-event'))
    manifest_id=f'EV-MANIFEST-{suf}'; ev[manifest_id]=evidence(manifest_id,'manifest',app,subject,app,application['application_digest'],scope,ids['custodian'],'PENDING')
    bundle=seal({'bundle_id':f'BUNDLE-{suf}','application_id':app,'manifest_ref':manifest_id,'artifact_ref':artifact,'signature_ref':signature,'holdout_ref':holdout,'grader_ref':grader,'failure_ref':failure,'cost_ref':cost,'trial_refs':trial_ids,'d21_refs':d21,'bundle_digest':''},'bundle_digest')
    ev[manifest_id]['content_digest']=sha({'trials':sorted(trials),'evidence':sorted(k for k in ev if k!=manifest_id)}); ev[manifest_id]=seal(ev[manifest_id])
    review=seal({'review_id':f'REVIEW-{suf}','application_id':app,'application_digest':application['application_digest'],'author':ids['author'],'controller':ids['controller'],'reviewer':ids['reviewer'],'domain_expert':ids['expert'],'conflicts_disclosed':True,'decision':'PASS','signature_ref':signature,'issued_at':'2026-09-30T11:30:00Z','record_digest':''})
    appeal=seal({'appeal_id':f'APPEAL-{suf}','application_id':app,'opened':False,'original_record_ref':review['review_id'],'reviewer':ids['appeal'],'authority_ref':f'AUTH-APPEAL-{suf}','decision':'NOT_OPENED','hard_gate_override':False,'issued_at':'2026-09-30T11:40:00Z','record_digest':''})
    maturity=seal({'maturity_id':f'MATURITY-{suf}','application_id':app,'requested':'MAT-L2','supported':'MAT-L2','prerequisites':['MAT-L0','MAT-L1'],'dimensions':dimensions,'organization_ref':'NONE','decision':'PASS','issued_at':'2026-09-30T11:25:00Z','expires_at':'2026-10-30T00:00:00Z','record_digest':''})
    namespace=seal({'namespace_id':f'NS-{suf}','application_id':app,'graduation':'COMPLETE','mat':'MAT-L2','au':'AU-L1','authorization_ref':f'AUTH-OPERATE-{suf}','certification_decision':'PASS','issued_at':'2026-09-30T11:26:00Z','expires_at':'2026-10-30T00:00:00Z','record_digest':''})
    empty_retest_manifest=seal({'manifest_id':'NONE','change_id':f'CHANGE-{suf}','pre_change_release':'NONE','post_change_release':'NONE','affected_scopes':[],'required_layers':[],'required_security_slices':[],'entries':[],'manifest_digest':''},'manifest_digest')
    change=seal({'change_id':f'CHANGE-{suf}','application_id':app,'material':False,'kind':'NONE','impact_review':'NOT_REQUIRED','retest':'NOT_REQUIRED','owner':ids['changeowner'],'authority_ref':f'AUTH-CHANGE-{suf}','evidence_ref':change_ev,'issued_at':'2026-09-30T11:20:00Z','affected_scopes':[],'post_change_release':'NONE','retest_trial_refs':[],'retest_evidence_refs':[],'retest_review_ref':'NONE','retest_manifest':empty_retest_manifest,'record_digest':''})
    ev[change_ev]['content_digest']=sha(change_payload(application,change)); ev[change_ev]=seal(ev[change_ev])
    issued='2026-09-30T11:00:00Z'; expires='2026-09-30T11:59:00Z' if lifecycle=='EXPIRED' else '2026-10-29T00:00:00Z'
    certificate=seal({'certificate_id':cert,'application_id':app,'application_digest':application['application_digest'],'subject_id':subject,'scope':scope,'release':release,'decision':'PASS','lifecycle':lifecycle,'issued_at':issued,'expires_at':expires,'public_claim':claim_text,'public_claim_ref':claim,'signer':ids['certifier'],'authority_ref':f'AUTH-ISSUE-{suf}','review_ref':review['review_id'],'maturity_digest':maturity['record_digest'],'namespace_digest':namespace['record_digest'],'bundle_digest':bundle['bundle_digest'],'real_certificate':False,'record_digest':''})
    kind={'LIMITED':'LIMIT','ACTIVE':'ACTIVATE','EXPIRED':'EXPIRE','SUSPENDED':'SUSPEND','REVOKED':'REVOKE'}[lifecycle]
    life=seal({'event_id':f'LIFE-{suf}','certificate_id':cert,'previous':'NONE','current':lifecycle,'kind':kind,'authority_ref':f'AUTH-LIFE-{suf}','evidence_ref':life_ev,'occurred_at':'2026-09-30T11:59:30Z' if lifecycle=='EXPIRED' else '2026-09-30T11:05:00Z','record_digest':''})

    # v2.6 assigns every consumed record to one frozen causal event.  The
    # pre-certificate manifest intentionally excludes claim/lifecycle evidence
    # so the review dependency graph remains acyclic.
    evidence_times={
        signature:'2026-09-30T09:10:00Z',holdout:'2026-09-30T09:20:00Z',grader:'2026-09-30T09:25:00Z',
        artifact:'2026-09-30T10:30:00Z',failure:'2026-09-30T10:31:00Z',cost:'2026-09-30T10:32:00Z',
        d21['technical']:'2026-09-30T10:33:00Z',d21['delivery']:'2026-09-30T10:34:00Z',d21['business_environment']:'2026-09-30T10:36:00Z',
        change_ev:'2026-09-30T10:46:00Z',manifest_id:'2026-09-30T10:47:00Z',claim:'2026-09-30T11:01:00Z',
        life_ev:'2026-09-30T11:59:40Z' if lifecycle=='EXPIRED' else '2026-09-30T11:06:00Z',
    }
    for index,dimension in enumerate(('quality','generalization','safety','stability','efficiency','collaboration','governability')):
        evidence_times[dimensions[dimension]['evidence_ref']]=f'2026-09-30T10:{37+index:02d}:00Z'
    trial_schedule=(('2026-09-30T10:00:00Z','2026-09-30T10:05:00Z','2026-09-30T10:06:00Z'),('2026-09-30T10:10:00Z','2026-09-30T10:15:00Z','2026-09-30T10:16:00Z'),('2026-09-30T10:20:00Z','2026-09-30T10:25:00Z','2026-09-30T10:26:00Z'))
    for trial,(started,completed,output_at) in zip(sorted(trials.values(),key=lambda x:x['trial_id']),trial_schedule):
        trial['completed_at']=completed; trial.update(seal(trial)); evidence_times[trial['output_ref']]=output_at
    for ref,when in evidence_times.items():
        ev[ref]['issued_at']=when; ev[ref]=seal(ev[ref])
    namespace['issued_at']='2026-09-30T09:30:00Z'; namespace=seal(namespace)
    maturity['issued_at']='2026-09-30T10:44:00Z'; maturity=seal(maturity)
    change['issued_at']='2026-09-30T10:45:00Z'; change=seal(change)
    ev[change_ev]['content_digest']=sha(change_payload(application,change)); ev[change_ev]=seal(ev[change_ev])
    pre_cert_refs=sorted(ref for ref,row in ev.items() if row['kind'] not in {'manifest','public_claim','lifecycle_event'})
    ev[manifest_id]['content_digest']=sha({'phase':'pre-certificate','trials':sorted(trials),'evidence':pre_cert_refs}); ev[manifest_id]=seal(ev[manifest_id])
    review['issued_at']='2026-09-30T10:50:00Z'; review=seal(review)
    appeal['issued_at']='2026-09-30T10:55:00Z'; appeal=seal(appeal)
    certificate['issued_at']=issued; certificate['namespace_digest']=namespace['record_digest']; certificate['maturity_digest']=maturity['record_digest']; certificate=seal(certificate)
    ev[life_ev]['content_digest']=sha(lifecycle_payload(life)); ev[life_ev]=seal(ev[life_ev])

    events={}; previous=[]; sequence=0
    def add_event(tag,event_kind,subject,when):
        nonlocal sequence,previous
        sequence+=1; eid=f'EVT-{tag}-{suf}'; events[eid]=event(eid,app,event_kind,subject,when,sequence,previous[-1:]); previous.append(eid)
    add_event('AUTHORITY','AUTHORITY_READY',app,'2026-09-30T09:00:30Z')
    add_event('SIGN','APPLICATION_SIGNED',signature,evidence_times[signature])
    add_event('MANIFEST-PREREG','MANIFEST_PREREGISTERED',manifest_id,'2026-09-30T09:15:00Z')
    add_event('HOLDOUT','HOLDOUT_FROZEN',holdout,evidence_times[holdout])
    add_event('GRADER','GRADER_PREREGISTERED',grader,evidence_times[grader])
    add_event('NAMESPACE','NAMESPACE_FROZEN',namespace['namespace_id'],namespace['issued_at'])
    for trial,(started,completed,output_at) in zip(sorted(trials.values(),key=lambda x:x['trial_id']),trial_schedule):
        add_event('INPUT-'+trial['trial_id'],'TRIAL_INPUT_ACCEPTED',trial['trial_id'],started)
        add_event('COMPLETE-'+trial['trial_id'],'TRIAL_COMPLETED',trial['trial_id'],completed)
        add_event('OUTPUT-'+trial['trial_id'],'TRIAL_OUTPUT_RECORDED',trial['output_ref'],output_at)
    add_event('ARTIFACT','ARTIFACT_RECORDED',artifact,evidence_times[artifact])
    add_event('FAILURES','FAILURE_ARCHIVED',failure,evidence_times[failure])
    add_event('COST','COST_RECORDED',cost,evidence_times[cost])
    add_event('D21-TECH','D21_TECHNICAL_RECORDED',d21['technical'],evidence_times[d21['technical']])
    add_event('D21-DELIVERY','D21_DELIVERY_RECORDED',d21['delivery'],evidence_times[d21['delivery']])
    add_event('ENVIRONMENT','ENVIRONMENT_OUTCOME_RECORDED',task,'2026-09-30T10:35:00Z')
    add_event('D21-BUSINESS','D21_BUSINESS_RECORDED',d21['business_environment'],evidence_times[d21['business_environment']])
    for dimension in ('quality','generalization','safety','stability','efficiency','collaboration','governability'):
        ref=dimensions[dimension]['evidence_ref']; add_event('DIM-'+dimension.upper(),'DIMENSION_RECORDED',ref,evidence_times[ref])
    add_event('MATURITY','MATURITY_RECORDED',maturity['maturity_id'],maturity['issued_at'])
    add_event('CHANGE','CHANGE_RECORDED',change['change_id'],change['issued_at'])
    add_event('CHANGE-EVIDENCE','CHANGE_EVIDENCE_RECORDED',change_ev,evidence_times[change_ev])
    add_event('MANIFEST-SEAL','MANIFEST_SEALED',manifest_id,evidence_times[manifest_id])
    add_event('REVIEW','REVIEW_RECORDED',review['review_id'],review['issued_at'])
    add_event('APPEAL','APPEAL_RECORDED',appeal['appeal_id'],appeal['issued_at'])
    add_event('CERT','CERTIFICATE_ISSUED',cert,certificate['issued_at'])
    add_event('CLAIM','PUBLIC_CLAIM_RECORDED',claim,evidence_times[claim])
    add_event('LIFECYCLE','LIFECYCLE_OCCURRED',life['event_id'],life['occurred_at'])
    add_event('LIFECYCLE-EVIDENCE','LIFECYCLE_EVIDENCE_RECORDED',life_ev,evidence_times[life_ev])
    return {'application':application,'principal_registry':ps,'authority_registry':auths,'event_registry':events,'role_conflict_exceptions':[],'review_registry':{review['review_id']:review},'appeal_registry':{appeal['appeal_id']:appeal},'evidence_registry':ev,'trial_registry':trials,'evidence_bundle':bundle,'maturity':maturity,'organization_registry':{},'namespace':namespace,'certificate_registry':{cert:certificate},'certificate_ref':cert,'lifecycle':life,'change':change,'effect_ledger':[]}

def reseal(state,path,field='record_digest'):
    obj=state
    for p in path: obj=obj[p]
    obj.update(seal(obj,field))

def mutate(s,name):
    a=s['application']; suf=a['application_id'].split('-')[-1]; issue=f'AUTH-ISSUE-{suf}'; op=f'AUTH-OPERATE-{suf}'; cert=a['certificate_id']; review=next(iter(s['review_registry'].values())); appeal=next(iter(s['appeal_registry'].values())); ev=s['evidence_registry']; b=s['evidence_bundle']; c=s['certificate_registry'][cert]
    if name=='unknown_authority_actor': s['authority_registry'][issue]['actor']='UNKNOWN'; reseal(s,['authority_registry',issue])
    elif name=='expired_authority': s['authority_registry'][issue]['expires_at']='2026-09-29T00:00:00Z'; reseal(s,['authority_registry',issue])
    elif name=='unbound_authority_digest': s['authority_registry'][issue]['object_digest']=sha('wrong'); reseal(s,['authority_registry',issue])
    elif name=='authority_subject_mismatch': s['authority_registry'][issue]['subject_id']='APP-WRONG'; reseal(s,['authority_registry',issue])
    elif name=='author_alias_as_reviewer': s['principal_registry'][a['author']]['aliases']=[review['reviewer']]; reseal(s,['principal_registry',a['author']])
    elif name=='author_as_domain_expert': review['domain_expert']=a['author']; reseal(s,['review_registry',review['review_id']])
    elif name=='appeal_record_not_preserved': appeal.update(opened=True,original_record_ref='NONE',decision='PASS'); reseal(s,['appeal_registry',appeal['appeal_id']])
    elif name=='unknown_appeal_reviewer': appeal.update(opened=True,reviewer='UNKNOWN',decision='PASS'); reseal(s,['appeal_registry',appeal['appeal_id']])
    elif name=='one_character_manifest_digest': ev[b['manifest_ref']]['record_digest']='sha256:x'
    elif name=='one_character_artifact_digest': ev[b['artifact_ref']]['record_digest']='sha256:y'
    elif name=='blank_holdout_lineage': ev[b['holdout_ref']]['source']=''
    elif name=='nan_trial_count': next(iter(s['trial_registry'].values()))['cost']=float('nan')
    elif name=='certificate_decision_fail_but_pass': c['decision']='FAIL'; reseal(s,['certificate_registry',cert])
    elif name=='namespace_decision_fail_but_pass': s['namespace']['certification_decision']='FAIL'; reseal(s,['namespace'])
    elif name=='missing_mat_prerequisites': s['maturity']['prerequisites']=[]; reseal(s,['maturity'])
    elif name=='safety_dimension_fail':
        row=s['maturity']['dimensions']['safety']; row['status']='FAIL'; ev[row['evidence_ref']]['status']='FAIL'; reseal(s,['evidence_registry',row['evidence_ref']]); reseal(s,['maturity'])
    elif name=='organization_without_roster': a['subject_kind']='multi_agent_organization'; a.update(seal(a,'application_digest'))
    elif name=='invalid_issued_at': c['issued_at']='not-a-time'
    elif name=='issued_after_expiry': c['issued_at']='2026-11-01T00:00:00Z'; reseal(s,['certificate_registry',cert])
    elif name=='unfixed_release': a['release']='openclaw@latest'; a.update(seal(a,'application_digest'))
    elif name=='invalid_risk_enum': a['risk']='R9'
    elif name=='nan_budget': a['budget']=float('nan')
    elif name=='invalid_change_kind': s['change']['kind']='SELF_MODIFY'
    elif name=='unsupported_public_claim': c['public_claim']='industry strongest certified'; ev[c['public_claim_ref']]['content_digest']=sha(c['public_claim']); reseal(s,['evidence_registry',c['public_claim_ref']]); reseal(s,['certificate_registry',cert])
    elif name=='unknown_authorization': s['namespace']['authorization_ref']='UNKNOWN'; reseal(s,['namespace'])
    elif name=='duplicate_trial_id':
        keys=list(s['trial_registry']); s['trial_registry'][keys[1]]['trial_id']=keys[0]
    elif name=='duplicate_evidence_id':
        keys=list(ev); ev[keys[1]]['evidence_id']=keys[0]
    elif name=='real_world_attempt': pass
    elif name=='real_certificate_attempt': c['real_certificate']=True; reseal(s,['certificate_registry',cert])
    elif name=='external_effect_attempt':
        view={'effect_id':f'EFFECT-{suf}','status':'APPLIED','external':True,'environment':'external'}
        s['effect_ledger']=[seal({'effect_id':f'EFFECT-{suf}','application_id':a['application_id'],'external':True,'status':'APPLIED','environment':'external','receipt':view,'receipt_digest':sha(view),'readback':view,'readback_digest':sha(view),'record_digest':''})]
    elif name=='valid_digest_wrong_manifest_content': ev[b['manifest_ref']]['content_digest']=sha('wrong manifest'); reseal(s,['evidence_registry',b['manifest_ref']])
    elif name=='signature_wrong_subject': ev[b['signature_ref']]['subject_id']='SUB-WRONG'; reseal(s,['evidence_registry',b['signature_ref']])
    elif name=='signature_wrong_scope': ev[b['signature_ref']]['scope']='other-scope'; reseal(s,['evidence_registry',b['signature_ref']])
    elif name=='signature_wrong_version': ev[b['signature_ref']]['object_version']=sha('wrong'); reseal(s,['evidence_registry',b['signature_ref']])
    elif name=='holdout_stale': ev[b['holdout_ref']]['expires_at']='2026-09-29T00:00:00Z'; reseal(s,['evidence_registry',b['holdout_ref']])
    elif name=='grader_leak': ev[b['grader_ref']]['owner']=a['author']; reseal(s,['evidence_registry',b['grader_ref']])
    elif name=='failure_deleted':
        t=next(iter(s['trial_registry'].values())); t['status']='FAILED'; reseal(s,['trial_registry',t['trial_id']])
    elif name=='cost_mismatch': ev[b['cost_ref']]['content_digest']=sha({'trial_count':3,'cost':999}); reseal(s,['evidence_registry',b['cost_ref']])
    elif name=='certificate_wrong_subject': c['subject_id']='SUB-WRONG'; reseal(s,['certificate_registry',cert])
    elif name=='certificate_wrong_release': c['release']='openclaw@wrong'; reseal(s,['certificate_registry',cert])
    elif name=='multi_certificate_conflict':
        x=copy.deepcopy(c); x['certificate_id']=f'CERT-SECOND-{suf}'; x=seal(x); s['certificate_registry'][x['certificate_id']]=x
    elif name=='suspended_still_public': c['lifecycle']='SUSPENDED'; reseal(s,['certificate_registry',cert]); s['lifecycle']['current']='SUSPENDED'; s['lifecycle']['kind']='SUSPEND'; reseal(s,['lifecycle'])
    elif name=='revoked_authorization': s['authority_registry'][op]['status']='REVOKED'; reseal(s,['authority_registry',op])
    elif name=='invalid_lifecycle_binding': s['lifecycle']['current']='ACTIVE'; reseal(s,['lifecycle'])
    elif name=='dimension_missing_evidence': s['maturity']['dimensions']['quality']['evidence_ref']='UNKNOWN'; reseal(s,['maturity'])
    elif name=='review_signature_missing': review['signature_ref']='UNKNOWN'; reseal(s,['review_registry',review['review_id']])
    elif name=='wrong_certificate_authority': c['authority_ref']=op; reseal(s,['certificate_registry',cert])
    elif name=='public_claim_evidence_fail': ev[c['public_claim_ref']]['status']='FAIL'; reseal(s,['evidence_registry',c['public_claim_ref']])
    elif name=='trial_unknown':
        t=next(iter(s['trial_registry'].values())); t['status']='UNKNOWN'; reseal(s,['trial_registry',t['trial_id']])
    elif name=='d21_unknown':
        ref=b['d21_refs']['delivery']; ev[ref]['status']='REVIEW_REQUIRED'; reseal(s,['evidence_registry',ref])
    elif name=='dimension_unknown':
        row=s['maturity']['dimensions']['quality']; row['status']='REVIEW_REQUIRED'; ev[row['evidence_ref']]['status']='REVIEW_REQUIRED'; reseal(s,['evidence_registry',row['evidence_ref']]); reseal(s,['maturity']); c['maturity_digest']=s['maturity']['record_digest']; reseal(s,['certificate_registry',cert])
    elif name=='material_change_unknown':
        trial_refs=sorted(s['trial_registry']); output_refs=[s['trial_registry'][x]['output_ref'] for x in trial_refs]
        s['change'].update(material=True,kind='MODEL',impact_review='REVIEW_REQUIRED',retest='REVIEW_REQUIRED',issued_at='2026-09-30T11:05:00Z',affected_scopes=['MODEL'],post_change_release=a['release'],retest_trial_refs=trial_refs,retest_evidence_refs=output_refs,retest_review_ref=review['review_id']); reseal(s,['change'])
        for ref in output_refs:
            ev[ref]['issued_at']='2026-09-30T11:20:00Z'; reseal(s,['evidence_registry',ref])
        ref=s['change']['evidence_ref']; ev[ref]['content_digest']=sha(change_payload(a,s['change'])); reseal(s,['evidence_registry',ref])
    elif name=='platform_independent_evidence': a['platform']='hermes'; a.update(seal(a,'application_digest'))
    elif name=='hard_plus_unknown':
        c['decision']='FAIL'; reseal(s,['certificate_registry',cert]); t=next(iter(s['trial_registry'].values())); t['status']='UNKNOWN'; reseal(s,['trial_registry',t['trial_id']])
    elif name=='valid_shortened_certificate_window':
        c['expires_at']='2026-10-15T00:00:00Z'; reseal(s,['certificate_registry',cert])
    return s

def scenario(i,name=None,lifecycle='LIMITED'):
    s=make_state(i,lifecycle); layer='representative_real_world' if name=='real_world_attempt' else 'holdout'
    if name: mutate(s,name)
    a=s['application']; trials=list(s['trial_registry']); evs=list(s['evidence_registry']); return {'scenario_id':f'S24-{i:03d}','application_id':a['application_id'],'subject_id':a['subject_id'],'task_id':a['task_id'],'trial_id':trials[0],'evidence_id':evs[0],'certificate_id':a['certificate_id'],'layer':layer,'security_slices':[] if not name else ['certification-redteam'],'state':s}

def state_scenario(i,state,security=True):
    a=state['application']; trials=list(state['trial_registry']); evs=list(state['evidence_registry'])
    return {'scenario_id':f'S24-{i:03d}','application_id':a['application_id'],'subject_id':a['subject_id'],'task_id':a['task_id'],'trial_id':trials[0],'evidence_id':evs[0],'certificate_id':a['certificate_id'],'layer':'holdout','security_slices':['certification-redteam'] if security else [],'state':state}

def add_positive_control_plan(state,control):
    """Bind a preregistered positive-control plan into the frozen state."""
    a=state['application']; suf=a['application_id'].split('-')[-1]; ev=state['evidence_registry']; bundle=state['evidence_bundle']
    custodian=next(pid for pid,row in state['principal_registry'].items() if 'evidence_custodian' in row['roles'])
    eid=f'EV-POSITIVE-PLAN-{suf}'
    ev[eid]=evidence(eid,'appeal_record',a['application_id'],a['subject_id'],control['control_id'],control['schema'],a['scope'],custodian,sha(control),source='preregistered-positive-control-plan')
    ev[eid]['issued_at']='2026-09-30T09:40:00Z'; ev[eid]=seal(ev[eid])
    manifest=ev[bundle['manifest_ref']]
    pre_cert_refs=sorted(ref for ref,row in ev.items() if row['kind'] not in {'manifest','public_claim','lifecycle_event'})
    manifest['content_digest']=sha({'phase':'pre-certificate','trials':sorted(state['trial_registry']),'evidence':pre_cert_refs}); ev[bundle['manifest_ref']]=seal(manifest)
    return eid

def make_renewal_positive(i):
    """Create a rooted current certificate plus a preregistered original-certificate renewal plan."""
    state=make_state(i,'ACTIVE'); a=state['application']; cert=state['certificate_registry'][state['certificate_ref']]
    review=next(iter(state['review_registry'].values())); issue=next(x for x in state['authority_registry'].values() if x['action']=='issue_synthetic_assessment')
    original_application=seal({'application_id':f'APP-ORIGINAL-{i:03d}','subject_id':a['subject_id'],'scope':a['scope'],'release':a['release'],'task_id':a['task_id'],'platform':a['platform'],'model':a['model'],'tools':a['tools'],'data':a['data'],'budget':a['budget'],'risk':a['risk'],'environment':a['environment'],'expires_at':'2026-10-01T00:00:00Z','issued_at':'2026-09-01T09:00:00Z','record_digest':''})
    original_authority=seal({'authority_id':f'AUTH-ISSUE-ORIGINAL-{i:03d}','actor':issue['actor'],'action':'issue_synthetic_assessment','subject_type':'application','subject_id':original_application['application_id'],'object_digest':original_application['record_digest'],'scope':a['scope'],'status':'ACTIVE','issued_at':'2026-09-01T09:05:00Z','not_before':'2026-09-01T09:05:00Z','expires_at':'2026-10-30T00:00:00Z','record_digest':''})
    original_bundle=seal({'bundle_id':f'BUNDLE-ORIGINAL-{i:03d}','application_id':original_application['application_id'],'issued_at':'2026-09-02T09:00:00Z','status':'PASS','record_digest':''})
    original_maturity=seal({'maturity_id':f'MATURITY-ORIGINAL-{i:03d}','application_id':original_application['application_id'],'supported':'MAT-L2','decision':'PASS','issued_at':'2026-09-02T09:10:00Z','record_digest':''})
    original_namespace=seal({'namespace_id':f'NS-ORIGINAL-{i:03d}','application_id':original_application['application_id'],'mat':'MAT-L2','au':'AU-L1','certification_decision':'PASS','issued_at':'2026-09-02T09:20:00Z','record_digest':''})
    original_review=seal({'review_id':f'REVIEW-ORIGINAL-{i:03d}','application_id':original_application['application_id'],'application_digest':original_application['record_digest'],'author':a['author'],'controller':a['controller'],'reviewer':review['reviewer'],'domain_expert':review['domain_expert'],'conflicts_disclosed':True,'decision':'PASS','signature_ref':state['evidence_bundle']['signature_ref'],'issued_at':'2026-09-02T12:00:00Z','record_digest':''})
    original_claim=seal({'evidence_id':f'EV-CLAIM-ORIGINAL-{i:03d}','certificate_id':f'CERT-ORIGINAL-{i:03d}','claim':'synthetic active assessment','status':'PASS','issued_at':'2026-09-03T00:01:00Z','record_digest':''})
    original_certificate=seal({'certificate_id':f'CERT-ORIGINAL-{i:03d}','application_id':original_application['application_id'],'application_digest':original_application['record_digest'],'subject_id':a['subject_id'],'scope':a['scope'],'release':a['release'],'decision':'PASS','lifecycle':'ACTIVE','issued_at':'2026-09-03T00:00:00Z','expires_at':'2026-10-01T00:00:00Z','public_claim':'synthetic active assessment','public_claim_ref':original_claim['evidence_id'],'signer':original_authority['actor'],'authority_ref':original_authority['authority_id'],'review_ref':original_review['review_id'],'maturity_digest':original_maturity['record_digest'],'namespace_digest':original_namespace['record_digest'],'bundle_digest':original_bundle['record_digest'],'real_certificate':False,'record_digest':''})
    control={'schema':'c24.cert.positive-control.v2.7','control_id':f'C24-POS-RENEWAL-{i:03d}','kind':'LEGAL_RENEWAL','application_id':a['application_id'],'subject_id':a['subject_id'],'scope':a['scope'],'release':a['release'],'original_application':original_application,'original_authority':original_authority,'original_bundle':original_bundle,'original_maturity':original_maturity,'original_namespace':original_namespace,'original_review':original_review,'original_public_claim':original_claim,'original_certificate':original_certificate,'renewal_request':{'requested_at':'2026-09-30T09:35:00Z','reason':'scheduled renewal before original expiry','previous_certificate_ref':original_certificate['certificate_id'],'current_certificate_ref':cert['certificate_id'],'independent_review_ref':review['review_id'],'issuance_authority_ref':issue['authority_id']},'lifecycle_order':[{'kind':'ORIGINAL_CERTIFICATE_ISSUED','occurred_at':original_certificate['issued_at']},{'kind':'RENEWAL_REQUESTED','occurred_at':'2026-09-30T09:35:00Z'},{'kind':'INDEPENDENT_REVIEW_RECORDED','occurred_at':review['issued_at']},{'kind':'RENEWED_CERTIFICATE_ISSUED','occurred_at':cert['issued_at']},{'kind':'RENEWED_CERTIFICATE_ACTIVATED','occurred_at':state['lifecycle']['occurred_at']},{'kind':'ORIGINAL_CERTIFICATE_EXPIRES','occurred_at':original_certificate['expires_at']}],'representative_real_world':{'status':'NOT_APPLICABLE','policy_authority_ref':'C24-D22-RECERT-v2.6','approval_authority_ref':issue['authority_id'],'reason':'offline synthetic control cannot claim representative real-world execution'}}
    add_positive_control_plan(state,control)
    return state,control

def rebuild_event_chain(state):
    """Rebuild the v2.6 frozen event chain after a legal material change."""
    a=state['application']; suf=a['application_id'].split('-')[-1]; ev=state['evidence_registry']; bundle=state['evidence_bundle']; ch=state['change']; cert=state['certificate_registry'][state['certificate_ref']]; life=state['lifecycle']; review=next(iter(state['review_registry'].values())); appeal=next(iter(state['appeal_registry'].values()))
    items=[]
    def add(tag,kind,subject,when): items.append((when,tag,kind,subject))
    add('AUTHORITY','AUTHORITY_READY',a['application_id'],'2026-09-30T09:00:30Z')
    add('SIGN','APPLICATION_SIGNED',bundle['signature_ref'],ev[bundle['signature_ref']]['issued_at'])
    add('MANIFEST-PREREG','MANIFEST_PREREGISTERED',bundle['manifest_ref'],'2026-09-30T09:15:00Z')
    add('HOLDOUT','HOLDOUT_FROZEN',bundle['holdout_ref'],ev[bundle['holdout_ref']]['issued_at'])
    add('GRADER','GRADER_PREREGISTERED',bundle['grader_ref'],ev[bundle['grader_ref']]['issued_at'])
    add('NAMESPACE','NAMESPACE_FROZEN',state['namespace']['namespace_id'],state['namespace']['issued_at'])
    add('CHANGE','CHANGE_RECORDED',ch['change_id'],ch['issued_at'])
    starts=['2026-09-30T10:00:00Z','2026-09-30T10:10:00Z','2026-09-30T10:20:00Z']
    ordered=sorted(state['trial_registry'].values(),key=lambda x:{'training':0,'regression':1,'holdout':2}[x['layer']])
    for trial,started in zip(ordered,starts):
        add('INPUT-'+trial['trial_id'],'TRIAL_INPUT_ACCEPTED',trial['trial_id'],started)
        add('COMPLETE-'+trial['trial_id'],'TRIAL_COMPLETED',trial['trial_id'],trial['completed_at'])
        add('OUTPUT-'+trial['trial_id'],'TRIAL_OUTPUT_RECORDED',trial['output_ref'],ev[trial['output_ref']]['issued_at'])
    for tag,kind,subject,when in (
        ('ARTIFACT','ARTIFACT_RECORDED',bundle['artifact_ref'],ev[bundle['artifact_ref']]['issued_at']),('FAILURES','FAILURE_ARCHIVED',bundle['failure_ref'],ev[bundle['failure_ref']]['issued_at']),('COST','COST_RECORDED',bundle['cost_ref'],ev[bundle['cost_ref']]['issued_at']),('D21-TECH','D21_TECHNICAL_RECORDED',bundle['d21_refs']['technical'],ev[bundle['d21_refs']['technical']]['issued_at']),('D21-DELIVERY','D21_DELIVERY_RECORDED',bundle['d21_refs']['delivery'],ev[bundle['d21_refs']['delivery']]['issued_at']),('ENVIRONMENT','ENVIRONMENT_OUTCOME_RECORDED',a['task_id'],'2026-09-30T10:35:00Z'),('D21-BUSINESS','D21_BUSINESS_RECORDED',bundle['d21_refs']['business_environment'],ev[bundle['d21_refs']['business_environment']]['issued_at'])): add(tag,kind,subject,when)
    for dimension,meta in state['maturity']['dimensions'].items(): add('DIM-'+dimension.upper(),'DIMENSION_RECORDED',meta['evidence_ref'],ev[meta['evidence_ref']]['issued_at'])
    add('MATURITY','MATURITY_RECORDED',state['maturity']['maturity_id'],state['maturity']['issued_at'])
    add('CHANGE-EVIDENCE','CHANGE_EVIDENCE_RECORDED',ch['evidence_ref'],ev[ch['evidence_ref']]['issued_at'])
    add('MANIFEST-SEAL','MANIFEST_SEALED',bundle['manifest_ref'],ev[bundle['manifest_ref']]['issued_at'])
    add('REVIEW','REVIEW_RECORDED',review['review_id'],review['issued_at']); add('APPEAL','APPEAL_RECORDED',appeal['appeal_id'],appeal['issued_at'])
    add('CERT','CERTIFICATE_ISSUED',cert['certificate_id'],cert['issued_at']); add('CLAIM','PUBLIC_CLAIM_RECORDED',cert['public_claim_ref'],ev[cert['public_claim_ref']]['issued_at'])
    add('LIFECYCLE','LIFECYCLE_OCCURRED',life['event_id'],life['occurred_at']); add('LIFECYCLE-EVIDENCE','LIFECYCLE_EVIDENCE_RECORDED',life['evidence_ref'],ev[life['evidence_ref']]['issued_at'])
    items.sort(); previous=[]; events={}
    for sequence,(when,tag,kind,subject) in enumerate(items,1):
        event_id=f'EVT-{tag}-{suf}'; events[event_id]=event(event_id,a['application_id'],kind,subject,when,sequence,previous[-1:]); previous.append(event_id)
    state['event_registry']=events

def make_material_recert_positive(i):
    state=make_state(i,'ACTIVE'); a=state['application']; ch=state['change']; ev=state['evidence_registry']; review=next(iter(state['review_registry'].values())); issue=next(x for x in state['authority_registry'].values() if x['action']=='issue_synthetic_assessment')
    entries=[]
    for trial in sorted(state['trial_registry'].values(),key=lambda x:{'training':0,'regression':1,'holdout':2}[x['layer']]):
        entries.append({'trial_ref':trial['trial_id'],'evidence_ref':trial['output_ref'],'layer':trial['layer'],'security_slices':['certification-redteam'],'affected_scopes':['MODEL']})
    manifest={'manifest_id':f'RETEST-{i:03d}','change_id':ch['change_id'],'pre_change_release':'openclaw@prechange-2026.9.5','post_change_release':a['release'],'affected_scopes':['MODEL'],'required_layers':['training','regression','holdout'],'required_security_slices':['certification-redteam'],'entries':entries,'manifest_digest':''}
    manifest['manifest_digest']=sha({k:v for k,v in manifest.items() if k!='manifest_digest'})
    ch.update(material=True,kind='MODEL',impact_review='PASS',retest='PASS',issued_at='2026-09-30T09:35:00Z',affected_scopes=['MODEL'],post_change_release=a['release'],retest_trial_refs=[x['trial_ref'] for x in entries],retest_evidence_refs=[x['evidence_ref'] for x in entries],retest_review_ref=review['review_id'],retest_manifest=manifest); state['change']=seal(ch)
    ev[state['change']['evidence_ref']]['content_digest']=sha(change_payload(a,state['change'])); ev[state['change']['evidence_ref']]=seal(ev[state['change']['evidence_ref']])
    control={'schema':'c24.cert.positive-control.v2.7','control_id':f'C24-POS-MATERIAL-RECERT-{i:03d}','kind':'LEGAL_MATERIAL_CHANGE_THREE_LAYER_RECERTIFICATION','application_id':a['application_id'],'subject_id':a['subject_id'],'scope':a['scope'],'pre_change_release':'openclaw@prechange-2026.9.5','post_change_release':a['release'],'change_ref':state['change']['change_id'],'required_layers':['training','regression','holdout'],'required_security_slices':['certification-redteam'],'trial_refs':[x['trial_ref'] for x in entries],'output_refs':[x['evidence_ref'] for x in entries],'independent_review_ref':review['review_id'],'issuance_authority_ref':issue['authority_id'],'representative_real_world':{'status':'NOT_APPLICABLE','policy_authority_ref':'C24-D22-RECERT-v2.6','approval_authority_ref':issue['authority_id'],'reason':'offline synthetic change control uses D22 training, regression and holdout only; real-world evidence is explicitly unclaimed'}}
    add_positive_control_plan(state,control); rebuild_event_chain(state)
    return state,control

def build_authority(scenarios,now):
    source={'schema':'c24.cert.input.v2.6','now':now,'environment':{'mode':'offline_synthetic','network':False,'real_credentials':False,'production_write':False,'may_issue_real_certificate':False,'external_effects_allowed':False},'authority_ref':{'bundle_id':'PENDING','root_digest':'sha256:'+'0'*64},'scenarios':scenarios}
    return runner.derive_authority(source,now)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',default=str(HERE/'synthetic-certification-input.yaml')); p.add_argument('--authority-output',default=str(HERE/'frozen-certification-authority.yaml')); p.add_argument('--positive-contract-output',default=str(HERE/'v2.7-positive-control-contracts.yaml')); z=p.parse_args()
    attacks=['unknown_authority_actor','expired_authority','unbound_authority_digest','authority_subject_mismatch','author_alias_as_reviewer','author_as_domain_expert','appeal_record_not_preserved','unknown_appeal_reviewer','one_character_manifest_digest','one_character_artifact_digest','blank_holdout_lineage','nan_trial_count','certificate_decision_fail_but_pass','namespace_decision_fail_but_pass','missing_mat_prerequisites','safety_dimension_fail','organization_without_roster','invalid_issued_at','issued_after_expiry','unfixed_release','invalid_risk_enum','nan_budget','invalid_change_kind','unsupported_public_claim','unknown_authorization','duplicate_trial_id','duplicate_evidence_id','real_world_attempt','real_certificate_attempt','external_effect_attempt','valid_digest_wrong_manifest_content','signature_wrong_subject','signature_wrong_scope','signature_wrong_version','holdout_stale','grader_leak','failure_deleted','cost_mismatch','certificate_wrong_subject','certificate_wrong_release','multi_certificate_conflict','suspended_still_public','revoked_authorization','invalid_lifecycle_binding','dimension_missing_evidence','review_signature_missing','wrong_certificate_authority','public_claim_evidence_fail','trial_unknown','d21_unknown','dimension_unknown','material_change_unknown','platform_independent_evidence','hard_plus_unknown','valid_shortened_certificate_window']
    scenarios=[scenario(1),scenario(2,lifecycle='ACTIVE'),scenario(3,lifecycle='EXPIRED')]
    scenarios += [scenario(i+4,name) for i,name in enumerate(attacks)]
    renewal_state,renewal_control=make_renewal_positive(59); recert_state,recert_control=make_material_recert_positive(60)
    scenarios += [state_scenario(59,renewal_state),state_scenario(60,recert_state)]
    now='2026-09-30T12:00:00Z'; authority_root=build_authority(scenarios,now)
    root={'schema':'c24.cert.input.v2.6','now':now,'environment':{'mode':'offline_synthetic','network':False,'real_credentials':False,'production_write':False,'may_issue_real_certificate':False,'external_effects_allowed':False},'authority_ref':{'bundle_id':authority_root['bundle_id'],'root_digest':authority_root['root_digest']},'scenarios':scenarios}
    Path(z.output).write_text(json.dumps(root,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=True)+'\n')
    Path(z.authority_output).write_text(json.dumps(authority_root,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    controls={'schema':'c24.cert.positive-controls.v2.7','scope':'offline_synthetic_only','controls':[renewal_control,recert_control],'limits':{'representative_real_world_executed':False,'real_certificate_issued':False,'external_effects_executed':False,'author_self_approval':False}}
    Path(z.positive_contract_output).write_text(json.dumps(controls,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(authority_root['root_digest'])
if __name__=='__main__': main()
