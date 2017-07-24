import os
import sys
import subprocess
import string
import random

bashfile=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
bashfile='/tmp/'+bashfile+'.sh'

f = open(bashfile, 'w')
s = """#! /usr/bin/env bash
if [ "$#" != "1" ]; then
	echo 'convert a bash file to python file'
	echo 'example:'
	echo "	$0  abc.sh"
	exit -1
fi

if [[ ! -f $1 ]]; then
	echo "Error: $1 not exist"
	exit -1
fi

bashfile=$1
pythonfile="$bashfile".py
special='"''"''"'
newspecial='\\''"''\\''"''\\''"'
slash='\\\\'

echo "import os" > $pythonfile
echo "import sys" >> $pythonfile
echo "import subprocess" >> $pythonfile
echo "import string" >> $pythonfile
echo "import random" >> $pythonfile
echo "" >> $pythonfile

echo "bashfile=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))" >> $pythonfile 
echo "bashfile='/tmp/'+bashfile+'.sh'" >> $pythonfile
echo "" >> $pythonfile

echo "f = open(bashfile, 'w')" >> $pythonfile
echo -n 's = \"\"\"' >> $pythonfile
while IFS= read -r line; do line=${line//$slash/$slash}; line=${line//$special/$newspecial}; echo "$line" >> $pythonfile ;  done < $bashfile
echo '\"\"\"' >> $pythonfile
echo "f.write(s)" >> $pythonfile
echo "f.close()" >> $pythonfile
echo "os.chmod(bashfile, 0o755)" >> $pythonfile
echo "bashcmd=bashfile" >> $pythonfile
echo "for arg in sys.argv[1:]:" >> $pythonfile
echo "  bashcmd += ' '+arg" >> $pythonfile
echo "subprocess.call(bashcmd, shell=True)" >> $pythonfile

"""
f.write(s)
f.close()
os.chmod(bashfile, 0o755)
bashcmd=bashfile
for arg in sys.argv[1:]:
  bashcmd += ' '+arg
subprocess.call(bashcmd, shell=True)
