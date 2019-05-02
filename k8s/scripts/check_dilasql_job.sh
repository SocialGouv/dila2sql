#!/bin/sh

DILA2SQL_JOB_STATUS=$(kubectl get job dila2sql)

# Check if dila2sql job exists
if [ ! "$DILA2SQL_JOB_STATUS" ]
then
    kubectl apply -f k8s/dila2sql/importer-dila2sql.yml
else
    kubectl delete job dila2sql
    kubectl apply -f k8s/dila2sql/importer-dila2sql.yml
fi
