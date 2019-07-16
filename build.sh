#!/bin/bash

echo "Setup environment variables ..."
MACHINE=imx6ulevk
LINUX_IMAGE=core-image-base
DISTRO=fsl-imx-fb

export PROJECT_DIR=$(pwd)
export DEPLOY_DIR=$PROJECT_DIR/build/tmp/deploy/images/
export IMAGE_NAME=$LINUX_IMAGE-$MACHINE.sdcard.bz2

echo "$MACHINE"
echo "$LINUX_IMAGE"
echo "$DISTRO"
echo "$PROJECT_DIR"
echo "$DEPLOY_DIR"
echo "$IMAGE_NAME"

DISTRO=$DISTRO MACHINE=$MACHINE source fsl-setup-release.sh -b build/

bitbake $LINUX_IMAGE
