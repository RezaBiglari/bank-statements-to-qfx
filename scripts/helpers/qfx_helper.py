from helpers import convert_to_custom_format, convert_currency_to_float, generate_transaction_id

def create_qfx(data, 
               bid, 
               acc_id, 
               acc_type="CHECKING",
               closing_balance=0.0,
               closing_balance_date="20000101",
               fitid_fixed_prefix="", 
               fitid_fixed_suffix=""):
    qfx_content = f'''OFXHEADER:100
OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE

<OFX>
 <SIGNONMSGSRSV1>
  <SONRS>
   <STATUS>
    <CODE>0
    <SEVERITY>INFO
    <MESSAGE>OK
   </STATUS>
   <DTSERVER>20241219192958[-5]
   <LANGUAGE>ENG
   <INTU.BID>{bid}
  </SONRS>
 </SIGNONMSGSRSV1>
 <BANKMSGSRSV1>
  <STMTTRNRS>
   <TRNUID>1
   <STATUS>
    <CODE>0
    <SEVERITY>INFO
    <MESSAGE>OK
   </STATUS>
   <STMTRS>
    <CURDEF>CAD
    <BANKACCTFROM>
     <ACCTID>{acc_id}
     <ACCTTYPE>{acc_type}
    </BANKACCTFROM>
    <BANKTRANLIST>'''

    for row in data:
        try:
            (date, description, debits, credits, balance, _) = row
            
            amount = convert_currency_to_float(debits) if debits else convert_currency_to_float(credits)
            fromatted_amount = f"{amount:.2f}"

            qfx_content += f'''
     <STMTTRN>
      <TRNTYPE>{'DEBIT' if debits else 'CREDIT'}
      <DTPOSTED>{convert_to_custom_format(date)}
      <TRNAMT>{fromatted_amount}
      <FITID>{generate_transaction_id(date, fixed_prefix=fitid_fixed_prefix, fixed_suffix=fitid_fixed_suffix)}
      <NAME>{description}              
     </STMTTRN>'''
        except Exception as e:
            print(f"Exception in converting a row: '{row}'")
            print(e)

    qfx_content += f'''
    </BANKTRANLIST>
    <LEDGERBAL>
     <BALAMT>{f"{closing_balance:.2f}"}
     <DTASOF>{closing_balance_date}
    </LEDGERBAL>
    <AVAILBAL>
     <BALAMT>{f"{closing_balance:.2f}"}
     <DTASOF>{closing_balance_date}
    </AVAILBAL>
   </STMTRS>
  </STMTTRNRS>
 </BANKMSGSRSV1>
</OFX>
'''
    return qfx_content
