# The MIT License (MIT)
#
# Copyright (c) 2016 Oracle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (Oracle A-Team)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from oc_provision_wrappers import commerce_setup_helper


json_key = 'WEBLOGIC_managed_servers'
common_key = 'WEBLOGIC_common'
service_name = "WebLogic Servers"

def create_servers(configData, full_path): 
    
    """
    Create references to managed servers in the Weblogic Admin instance
    """   
    if json_key in configData:
        jsonDataArray = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return
    
    if common_key in configData:
        commonData = configData[common_key]
    else:
        print common_key + " config data missing from json. will not install"
        return 

    response_files_path = full_path + "/responseFiles/wls-12.1.2"
                    
    print "Updating " + service_name   

    commonRequiredFields = ['middlewareHome', 'installOwner', 'wl_adminUser', 'wl_adminHttpPort', 'wl_adminHost' 'wl_adminPassword']
    commerce_setup_helper.check_required_fields(commonData, commonRequiredFields)

    INSTALL_DIR = commonData['middlewareHome']
    INSTALL_OWNER = commonData['installOwner']
    WL_ADMIN_USER = commonData['wl_adminUser']
    WL_ADMIN_PW = commonData['wl_adminPassword']
    WL_ADMIN_HOST = commonData['wl_adminHost']
    WL_ADMIN_HTTP_PORT = commonData['wl_adminHttpPort']
                    
    for jsonData in jsonDataArray:            
      
        requiredFields = ['managedServerName', 'managedServerHttpPort', 'managedServerHost']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)    
    
        WL_SERVER_NAME = jsonData['managedServerName']
        WL_SERVER_PORT = jsonData['managedServerHttpPort']
        WL_SERVER_HOST = jsonData['managedServerHost']
                    
        wlCmd = "\"" + INSTALL_DIR + "/wlserver/common/bin/wlst.sh " + response_files_path + "/createManagedServer.py -u " + WL_ADMIN_USER + \
        " -p " + WL_ADMIN_PW + " -a t3://" + WL_ADMIN_HOST + ":" + WL_ADMIN_HTTP_PORT + " -n " + WL_SERVER_NAME + " -h " + WL_SERVER_PORT + " -m " + WL_SERVER_HOST + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, wlCmd)  
    
