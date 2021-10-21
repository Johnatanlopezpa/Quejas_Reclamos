import pandas as pd
from connection.Oracle_connection import connection_oracle as con_oracle
from datetime import date
from datetime import datetime
from datetime import timedelta
from email import send_email

def extract_claims():
    today = date.today()
    yesterday = today - timedelta(days=1)
    date_1 = date.strftime(yesterday, '%Y')
    date_2 = date.strftime(yesterday, '%m')
    date_final = f'SIRA.TBL_TIPI_{date_1}_{date_2}@SIRA'
    name_csv = f'Quejas_{yesterday}.csv'
    file_local = f'./reportes/{name_csv}'
    connection = con_oracle()
    script_oracle ='''SELECT * FROM (
                                        SELECT * FROM
                                            (
                                                SELECT TO_CHAR(TO_DATE(FECHA),'YYYYMM') PERIODO, CALLID, 
                                                       ANI AS TELEFONO, DURACIONSEG AS AHT, TESPERA_SEG AS ASA, 
                                                       PILOTO,FECHA, HORA, NIVEL1, NIVEL2, NIVEL3, NIVEL4, 
                                                       CODFINALIZACION, 
                                                       REGEXP_REPLACE(TRIM(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(REGEXP_REPLACE(REGEXP_REPLACE(NIVEL1,'[ ]+',' '),'\s+',' ')),'_',' '),'.',''),'?','Ñ'),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ã‘','Ñ'),'',' ')) || ' - ' || TRIM(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(REGEXP_REPLACE(REGEXP_REPLACE(CODFINALIZACION,'[ ]+',' '),'\s+',' ')),'_',' '),'.',''),'?','Ñ'),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ã‘','Ñ'),'',' ')),'\s+',' ') AS TRANSACCION
                                                FROM '''+date_final+'''
                                                WHERE PILOTO IN ('Grup_Skill_UNIV','CMV UNIVERSAL',
                                                         'UNE_TIGO_PYMES','CMV_UNE_TIGO_EYG',
                                                         'CMV_SIEBEL_8.1','CMV_BQ_SER_CLIEN',
                                                         'CMV_BQ_ECOMER','CMV_TIGO_ALTOV_MED') 
                                                AND ESTADO = 'Atendido'AND DURACIONSEG > 60
                                            ) LLAMADA,
                                            (
                                                SELECT SUBSERVICIO, APLICA_BU, CLASIFICACION_MILLICOM, 
                                                       QUEJA_MILLICOM,TIPO_QUEJA_MILLICOM, CATEGORIA, 
                                                       SUBCATEGORIA, BU || '-' || CANAL AS KEY
                                                FROM MADAVIL.TBL_TIPI_EQUIVALENCIAS_3 
                                                 WHERE QUEJA_MILLICOM = 'QUEJA - DATOS' AND 
                                                       APLICA_BU = 'SI' AND CLASIFICACION_MILLICOM = 'RECLAMOS'
                                            ) TABLA_EQUIVALENCIA
                                        WHERE LLAMADA.TRANSACCION = TABLA_EQUIVALENCIA.SUBSERVICIO (+)
                                              AND 'MOVIL-CONTACT CENTER' = TABLA_EQUIVALENCIA.KEY (+)
                                        UNION ALL
                                        SELECT * FROM
                                            (
                                                SELECT TO_CHAR(TO_DATE(FECHA),'YYYYMM') PERIODO, CALLID, 
                                                       ANI AS TELEFONO, DURACIONSEG AS AHT, TESPERA_SEG AS ASA,
                                                       PILOTO,FECHA, HORA, NIVEL1, NIVEL2, NIVEL3, NIVEL4, 
                                                       CODFINALIZACION, 
                                                       REGEXP_REPLACE(TRIM(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(REGEXP_REPLACE(REGEXP_REPLACE(NIVEL1,'[ ]+',' '),'\s+',' ')),'_',' '),'.',''),'?','Ñ'),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ã‘','Ñ'),'',' ')) || ' - ' || TRIM(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(REGEXP_REPLACE(REGEXP_REPLACE(CODFINALIZACION,'[ ]+',' '),'\s+',' ')),'_',' '),'.',''),'?','Ñ'),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ã‘','Ñ'),'',' ')),'\s+',' ') AS TRANSACCION
                                                FROM '''+date_final+'''
                                                WHERE PILOTO IN ('Grup_Skill_UNIV','CMV UNIVERSAL',
                                                                 'UNE_TIGO_PYMES','CMV_UNE_TIGO_EYG',
                                                                 'CMV_SIEBEL_8.1','CMV_BQ_SER_CLIEN',
                                                                 'CMV_BQ_ECOMER','CMV_TIGO_ALTOV_MED') 
                                                AND ESTADO = 'Atendido'
                                             ) LLAMADA,
                                            (
                                                SELECT SUBSERVICIO, APLICA_BU, CLASIFICACION_MILLICOM, 
                                                       QUEJA_MILLICOM,TIPO_QUEJA_MILLICOM, CATEGORIA, 
                                                       SUBCATEGORIA, BU || '-' || CANAL AS KEY
                                                FROM MADAVIL.TBL_TIPI_EQUIVALENCIAS_3
                                                WHERE QUEJA_MILLICOM <> 'QUEJA - DATOS' AND APLICA_BU = 'SI' 
                                                      AND CLASIFICACION_MILLICOM = 'RECLAMOS'
                                            ) TABLA_EQUIVALENCIA
                                        WHERE LLAMADA.TRANSACCION = TABLA_EQUIVALENCIA.SUBSERVICIO (+)
                                              AND 'MOVIL-CONTACT CENTER' = TABLA_EQUIVALENCIA.KEY (+)
                                    ) WHERE QUEJA_MILLICOM is not null'''
                                    
    df=pd.read_sql (script_oracle,connection)
    df.to_csv(file_local,encoding='utf-8-sig', sep=';' , index=False)
    send_email_out = send_email()
    
def main():
     extract_claims()


if __name__ == "__main__":
    main()