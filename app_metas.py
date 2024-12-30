# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 15:24:40 2024

@author: André Luiz
"""
import pandas as pd
import PySimpleGUI as sg

import threading
import subprocess
import os 
import time
from datetime import datetime

class GenerateGoals:
    def __init__(self, path, name_file_generated, encoding="ISO-8859-1" , sep=';'):
        if not os.path.exists(path):
            print('caminho ou arquivo inexistente')
        else:
            self.df = pd.read_csv(path, encoding=encoding, sep=sep)
            self.df['DTREF'] = pd.to_datetime(self.df['DTREF'], format="%d/%m/%Y")
            self.df['CODPROD'] = pd.to_numeric(self.df['CODPROD'])
            self.df['CODPARC'] = pd.to_numeric(self.df['CODPARC'])
            self.df['QTDPREV'] = self.df['QTDPREV'].apply(lambda x: float(x.replace(',', '.')))
            self.df['TOTALAUTINV'] = self.df['TOTALAUTINV'].apply(lambda x: float(x.replace(',', '.')))
            self.df['PREVREC'] = self.df['PREVREC'].apply(lambda x: float(x.replace(',', '.')))
            self.df['PERCCOMISSPARC_NTL'] = self.df['PERCCOMISSPARC_NTL'].apply(lambda x: float(str(x).replace(',', '.')))
            self.df['PERCENTUAL'] = self.df['PERCENTUAL'].fillna(0)
            
            self.file = name_file_generated
            
    def _format_values(self,valuer):
        if isinstance(valuer, (int, float)):
            return str(valuer)
        elif isinstance(valuer, str):
            return f"'{valuer}'"
        else:
            return str(valuer)
    
    def _format_duplicated(self, df):
        duplicatas = df[['DTREF','CODVEND', 'CODPROD', 'CODPARC']].duplicated(keep=False)
        second_occurrence = duplicatas & df[['DTREF','CODVEND', 'CODPROD', 'CODPARC']].duplicated(keep='first')
        
        df.loc[:,'contador'] = df.groupby(['DTREF','CODVEND', 'CODPROD', 'CODPARC']).cumcount()
        
        df.loc[second_occurrence, 'DTREF'] += pd.to_timedelta(df['contador'], unit='D')
        
        df = df.drop(columns='contador')
        
        return df
    
    def filter(self, initial_date, final_date, typesale, callback=None):
        df = self.df[(self.df['DTREF'] >= initial_date) & (self.df['DTREF'] <= final_date) & (self.df['TIPVENDA'] == typesale)]
        
        df = self._format_duplicated(df)
        
        df['DTREF'] = df['DTREF'].dt.strftime('%d/%m/%Y')
        
        name_columns = df.columns.tolist()
        name_columns = ','.join(name_columns)
        
        df_formatted = df.apply(lambda x: x.apply(self._format_values))
        df_formatted['DTREF'] = df_formatted['DTREF'].apply(lambda x: f"TO_DATE({x}, 'DD/MM/YYYY')")

        try:
            with open(self.file, 'w') as f:
                for values in [', '.join(map(str, linha))  for linha in df_formatted.values]:
                    string = f'INSERT INTO TGFMET ({name_columns}) VALUES ({values});\n'
                    f.write(string)
        except: 
            sg.popup('Erro ao executar script')
        
        result = '\nProcesso finalizado...'
        callback(result)

def generate_model_excell(path):
    data = {
    'CODMETA': [4],
    'DTREF': ['01/01/2024'],
    'CODPROD': [123434],
    'CODGRUPOPROD': [0],
    'CODLOCAL': [0],
    'CODPROJ': [0],
    'CODCENCUS': [0],
    'CODNAT': [0],
    'CODREG': [0],
    'CODGER': [0],
    'CODVEND': [54],
    'CODPARC': [123123],
    'CODUF': [0],
    'CODCID': [0],
    'CODPAIS': [0],
    'CODTIPPARC': [0],
    'QTDPREV': [550],
    'TOTALAUTINV': [85.65],
    'PREVDESP': [0],
    'QTDREAL': [0],
    'REALREC': [0],
    'REALDESP': [0],
    'PERCENTUAL': [None],
    'PREVREC': [47107.5],
    'SUPLEMENTODESP': [0],
    'ANTECIPDESP': [0],
    'TRANSFDESP': [0],
    'TRANSFSALDODESP': [0],
    'REDUCAODESP': [0],
    'COMPROMISSODESP': [0],
    'ANALITICO': ['S'],
    'TIPOMSG': ['Z'],
    'PERCAVISO': [0],
    'DIA': [0],
    'SEMANAMES': [0],
    'CODEMP': [0],
    'TIPVENDA': [1],
    'PERCCOMISSPARC_NTL': [1]
    }

    # Criar o DataFrame
    df = pd.DataFrame(data)

    # Salvar como CSV
    df.to_csv(path, index=False, sep=';')


#gerar = GerarMetas('metas/META SANKYA 2024.csv')

def main():
    layout = [
        [sg.Text('Arquivo csv:', size=(8,1)), sg.InputText(key='-PAPH-', enable_events=True), sg.FileBrowse(button_text='Arquivo')],
        [sg.Text('Data Inicial', size=(8,1)),
         sg.InputText(key='-DATE-INITIAL-',size=(15, 1), enable_events=True, disabled=True),
         sg.CalendarButton('Data', target='-DATE-INITIAL-', format='%d/%m/%Y')],
         [sg.Text('Data Final', size=(8,1)),
          sg.InputText(key='-DATE-FINAL-', size=(15, 1), enable_events=True, disabled=True), 
          sg.CalendarButton('Data', target='-DATE-FINAL-', format='%d/%m/%Y')],
         
         [sg.Radio('Comercio', '1', key='-BUSINESS-', default=True, enable_events=True), 
          sg.Radio('Representação', '2', key='-REPRESENTATION-', enable_events=True)],
        [sg.Button('Gerar', key='-BTN-TO-GENERATE-', disabled=True, enable_events=True),
         sg.Button("Gerar Modelo", key='-BTN-TO-GERENATE-MODEL-EXCELL-')]
    ]
    
    window = sg.Window('Gera código de metas', layout)
    
    while True:
            event, values = window.read()
    
            if event == sg.WINDOW_CLOSED:
                break
            elif event == '-BUSINESS-':
                window['-REPRESENTATION-'].update(value=False)
            elif event == '-REPRESENTATION-':
                window['-BUSINESS-'].update(value=False)
            elif event == '-BTN-TO-GENERATE-':
                filer_path = values['-PAPH-']
                data_initial = datetime.strptime(values['-DATE-INITIAL-'], "%d/%m/%Y")
                data_final = datetime.strptime(values['-DATE-FINAL-'], "%d/%m/%Y")
                selected_option_radio = 1 if values['-BUSINESS-'] == True else 2
                
                if not os.path.isfile(filer_path):
                    sg.popup_error('O arquivo não existe')
                else:
                    _, file_extension = os.path.splitext(filer_path)
                    if file_extension.lower() != '.csv':
                        sg.popup('Não é uma extensão csv')
                    else:
                        window['-BTN-TO-GENERATE-'].update(disabled=True)
                        name_file_generated = os.getcwd()+'//metas.txt'
                        generated = GenerateGoals(filer_path, name_file_generated)
                        thread_generated = threading.Thread(target = generated.filter, args=(data_initial,data_final, selected_option_radio, lambda result: window.write_event_value('-THREAD-FINALIZADA-', result),))
                        
                        thread_notepad = None
                        if os.path.isfile(name_file_generated):
                            
                            thread_notepad = threading.Thread(target = subprocess.run, args = (['notepad.exe', name_file_generated], ))
                         
                        thread_generated.daemon = True
                        thread_generated.start()
                        
                        if thread_notepad != None:
                            time.sleep(1)
                            thread_notepad.daemon = True
                            thread_notepad.start()
            elif event == '-THREAD-FINALIZADA-':
                if window['-BTN-TO-GENERATE-'].Disabled:
                    window['-BTN-TO-GENERATE-'].update(disabled=False)
            elif values['-PAPH-'] == None or values['-PAPH-'] == '' \
            or values['-DATE-INITIAL-'] == None or values['-DATE-FINAL-'] == None:
                window['-BTN-TO-GENERATE-'].update(disabled=True)
            elif values['-PAPH-'] != '' \
            and values['-DATE-INITIAL-'] !=  '' and values['-DATE-FINAL-'] !=  '':
                window['-BTN-TO-GENERATE-'].update(disabled=False)
            if event == '-BTN-TO-GERENATE-MODEL-EXCELL-':
                file_path = sg.popup_get_file(
                    "Salvar como",
                    save_as=True,
                    file_types=(("css", "*.css"), ("All Files", "*.*"))
                )

                if os.path.exists(os.path.dirname(file_path)):
                    generate_model_excell(file_path)
    window.close()

if __name__ == '__main__':
    main()

#gerar.filter(datetime(2024, 1, 1), datetime(2024, 1, 1), 2)