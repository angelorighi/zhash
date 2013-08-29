#!/usr/bin/env python

import os
import sys
import getopt
import hashlib
import zipfile

VERSION = '0.3'

class Zhash:
  """ Compresses a directory and calculates the sha1 hash """
  
  def __init__(self):
    self.verbose = False
    self.hash = None
    self.output_file = None
  
  def __sha1Checksum(self,filePath):
      with open(filePath, 'rb') as fh:
          m = hashlib.sha1()
          while True:
              data = fh.read(8192)
              if not data:
                  break
              m.update(data)
          return m.hexdigest().upper()

  def __zipper(self,dir, zip_file):
      zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
      root_len = len(os.path.abspath(dir))
      for root, dirs, files in os.walk(dir):
          archive_root = os.path.abspath(root)[root_len:]
          for d in dirs:
                fullpath = os.path.join(root,d) + "\\"
                archive_name = os.path.join(archive_root, d)
                if self.verbose:
                  print fullpath
                zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
  
          for f in files:
              fullpath = os.path.join(root, f)
              archive_name = os.path.join(archive_root, f)
              if self.verbose:
                print fullpath
              zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
      zip.close()
      return zip_file

  def run(self,input_dir, output_file=None):
    if os.path.exists(input_dir) == False:
      raise Exception("Path %s non found" % input_dir)

    if output_file == None:
      output_file = input_dir 
      
    output_hash = output_file + '.sha1'
    output_file += '.zip'

    self.__zipper(input_dir,output_file)
    self.hash = self.__sha1Checksum(output_file)
    self.file = output_file
    
    with open(output_hash, "w") as text_file:
      text_file.write("%s" % hash)
  
def usage():
  script_name = os.path.basename(sys.argv[0])
  print "Usage: %s -d <directory> [-v] [-h]" % script_name
  print """  -d, --directory <directory>: Directory to zip
  -o, --output <filename> (without extension): Output file
  -v, --verbose: Verbosity
  -h, --help: This help
  """
  
def main():
    verbose = False
    input_dir = None
    output_file = None

    print "\nZhash v%s: Zip & Hash a directory" % VERSION

    if len(sys.argv[1:]) == 0:
      usage()
      sys.exit(0)
    
    try:
      options, remainder = getopt.getopt(sys.argv[1:], 'd:o:hv', ['directory=', 
                                                             'output',
                                                             'verbose',
                                                             'help'
                                                               ])
    except getopt.GetoptError, err:
		  print str(err) 
		  usage()
		  sys.exit(2)

    for opt, arg in options:
        if opt in ('-d', '--directory'):
            input_dir = arg
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-o', '--output'):
            output_file = arg
        elif opt in ('-h', '--help'):
            usage()
            sys.exit(0)

    if input_dir == None:
      usage()
      sys.exit(2)

    zhash = Zhash()
    zhash.verbose = verbose
    try:
      print "Wait..."
      zhash.run(input_dir,output_file)
      print '%s -> %s' % (zhash.file,zhash.hash)
      print "Done!"
    except Exception, e:
      print e
      sys.exit(1)

if __name__ == '__main__':
  main()
