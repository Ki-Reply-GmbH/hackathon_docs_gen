### As seqdiag doest not work on the latest version of python. It only works on python 3.8 with the 
### following version of the mentioned libraries.

# 1. creating a virtual environment:
   pip install virtualenv
   
   virtualenv -p python3.8 seqdiag-env

# 2. Activate the virtual Environment:#
   seqdiag-env\Scripts\activate

# 3. Install Dependecies:
   
   pip install pillow==6.2.2
   pip install reportlab==3.5.34
   pip install seqdiag
