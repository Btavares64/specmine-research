import argparse
from pathlib import Path
import pandas as pd

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data-dir',type=Path,default=Path('../specmine-official/data'))
    args=parser.parse_args()
    prs=pd.read_parquet(args.data_dir/'pull_requests.parquet')
    commits=pd.read_parquet(args.data_dir/'spec_file_commits.parquet')
    key=['repo_name','pr_number']
    prs=prs.drop_duplicates(key).copy() # arbitrary row selection affects window only if dates differ
    for col in ['created_at','merged_at']:
        prs[col]=pd.to_datetime(prs[col],utc=True,errors='coerce')
    commits['committed_at']=pd.to_datetime(commits['committed_at'],utc=True,errors='coerce')
    windows=prs.loc[prs.created_at.notna() & prs.merged_at.notna(),key+['created_at','merged_at']]
    candidates=windows.merge(commits[['repo_name','commit_sha','committed_at']],on='repo_name',how='inner')
    candidates=candidates.loc[candidates.committed_at.ge(candidates.created_at) & candidates.committed_at.le(candidates.merged_at)]
    count=len(candidates[key].drop_duplicates())
    out=Path('results');out.mkdir(exist_ok=True)
    pd.DataFrame([{'metric':'Unique PRs with repository-level timestamp-overlap candidate','count':count}]).to_csv(out/'timing_candidates.csv',index=False)
    print(f'PRs with same-repository spec commits inside PR window: {count}')
    print('WARNING: this is only a repository/time-window overlap. It DOES NOT establish commit membership in a PR, nor spec-before-code ordering.')

if __name__=='__main__':main()
