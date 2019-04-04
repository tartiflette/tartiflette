#!/bin/sh

cat /github/workflow/event.json | jq -e ". | select(.ref==\"$REF_NAME\")"

return_code=$?

if [ $return_code -ne 0 ]; then
   exit 78
fi

exit 0