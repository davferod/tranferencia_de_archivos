#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import LabelFrame, Label, Text, Tk, ttk, StringVar
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import os
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


source = ""
destination = ""

class App:
    def __init__(self, root):
        self.window = root
        self.window.geometry('600x500')
        self.window.title('acelerador de transferencia archivos')
        self.source = source
        self.dest = destination
        self.source = StringVar()
        self.dest = StringVar()
        self.progress_var = StringVar()

        frame = LabelFrame(self.window, bg = 'gray26')
        frame.grid(row = 0, columnspan = 8, pady = 10)
        frame2 = LabelFrame(self.window, bg = 'gray26')
        frame2.grid(row = 1, columnspan = 8, pady = 10)
        frame3 = LabelFrame(self.window, bg = 'white')
        frame3.grid(row = 2, columnspan = 8, pady = 10, padx = 20)
        frame4 = LabelFrame(self.window, bg = 'white')
        frame4.grid(row = 3, columnspan = 8, pady = 10, padx = 20)
        frame5 = LabelFrame(self.window, bg = 'white')
        frame5.grid(row = 4, columnspan = 8, pady = 1)

        self.b_df1 = ttk.Button(frame, text='FUENTE', command=partial(self.load, 1))
        self.b_df1.focus()
        self.b_df1.grid(row = 1, column = 0, columnspan = 2)
        self.b_df2 = ttk.Button(frame, text='DESTINO', command=partial(self.load, 2))
        self.b_df2.grid(row = 3, column = 0, columnspan = 2)
        Label(frame, text= '# pdf en la fuente: ').grid(row = 4, column = 0, columnspan = 2, pady = 5)
        self.folder = Label(frame, text = '', width=5)
        self.folder.grid(row = 4, column = 1, columnspan = 6, pady = 5)
        Label(frame, text= '# pdf en la dest: ').grid(row = 5, column = 0, columnspan = 2, pady = 5)
        self.dest_file = Label(frame, text = '', width=5)
        self.dest_file.grid(row = 5, column = 1, columnspan = 6, pady = 5)
        self.progress_label = Label(frame, textvariable=self.progress_var, width=30)
        self.progress_label.grid(row = 6, column = 2, columnspan = 2, pady = 5)

        ttk.Button(frame2, text='cargar', command=self.data_dir).grid(row = 5, column = 0, columnspan = 2)
        ttk.Button(frame2, text='ejecutar', command=self.execute).grid(row = 5, column = 2, columnspan = 2)
        ttk.Button(frame5, text='validacion', command=self.destino).grid(row = 1, column = 2, columnspan = 2)

        Label(frame3, text= 'listado de archivos dir fuente').grid(row = 0, column = 0, columnspan = 2)
        self.textBox = Text(frame3, width=60, height=5)
        self.textBox.grid(row = 1, columnspan = 8)

        Label(frame3, text= 'listado de archivos dir destino').grid(row = 3, column = 0, columnspan = 2)
        self.textBox2 = Text(frame3, width=60, height=5)
        self.textBox2.grid(row = 4, columnspan = 8)

        self.indica = Label(frame, text = '', width=40,)
        self.indica.grid(row = 1, column = 2, columnspan = 6)
        self.indica2 = Label(frame, text = '', width=40,)
        self.indica2.grid(row = 3, column = 2, columnspan = 6)

        # Set default values
        self.progress_var.set('')
        # Set up logging
        logging.basicConfig(filename='transferencia.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    def load(self, button):
        file = filedialog.askdirectory(initialdir = dir)
        if button == 1:
            self.indica['text'] = file
        else:
            self.indica2['text'] = file

    def data_dir(self):
        loadFolder = self.indica['text']
        loadFolder2 = self.indica2['text']
        obj = os.scandir(loadFolder)
        self.source = r'{}'.format(loadFolder)
        self.dest = r'{}'.format(loadFolder2)
        init_count = 0
        for path in os.listdir(loadFolder):
            if os.path.isfile(os.path.join(loadFolder, path)):
                init_count += 1
        self.folder['text'] = init_count
        for entry in obj:
            if entry.is_file():
                self.textBox.insert("1.0", "'% s'\n" % entry.name)
        obj.close()

    def execute(self):
        t = threading.Thread(target=self.engine, args=(self.source,  self.dest))
        t.start()

    def destino(self):
        loadFolder2 = self.indica2['text']
        init_count = 0
        for path in os.listdir(loadFolder2):
            if os.path.isfile(os.path.join(loadFolder2, path)):
                init_count += 1
        self.dest_file['text'] = init_count
        obj = os.scandir(loadFolder2)
        for entry in obj:
            if entry.is_file():
                self.textBox2.insert("1.0", "'% s'\n" % entry.name)
        obj.close()
        messagebox.showinfo('ejecución exitosa', 'ejecucion exitosa')

    def engine(self, source_path, dest_path):
        directory = os.getcwd()
                #carga lista de archivos transferidos desde el log, si existe
        transferred_files = set()
        if os.path.exists('progress.log'):
            with open('progress.log', 'r') as f:
                for line in f:
                    filename = line.strip()
                    transferred_files.add(filename)

        # obtiene la lita de achivos de la fuente
        files = [f for f in os.listdir(source_path) if f.endswith('.pdf') and f not in transferred_files]
        num_files = len(files)
        files_transferred = 0
        # crea un banco de hilos con 5 trabajos
        with ThreadPoolExecutor(max_workers=5) as executor:
            # transfiere cada archivo asynchronously
            futures = {executor.submit(self.transfer_file, source_path, dest_path, filename): filename for filename in files}

            # Log progress and wait for completion of each transfer
            for future in as_completed(futures):
                filename = futures[future]
                try:
                    future.result()
                    transferred_files.add(filename)
                    with open('progress.log', 'a') as f:
                        f.write(filename + '\n')
                    logging.info(f'Transferred file: {filename}')
                    files_transferred += 1
                    progress_text = f'{files_transferred} / {num_files} archivos transferidos'
                    self.progress_var.set(progress_text)
                    self.window.update_idletasks()
                except Exception as e:
                    logging.error(f'Error transferring file: {filename}, error: {e}')
                else:
                    logging.info(f'Transfer complete: {filename}')

        # Update the progress label to indicate that the transfer is complete
        self.progress_var.set('Transfer complete')
        self.window.update_idletasks()

    def transfer_file(self, source_path, dest_path, filename):
        source_file = os.path.join(source_path, filename)
        # Transfer the file
        dest_file = os.path.join(dest_path, filename)
        with open(source_file, 'rb') as f:
            with open(dest_file, 'wb') as g:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    g.write(chunk)

def main():
    root = Tk()
    mi_app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
