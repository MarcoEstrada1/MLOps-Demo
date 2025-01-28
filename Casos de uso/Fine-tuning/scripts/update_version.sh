#!/bin/bash
# Incrementar la versión automáticamente
set -e

VERSION_FILE="VERSION"
if [ ! -f $VERSION_FILE ]; then
  echo "v2" > $VERSION_FILE
else
  CURRENT_VERSION=$(cat $VERSION_FILE)
  NEXT_VERSION="v$(( ${CURRENT_VERSION#v} + 1 ))"
  echo $NEXT_VERSION > $VERSION_FILE
fi

echo "Nueva versión: $(cat $VERSION_FILE)"
