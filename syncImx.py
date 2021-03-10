# -*- coding: utf-8 -*-
import re
import sys
import os

imx8_source="repo init -u https://source.codeaurora.org/external/imx/imx-manifest -b imx-linux-sumo -m imx-4.14.98-2.0.0_ga.xml"
sync_cmd="repo sync --no-tags -c -q -j11"

caf_cmd="repo init -u https://source.codeaurora.org/quic/le/le/manifest.git -b release -m "
delete_dir=["poky","meta-openembedded","meta-freescale"]
cur_dir=os.getcwd()

file_list=["imx8source/sources/base/conf/bblayers.conf"]

code_base=['BBLAYERS += "${BSPDIR}/sources/meta-qti-eap " BBLAYERS += "${BSPDIR}/sources/meta-qti-eap-prop " BBLAYERS += "${BSPDIR}/sources/meta-openembedded/meta-python " BBLAYERS += "${BSPDIR}/sources/meta-openembedded/meta-networking " export WORKSPACE := "${COREBASE}/../.."']


##this functions check if directory/file is present or not
##if not present then then it will skips
##otherwise it will delete the file/directory
def check_dir_file(file_name,file_type):
	list_dir=os.listdir(os.getcwd())
	for x in list_dir:
		if x==file_name:
			os.system("rm -rf "+x)

##This function deletes the existing imx8source directory and sync the CAF code.
def create_imx_source():
	check_dir_file("imx8source","d")
       	path = os.path.join(os.getcwd()+"/","imx8source")
       	os.mkdir(path)
       	os.chdir("imx8source")
	os.system(imx8_source)
       	os.system(sync_cmd)
	os.chdir(cur_dir)
	os.system("cp -Rf sa415m-le-1-7_amss_standard_oem_imx/SA415M_apps_fsl/apps_proc/* imx8source/")


##Function downloads the CAF source and removes the EAP source
##Limitation - unable to clone the CHIPCODE build
def create_chipcode_source(imx_link):
      #print("Current directory is "+os.getcwd())
      os.chdir(cur_dir+"/"+"sa415m-le-1-7_amss_standard_oem_imx/SA415M_apps_fsl/apps_proc")
      check_dir_file(".repo","f")
      os.system(imx_link)
      os.system(sync_cmd)

      i=0
      for x in delete_dir:
	os.system("rm -rf sources/"+x)


def add_code_imx(file_content,file_path,file_name):      
      os.chdir(cur_dir)
      #print("Current directory is "+os.getcwd())
      os.chdir(file_path)
      #print("Current Directory "+os.getcwd())	
      if(os.path.isfile(file_name)):
      		file_obj=open(file_name,'a')
       		file_obj.write(file_content)
      else:
      	print("File doesn't exist")
      
def run_build():
	os.chdir(cur_dir)
	print("Current owrking directory"+os.getcwd())
	os.system("./append_code.sh")
	os.chdir(cur_dir+"/"+"imx8source/")
	print("Current owrking directory"+os.getcwd())
	os.system("EULA=1 DISTRO=fsl-imx-wayland MACHINE=imx8qxpmek")
	os.system("umask 022")
	#os.system("source fsl-setup-release.sh")
	#os.system("bitbake core-image-minimal")	

##this will validate the provided release xml file
def validate_xml_name(xml_file):
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        if(regex.search(xml_file) == None):
                return True
        else:
                return False

def create_target_build():
	if len(sys.argv)==2:
		xml_file=sys.argv[1]
		if(validate_xml_name(xml_file)):
			create_imx_source()
			create_chipcode_source(caf_cmd+xml_file)
			run_build()			
			#for st in file_list:
				#print("File name is "+st[(st.rfind('/',0,len(st))+1):]+" and its path is "+st[0:(st.rfind('/',0,len(st))+1)])
			#	path=st[0:(st.rfind('/',0,len(st))+1)]
			#	name=st[(st.rfind('/',0,len(st))+1):]
			#	add_code_imx(code_base.pop(0),path,name)
		else:
			print("Invalid file name and it has one of the special characters [@!#$%^&*()<>?/\|}{~:]")
	else:
		print("Command USAGE: python syncImx.py [Release xml file] ")


create_target_build()
