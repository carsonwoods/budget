import os
import argparse
import json
import pandas

def parse_arguments():
    """
    Parse the arguments given on the command line.
    """

    parser = argparse.ArgumentParser(prog='Runtime Environment Capture')

    # general flags
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 0.1',
                        help='print version of Budget')

    parser.add_argument('-d', '--directory',
                        action='store_true',
                        help='treats file path as directory.'
                             'will parse multiple csv_files')

    parser.add_argument('file',
                        nargs='*',
                        action='store',
                        help='path to transaction file')

    arguments = parser.parse_args()

    # check for valid input
    if not arguments.file:
        parser.print_help()
        exit()

    return arguments


if __name__ == '__main__':

    arguments = parse_arguments()

    budget = dict()

    month = arguments.file[0].split('/')[1].split('_')[0]
    df = pandas.read_csv(arguments.file[0])

    categories_list = list(df.Category.unique())
    categories_list.remove('Payment')

    budget[month] = dict()
    budget[month]['total_spent'] = 0
    budget[month]['categories'] = dict()

    for category in categories_list:
        temp = dict()
        c_df = df.loc[df['Category'] == category]
        temp['total'] = round(c_df['Amount (USD)'].sum(), 2)
        #temp['df'] = c_df
        budget[month]['categories'][category] = temp
        budget[month]['total_spent'] += temp['total']

    budget[month]['total_spent'] = round(budget[month]['total_spent'], 2)

print(json.dumps(budget[month], indent=4))
