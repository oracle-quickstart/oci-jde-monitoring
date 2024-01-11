import oci
import os,glob
import sys, getopt
import json
import time
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import random

def main(argv):
    try:
        options, args = getopt.getopt(argv, "h:a:p:e:f:",
                                      ["authtype =",
                                       "profile =",
                                       "entityprops =",
                                       "filepath ="])
        print('options: ', options)
        print('args: ', args)
    except:
        print("Error Message ")

    entityprops = ''
    filepath = ''
    # authType = 'user'
    profile = ''
    for name, value in options:
        if name in ['-a', '--authtype']:
            authType = value
        elif name in ['-p', '--profile']:
            profile = value
        elif name in ['-e', '--entityprops']:
            entityprops = value
        elif name in ['-f', '--filepath']:
            filepath = value

    try:
        if (not filepath):
            print ("Error: Source filepath is empty!")
            return
        if filepath.startswith('"') and filepath.endswith('"'):
            filepath = filepath[1:-1]

        print("######################### Content Details ######################")
        print("authtype :: ", authType)
        print("profile :: ", profile)
        print("entityprops :: ", entityprops)
        print("filepath :: ", filepath)

        # config = oci.config.from_file()
        # la_client = oci.log_analytics.LogAnalyticsClient(config=config)
        # object_storage_client = oci.object_storage.ObjectStorageClient(config=config)
        if (authType == 'user'):
            config = oci.config.from_file("~/.oci/config", profile)
            la_client = oci.log_analytics.LogAnalyticsClient(config=config)
            object_storage_client = oci.object_storage.ObjectStorageClient(config=config)
        else:
            # get oci obo token from env var settings and create signer from obo delegation token
            obo_token = os.environ.get("OCI_obo_token")
            signer = oci.auth.signers.InstancePrincipalsDelegationTokenSigner(delegation_token=obo_token)
            # create LogAnalytics client using signer
            la_client = oci.log_analytics.LogAnalyticsClient(config={}, signer=signer)
            object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)

        namespace = object_storage_client.get_namespace().data
        print("Tenancy NameSpace :: ", namespace)

        substituteprops(filepath, entityprops)

        for zip_file in glob.glob(os.path.join(filepath, '*.zip')):
            print('zip_file ::', zip_file)

            bytes_content = b''
            with open(zip_file, 'rb') as file_data:
                bytes_content = file_data.read()

            response = la_client.import_custom_content(
                namespace_name=namespace,
                import_custom_content_file_body=bytes_content,
                is_overwrite=True)

            print("import response:: ", response.headers)

    except Exception as e:
            print("Error in importing sources: ",e)
            raise

#def substituteprops(filepath, entityprops):
#    content_dir = filepath
#    print("content_dir :: ", content_dir)
#
#    dict = json.loads(entityprops)
#    #for key, value in dict.items():
#    #    print(key+" "+ str(value))
#    
#    for content_file in glob.glob(os.path.join(content_dir, '*.zip')):
#        print('content_file ::', content_file)
#        file_name = ''
#        with ZipFile(content_file, 'r') as zipfile:
#            zipfile.extractall(content_dir)
#        for f_name in os.listdir(content_dir):
#            if (f_name.endswith('.xml') or f_name.endswith('.XML')):
#                file_in = open(content_dir+os.sep+f_name, "rt")
#                xml_content = file_in.read()
#                file_in.close()
#                for key, value in dict.items():
#                    xml_content = xml_content.replace("{"+key+"}", value)
#                file_in  = open(content_dir+os.sep+f_name, "wt")
#                file_in.write(xml_content)
#                file_in.close()
#                file_name = f_name
#                print("file_name: ", file_name)
#        os.remove(content_file)
#        with ZipFile(content_file, 'w') as zip:
#            zip.write(content_dir+os.sep+file_name,file_name)
#        os.remove(content_dir+os.sep+file_name)

#JDE def substituteprops(filepath, entityprops):
#JDE     content_dir = filepath
#JDE     print("content_dir :: ", content_dir)
#JDE 
#JDE     dict = json.loads(entityprops)
#JDE     #for key, value in dict.items():
#JDE     #    print(key+" "+ str(value))
#JDE 
#JDE     tmpfile = 'content' + str(random.randint(0,999999)) + '.xml'
#JDE     for content_file in glob.glob(os.path.join(content_dir, '*.xml')):
#JDE         print('content_file ::', content_file)
#JDE 
#JDE         with open(content_file) as f:
#JDE           tree = ET.parse(f)
#JDE           root = tree.getroot()
#JDE 
#JDE           for elem in root.iter():
#JDE             try:
#JDE               for key, value in dict.items():
#JDE                 key1 = "{" + key + "}"
#JDE                 elem.text = elem.text.replace(key1, value)
#JDE             except AttributeError:
#JDE               pass
#JDE 
#JDE         tree.write(tmpfile)
#JDE 
#JDE         with ZipFile(content_file + '.zip', 'w') as zip_object:
#JDE             zip_object.write(tmpfile)
#JDE 
#JDE         tmpfilepath = os.path.join('.', tmpfile)
#JDE         os.remove(tmpfilepath)
#JDE         os.remove(content_file)

def substituteprops(filepath, entityprops):
    content_dir = filepath
    print("content_dir :: ", content_dir)

    dict = json.loads(entityprops)
    #for key, value in dict.items():
    #    print(key+" "+ str(value))
    
    for content_file in glob.glob(os.path.join(content_dir, '*.zip')):
        print('content_file ::', content_file)
        file_name = ''
        with ZipFile(content_file, 'r') as zipfile:
            zipfile.extractall(content_dir)
        for f_name in os.listdir(content_dir):
            if (f_name.endswith('.xml') or f_name.endswith('.XML')):
                file_in = open(content_dir+os.sep+f_name, "rt")
                xml_content = file_in.read()
                file_in.close()
                for key, value in dict.items():
                    xml_content = xml_content.replace("{"+key+"}", value)
                file_in  = open(content_dir+os.sep+f_name, "wt")
                file_in.write(xml_content)
                file_in.close()
                file_name = f_name
                print("file_name: ", file_name)
        os.remove(content_file)
        with ZipFile(content_file, 'w') as zip:
            zip.write(content_dir+os.sep+file_name,file_name)
        os.remove(content_dir+os.sep+file_name)

if __name__ == "__main__":
    main(sys.argv[1:])
