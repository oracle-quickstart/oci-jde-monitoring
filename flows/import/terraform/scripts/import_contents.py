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
    authType = 'user'
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

        config = oci.config.from_file()
        la_client = oci.log_analytics.LogAnalyticsClient(config=config)
        object_storage_client = oci.object_storage.ObjectStorageClient(config=config)

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

def substituteprops(filepath, entityprops):
    content_dir = filepath
    print("content_dir :: ", content_dir)

    dict = json.loads(entityprops)
    #for key, value in dict.items():
    #    print(key+" "+ str(value))

    tmpfile = 'content' + str(random.randint(0,999999)) + '.xml'
    for content_file in glob.glob(os.path.join(content_dir, '*.xml')):
        print('content_file ::', content_file)

        with open(content_file) as f:
          tree = ET.parse(f)
          root = tree.getroot()

          for elem in root.getiterator():
            try:
              for key, value in dict.items():
                elem.text = elem.text.replace(key, value)
            except AttributeError:
              pass

        tree.write(tmpfile)

        with ZipFile(content_file + '.zip', 'w') as zip_object:
            zip_object.write(tmpfile)

        tmpfilepath = os.path.join('.', tmpfile)
        os.remove(tmpfilepath)

if __name__ == "__main__":
    main(sys.argv[1:])
