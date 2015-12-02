import os, sys
os.system("rm setup.py")
os.system("py2applet --make-setup "+sys.argv[1]+" Lexicon.txt")
os.system("rm -rf build dist")
os.system("python setup.py py2app")