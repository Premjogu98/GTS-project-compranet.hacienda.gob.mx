import time
from datetime import datetime
import Global_var
# from Insert_On_Datbase import insert_in_Local
import sys , os
import string
import time
from datetime import datetime
import html

def scrap_data(get_attribute):
    get_attribute = html.unescape(str(get_attribute))
    Email = get_attribute.partition('Correo Electrónico del Operador en la UC')[2].partition("</li>")[0].strip()
    Email = Email.partition('">')[2].partition("</div>")[0].strip()
    print(Email)
    pass