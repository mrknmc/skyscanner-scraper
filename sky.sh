# #!/bin/sh

function sched {
    curl http://localhost:6800/schedule.json -d project=default -d spider=sky -d from=$1 -d to=$2 -d date=$3 -d rtn=$4
}

if [ -z "$1" ]
    then
    echo "No argument supplied."
else
    FROM=$( echo $1 | grep -E '^[A-Z]{3}$')
    if [ $1 = $FROM ]
        then
        if [ -z "$2" ]
            then
            echo "At least two arguments needed."
        else
            TO=$( echo $2 | grep -E '^[A-Z]{3}$')
            if [ $2 = $TO ]
                then
                if [ -n "$3" ]
                    then
                    DATE=$(echo $3 | grep -E '^[0-9]{4,6}')
                    if [ $3 = $DATE ]
                        then
                        if [ -n "$4" ]
                            then
                            RTN=$(echo $4 | grep -E '^[01]')
                        fi
                    fi
                fi
                sched $FROM $TO $DATE $RTN
            fi
        fi
    fi
fi