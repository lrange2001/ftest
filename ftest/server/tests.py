from django.test import TestCase

# Create your tests here.
sss =  [{'device': '/dev/vda', 'type': 'SSD', 'size': '60G'}]

for __ in sss:
    print(__['device'])