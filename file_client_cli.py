import socket
import json
import base64
import logging
import os

server_address=('localhost',6666)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received="" #empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("\nDaftar file di server:")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal mendapatkan daftar file")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {namafile} berhasil didownload")
        return True
    else:
        print(f"Gagal download file {filename}")
        return False

def remote_upload(filename=""):
    if not os.path.exists(filename):
        print(f"File {filename} tidak ditemukan")
        return False
        
    with open(filename, 'rb') as fp:
        file_content = base64.b64encode(fp.read()).decode()
    
    command_str=f"UPLOAD {filename} {file_content}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"File {filename} berhasil diupload")
        return True
    else:
        print("Gagal upload file:", hasil['message'])
        return False

def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"File {filename} berhasil dihapus")
        return True
    else:
        print("Gagal menghapus file:", hasil['message'])
        return False

def show_menu():
    print("\n=== FILE SERVER MENU ===")
    print("1. List File")
    print("2. Download File")
    print("3. Upload File")
    print("4. Delete File")
    print("0. Exit")
    print("----------------------")

if __name__=='__main__':
    server_address=('localhost',6666)
    
    while True:
        show_menu()
        try:
            choice = input("Pilih menu (0-4): ")
            
            if choice == "1":
                remote_list()
            
            elif choice == "2":
                remote_list()
                filename = input("Masukkan nama file yang akan didownload: ")
                remote_get(filename)
            
            elif choice == "3":
                filename = input("Masukkan path file yang akan diupload: ")
                remote_upload(filename)
            
            elif choice == "4":
                remote_list()
                filename = input("Masukkan nama file yang akan dihapus: ")
                remote_delete(filename)
            
            elif choice == "0":
                print("Terima kasih telah menggunakan layanan file server")
                break
            
            else:
                print("Pilihan tidak valid!")
                
        except Exception as e:
            print(f"Terjadi kesalahan: {str(e)}")
            print("Silakan coba lagi")