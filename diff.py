# -*- coding: utf-8 -*-
import click
import os
import csv


HASH_CHARACTER = '#'
IGNORED_KEYS = (
    'Reward',
    'Contrepartie',
    'Quanity',
    'Quantité',
    'Payment method'
    'Type de paiement',
    'Language',
    'Langue',
)


@click.command()
@click.option('--src', help='Source file path')
@click.option('--dst', help='Destination file path')
@click.option('--output', help='Output file')
def diff(src, dst, output=None):
    if not os.path.exists(src):
        raise Exception('Source file {} does not exists'.format(src))

    if not os.path.exists(dst):
        raise Exception('Destination file {} does not exists'.format(dst))

    filename, ext = os.path.splitext(src)
    if ext != '.csv':
        raise Exception('Source file {} should be in CSV'.format(src))

    filename, ext = os.path.splitext(dst)
    if ext != '.csv':
        raise Exception('Source file {} should be in CSV'.format(dst))

    if output is not None:
        filename, ext = os.path.splitext(output)
        if ext != '.csv':
            raise Exception('Output file {} should be in CSV'.format(output))

    with open(src) as src_csvfile:
        reader = csv.DictReader(src_csvfile)

        # Map<Int, Dict>
        src_diff = dict((row[HASH_CHARACTER], row) for row in reader)

    diff_rows = {}

    with open(dst) as dst_csvfile:
        reader = csv.DictReader(dst_csvfile)

        for row in reader:
            identifier = row[HASH_CHARACTER]

            # if identifier is not in the source file
            if identifier not in src_diff:
                print('Order {} is not in source file'.format(identifier))

                diff_rows[identifier] = row
                continue

            current = src_diff[identifier]

            for key, value in row.items():
                if key in IGNORED_KEYS:
                    break

                if current[key] != value:
                    print('Value for "{}" is different from source file: {} != {}'.format(key, current[key] or '(empty)', value))
                    diff_rows[identifier] = row
                    break

    if diff_rows:
        if output is not None:
            print('Exporting diff to {}'.format(output))

            with open(output, 'w') as csvfile:
                fieldnames = diff_rows[diff_rows.keys()[0]].keys()

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in diff_rows.values():
                    writer.writerow(row)
    else:
        print('No diff has been found between {} and {}'.format(src, dst))


# python diff.py --src=path/to/file.csv --dst=path/to/file.csv --output=path/to/output.csv
# `src` should be the oldest file
# `dst` should be the newest file
if __name__ == '__main__':
    diff()
