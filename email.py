import win32com.client as win32
from datetime import date
from datetime import datetime
from datetime import timedelta

def send_email():
    today = date.today()
    yesterday = today - timedelta(days=1)
    name_csv = f'Quejas_{yesterday}.csv'
    file_local = f'''D:/Desarrollo/Quejas_Millicom_Alejandro/reportes/{name_csv}'''
    firma =f'''D:/Desarrollo/Quejas_Millicom_Alejandro/img/firma.jpeg'''
    
    olApp = win32.Dispatch('Outlook.Application')
    olNS = olApp.GetNameSpace('MAPI')

    mailItem = olApp.CreateItem(0)
    mailItem.Subject = 'Consulta de Quejas'
    mailItem.BodyFormat = 2
    attachment = mailItem.Attachments.Add(firma)
    attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "MyId1")
    mailItem.HTMLBody = "<html><body><p>Hola Edgar,Te comparto el archivo con la información.</p>\
                               <p>Saludos.</p>\
                              <img src=""cid:MyId1""></body></html>"
    mailItem.GetInspector 
    attachment1 = file_local
    mailItem.Attachments.Add(Source=attachment1)
    mailItem.To ='Edgar.Lopez@tigo.com.co'
    #mailItem.To ='yerson@veredata.co;Cristian.Marin.Alvarez@tigo.com.co;johnatan.lopez@tigo.com.co'
    mailItem._oleobj_.Invoke(*(64209,0,8,0,olNS.Accounts.item('johnatan.lopez@tigo.com.co')))
    
    mailItem.Display()
    mailItem.Save()
    mailItem.Send()
    




