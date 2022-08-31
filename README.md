# imagebuild_wrapper

## Overview

This repository provides tooling to assist with Tanzu Kubernetes Grid node image creation. The tooling currently provides options to be able to generate required files for vSphere and Azure images and create them using the [image builder](https://docs.vmware.com/en/VMware-Tanzu-Kubernetes-Grid/1.5/vmware-tanzu-kubernetes-grid-15/GUID-build-images-index.html).

## Setup
To setup the workstation to be able to build images, run the script with the --bootstrap option. This will install the required Docker components and add the user running the script to the docker group. After this happens, you will need to log out and back on.

Additionally, you will need to visit the VMware developer portal and download the TKG bundle for the version of Tanzu Kubernetes Grid that you wish to build.  To do so, visit this website in your browser
https://developer.vmware.com/samples?categories=Sample&keywords=tkg%20image%20builder&tags=&groups=&filters=&sort=&page= 
Download the bundle and extract it to a location that this user has read/write access to, such as your home directory.
This full path will be the option --tkgbundledir when running the script.

## Requirements
  
- Docker cli, Docker CE, and Containerd are required for the imagebuild container to run.
- You will need network connectivity and proper access levels to the environment that you wish to build images for.
- You will need to have environment details that can be provided to the tooling to be able to access and build the images.
- For customization, you will need a basic understanding of Ansible.

## Usage

Usage:  image_build_init.py [options] arg1

The image_build_init.py script, is designed to assist in creation of Azure and vSphere node images. Please note,
this is not for creating container images, but rather the Tanzu Kubernetes Grid cluster node custom images.

It can be easily expanded to include additional image types and include the required
parameters for those image types.  The idea behind this script was an easy to use wrapper with the ability to pass
and validate that the required parameters are set for the image type. Currently this script will only build one image
type at a time, so it would need to be ran twice to build both vSphere and Azure. This was designed this way since often
the build will be done via a pipeline and usually each pipeline has a single focus.

Setup:
To setup the workstation to be able to build images, run the script with the --bootstrap option. This will install the required
Docker components and add the user running the script to the docker group. After this happens, you will need to log out and back on.

Additionally, you will need to visit the VMware developer portal and download the TKG bundle for the version of Tanzu Kubernetes Grid
that you wish to build.  To do so, visit this website in your browser
https://developer.vmware.com/samples?categories=Sample&keywords=tkg%20image%20builder&tags=&groups=&filters=&sort=&page=

Download the bundle and extract it to a location that this user has read/write access to, such as your home directory.
This full path will be the option --tkgbundledir when running the script.


Options:
  -h, --help            show this help message and exit
  -d, --debug           Turn on debug messages
  --bootstrap           Install pre-requisites required to build images.
  --imagetype=IMAGETYPE
                        Turn on debug messages
  --versionstamp=VERSIONSTAMP
                        Set the version stamp of the new image.
  --tkgbundledir=TKGBUNDLEDIR
                        Set the destination to store the new image.
  --imagedir=IMAGEDIR   Set the destination to store the new image.

  vSphere Options:
    These are the options for building vSphere images.

    --vcenter=VCENTER   The vCenter server that you wish to connect to.
    --cluster=CLUSTER   Sets the cluster in the target vCenter to use.
    --no-template       Do not convert the built virtual machine to a template
                        when build is complete?
    --template          Convert the built virtual machine to a template when
                        build is complete?
    --datacenter=DATACENTER
                        The datacenter to use in the target vCenter.
    --datastore=DATASTORE
                        The datastore to use in the target vCenter.
    --folder=FOLDER     The folder where you wish virtual machine to be built
                        in the target vCenter.
    --secure            connect to vCenter securely
    --insecure          connect to vCenter insecurely
    --network=NETWORK   The network in the target vCenter that you wish to
                        use. This network must have dhcp.
    --resourcepool=RESOURCEPOOL
                        The vCenter resource pool to use.
    --username=USERNAME
                        The vCenter username that can connect and build VMs on
                        the target vCenter.
    --password=PASSWORD
                        The vCenter password for the user.

  Azure Options:
    These are the options for building Azure images.

    --subscription=SUBSCRIPTION
                        Input the Azure Subscription ID
    --tenantid=TENANTID
                        Input the Azure Tenant ID
    --clientid=CLIENTID
                        Input the Azure client id with the capabilities needed
    --clientsecret=CLIENTSECRET
                        Input the Azure client Secret

## License

This content in this repository is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International Public License](LICENSE-CC-Attribution-ShareAlike4.0)