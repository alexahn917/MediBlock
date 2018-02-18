#!/bin/sh
x=`lsof -Fp -i:5432`
kill -9 ${x##p}
pushd dev-env
./cloud_sql_proxy -instances="mediblock-195521:us-central1:mediblock-vm"=tcp:5432 -credential_file=mediblock-cred.json
popd
