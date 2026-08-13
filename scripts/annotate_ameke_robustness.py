#!/usr/bin/env python3
import json
from pathlib import Path
from research_common import OUT,dump

TARGET_P=0.05

def main():
    detail=json.loads((OUT/'ameke_ugameke_robustness_controls.json').read_text(encoding='utf-8'))
    summary=json.loads((OUT/'ameke_ugameke_robustness_controls_summary.json').read_text(encoding='utf-8'))
    subs=[x for x in detail.get('provenance_subgroups',[]) if x.get('status')=='estimable']
    rows=[]
    for x in subs:
        ce=x['context_effect'];be=x['member_binary_effect']
        rows.append({'provenance':x['provenance'],'member_count':x['member_count'],'target_member_count':x['target_member_count'],
          'context_rate_difference':ce['observed']['rate_difference'],'context_empirical_two_sided_p':ce['empirical_two_sided_p'],
          'member_binary_rate_difference':be['observed']['rate_difference'],'member_binary_empirical_two_sided_p':be['empirical_two_sided_p'],
          'context_p_le_0_05':ce['empirical_two_sided_p']<=TARGET_P,'member_binary_p_le_0_05':be['empirical_two_sided_p']<=TARGET_P})
    all_context=bool(rows) and all(x['context_p_le_0_05'] for x in rows)
    all_binary=bool(rows) and all(x['member_binary_p_le_0_05'] for x in rows)
    summary['provenance_subgroup_diagnostics']=rows
    summary['estimable_provenance_subgroup_count']=len(rows)
    summary['provenance_subgroups_context_p_le_0_05_count']=sum(x['context_p_le_0_05'] for x in rows)
    summary['provenance_subgroups_member_binary_p_le_0_05_count']=sum(x['member_binary_p_le_0_05'] for x in rows)
    summary['replicated_context_signal_across_all_estimable_provenance_subgroups']=all_context
    summary['replicated_member_binary_signal_across_all_estimable_provenance_subgroups']=all_binary
    summary['provenance_sensitivity_flag']=not (all_context and all_binary)
    summary['provenance_interpretation']='Aggregate and stratified permutation robustness does not imply independent replication by provenance. If provenance_sensitivity_flag is true, the signal must be reported as provenance-sensitive rather than source-independent.'
    dump(OUT/'ameke_ugameke_robustness_controls_summary.json',summary)
    print(json.dumps({'provenance_sensitivity_flag':summary['provenance_sensitivity_flag'],'subgroups':rows},ensure_ascii=False))

if __name__=='__main__':main()
