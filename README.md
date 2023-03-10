# Acelerador de tranferencia de archivos

Este script permite transferir archivos PDF desde una carpeta de origen a una carpeta de destino, y proporciona una interfaz de usuario gráfica para realizar la tarea.

## Requisitos

- Python 3.x
- tkinter
- concurrent.futures
- threading
- os
- logging

## Cómo usar

1. Ejecutar el archivo `main.py` en Python.
2. Seleccionar la carpeta de origen con el botón "FUENTE".
3. Seleccionar la carpeta de destino con el botón "DESTINO".
4. Clic en el botón "cargar" para obtener la lista de archivos en la carpeta de origen.
5. Clic en el botón "ejecutar" para transferir los archivos PDF de la carpeta de origen a la carpeta de destino.
6. Clic en el botón "validación" para comprobar si los archivos se han transferido correctamente.

## Autor

Este script fue creado por DAVFEROD.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE.md](LICENSE.md) para más detalles.


This program is designed to manage and move PDF files between two directories, which are called source and destination.

The program GUI is built using the Tkinter library. Once the user selects the source and destination directories, the program scans the source directory and displays the number of PDF files in it. The user can then load the list of files present in the source directory and check the list of files in the destination directory.

After loading the files, the user can execute the program to move the PDF files to the destination directory. The program uses threads to execute the task in the background while displaying the progress in the GUI. The progress is displayed using a label widget.

The program also has a validation feature that checks the files in the destination directory to verify that the files were transferred successfully.

## Requirements
The following Python libraries are required to run the program:

tkinter
threading
logging
os
concurrent.futures
functools

## How to use
To use this program, follow these steps:

Run the program by executing the main.py file.
Select the source directory using the 'FUENTE' button.
Select the destination directory using the 'DESTINO' button.
Click the 'cargar' button to load the list of files in the source directory.
Click the 'ejecutar' button to move the files to the destination directory.
(Optional) Click the 'validacion' button to verify that the files were transferred successfully.
Acknowledgements
This program was created by DAVFEROD as part of acelerador de transferencia de archivos.