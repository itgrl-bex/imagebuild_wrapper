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

- -h, --help            show this help message and exit
- -d, --debug           Turn on debug messages
- --bootstrap           Install pre-requisites required to build images.
- --imagetype=IMAGETYPE
                        Set the image type of the build.  i.e. vsphere or azure
- --versionstamp=VERSIONSTAMP
                        Set the version stamp of the new image.
- --tkgbundledir=TKGBUNDLEDIR
                        Set the destination of the downloaded TKG bundle from [here](https://developer.vmware.com/samples?categories=Sample&keywords=tkg%20image%20builder&tags=&groups=&filters=&sort=&page=)
- --imagedir=IMAGEDIR   Set the destination to store the new image.
- --shareddir=SHAREDDIR
                        Set the source of files that can be used to build the
                        new image.
- --customizations=CUSTOMIZATIONS
                        Set the full path to the CUSTOMIZATIONS.json file.

  vSphere Options:
    These are the options for building vSphere images.

  - --vcenter=VCENTER   The vCenter server that you wish to connect to.
  - --cluster=CLUSTER   Sets the cluster in the target vCenter to use.
  - --no-template       Do not convert the built virtual machine to a template
                        when build is complete?
  - --template          Convert the built virtual machine to a template when
                        build is complete? *Note: This template may not be usable to create clusters, instead use the exported ova.*
  - --datacenter=DATACENTER
                        The datacenter to use in the target vCenter.
  - --datastore=DATASTORE
                        The datastore to use in the target vCenter.
  - --folder=FOLDER     The folder where you wish virtual machine to be built
                        in the target vCenter.
  - --secure            connect to vCenter securely
  - --insecure          connect to vCenter insecurely
  - --network=NETWORK   The network in the target vCenter that you wish to
                        use. This network must have dhcp.
  - --resourcepool=RESOURCEPOOL
                        The vCenter resource pool to use.
  - --username=USERNAME
                        The vCenter username that can connect and build VMs on
                        the target vCenter.
  - --password=PASSWORD
                        The vCenter password for the user.

  Azure Options:
    These are the options for building Azure images.
  - --azlogin           Do `az login inside of the container when security restrictions prevent token reuse between machines.
  - --subscription=SUBSCRIPTION
                        Input the Azure Subscription ID
  - --tenantid=TENANTID
                        Input the Azure Tenant ID
  - --clientid=CLIENTID
                        Input the Azure client id with the capabilities needed
  - --clientsecret=CLIENTSECRET
                        Input the Azure client Secret
  - --resourcegroup=RESOURCEGROUP
                        Optional: The resource group for this build.
  - --storageaccount=STORAGEACCOUNT
                        Optional: The storage account for this build.
  - --azlocation=AZLOCATION
                        Optional: The Azure Location for this build.
  - --galleryname=GALLERYNAME
                        Optional: The Azure Image Gallery Name for this build.

## Image Builder options

Below you will find a list of current options that can be passed as the arg1 parameter to the script.  This will pass the option to the docker container to indicate which option to execute.

Helpers

- help                                 Display this help
- version                              Display version of image-builder

Builds

- build-ami-amazon-2                       Builds Amazon-2 Linux AMI
- build-ami-centos-7                       Builds CentOS 7 AMI
- build-ami-ubuntu-1804                    Builds Ubuntu 18.04 AMI
- build-ami-ubuntu-2004                    Builds Ubuntu 20.04 AMI
- build-ami-rockylinux-8                   Builds RockyLinux 8 AMI
- build-ami-flatcar                        Builds Flatcar
- build-ami-windows-2019                   Builds Windows Server 2019 AMI Packer config
- build-ami-windows-2004                   Builds Windows Server 2004 SAC AMI Packer config
- build-ami-all                            Builds all AMIs
- build-azure-sig-ubuntu-1804              Builds Ubuntu 18.04 Azure managed image in Shared Image Gallery
- build-azure-sig-ubuntu-2004              Builds Ubuntu 20.04 Azure managed image in Shared Image Gallery
- build-azure-sig-centos-7                 Builds CentOS 7 Azure managed image in Shared Image Gallery
- build-azure-sig-windows-2019             Builds Windows Server 2019 Azure managed image in Shared Image Gallery
- build-azure-sig-windows-2019-containerd  Builds Windows Server 2019 with containerd Azure managed image in Shared Image Gallery
- build-azure-sig-windows-2022-containerd  Builds Windows Server 2022 with containerd Azure managed image in Shared Image Gallery
- build-azure-sig-windows-2004             Builds Windows Server 2004 SAC Azure managed image in Shared Image Gallery
- build-azure-vhd-ubuntu-1804              Builds Ubuntu 18.04 VHD image for Azure
- build-azure-vhd-ubuntu-2004              Builds Ubuntu 20.04 VHD image for Azure
- build-azure-vhd-centos-7                 Builds CentOS 7 VHD image for Azure
- build-azure-vhd-windows-2019             Builds for Windows Server 2019
- build-azure-vhd-windows-2019-containerd  Builds for Windows Server 2019 with containerd
- build-azure-vhd-windows-2022-containerd  Builds for Windows Server 2022 with containerd
- build-azure-vhd-windows-2004             Builds for Windows Server 2004 SAC
- build-azure-sig-centos-7-gen2            Builds CentOS Gen2 managed image in Shared Image Gallery
- build-azure-sig-flatcar                  Builds Flatcar Azure managed image in Shared Image Gallery
- build-azure-sig-flatcar-gen2             Builds Flatcar Azure Gen2 managed image in Shared Image Gallery
- build-azure-sig-ubuntu-1804-gen2         Builds Ubuntu 18.04 Gen2 managed image in Shared Image Gallery
- build-azure-sig-ubuntu-2004-gen2         Builds Ubuntu 20.04 Gen2 managed image in Shared Image Gallery
- build-azure-vhds                         Builds all Azure VHDs
- build-azure-sigs                         Builds all Azure Shared Image Gallery images
- build-do-ubuntu-1804                     Builds Ubuntu 18.04 DigitalOcean Snapshot
- build-do-ubuntu-2004                     Builds Ubuntu 20.04 DigitalOcean Snapshot
- build-do-centos-7                        Builds Centos 7 DigitalOcean Snapshot
- build-do-all                             Builds all DigitalOcean Snapshot
- build-gce-ubuntu-1804                    Builds the GCE ubuntu-1804 image
- build-gce-ubuntu-2004                    Builds the GCE ubuntu-2004 image
- build-gce-all                            Builds all GCE image
- build-node-ova-local-centos-7            Builds CentOS 7 Node OVA w local hypervisor
- build-node-ova-local-flatcar             Builds Flatcar stable Node OVA w local hypervisor
- build-node-ova-local-photon-3            Builds Photon 3 Node OVA w local hypervisor
- build-node-ova-local-rhel-7              Builds RHEL 7 Node OVA w local hypervisor
- build-node-ova-local-rhel-8              Builds RHEL 8 Node OVA w local hypervisor
- build-node-ova-local-rockylinux-8        Builds RockyLinux 8 Node OVA w local hypervisor
- build-node-ova-local-ubuntu-1804         Builds Ubuntu 18.04 Node OVA w local hypervisor
- build-node-ova-local-ubuntu-2004         Builds Ubuntu 20.04 Node OVA w local hypervisor
- build-node-ova-local-windows-2019        Builds for Windows Server 2019 Node OVA w local hypervisor
- build-node-ova-local-windows-2004        Builds for Windows Server 2004 SAC Node OVA w local hypervisor
- build-node-ova-local-all                 Builds all Node OVAs w local hypervisor
- build-node-ova-vsphere-centos-7          Builds CentOS 7 Node OVA and template on vSphere
- build-node-ova-vsphere-flatcar           Builds Flatcar stable Node OVA and template on vSphere
- build-node-ova-vsphere-photon-3          Builds Photon 3 Node OVA and template on vSphere
- build-node-ova-vsphere-rhel-7            Builds RHEL 7 Node OVA and template on vSphere
- build-node-ova-vsphere-rhel-8            Builds RHEL 8 Node OVA and template on vSphere
- build-node-ova-vsphere-rockylinux-8      Builds RockyLinux 8 Node OVA and template on vSphere
- build-node-ova-vsphere-ubuntu-1804       Builds Ubuntu 18.04 Node OVA and template on vSphere
- build-node-ova-vsphere-ubuntu-2004       Builds Ubuntu 20.04 Node OVA and template on vSphere
- build-node-ova-vsphere-windows-2019      Builds for Windows Server 2019 and template on vSphere
- build-node-ova-vsphere-windows-2004      Builds for Windows Server 2004 SAC and template on vSphere
- build-node-ova-vsphere-windows-2022      Builds for Windows Server 2022 template on vSphere
- build-node-ova-vsphere-ubuntu-2004-efi   Builds Ubuntu 20.04 Node OVA and template on vSphere that EFI boots
- build-node-ova-vsphere-all               Builds all Node OVAs and templates on vSphere
- build-node-ova-vsphere-clone-centos-7    Builds CentOS 7 Node OVA and template on vSphere
- build-node-ova-vsphere-clone-photon-3    Builds Photon 3 Node OVA and template on vSphere
- build-node-ova-vsphere-clone-rhel-7      Builds RHEL 7 Node OVA and template on vSphere
- build-node-ova-vsphere-clone-rhel-8      Builds RHEL 8 Node OVA and template on vSphere
- build-node-ova-vsphere-clone-rockylinux-8  Builds RockyLinux 8 Node OVA and template on vSphere
- build-node-ova-vsphere-clone-ubuntu-1804   Builds Ubuntu 18.04 Node OVA and template on vSphere
- build-node-ova-vsphere-clone-ubuntu-2004   Builds Ubuntu 20.04 Node OVA and template on vSphere
- build-node-ova-vsphere-clone-all           Builds all Node OVAs and templates on vSphere
- build-node-ova-vsphere-base-centos-7       Builds base CentOS 7 Node OVA and template on vSphere
- build-node-ova-vsphere-base-photon-3  Builds base Photon 3 Node OVA and template on vSphere
- build-node-ova-vsphere-base-rhel-7   Builds base RHEL 7 Node OVA and template on vSphere
- build-node-ova-vsphere-base-rhel-8   Builds base RHEL 8 Node OVA and template on vSphere
- build-node-ova-vsphere-base-rockylinux-8  Builds base RockyLinux 8 Node OVA and template on vSphere
- build-node-ova-vsphere-base-ubuntu-1804  Builds base Ubuntu 18.04 Node OVA and template on vSphere
- build-node-ova-vsphere-base-ubuntu-2004  Builds base Ubuntu 20.04 Node OVA and template on vSphere
- build-node-ova-vsphere-base-all      Builds all base Node OVAs and templates on vSphere
- build-node-ova-local-vmx-photon-3    Builds Photon 3 Node OVA from VMX file w local hypervisor
- build-node-ova-local-vmx-centos-7    Builds Centos 7 Node OVA from VMX file w local hypervisor
- build-node-ova-local-vmx-rhel-7      Builds RHEL 7 Node OVA from VMX file w local hypervisor
- build-node-ova-local-vmx-rhel-8      Builds RHEL 8 Node OVA from VMX file w local hypervisor
- build-node-ova-local-vmx-rockylinux-8  Builds RockyLinux 8 Node OVA from VMX file w local hypervisor
- build-node-ova-local-vmx-ubuntu-1804  Builds Ubuntu 18.04 Node OVA from VMX file w local hypervisor
- build-node-ova-local-vmx-ubuntu-2004  Builds Ubuntu 20.04 Node OVA from VMX file w local hypervisor
- build-node-ova-local-base-photon-3   Builds Photon 3 Base Node OVA w local hypervisor
- build-node-ova-local-base-centos-7   Builds Centos 7 Base Node OVA w local hypervisor
- build-node-ova-local-base-rhel-7     Builds RHEL 7 Base Node OVA w local hypervisor
- build-node-ova-local-base-rhel-8     Builds RHEL 8 Base Node OVA w local hypervisor
- build-node-ova-local-base-rockylinux-8  Builds RockyLinux 8 Base Node OVA w local hypervisor
- build-node-ova-local-base-ubuntu-1804  Builds Ubuntu 18.04 Base Node OVA w local hypervisor
- build-node-ova-local-base-ubuntu-2004  Builds Ubuntu 20.04 Base Node OVA w local hypervisor
- build-qemu-flatcar                   Builds Flatcar QEMU image
- build-qemu-ubuntu-1804               Builds Ubuntu 18.04 QEMU image
- build-qemu-ubuntu-2004               Builds Ubuntu 20.04 QEMU image
- build-qemu-ubuntu-2004-efi           Builds Ubuntu 20.04 QEMU image that EFI boots
- build-qemu-centos-7                  Builds CentOS 7 QEMU image
- build-qemu-rhel-8                    Builds RHEL 8 QEMU image
- build-qemu-rockylinux-8              Builds Rocky 8 QEMU image
- build-qemu-all                       Builds all Qemu images
- build-raw-flatcar                    Builds Flatcar RAW image
- build-raw-ubuntu-1804                Builds Ubuntu 18.04 RAW image
- build-raw-ubuntu-2004                Builds Ubuntu 20.04 RAW image
- build-raw-ubuntu-2004-efi            Builds Ubuntu 20.04 RAW image that EFI boots
- build-raw-all                        Builds all RAW images
- build-oci-ubuntu-1804                Builds the OCI ubuntu-1804 image
- build-oci-ubuntu-2004                Builds the OCI ubuntu-2004 image
- build-oci-oracle-linux-8             Builds the OCI Oracle Linux 8.x image
- build-oci-all                        Builds all OCI image
- build-vbox-windows-2019              Builds for Windows Server 2019 Node VirtualBox w local hypervisor
- build-vbox-all                       Builds all Qemu images

Validate packer config

- validate-ami-amazon-2                Validates Amazon-2 Linux AMI Packer config
- validate-ami-centos-7                Validates CentOS 7 AMI Packer config
- validate-ami-rockylinux-8            Validates RockyLinux 8 AMI Packer config
- validate-ami-flatcar                 Validates Flatcar AMI Packer config
- validate-ami-ubuntu-1804             Validates Ubuntu 18.04 AMI Packer config
- validate-ami-ubuntu-2004             Validates Ubuntu 20.04 AMI Packer config
- validate-ami-windows-2019            Validates Windows Server 2019 AMI Packer config
- validate-ami-windows-2004            Validates Windows Server 2004 SAC AMI Packer config
- validate-ami-all                     Validates all AMIs Packer config
- validate-azure-sig-centos-7          Validates CentOS 7 Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-ubuntu-1804       Validates Ubuntu 18.04 Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-ubuntu-2004       Validates Ubuntu 20.04 Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-windows-2019      Validate Windows Server 2019 Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-windows-2019-containerd  Validate Windows Server 2019 with containerd Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-windows-2022-containerd  Validate Windows Server 2022 with containerd Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-windows-2004      Validate Windows Server 2004 SAC Azure managed image in Shared Image Gallery Packer config
- validate-azure-vhd-centos-7          Validates CentOS 7 VHD image Azure Packer config
- validate-azure-vhd-ubuntu-1804       Validates Ubuntu 18.04 VHD image Azure Packer config
- validate-azure-vhd-ubuntu-2004       Validates Ubuntu 20.04 VHD image Azure Packer config
- validate-azure-vhd-windows-2019      Validate Windows Server 2019 VHD image Azure Packer config
- validate-azure-vhd-windows-2019-containerd  Validate Windows Server 2019 VHD with containerd image Azure Packer config
- validate-azure-vhd-windows-2022-containerd  Validate Windows Server 2022 VHD with containerd image Azure Packer config
- validate-azure-vhd-windows-2004      Validate Windows Server 2004 SAC VHD image Azure Packer config
- validate-azure-sig-centos-7-gen2     Validates CentOS 7 Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-ubuntu-1804-gen2  Validates Ubuntu 18.04 Azure managed image in Shared Image Gallery Packer config
- validate-azure-sig-ubuntu-2004-gen2  Validates Ubuntu 20.04 Azure managed image in Shared Image Gallery Packer config
- validate-azure-all                   Validates all images for Azure Packer config
- validate-do-ubuntu-1804              Validates Ubuntu 18.04 DigitalOcean Snapshot Packer config
- validate-do-ubuntu-2004              Validates Ubuntu 20.04 DigitalOcean Snapshot Packer config
- validate-do-centos-7                 Validates Centos 7 DigitalOcean Snapshot Packer config
- validate-do-all                      Validates all DigitalOcean Snapshot Packer config
- validate-gce-ubuntu-1804             Validates Ubuntu 18.04 GCE Snapshot Packer config
- validate-gce-ubuntu-2004             Validates Ubuntu 20.04 GCE Snapshot Packer config
- validate-gce-all                     Validates all GCE Snapshot Packer config
- validate-node-ova-local-centos-7     Validates CentOS 7 Node OVA Packer config w local hypervisor
- validate-node-ova-local-flatcar      Validates Flatcar stable Node OVA Packer config w local hypervisor
- validate-node-ova-local-photon-3     Validates Photon 3 Node OVA Packer config w local hypervisor
- validate-node-ova-local-rhel-7       Validates RHEL 7 Node OVA Packer config w local hypervisor
- validate-node-ova-local-rhel-8       Validates RHEL 8 Node OVA Packer config w local hypervisor
- validate-node-ova-local-rockylinux-8  Validates RockyLinux 8 Node OVA Packer config w local hypervisor
- validate-node-ova-local-ubuntu-1804  Validates Ubuntu 18.04 Node OVA Packer config w local hypervisor
- validate-node-ova-local-ubuntu-2004  Validates Ubuntu 20.04 Node OVA Packer config w local hypervisor
- validate-node-ova-local-windows-2019  Validates Windows Server 2019 Node OVA Packer config w local hypervisor
- validate-node-ova-local-windows-2004  Validates Windows Server 2004 SAC Node OVA Packer config w local hypervisor
- validate-node-ova-local-windows-2022  Validates Windows Server 2022 Node OVA Packer config w local hypervisor
- validate-node-ova-local-all          Validates all Node OVAs Packer config w local hypervisor
- validate-node-ova-local-vmx-photon-3  Validates Photon 3 Node OVA from VMX file w local hypervisor
- validate-node-ova-local-vmx-centos-7  Validates Centos 7 Node OVA from VMX file w local hypervisor
- validate-node-ova-local-vmx-rhel-7   Validates RHEL 7 Node OVA from VMX file w local hypervisor
- validate-node-ova-local-vmx-rhel-8   Validates RHEL 8 Node OVA from VMX file w local hypervisor
- validate-node-ova-local-vmx-rockylinux-8  Validates RockyLinux 8 Node OVA from VMX file w local hypervisor
- validate-node-ova-local-vmx-ubuntu-1804  Validates Ubuntu 18.04 Node OVA from VMX file w local hypervisor
- validate-node-ova-local-vmx-ubuntu-2004  Validates Ubuntu 20.04 Node OVA from VMX file w local hypervisor
- validate-node-ova-local-base-photon-3  Validates Photon 3 Base Node OVA w local hypervisor
- validate-node-ova-local-base-centos-7  Validates Centos 7 Base Node OVA w local hypervisor
- validate-node-ova-local-base-rhel-7  Validates RHEL 7 Base Node OVA w local hypervisor
- validate-node-ova-local-base-rhel-8  Validates RHEL 8 Base Node OVA w local hypervisor
- validate-node-ova-local-base-rockylinux-8  Validates RockyLinux 8 Base Node OVA w local hypervisor
- validate-node-ova-local-base-ubuntu-1804  Validates Ubuntu 18.04 Base Node OVA w local hypervisor
- validate-node-ova-local-base-ubuntu-2004  Validates Ubuntu 20.04 Base Node OVA w local hypervisor
- validate-qemu-flatcar                Validates Flatcar QEMU image packer config
- validate-qemu-ubuntu-1804            Validates Ubuntu 18.04 QEMU image packer config
- validate-qemu-ubuntu-2004            Validates Ubuntu 20.04 QEMU image packer config
- validate-qemu-ubuntu-2004-efi        Validates Ubuntu 20.04 QEMU EFI image packer config
- validate-qemu-centos-7               Validates CentOS 7 QEMU image packer config
- validate-qemu-rhel-8                 Validates RHEL 8 QEMU image
- validate-qemu-rockylinux-8           Validates Rocky Linux 8 QEMU image packer config
- validate-qemu-all                    Validates all Qemu Packer config
- validate-raw-flatcar                 Validates Flatcar RAW image packer config
- validate-raw-ubuntu-1804             Validates Ubuntu 18.04 RAW image packer config
- validate-raw-ubuntu-2004             Validates Ubuntu 20.04 RAW image packer config
- validate-raw-ubuntu-2004-efi         Validates Ubuntu 20.04 RAW EFI image packer config
- validate-raw-all                     Validates all RAW Packer config
- validate-oci-ubuntu-1804             Validates the OCI ubuntu-1804 image packer config
- validate-oci-ubuntu-2004             Validates the OCI ubuntu-2004 image packer config
- validate-oci-oracle-linux-8          Validates the OCI Oracle Linux 8.x image packer config
- validate-oci-all                     Validates all OCI image packer config
- validate-vbox-windows-2019           Validates Windows Server 2019 Node VirtualBox Packer config w local hypervisor
- validate-vbox-all                    Validates all RAW Packer config
- validate-powervs-centos-8            Validates the PowerVS CentOS image packer config
- validate-powervs-all                 Validates all PowerVS Packer config
- validate-all                         Validates the Packer config for all build targets

Cleaning

- clean                                Removes all image output directories and packer image cache
- clean-ova                            Removes all ova image output directories (see NOTE at top of help)
- clean-qemu                           Removes all qemu image output directories (see NOTE at top of help)
- clean-raw                            Removes all raw image output directories (see NOTE at top of help)
- clean-vbox                           Removes all vbox image output directories (see NOTE at top of help)
- clean-packer-cache                   Removes the packer cache

Docker

- docker-build                         Build the docker image for controller-manager
- docker-push                          Push the docker image

Testing

- test-azure                           Run the tests for Azure builders

## Customization

Edit CUSTOMIZATIONS.yaml with the required changes leveraging [this doc](https://image-builder.sigs.k8s.io/capi/capi.html#customization) as a guide for available customizations.

You can use Ansible Roles, Tasks, and Playbooks to automate the customizations.

With the addition of the shared directory option `--shareddir` you can put your files, CUSTOMIZATIONS.json and Ansible roles for use within the image builder.
With the current version of imagebuilder container, the `custom_role_names` parameter is used instead of other parameters.

Sample CUSTOMIZATIONS.json contents when providing script options `--shareddir /home/user/shared` and `--customizations /home/user/shared/CUSTOMIZATIONS.json`

```
{
  "custom_role_names": "/home/imagebuilder/shared/ansible/roles/custom /home/imagebuilder/tkg",
  "extra_debs": "\"inetutils-traceroute\""
}
```

**Note:** *You must include the role `/home/imagebuilder/tkg` in your `custom_role_names` list.*

## License

This content in this repository is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE)
