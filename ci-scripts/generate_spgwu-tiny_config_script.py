#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *      contact@openairinterface.org
# */
#---------------------------------------------------------------------

import os
import re
import subprocess
import sys

class spgwuConfigGen():
	def __init__(self):
		self.kind = ''
		self.s1u_name = ''
		self.sgi_name = ''
		self.sxu_name = ''
		self.spgwc0_ip_addr = ''
		self.pdn_list = ''
		self.prefix = ''
		self.fromDockerFile = False
		self.addFQDN = False

	def GenerateSpgwuConfigurer(self):
		pdns = self.pdn_list.split();
		conf_file = open('./spgw_u.conf', 'w')
		conf_file.write('# generated by generate_spgwu-tiny_config_scripts.py\n')
		conf_file.write('SPGW-U =\n')
		conf_file.write('{\n')
		if self.addFQDN:
			conf_file.write('    FQDN = "gw1.spgw.node.epc.mnc230.mcc320.openairinterface.org";\n')
		conf_file.write('    INSTANCE      = 0;            # 0 is the default\n')
		conf_file.write('    PID_DIRECTORY = "/var/run";     # /var/run is the default\n')
		conf_file.write('    #ITTI_TASKS :\n')
		conf_file.write('    #{\n')
		conf_file.write('        #ITTI_TIMER_SCHED_PARAMS :\n')
		conf_file.write('        #{\n')
		conf_file.write('            #CPU_ID       = 1;\n')
		conf_file.write('            #SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
		conf_file.write('            #SCHED_PRIORITY = 85;\n')
		conf_file.write('        #};\n')
		conf_file.write('        #S1U_SCHED_PARAMS :\n')
		conf_file.write('        #{\n')
		conf_file.write('            #CPU_ID       = 1;\n')
		conf_file.write('            #SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
		conf_file.write('            #SCHED_PRIORITY = 84;\n')
		conf_file.write('        #};\n')
		conf_file.write('        #SX_SCHED_PARAMS :\n')
		conf_file.write('        #{\n')
		conf_file.write('            #CPU_ID       = 1;\n')
		conf_file.write('            #SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
		conf_file.write('            #SCHED_PRIORITY = 84;\n')
		conf_file.write('        #};\n')
		conf_file.write('        #ASYNC_CMD_SCHED_PARAMS :\n')
		conf_file.write('        #{\n')
		conf_file.write('            #CPU_ID       = 1;\n')
		conf_file.write('            #SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
		conf_file.write('            #SCHED_PRIORITY = 84;\n')
		conf_file.write('        #};\n')
		conf_file.write('    #};\n')
		# check if PRIO and THREAD numbers are needed
		cmd = 'grep THREAD_S1U_PRIO component/oai-spgwu-tiny/etc/spgw_u.conf || true'
		grepRet = subprocess.check_output(cmd, shell=True, universal_newlines=True)
		threadPrioNeeded = False
		if grepRet is not None:
			isPrioNeeded = re.search('@THREAD_S1U_PRIO@', grepRet.strip())
			if isPrioNeeded is not None:
				threadPrioNeeded = True
		conf_file.write('    INTERFACES :\n')
		conf_file.write('    {\n')
		conf_file.write('        S1U_S12_S4_UP :\n')
		conf_file.write('        {\n')
		conf_file.write('            # S-GW binded interface for S1-U communication (GTPV1-U) can be ethernet interface, virtual ethernet interface, we don\'t advise wireless interfaces\n')
		conf_file.write('            INTERFACE_NAME         = "'+self.s1u_name+'";  # STRING, interface name, YOUR NETWORK CONFIG HERE\n')
		conf_file.write('            IPV4_ADDRESS           = "read";                                    # STRING, CIDR or "read to let app read interface configured IP address\n')
		conf_file.write('            #PORT                   = 2152;                                     # Default is 2152\n')
		if threadPrioNeeded:
			conf_file.write('            SCHED_PARAMS :\n')
			conf_file.write('            {\n')
			conf_file.write('                #CPU_ID       = 2;\n')
			conf_file.write('                SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
			conf_file.write('                SCHED_PRIORITY = 80;\n')
			conf_file.write('                POOL_SIZE = 8;\n')
			conf_file.write('            };\n')
		else:
			conf_file.write('            #SCHED_PARAMS :\n')
			conf_file.write('            #{\n')
			conf_file.write('                #CPU_ID       = 2;\n')
			conf_file.write('                #SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
			conf_file.write('                #SCHED_PRIORITY = 98;\n')
			conf_file.write('            #};\n')
		conf_file.write('        };\n')
		conf_file.write('        SX :\n')
		conf_file.write('        {\n')
		conf_file.write('            # S/P-GW binded interface for SX communication\n')
		conf_file.write('            INTERFACE_NAME         = "'+self.sxu_name+'"; # STRING, interface name\n')
		conf_file.write('            IPV4_ADDRESS           = "read";                        # STRING, CIDR or "read" to let app read interface configured IP address\n')
		conf_file.write('            #PORT                   = 8805;                         # Default is 8805\n')
		if threadPrioNeeded:
			conf_file.write('            SCHED_PARAMS :\n')
			conf_file.write('            {\n')
			conf_file.write('                #CPU_ID       = 1;\n')
			conf_file.write('                SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
			conf_file.write('                SCHED_PRIORITY = 81;\n')
			conf_file.write('                POOL_SIZE = 1;\n')
			conf_file.write('            };\n')
		else:
			conf_file.write('            #SCHED_PARAMS :\n')
			conf_file.write('            #{\n')
			conf_file.write('                #CPU_ID       = 1;\n')
			conf_file.write('                #SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
			conf_file.write('                #SCHED_PRIORITY = 95;\n')
			conf_file.write('            #};\n')
		conf_file.write('        };\n')
		conf_file.write('        SGI :\n')
		conf_file.write('        {\n')
		conf_file.write('           # No config to set, the software will set the SGi interface to the interface used for the default route.\n')
		conf_file.write('            INTERFACE_NAME         = "'+self.sgi_name+'"; # STRING, interface name or "default_gateway"\n')
		conf_file.write('            IPV4_ADDRESS           = "read";                         # STRING, CIDR or "read" to let app read interface configured IP address\n')
		if threadPrioNeeded:
			conf_file.write('            SCHED_PARAMS :\n')
			conf_file.write('            {\n')
			conf_file.write('                #CPU_ID       = 3;\n')
			conf_file.write('                SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
			conf_file.write('                SCHED_PRIORITY = 80;\n')
			conf_file.write('                POOL_SIZE = 8;\n')
			conf_file.write('            };\n')
		else:
			conf_file.write('            #SCHED_PARAMS :\n')
			conf_file.write('            #{\n')
			conf_file.write('                #CPU_ID       = 3;\n')
			conf_file.write('                #SCHED_POLICY = "SCHED_FIFO"; # Values in { SCHED_OTHER, SCHED_IDLE, SCHED_BATCH, SCHED_FIFO, SCHED_RR }\n')
			conf_file.write('                #SCHED_PRIORITY = 98;\n')
			conf_file.write('            #};\n')
		conf_file.write('        };\n')
		conf_file.write('    };\n')
		if threadPrioNeeded:
			conf_file.write('    SNAT = "no";\n')
			conf_file.write('    PDN_NETWORK_LIST  = (\n')
			# Only one is now supported
			pdn = pdns[0]
			conf_file.write('                      {NETWORK_IPV4 = "'+pdn+'";}\n')
			conf_file.write('                    );\n')
		else:
			conf_file.write('    PDN_NETWORK_LIST  = (\n')
			for pdn in pdns[ 0:len(pdns)-1 ]:
				conf_file.write('                      {NETWORK_IPV4 = "'+pdn+'"; SNAT = "no";},\n')
			pdn = pdns[len(pdns) - 1]
			conf_file.write('                      {NETWORK_IPV4 = "'+pdn+'"; SNAT = "no";}\n')
			conf_file.write('                    );\n')

		conf_file.write('    SPGW-C_LIST = (\n')
		conf_file.write('         {IPV4_ADDRESS="' + self.spgwc0_ip_addr + '" ;}\n')
		conf_file.write('    );\n')
		if threadPrioNeeded:
			conf_file.write('    NON_STANDART_FEATURES :\n')
			conf_file.write('    {\n')
			conf_file.write('        BYPASS_UL_PFCP_RULES = "no";\n')
			conf_file.write('    };\n')
		conf_file.write('};\n')
		conf_file.close()

#-----------------------------------------------------------
# Usage()
#-----------------------------------------------------------
def Usage():
	print('--------------------------------------------------------------------')
	print('generate_spgwu-tiny_config_scripts.py')
	print('   Prepare a bash script to be run in the workspace where SPGW-U-TINY is being built.')
	print('   That bash script will copy configuration template files and adapt to your configuration.')
	print('--------------------------------------------------------------------')
	print('Usage: python3 generate_spgwu-tiny_config_scripts.py [options]')
	print('  --help  Show this help.')
	print('--------------- SPGW-U Options -----')
	print('  --kind=SPGW-U')
	print('  --sxc_ip_addr=[SPGW-C SX IP address]')
	print('  --sxu=[SPGW-U SX Interface Name]')
	print('  --s1u=[SPGW-U S1-U Interface Name]')
	print('  --sgi=[SPGW-U SGi Interface Name]')
	print('  --pdn_list=["PDNs"]')
	print('  --prefix=["Prefix for configuration files"]')
	print('  --from_docker_file')

argvs = sys.argv
argc = len(argvs)
cwd = os.getcwd()

mySpgwuCfg = spgwuConfigGen()

while len(argvs) > 1:
	myArgv = argvs.pop(1)
	if re.match('^\-\-help$', myArgv, re.IGNORECASE):
		Usage()
		sys.exit(0)
	elif re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE)
		mySpgwuCfg.kind = matchReg.group(1)
	elif re.match('^\-\-sxu=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-sxu=(.+)$', myArgv, re.IGNORECASE)
		mySpgwuCfg.sxu_name = matchReg.group(1)
	elif re.match('^\-\-sxc_ip_addr=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-sxc_ip_addr=(.+)$', myArgv, re.IGNORECASE)
		mySpgwuCfg.spgwc0_ip_addr = matchReg.group(1)
	elif re.match('^\-\-s1u=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-s1u=(.+)$', myArgv, re.IGNORECASE)
		mySpgwuCfg.s1u_name = matchReg.group(1)
	elif re.match('^\-\-sgi=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-sgi=(.+)$', myArgv, re.IGNORECASE)
		mySpgwuCfg.sgi_name = matchReg.group(1)
	elif re.match('^\-\-pdn_list=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-pdn_list=(.+)$', myArgv, re.IGNORECASE)
		mySpgwuCfg.pdn_list = str(matchReg.group(1))
	elif re.match('^\-\-prefix=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-prefix=(.+)$', myArgv, re.IGNORECASE)
		mySpgwuCfg.prefix = matchReg.group(1)
	elif re.match('^\-\-from_docker_file', myArgv, re.IGNORECASE):
		mySpgwuCfg.fromDockerFile = True
	elif re.match('^\-\-addFQDN', myArgv, re.IGNORECASE):
		mySpgwuCfg.addFQDN = True
	else:
		Usage()
		sys.exit('Invalid Parameter: ' + myArgv)

if mySpgwuCfg.kind == '':
	Usage()
	sys.exit('missing kind parameter')

if mySpgwuCfg.kind == 'SPGW-U':
	if mySpgwuCfg.sxu_name == '':
		Usage()
		sys.exit('missing SX Interface Name on SPGW-U container')
	elif mySpgwuCfg.s1u_name == '':
		Usage()
		sys.exit('missing S1-U Interface Name on SPGW-U container')
	elif mySpgwuCfg.sgi_name == '':
		Usage()
		sys.exit('missing SGi Interface Name on SPGW-U container')
	elif mySpgwuCfg.pdn_list == '':
		Usage()
		sys.exit('missing pdn_list')
	elif mySpgwuCfg.spgwc0_ip_addr == '':
		Usage()
		sys.exit('missing SPGW-C #0 IP address on SX interface')
	elif mySpgwuCfg.prefix == '':
		Usage()
		sys.exit('missing prefix')
	else:
		mySpgwuCfg.GenerateSpgwuConfigurer()
		sys.exit(0)
else:
	Usage()
	sys.exit('invalid kind parameter')
