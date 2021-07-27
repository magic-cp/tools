#!/usr/bin/env python3
import requests
import argparse
import io
import csv
from commons import build_url

CONTEST_LIST_URL = build_url('contest.list')

def main():
    (search_filter, verbose) = parse()
    if verbose:
        print(f'Searching for "{search_filter}"')
        print(f'Calling {CONTEST_LIST_URL} to get the list of all contests...')
    response = requests.get(CONTEST_LIST_URL).json()

    if response['status'] != 'OK':
        raise ValueError('Invalid response from CF API {response}')

    contests = response['result']

    if verbose:
        print(f'There is a total of {len(contests)} contests')

    finished_contests = list(filter(lambda x: x['phase'] == 'FINISHED', contests))

    if verbose:
        print(f'There is a total of {len(finished_contests)} finished contests')

    f = io.StringIO()
    writer = csv.DictWriter(f, fieldnames=['id', 'name'])
    writer.writeheader()
    for contest in finished_contests:
        contest_name = contest['name']
        contest_id = contest['id']
        if search_filter in contest_name:
            writer.writerow({'id': contest_id, 'name': contest_name})

    print(f.getvalue(), end='')
    f.close()

def parse() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('--search-filter', help='Search term to filter contests', type=str, required=False, default='')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    return (args.search_filter, args.verbose)

if __name__ == '__main__':
    main()
