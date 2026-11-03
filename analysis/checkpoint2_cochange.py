import argparse
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=Path, default=Path('../specmine-official/data'))
    args = parser.parse_args()
    prs = pd.read_parquet(args.data_dir / 'pull_requests.parquet')
    key = ['repo_name', 'pr_number']
    prs['cochange'] = prs['n_spec_files'].gt(0) & prs['n_code_files'].gt(0)
    unique = prs.groupby(key, dropna=False).agg(cochange=('cochange','any'), tools=('tool','nunique')).reset_index()
    summary = pd.DataFrame([
        {'metric':'Original PR rows','count':len(prs)},
        {'metric':'Unique PR keys','count':len(unique)},
        {'metric':'Extra records beyond unique PR keys','count':len(prs)-len(unique)},
        {'metric':'Unique PRs co-changing spec and code','count':int(unique.cochange.sum())},
        {'metric':'Unique PRs associated with multiple tools','count':int(unique.tools.gt(1).sum())},
        {'metric':'Fully identical PR rows','count':int(prs.drop(columns='cochange').duplicated().sum())},
    ])
    out=Path('results'); out.mkdir(exist_ok=True)
    summary.to_csv(out/'cochange_summary.csv', index=False)
    print(summary.to_string(index=False))
    print(f"Co-change rate: {unique.cochange.mean():.2%}")
    print('Note: multiple tool associations are counted once per repo/PR; tool-specific records remain in source data.')

if __name__ == '__main__': main()
