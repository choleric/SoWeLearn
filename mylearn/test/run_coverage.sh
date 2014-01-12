#!/bin/bash
basedir=$(dirname $0)
srcdir=${basedir}/../mylearn
MYLEARN_MODE=dev coverage run \
  --rcfile=${basedir}/coverage.ini \
  ${basedir}/../manage.py test ${srcdir}/apps && coverage report
