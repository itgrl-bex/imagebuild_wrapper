#!/usr/bin/python3

################################################################
##                                                            ##
## Script Name: image_build_init.py                           ##
## Author: Rebecca Robinson  <rerobinson@vmware.com>          ##
##                                                            ##
## This script is a sample wrapper script for image creation  ##
## for use standalone or within a pipeline.  Currently this   ##
## is built for a single TKG version to build.                ##
## Manual download and extraction of tkg bundle is required.  ##
##                                                            ##
################################################################

import optparse
import logging, sys
import os
import shutil
import subprocess

usage = """ %prog [options] arg1

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
"""

## Parse Options
parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", "--debug",
        action="store_true",
        dest="_DEBUG",
        default=False,
        help="Turn on debug messages")
parser.add_option("--bootstrap",
        action="store_true",
        dest="bootstrap",
        default=False,
        help="Install pre-requisites required to build images.")
parser.add_option("--imagetype",
        action="store",
        dest="imagetype",
        default='vsphere',
        help="Turn on debug messages")
parser.add_option("--versionstamp",
        action="store",
        dest="versionstamp",
        default="v1.22.9+vmware.1-myorg.0",
        help="Set the version stamp of the new image.")
parser.add_option("--tkgbundledir",
        action="store",
        dest="tkgbundledir",
        default='/home/builder/TKG-Image-Builder-for-Kubernetes-v1_22_9---vmware_1-tkg-v_1_5_4',
        help="Set the destination to store the new image.")
parser.add_option("--imagedir",
        action="store",
        dest="imageDir",
        default="/tmp/images",
        help="Set the destination to store the new image.")



vsphere_group = optparse.OptionGroup(parser, "vSphere Options",
        "These are the options for building vSphere images.")
vsphere_group.add_option("--vcenter",
        action="store",
        dest="vcenter",
        help="The vCenter server that you wish to connect to.")
vsphere_group.add_option("--cluster",
        action="store",
        dest="cluster",
        help="Sets the cluster in the target vCenter to use.")
vsphere_group.add_option("--no-template",
        action="store_false",
        dest="template",
        default=True,
        help="Do not convert the built virtual machine to a template when build is complete?")
vsphere_group.add_option("--template",
        action="store_true",
        dest="template",
        default=True,
        help="Convert the built virtual machine to a template when build is complete?")
vsphere_group.add_option("--datacenter",
        action="store",
        dest="datacenter",
        help="The datacenter to use in the target vCenter.")
vsphere_group.add_option("--datastore",
        action="store",
        dest="datastore",
        help="The datastore to use in the target vCenter.")
vsphere_group.add_option("--folder",
        action="store",
        dest="folder",
        help="The folder where you wish virtual machine to be built in the target vCenter.")
vsphere_group.add_option("--secure",
        action="store_false",
        dest="insecure",
        default=False,
        help="connect to vCenter securely")
vsphere_group.add_option("--insecure",
        action="store_true",
        dest="insecure",
        default=False,
        help="connect to vCenter insecurely")
vsphere_group.add_option("--network",
        action="store",
        dest="network",
        help="The network in the target vCenter that you wish to use. This network must have dhcp.")
vsphere_group.add_option("--resourcepool",
        action="store",
        dest="resourcepool",
        help="The vCenter resource pool to use.")
vsphere_group.add_option("--username",
        action="store",
        dest="username",
        help="The vCenter username that can connect and build VMs on the target vCenter.")
vsphere_group.add_option("--password",
        action="store",
        dest="password",
        help="The vCenter password for the user.")
parser.add_option_group(vsphere_group)

az_group = optparse.OptionGroup(parser, "Azure Options",
        "These are the options for building Azure images.")
az_group.add_option("--subscription",
        action="store",
        dest="subscription",
        help="Input the Azure Subscription ID")
az_group.add_option("--tenantid",
        action="store",
        dest="tenantid",
        help="Input the Azure Tenant ID")
az_group.add_option("--clientid",
        action="store",
        dest="clientid",
        help="Input the Azure client id with the capabilities needed")
az_group.add_option("--clientsecret",
        action="store",
        dest="clientsecret",
        help="Input the Azure client Secret")

parser.add_option_group(az_group)

(options, args) = parser.parse_args()

if options._DEBUG:
  logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
  logging.debug('Debug logging is enabled.')

if options.bootstrap:
  logging.info('Preparing user environment with pre-requisites required.')
  logging.info('Looking for OS package manager')
  is_yum = shutil.which("yum")
  is_apt = shutil.which("apt")
  if is_apt != None:
    logging.info('Using apt for os package management')    
    pkgmgr = 'apt'
    try:
        f = open('/tmp/docker.list', 'w')
        f.write("deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu   focal stable")
        f.close()
    except:
        raise RuntimeError("Unable to write /tmp/docker.list")
    getgpg = subprocess.Popen(('curl','-fsSL','https://download.docker.com/linux/ubuntu/gpg'), stdout=subprocess.PIPE)
    addgpg = subprocess.check_output(('sudo','gpg','--dearmor','-o','/etc/apt/keyrings/docker.gpg'), stdin=getgpg.stdout)
    cpaptlist = subprocess.run(['sudo','cp','/tmp/docker.list','/etc/apt/sources.list.d/docker.list'])
    print("Installing docker.list in /etc/apt/sources.list.d/ exited with exit code: %d" % cpaptlist.returncode)
    rmtmpaptlist = subprocess.run(['rm','--force','/tmp/docker.list'])
    aptupdate = subprocess.run(['sudo','apt','update'])
    print("apt update exited with code: %d" % aptupdate.returncode)
  elif is_yum != None:
    logging.info('Using yum for os package management')
    pkgmgr = 'yum'
  else:
    raise ValueError('Unsure of which package manager to use.  Please install docker manually.')
  logging.info('Checking for container runtime')
  has_dockerd = shutil.which("dockerd")
  if has_dockerd == None:
    logging.info('Installing docker-ce container runtime')
    install_docker = subprocess.run(['sudo',pkgmgr,'install','docker-ce','-y'])
    print("Docker-CE installation exit code was: %d" % install_docker.returncode)
  has_containerd = shutil.which("containerd")
  if has_containerd == None:
    logging.info('Installing containerd.io container runtime')
    install_containerd = subprocess.run(['sudo',pkgmgr,'install','containerd.io','-y'])
    print("Containerd.io installation exit code was: %d" % install_containerd.returncode)
  logging.info('Checking for docker cli')
  has_dockercli = shutil.which("docker")
  if has_dockercli == None:
    logging.info("Installing docker cli")
    install_dockercli = subprocess.run(['sudo',pkgmgr,'install','dockercli','-y'])
    print("dockercli installation exit code was: %d" % install_dockercli.returncode)
  if shutil.which("containerd") == None:
    logging.error("Install Failed: Failed to find containerd")
    raise RuntimeError('containerd.io is not installed')
  elif shutil.which("dockerd") == None:
    logging.error("Install Failed: Failed to find containerd")
    raise RuntimeError('dockerd is not installed')
  elif shutil.which("docker") == None:
    logging.error("Install Failed: Failed to find docker")
    raise RuntimeError('docker cli is not installed')
  else:
    logging.info("pre-requisites of docker-cli, docker-ce, and containerd.io are present on your system")
    addgroup = subprocess.run(['sudo','usermod','-a','-G','docker',os.getlogin()])
    print("User add to the docker group exited with exit code: %d" % addgroup.returncode)

  if options.tkgbundledir == None:
    raise ValueError("The tkgbundledir option is required but not specified")
  print('System is prepared to build images. Please logout and log back in to build images.')
  sys.exit()

## Functions
def stampversion():
  logging.debug("Version is: {}".format(options.versionstamp))
  logging.info('Writing version information:')
  versionfile = options.tkgbundledir + '/metadata.json'
  try:
    f = open(versionfile, 'w')
    f.write("{\n")
    f.write("  \"VERSION\": \"{}\"\n".format(options.versionstamp))
    f.write("}\n")
    f.close()
  except:
    raise RuntimeError("Unable to write file metadata.json")

def vspherejson():
  logging.debug("Creating or updating vsphere.json file with connection information.")
  logging.debug("Setting values:")
  logging.debug("\"cluster\": \"{}\"".format(options.cluster))
  if options.cluster == None:
    raise ValueError("The cluster option is required but not specified")
  logging.debug("\"convert_to_template\": \"{}\"".format(options.template))
  if options.template == None:
    raise ValueError("The template option is required but not specified")
  logging.debug("\"datacenter\": \"{}\"".format(options.datacenter))
  if options.datacenter == None:
    raise ValueError("The datacenter option is required but not specified")
  logging.debug("\"datastore\": \"{}\"".format(options.datastore))
  if options.datastore == None:
    raise ValueError("The datastore option is required but not specified")
  logging.debug("\"folder\": \"{}\"".format(options.folder))
  if options.folder == None:
    raise ValueError("The folder option is required but not specified")
  logging.debug("\"insecure_connection\": \"{}\"".format(options.insecure))
  if options.insecure == None:
    raise ValueError("The insecure option is required but not specified")
  logging.debug("\"network\": \"{}\"".format(options.network))
  if options.network == None:
    raise ValueError("The network option is required but not specified")
  logging.debug("\"password\": \"{}\"".format(options.password))
  if options.cluster == None:
    raise ValueError("The cluster option is required but not specified")
  logging.debug("\"resource_pool\": \"{}\"".format(options.resourcepool))
  if options.password == None:
    raise ValueError("The password option is required but not specified")
  logging.debug("\"username\": \"{}\"".format(options.username))
  if options.username == None:
    raise ValueError("The username option is required but not specified")
  logging.debug("\"vcenter_server\": \"{}\"".format(options.vcenter))
  if options.vcenter == None:
    raise ValueError("The vcenter option is required but not specified")
  logging.info("Writing {}/vsphere.json".format(options.tkgbundledir))

  vspherejsonfile = options.tkgbundledir + '/vsphere.json'
  try:
    f = open(vspherejsonfile, 'w')
    f.write("{\n")
    f.write("  \"cluster\": \"{}\",\n".format(options.cluster))
    f.write("  \"convert_to_template\": \"{}\",\n".format(options.template))
    f.write("  \"datacenter\": \"{}\",\n".format(options.datacenter))
    f.write("  \"datastore\": \"{}\",\n".format(options.datastore))
    f.write("  \"folder\": \"{}\",\n".format(options.folder))
    f.write("  \"insecure_connection\": \"{}\",\n".format(options.insecure))
    f.write("  \"network\": \"{}\",\n".format(options.network))
    f.write("  \"password\": \"{}\",\n".format(options.password))
    f.write("  \"resource_pool\": \"{}\",\n".format(options.resourcepool))
    f.write("  \"username\": \"{}\",\n".format(options.username))
    f.write("  \"vcenter_server\": \"{}\",\n".format(options.vcenter))
    f.write("  \"linked_clone\": \"true\",\n")
    f.write("  \"create_snapshot\": \"true\"\n")
    f.write("}\n")
    f.close()
  except:
    raise RuntimeError("Unable to write file {}".format(vspherejsonfile))

def azcreds():
  logging.debug("Creating or updating az-creds.env file with the supplied information.")
  logging.debug("AZURE_SUBSCRIPTION_ID={}".format(options.subscription))
  if options.subscription == None:
    raise ValueError("The subscription option is required but not specified")
  logging.debug("AZURE_TENANT_ID={}".format(options.tenantid))
  if options.tenantid == None:
    raise ValueError("The tenantid option is required but not specified")
  logging.debug("AZURE_CLIENT_ID={}".format(options.clientid))
  if options.clientid == None:
    raise ValueError("The clientid option is required but not specified")
  logging.debug("AZURE_CLIENT_SECRET={}".format(options.clientsecret))
  if options.clientsecret == None:
    raise ValueError("The clientsecret option is required but not specified")
  logging.info("Writing file {}/az-creds.env".format(options.tkgbundledir))
  azcredsfile = options.tkgbundledir + '/az-creds.env'
  try:
    f = open(azcredsfile, 'w')
    f.write("AZURE_SUBSCRIPTION_ID={}\n".format(options.subscription))
    f.write("AZURE_TENANT_ID={}\n".format(options.tenantid))
    f.write("AZURE_CLIENT_ID={}\n".format(options.clientid))
    f.write("AZURE_CLIENT_SECRET={}\n".format(options.clientsecret))
    f.close()
  except:
    raise RuntimeError("Unable to write {}".format(azcredsfile))

def buildvsphere():
  if options.imageDir == None:
    raise ValueError("The imageDir option is required but not specified")
  cmd = """/usr/bin/docker run -it --rm \
	-v $(pwd)/vsphere.json:/home/imagebuilder/vsphere.json \
	-v $(pwd)/tkg.json:/home/imagebuilder/tkg.json \
	-v $(pwd)/tkg:/home/imagebuilder/tkg \
	-v $(pwd)/goss/:/home/imagebuilder/goss/ \
	-v $(pwd)/metadata.json:/home/imagebuilder/metadata.json \
	-v $(pwd)/CUSTOMIZATIONS.json:/home/imagebuilder/CUSTOMIZATIONS.json \
	-v %s:/home/imagebuilder/output \
	--env PACKER_VAR_FILES="tkg.json vsphere.json CUSTOMIZATIONS.json" \
	--env OVF_CUSTOM_PROPERTIES=/home/imagebuilder/metadata.json \
	projects.registry.vmware.com/tkg/image-builder:v0.1.11_vmware.3 \
	%s
  """
  logging.debug("Executing the command")
  logging.debug(cmd % (str(options.imageDir),str(args[0])))
  logging.info("Building image %s and storing the image in %s" % (str(args[0]),str(options.imageDir)))
  try:
    build_vsphere = subprocess.Popen([cmd % (str(options.imageDir),str(args[0]))], cwd=options.tkgbundledir, shell=True)
    build_vsphere.wait()
  except:
    raise RuntimeError("Failed to build image")

def buildaz():
  cmd = """/usr/bin/docker run -it --rm \
    -v ~/.azure:/home/imagebuilder/.azure \
    -v $(pwd)/tkg.json:/home/imagebuilder/tkg.json \
    -v $(pwd)/tkg:/home/imagebuilder/tkg \
    -v $(pwd)/goss/:/home/imagebuilder/goss/goss.yaml \
    -v $(pwd)/CUSTOMIZATIONS.json:/home/imagebuilder/CUSTOMIZATIONS.json \
    --env PACKER_VAR_FILES="tkg.json CUSTOMIZATIONS.json" \
    --env-file $(pwd)/az-creds.env \
    projects.registry.vmware.com/tkg/image-builder:v0.1.11_vmware.3 \
	%s
  """
  logging.debug("Executing the command")
  logging.debug(cmd % (str(args[0])))
  logging.info("Building image %s" % (str(args[0])))
  try:
    az_build=Popen([cmd % (str(args[0]))], cwd=options.tkgbundledir, shell=True)
    az_build.wait()
  except:
    raise RuntimeError("Failed to build image")

### Code Execution
logging.debug("Checking for directory {}".format(options.tkgbundledir))
if not os.path.exists(options.tkgbundledir):
  logging.info("Cannot find bundle directory {}".format(options.tkgbundledir))
  logging.error("The TKG bundle must be downloaded and extracted and the tkgbundledir value updated to the correct path.")
  raise RuntimeError("The TKG bundle not found, please visit https://developer.vmware.com/samples?categories=Sample&keywords=tkg%20image%20builder&tags=&groups=&filters=&sort=&page= to download TKG image builder bundle.")
  sys.exit()

logging.debug("Checking for directory {}".format(options.imageDir))
if not os.path.exists(options.imageDir):
  try:
    os.makedirs(options.imageDir)
    logging.info("Created directory {}".format(options.imageDir))
  except:
    raise RuntimeError("Cannot create the image directory")

logging.info("Creating the version file.")
try:
  stampversion()
except:
  raise RuntimeError("Not all required parameters have been specified for the image type chosen.")
logging.info("Evaluating imagetype.")
# Check to see if we specified an image to build
if args[0] == None:
    raise ValueError("You must specify the image to build.")
    sys.exit()

if (options.imagetype.lower == 'vcenter' or options.imagetype == 'vsphere'):
  logging.info("Preparing to build vSphere image.")
  try:
    vspherejson()
  except:
    raise RuntimeError("Not all required parameters have been specified for the image type chosen.")
  try:
    buildvsphere()
  except ValueError:
    raise RuntimeError("Not all required parameters have been specified for the image type chosen.")
  except:
    raise RuntimeError("I failed to run")
elif options.imagetype == 'azure':
  logging.info("Preparing to build Azure image.")
  try:
    azcreds()
  except:
    raise RuntimeError("Not all required parameters have been specified for the image type chosen.")
  try:
    buildaz()
  except:
    raise RuntimeError("Not all required parameters have been specified for the image type chosen.") 
  
else:
  logging.error("Unknown imagetype {}".format(imagetype))
  sys.exit()

logging.info('The build has finished successfully')