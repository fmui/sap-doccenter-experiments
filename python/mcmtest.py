# -*- coding: utf-8 -*-

##########################################################################
# Copyright 2016, Florian Müller
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import mcmlib

if __name__ == '__main__':
    session = mcmlib.MCMSession("user", “password”, "https://<host>/mcm/b/json")
    
    myDocs = session.get_my_documents_repository()
    home = myDocs.get_home_folder()

    for child in home.get_children():
        print("[" + child.base_type_id + "] \t" + child.name + " (" + child.id + ")")
        
    session.close()