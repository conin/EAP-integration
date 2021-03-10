#!/bin/sh

echo '# Include the EAP machine configuration file in the machine config file
require ${WORKSPACE}/sources/meta-qti-eap/conf/machine/include/external-ap.inc
# Set target to 64-bit ARM, used to decide which binaries to copy
TARGET = "eap-imx64"
# Add CV2X feature flags and override to the machine:
MACHINEOVERRIDES =. "cv2x:"
# Force using u-boot-imx (needed due to some glitch in layer priorities)
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-imx"
BBMASK += "meta-qti-eap/recipes-core/systemd/systemd_%.bbappend"' >> imx8source/sources/meta-fsl-bsp-release/imx/meta-bsp/conf/machine/imx8qxpmek.conf


echo 'IMAGE_INSTALL += "packagegroup-telematics-utils"
IMAGE_INSTALL += "packagegroup-telematics-qti"
IMAGE_INSTALL_append_cv2x += "packagegroup-telematics-cv2x-qti"' >> imx8source/sources/poky/meta/recipes-core/images/core-image-minimal.bb


echo 'BBLAYERS += "${BSPDIR}/sources/meta-qti-eap "
BBLAYERS += "${BSPDIR}/sources/meta-qti-eap-prop "
BBLAYERS += "${BSPDIR}/sources/meta-openembedded/meta-python "
BBLAYERS += "${BSPDIR}/sources/meta-openembedded/meta-networking "
export WORKSPACE := "${COREBASE}/../.."' >> imx8source/sources/base/conf/bblayers.conf
