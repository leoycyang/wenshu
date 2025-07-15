#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Error: please provide a file path to store the new database"
    exit 1
fi
if [ -f "$1" ]; then
    echo "Error: '$1' already exists"
    exit 1
fi
touch "$1"
dbpath=$(realpath "$1")

curpath=`realpath .`
mypath=`realpath "$0"`
mybase=`dirname "$mypath"`
cd $mybase

create table schema:
sqlite3 "$dbpath" < create.sql
columns=(source_url case_id case_title court location case_type case_type_code source procedure ruling_date publication_date parties cause_of_action legal_basis full_text)

# load data:
for csvfile in data_raw/2018年裁判文书数据_马克数据网/2018年01*.csv; do
    echo "loading $csvfile..."
    cat <<EOF | sqlite3 "$dbpath"
.mode csv
.import -v --csv --skip 1 $csvfile wenshu
.mode list
SELECT 'INFO: rows loaded: ' || CAST(TOTAL_CHANGES() AS TEXT);
EOF
    # go through each column and check how many values are empty:
    for column in "${columns[@]}"; do
        cat <<EOF | sqlite3 "$dbpath"
UPDATE wenshu SET $column = NULL WHERE $column = '';
SELECT 'WARNING: NULLs in $column: ' || CAST(CHANGES() AS TEXT);
EOF
    done
done

csvfile=data_raw/guiding_cases.csv
echo "loading $csvfile..."
cat <<EOF | sqlite3 "$dbpath"
.mode csv
.import -v --csv --skip 1 $csvfile guiding_cases
.mode list
SELECT 'INFO: rows loaded: ' || CAST(TOTAL_CHANGES() AS TEXT);
EOF
