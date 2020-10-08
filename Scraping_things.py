import time
from datetime import datetime
import Global_var
from Insert_On_Datbase import insert_in_Local
import sys , os
import string
import time
from datetime import datetime
import html
import re

def scrap_data(href,get_htmlSource):

    SegField = []
    for data in range(45):
        SegField.append('')

    get_htmlSource = html.unescape(str(get_htmlSource))

    a = True
    while a == True:
        try:
            Email = get_htmlSource.partition('Correo Electrónico del Operador en la UC')[2].partition("</li>")[0].strip()
            Email = Email.partition('">')[2].partition("</div>")[0].strip().replace(';',' , ')
            Email_regex = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+)", Email)
            if len(Email_regex) == 0:
                Email = get_htmlSource.partition('correo electrónico del comprador')[2].partition("</li>")[0].strip()
                Email = Email.partition('">')[2].partition("</div>")[0].strip().replace(';',' , ')
                Email_regex = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+)", Email)
                try:  
                    SegField[1] = str(Email_regex[0])
                except:
                    SegField[1] = ''
            else:
                try:  
                    SegField[1] = str(Email_regex[0])
                except:
                    SegField[1] = ''
            
            Purchaser = get_htmlSource.partition('Nombre de la Unidad Compradora (UC)')[2].partition("</li>")[0].strip()
            Purchaser = Purchaser.partition('">')[2].partition("</div>")[0].strip()
            Purchaser = Purchaser.partition('-')[0].strip()
            SegField[12] = Purchaser

            Address = get_htmlSource.partition('Nombre de la Unidad Compradora (UC)')[2].partition("</li>")[0].strip()
            Address = Address.partition('">')[2].partition("</div>")[0].strip()

            Contact_name = get_htmlSource.partition('Nombre del Operador en la UC')[2].partition("</li>")[0].strip()
            Contact_name = Contact_name.partition('">')[2].partition("</div>")[0].strip()

            Full_Address = f'{Address}, Maxico.<br>\nContact Name: {Contact_name}'
            SegField[2] = Full_Address

            Notice_no = get_htmlSource.partition('Código del Expediente')[2].partition("</li>")[0].strip()
            Notice_no = Notice_no.partition('">')[2].partition("</div>")[0].strip()
            SegField[13] = Notice_no

            Title = get_htmlSource.partition('Descripción del Expediente')[2].partition("</li>")[0].strip()
            Title = Title.partition('">')[2].partition("</div>")[0].strip()
            Title = string.capwords(str(Title))
            SegField[19] = Title

            Deadline = get_htmlSource.partition('Plazo de participación o vigencia del anuncio')[2].partition("</li>")[0].strip()
            Deadline = Deadline.partition('">')[2].partition("</div>")[0].strip()
            Deadline = Deadline.partition(' ')[0].strip()
            # datetime_object = datetime.strptime(Deadline, '%d/%m/%Y %H:%M %p')
            datetime_object = datetime.strptime(Deadline, '%d/%m/%Y')
            Deadline = datetime_object.strftime("%Y-%m-%d")
            SegField[24] = Deadline

            
            Ad_Description = get_htmlSource.partition('Descripción del Anuncio')[2].partition("</li>")[0].strip()
            Ad_Description = Ad_Description.partition('">')[2].partition("</div>")[0].strip()
            Ad_Description = string.capwords(str(Ad_Description))

            File_Categories = get_htmlSource.partition('Categorias del Expediente')[2].partition("</li>")[0].strip()
            File_Categories = File_Categories.partition('">')[2].partition("</div>")[0].strip().replace('<div>','')
            File_Categories = string.capwords(str(File_Categories))

            File_Reference = get_htmlSource.partition('subtitle_02 showableTitleRow">')[2].partition("</div>")[0].strip()
            File_Reference = File_Reference.partition('Referencia del Expediente')[2].strip()

            File_Reference = string.capwords(str(File_Reference))
            if File_Reference == '':
                File_Reference = get_htmlSource.partition('Referencia del Expediente')[2].partition("</li>")[0].strip()
                File_Reference = File_Reference.partition('">')[2].partition("</div>")[0].strip()
                File_Reference = string.capwords(str(File_Reference))

            File_Type = get_htmlSource.partition('Tipo de Expediente')[2].partition("</li>")[0].strip()
            File_Type = File_Type.partition('">')[2].partition("</div>")[0].strip()
            File_Type = string.capwords(str(File_Type))

            Federal_entity = get_htmlSource.partition('Entidad Federativa')[2].partition("</li>")[0].strip()
            Federal_entity = Federal_entity.partition('">')[2].partition("</div>")[0].strip()
            Federal_entity = string.capwords(str(Federal_entity))

            Type_of_Contract = get_htmlSource.partition('Tipo de Contratación')[2].partition("</li>")[0].strip()
            Type_of_Contract = Type_of_Contract.partition('">')[2].partition("</div>")[0].strip()
            Type_of_Contract = string.capwords(str(Type_of_Contract))
            
            SegField[18] = f"{str(SegField[19])}<br>\nDescripción del Anuncio: {Ad_Description}<br>\nCategorias del Expediente: {File_Categories}<br>\nReferencia del Expediente: {File_Reference}<br>\nTipo de Expediente: {File_Type}<br>\nEntidad Federativa: {Federal_entity}<br>\nTipo de Contratación: {Type_of_Contract}"

            SegField[28] = href

            SegField[31] = 'compranet.hacienda.gob.mx'
            SegField[27] = "0"
            SegField[22] = "0"
            SegField[26] = "0.0"
            SegField[7] = "MX"
            SegField[14] = '2'
            SegField[16] = '1'
            SegField[17] = '0'
            SegField[20] = ""
            SegField[21] = "" 
            SegField[42] = SegField[7]
            SegField[43] = ""
            for SegIndex in range(len(SegField)):
                print(SegIndex, end=' ')
                print(SegField[SegIndex])
                SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")


            if len(SegField[19]) >= 200:
                SegField[19] = str(SegField[19])[:200]+'...'

            if len(SegField[18]) >= 1500:
                SegField[18] = str(SegField[18])[:1500]+'...'

            
            if SegField[19] == '':
                wx.MessageBox(' Short Desc Blank ','compranet.hacienda.gob.mx', wx.OK | wx.ICON_INFORMATION)
            else:
                check_date(get_htmlSource, SegField)
            a = False

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = True
            time.sleep(5)


def check_date(get_htmlSource, SegField):
    a = 0
    while a == 0:
        tender_date = str(SegField[24])
        nowdate = datetime.now()
        date2 = nowdate.strftime("%Y-%m-%d")
        try:
            if tender_date != '':
                deadline = time.strptime(tender_date , "%Y-%m-%d")
                currentdate = time.strptime(date2 , "%Y-%m-%d")
                if deadline > currentdate:
                    insert_in_Local(get_htmlSource, SegField)
                    a = 1
                else:
                    print("Tender Expired")
                    Global_var.expired += 1
                    a = 1
            else:
                print("Deadline was not given")
                Global_var.deadline_Not_given += 1
                a = 1
        except Exception as e:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            exc_type , exc_obj , exc_tb = sys.exc_info()
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" , exc_tb.tb_lineno)
            a = 0