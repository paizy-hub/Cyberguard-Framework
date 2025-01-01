import tkinter as tk
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import pyperclip
import mysql.connector
from mysql.connector import errors
import bcrypt  
import re
import os
import socket
import subprocess
import nmap
import cv2
from PIL import Image, ImageTk



font1 = ('Truculenta 12pt ExtraBold', 30, 'bold')
font0 = ('Truculenta 12pt ExtraBold', 27, 'bold')
font2 = ('Hammersmith One', 12)
font3 = ('Hammersmith One', 10)
font4 = ('Hammersmith One', 4)
font5 = ('Truculenta 12pt ExtraBold', 19, 'bold')
font6 = ('Truculenta 12pt ExtraBold', 23, 'bold')

#SQL
def initialize_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )

        cursor = conn.cursor()
        create_database(cursor)
        create_table(cursor)

        return conn, cursor
    except mysql.connector.Error as e:
        print(f"Error during database connection: {e}")
        messagebox.showerror("Database Connection Error", "Unable to connect to the database.")
        return None, None

def update_frame():
    global cap, label_video
    if cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Resize frame sesuai ukuran window
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            label_video.config(image=img)
            label_video.image = img
            root.after(10, update_frame)  # Jadwalkan frame berikutnya
        else:
            # Jika video mencapai akhir, reset ke awal
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            update_frame()  # Panggil kembali untuk melanjutkan loop


def initialize_video(video_path):
    global cap, label_video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", f"Cannot open video file: {video_path}")
        return
    

    label_video = Label(root)
    label_video.place(x=0, y=0, relwidth=1, relheight=1)
    update_frame()


def create_database(cursor):
    try:
        cursor.execute("SHOW DATABASES")
        temp = cursor.fetchall()
        databases = [item[0] for item in temp]

        if "pbl_kel10" not in databases:
            cursor.execute("CREATE DATABASE pbl_kel10")
        cursor.execute("USE pbl_kel10")
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")
        messagebox.showerror("Creating Database Error", "Unable to create the database.")

def create_table(cursor):
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = [item[0] for item in temp]

    if "users" not in tables:
        cursor.execute("""CREATE TABLE users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(21) UNIQUE,
            password VARCHAR(60),
            fullName VARCHAR(50)
        )""")

def login(cursor, data):
    cursor.execute("SELECT password FROM users WHERE username = %s", (data["username"],))
    result = cursor.fetchone()

    if result is not None and bcrypt.checkpw(data["password"].encode('utf-8'), result[0].encode('utf-8')):
        return True 
    else:
        return False  

def register(cursor, conn, data):
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password, fullName) VALUES (%s, %s, %s)", 
                   (data["username"], hashed_password.decode('utf-8'), data["fullName"]))
    conn.commit()


#GUI
class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Login')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)  # Allow resizing
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.master, width=425, height=500, bg="black")
        self.frame.place(x=450, y=80)

        self.heading = Label(self.frame, text='Login', fg='white', bg='black', font=font1)
        self.heading.place(x=164, y=50)

        self.username_entry = Entry(self.frame, width=17, fg='black', border=0, bg="white", font=font2)
        self.username_entry.place(x=115, y=150)
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', self.on_enter)
        self.username_entry.bind('<FocusOut>', self.on_leave)

        Frame(self.frame, width=189, height=2, bg='white').place(x=115, y=175)

        self.password_entry = Entry(self.frame, width=17, fg='black', border=0, bg="white", font=font2)
        self.password_entry.place(x=115, y=205)
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.on_enter)
        self.password_entry.bind('<FocusOut>', self.on_leave)

        Frame(self.frame, width=189, height=2, bg='white').place(x=115, y=230)

        Button(self.frame, width=14, pady=7, text='Login', bg='#fff', font=font3, fg='black', cursor='hand2', border=0, command=self.signin).place(x=150, y=290)
        

        label = Label(self.frame, text="Don't have an account?", fg='white', font=font3, bg='black')
        label.place(x=89, y=340)

        sign_up = Button(self.frame, width=6, text='Register', font=font3, border=0, bg='black', cursor='hand2', fg='blue', command=self.open_register_page)
        sign_up.place(x=248, y=340)

    def toggle_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')  
            self.toggle_button.config(text="🔒")  
        else:
            self.password_entry.config(show='*')  
            self.toggle_button.config(text="👁️")  


    def on_enter(self, event):
        if event.widget.get() in ['Username', 'Password']:
            event.widget.delete(0, 'end')
            event.widget.config(fg='black', show='*' if event.widget == self.password_entry else '')

    def on_leave(self, event):
        if not event.widget.get():
            event.widget.insert(0, 'Username' if event.widget == self.username_entry else 'Password')
            event.widget.config(fg='grey', show='' if event.widget == self.password_entry else '')

        self.toggle_button = Button(self.master, text="👁️", border=0, bg='white',fg='black', command=self.toggle_password)
        self.toggle_button.pack()
        self.toggle_button.place(x=720, y=285)

    def signin(self):
        data = {}
        data["username"] = self.username_entry.get()
        data["password"] = self.password_entry.get()
        
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()

        if not entered_username or not entered_password:
            messagebox.showerror("Login Failed", "Please fill a valid username and password.")
            self.open_login_page()  # Reopen the login page
            return

        if entered_username == 'Username' or entered_password == 'Password':
            messagebox.showerror("Login Failed", "Please fill a valid username and password.")
            return

        data = {"username": entered_username, "password": entered_password}
        result = login(cursor, data)

        if result:
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.destroy()
            HomePage(self.master, username=entered_username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

            self.open_login_page()

    def open_login_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        LoginPage(self.master)


    def open_register_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        RegisterPage(self.master)
         

class RegisterPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Register')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)  # Allow resizing
        self.create_widgets()
        
    def create_widgets(self):
        self.frame = Frame(self.master, width=425, height=500, bg="white")
        self.frame.place(x=450, y=80)

        self.heading = Label(self.frame, text='Register', fg='#000000', bg='white', font=font1)
        self.heading.place(x=145, y=50)

        self.username_entry = Entry(self.frame, width=21, fg='black', border=0, bg="white", font=font2)
        self.username_entry.place(x=115, y=150)
        self.username_entry.insert(0, 'Create Username')
        self.username_entry.bind('<FocusIn>', self.on_enter)
        self.username_entry.bind('<FocusOut>', self.on_leave)

        Frame(self.frame, width=180, height=2, bg='#000000').place(x=115, y=175)

        self.password_entry = Entry(self.frame, width=21, fg='black', border=0, bg="white", font=font2)
        self.password_entry.place(x=115, y=205)
        self.password_entry.insert(0, 'Create Password')
        self.password_entry.bind('<FocusIn>', self.on_enter)
        self.password_entry.bind('<FocusOut>', self.on_leave)

        Frame(self.frame, width=180, height=2, bg='black').place(x=115, y=230)

        self.fullname_entry = Entry(self.frame, width=21, fg='black', border=0, bg="white", font=font2)
        self.fullname_entry.place(x=115, y=260)
        self.fullname_entry.insert(0, 'Enter Full Name')
        self.fullname_entry.bind('<FocusIn>', self.on_enter)
        self.fullname_entry.bind('<FocusOut>', self.on_leave)

        Frame(self.frame, width=180, height=2, bg='black').place(x=115, y=285)

        Button(self.frame, width=14, pady=7, text='Register', font=font3, bg='#000000', fg='white', cursor='hand2', border=0, command=self.register).place(x=155, y=315)

        label = Label(self.frame, text="Already have an account?", font=font3, fg='black', bg='white')
        label.place(x=95, y=365)

        sign_in = Button(self.frame, width=6, text='Login', font=font3, border=0, bg='white', cursor='hand2', fg='blue', command=self.open_login_page)
        sign_in.place(x=260, y=365)

        self.username_entry.default_text = 'Create Username'
        self.password_entry.default_text = 'Create Password'
        self.fullname_entry.default_text = 'Enter Full Name'

    def on_enter(self, event):
        if event.widget.get() in ['Create Username', 'Create Password', 'Enter Full Name']:
            event.widget.delete(0, 'end')
            event.widget.config(fg='black', show='*' if event.widget == self.password_entry else '')

    def on_leave(self, event):
        if not event.widget.get():
            default_text = 'Create Username' if event.widget == self.username_entry else 'Create Password' if event.widget == self.password_entry else 'Enter Full Name'
            event.widget.insert(0, default_text)
            event.widget.config(fg='grey', show='' if event.widget == self.password_entry else '')

        self.toggle_button = Button(self.master, text="👁️", border=0, bg='white',fg='black', command=self.toggle_password)
        self.toggle_button.pack()
        self.toggle_button.place(x=730, y=285)

    def open_login_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        LoginPage(self.master)
    
    def open_register_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        RegisterPage(self.master)    

    def validate_password(self, password):
        # Buat cek pw ny 8 krkter ap g
        if len(password) < 8:
            return False, "Password harus memiliki setidaknya 8 karakter."

        # eini buat biar cek pw setidakny 1 angka
        if not re.search(r"\d", password):
            return False, "Password harus mengandung setidaknya satu angka."

        # ini cek stidknya pw 1 huruf
        if not re.search(r"[A-Za-z]", password):
            return False, "Password harus mengandung setidaknya satu huruf."

        # cek setidakny pw 1 krkter khusus
        if not re.search(r"[@$!%*?&]", password):
            return False, "Password harus mengandung setidaknya satu karakter khusus (@, $, !, %, *, ?, &)."

        # cek pw gbole ada spasii
        if " " in password:
            return False, "Password tidak boleh mengandung spasi."

        return True, "Password valid."

    def toggle_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')  
            self.toggle_button.config(text="🔒")  
        else:
            self.password_entry.config(show='*')  
            self.toggle_button.config(text="👁️") 

    def register(self):
        data = {}
        data["username"] = self.username_entry.get()
        data["password"] = self.password_entry.get()
        data["fullName"] = self.fullname_entry.get()

        default_username = self.username_entry.default_text
        default_password = self.password_entry.default_text
        default_fullname = self.fullname_entry.default_text

        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()
        entered_fullname = self.fullname_entry.get().strip()

        if not all([entered_username, entered_password, entered_fullname]) or \
           entered_username == default_username or entered_password == default_password or entered_fullname == default_fullname:
            messagebox.showerror("Registration Failed", "Please fill in all fields.")
            self.open_register_page()
            return

        # Validate password strength
        is_valid, message = self.validate_password(entered_password)
        if not is_valid:
            messagebox.showerror("Registration Failed", message)
            return

        try:
            data = {"username": entered_username, "password": entered_password, "fullName": entered_fullname}
            register(cursor, conn, data)

            messagebox.showinfo("Registration Successful", "Account has been successfully registered!")

            self.open_login_page()

        except errors.IntegrityError as e:
            if e.errno == 1062:  # MySQL error code for duplicate entry
                messagebox.showerror("Registration Failed", "Username already exists. Please choose another username.")
                self.open_register_page()

            else:
                messagebox.showerror("Registration Failed", f"An error occurred during registration: {e}")
        except Exception as e:
            messagebox.showerror("Registration Failed", f"An unexpected error occurred: {e}")

class HomePage:
    def __init__(self, master, username):
        self.master = master
        self.master.title('Home Page')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)  # Allow resizing
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.master, width=425, height=500, bg="#000000")
        self.frame.place(x=450, y=80)

        self.heading = Label(self.frame, text='Welcome To The', fg='#fff', bg='#000000', font=font1)
        self.heading.place(x=90, y=50)
        self.heading = Label(self.frame, text='Home Page', fg='#fff', bg='#000000', font=font1)
        self.heading.place(x=130, y=100)

        self.username_label = Label(self.frame, text=f'Logged in as: {self.username}', fg='white', bg='black', font=font2)
        self.username_label.place(x=15, y=170)

        Button(self.frame, width=14, pady=7, text='Go to Tools', bg='#fff', fg='#000000',
               cursor='hand2', font=font3, border=0, command=self.go_to_tools).place(x=160, y=270)
        
        Button(self.frame, width=14, pady=7, text='About Us', bg='#fff', fg='#000000',
               cursor='hand2', font=font3, border=0, command=self.go_to_about_us).place(x=160, y=310)

        Button(self.frame, width=14, pady=7, text='Log Out', bg='#fff', fg='#000000',
               cursor='hand2', font=font3, border=0, command=self.log_out).place(x=160, y=350) 

    def go_to_tools(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        ToolsPage(self.master, username=self.username)

    def go_to_about_us(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        AboutUsPage(self.master, username=self.username)  # Assuming AboutUsPage is defined elsewhere

    def log_out(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        LoginPage(self.master)  # Redirect to the Login Page

class ToolsPage:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.setup_page()

    def setup_page(self):
        # Window configuration
        self.master.title("Tools")
        self.master.configure(bg="#fff")
        self.master.resizable(True, True)

        # Create main frame
        self.frame = Frame(self.master, bg="#000000")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Heading
        Label(self.frame, text="Tools", fg="#fff", bg="black", font=font1).grid(row=0, column=0, columnspan=2, pady=20)

        # Buttons
        self.create_button("Ping to get IP", self.open_Ping_To_Get_Ip, 1)
        self.create_button("Port Scanner (nmap)", self.open_port_scanner, 2)
        self.create_button("Vulnerability Check", self.open_vulnerability_check, 3)
        self.create_button("Crypto Tools", self.open_Crypto_Tools, 4)
        self.create_button("Back", self.back_to_home, 5)

    def create_button(self, text, command, row):
        Button(self.frame, width=25, pady=7, text=text, bg="#fff", fg="#000000",
               cursor="hand2", font=font3, border=0, command=command).grid(row=row, column=0, padx=20, pady=10)

    def back_to_home(self):
        self.clean_up()
        HomePage(self.master, username=self.username)

    def open_Ping_To_Get_Ip(self):
        self.clean_up()
        PingToGetIP(self.master, username=self.username)

    def open_port_scanner(self):
        self.clean_up()
        PortScan(self.master, username=self.username)

    def open_vulnerability_check(self):
        self.clean_up()
        VulnerabilityCheck(self.master, username=self.username)

    def open_Crypto_Tools(self):
        self.clean_up()
        CryptoTools(self.master, username=self.username)

    def clean_up(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()

class CryptoTools:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.setup_page()

    def setup_page(self):
        # Window configuration
        self.master.title("Crypto Tools")
        self.master.configure(bg="#fff")
        self.master.resizable(True, True)

        # Create main frame
        self.frame = Frame(self.master, bg="#000000")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Heading
        Label(self.frame, text="Crypto Tools", fg="#fff", bg="black", font=font1).grid(row=0, column=0, columnspan=2, pady=20)

        # Buttons
        self.create_button("Binary Converter", self.open_Binary_Text_Converter, 1)
        self.create_button("Morse Converter", self.open_Morse_Converter, 2)
        self.create_button("Alphabet Phonetic Converter", self.open_Alphabet_Phonetik_Converter, 3)
        self.create_button("Substitution Cipher", self.open_substitution_chipper, 4)
        self.create_button("Back", self.back_to_tools, 5)

    def create_button(self, text, command, row):
        Button(self.frame, width=25, pady=7, text=text, bg="#fff", fg="#000000",
               cursor="hand2", font=font3, border=0, command=command).grid(row=row, column=0, padx=20, pady=10)

    def back_to_tools(self):
        self.clean_up()
        ToolsPage(self.master, username=self.username)

    def open_Binary_Text_Converter(self):
        self.clean_up()
        BinaryTextConverter(self.master, username=self.username)

    def open_Morse_Converter(self):
        self.clean_up()
        MorseConverter(self.master, username=self.username)

    def open_Alphabet_Phonetik_Converter(self):
        self.clean_up()
        AlphabetPhoneticConverter(self.master, username=self.username)

    def open_substitution_chipper(self):
        self.clean_up()
        SubstitutionCipher(self.master, username=self.username)

    def clean_up(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()


class BinaryTextConverter:
    def __init__(self, master, username):
        self.master = master
        self.master.title('Binary Text Converter')
        self.master.attributes('-fullscreen', False)
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        self.frame = tk.Frame(self.master, width=425, height=500, bg="white")
        self.frame.place(x=450, y=80)

        # Heading
        self.heading = tk.Label(self.frame, text='Binary Text Converter', fg='#000000', 
                              bg='white', font=font1)
        self.heading.place(x=50, y=20)

        # Input section
        tk.Label(self.frame, text="Enter text:", bg='white', 
                font=font2).place(x=27, y=80)
        self.text_frame = tk.Frame(self.frame, width=180, height=90, bg='black')
        self.text_frame.place(x=30, y=110)
        self.text_box = tk.Text(self.text_frame, width=32, height=4, wrap=tk.WORD, 
                               fg='black', borderwidth=2, relief="solid", bg="white", 
                               font=font2)
        self.text_box.pack()

        # Paste button
        self.paste_button = tk.Button(self.frame, text="Paste", bg='white', fg='blue',
                                    cursor='hand2', border=0, command=self.paste_from_clipboard)
        self.paste_button.place(x=348, y=170)

        # Conversion type dropdown
        tk.Label(self.frame, text="Select conversion:", bg='white', 
                font=font2).place(x=27, y=200)
        self.conversion_type = tk.StringVar(value="text_to_binary")
        self.conversion_menu = tk.OptionMenu(self.frame, self.conversion_type,
                                           "text_to_binary", "binary_to_text",
                                           "text_to_number", "number_to_text")
        self.conversion_menu.place(x=30, y=230)

        # Action buttons
        tk.Button(self.frame, width=14, pady=7, text='Convert', bg='#000000',
                 fg='white', cursor='hand2', border=0, font=font3,
                 command=self.convert).place(x=28, y=270)
        tk.Button(self.frame, width=14, pady=7, text='Clear', bg='#000000',
                 fg='white', cursor='hand2', border=0,font=font3,
                 command=self.reset_fields).place(x=159, y=270)
        tk.Button(self.frame, width=14, pady=7, text='Back', bg='#000000',
                 fg='white', cursor='hand2', border=0,font=font3,
                 command=self.back_to_tools).place(x=290, y=270)

        # Result section
        tk.Label(self.frame, text="Result:", bg='white', 
                font=font2).place(x=27, y=320)
        self.result_frame = tk.Frame(self.frame, width=180, height=90, bg='black')
        self.result_frame.place(x=30, y=350)
        self.result_box = tk.Text(self.result_frame, width=32, height=4, wrap=tk.WORD,
                                 fg='black', borderwidth=2, relief="solid", bg="white",
                                 font=font2)
        self.result_box.pack()
        self.result_box.config(state=tk.DISABLED)

        # Copy button
        self.copy_button = tk.Button(self.frame, text="Copy", bg='white', fg='blue',
                                   cursor='hand2', border=0, command=self.copy_to_clipboard)
        self.copy_button.place(x=348, y=408)

    def convert(self):
        text = self.text_box.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Convert Failed", "Please enter text to convert.")
            return

        conversion_type = self.conversion_type.get()
        try:
            if conversion_type == "text_to_binary":
                result = ' '.join(format(ord(char), '08b') for char in text)
            elif conversion_type == "binary_to_text":
                binary_values = text.split()
                result = ''.join(chr(int(binary, 2)) for binary in binary_values)
            elif conversion_type == "text_to_number":
                result = ' '.join(str(ord(char)) for char in text)
            else:  # number_to_text
                numbers = text.split()
                result = ''.join(chr(int(num)) for num in numbers)

            self.result_box.config(state=tk.NORMAL)
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, result)
            self.result_box.config(state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Error", "Invalid input format")

    def paste_from_clipboard(self):
        try:
            clipboard_text = pyperclip.paste()
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, clipboard_text)
        except:
            messagebox.showerror("Error", "Failed to paste from clipboard")

    def copy_to_clipboard(self):
        result_text = self.result_box.get("1.0", tk.END).strip()
        if result_text:
            pyperclip.copy(result_text)
            messagebox.showinfo("Copy Successful", "Text copied to clipboard.")
        else:
            messagebox.showwarning("Copy Failed", "No text to copy.")

    def reset_fields(self):
        self.text_box.delete("1.0", tk.END)
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.config(state=tk.DISABLED)

    def back_to_tools(self):
        self.frame.destroy()
        # Assuming ToolsPage class exists
        ToolsPage(self.master, username=self.username)

class MorseConverter:
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..',
        '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
    }

    def __init__(self, master, username):
        self.master = master
        self.master.title('Morse Converter')
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.master, width=425, height=500, bg="white")
        self.frame.place(x=450, y=80)

        tk.Label(self.frame, text="Morse Converter", bg='white', fg='black', 
                 font=font1).place(x=90, y=20)

        tk.Label(self.frame, text="Enter text:", bg='white', font=font2).place(x=27, y=80)
        self.text_box = tk.Text(self.frame, width=32, height=4, wrap=tk.WORD, borderwidth=2, relief="solid", 
                                fg='black', bg='white', font=font2)
        self.text_box.place(x=30, y=110)

        tk.Label(self.frame, text="Result:", bg='white', font=font2).place(x=27, y=200)
        self.result_box = tk.Text(self.frame, width=32, height=6, wrap=tk.WORD, borderwidth=2, relief="solid",
                                  fg='black', bg='white', font=font2)
        self.result_box.place(x=30, y=230)
        self.result_box.config(state=tk.DISABLED)

        tk.Button(self.frame, text="Convert to Morse", bg='#000000', font=font3, fg='white', command=self.text_to_morse).place(x=32, y=360)
        tk.Button(self.frame, text="Convert to Text", bg='#000000', fg='white', font=font3, command=self.morse_to_text).place(x=190, y=360)
        tk.Button(self.frame, text="Clear", bg='#000000', fg='white',font=font3, command=self.clear_fields).place(x=342, y=360)

        tk.Button(self.frame, text="Back to Tools", bg='#000000', font=font3, fg='white', command=self.back_to_tools).place(x=164, y=425)

    def text_to_morse(self):
        text = self.text_box.get("1.0", "end-1c").strip().upper()
        result = ' '.join(self.MORSE_CODE_DICT.get(char, '') for char in text)
        self.display_result(result)

    def morse_to_text(self):
        morse = self.text_box.get("1.0", "end-1c").strip()
        reverse_dict = {v: k for k, v in self.MORSE_CODE_DICT.items()}
        try:
            result = ''.join(reverse_dict.get(code, '') for code in morse.split())
            self.display_result(result)
        except Exception:
            messagebox.showerror("Error", "Invalid Morse Code")

    def display_result(self, result):
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, result)
        self.result_box.config(state=tk.DISABLED)

    def clear_fields(self):
        self.text_box.delete("1.0", tk.END)
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.config(state=tk.DISABLED)

    def back_to_tools(self):
        self.frame.destroy()
        ToolsPage(self.master, username=self.username)

class AlphabetPhoneticConverter:
    PHONETIC_ALPHABET = {
        'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
        'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
        'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
        'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
        'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee',
        'Z': 'Zulu', ' ': '/'
    }

    def __init__(self, master, username):
        self.master = master
        self.master.title('Phonetic Converter')
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.master, width=425, height=500, bg="white")
        self.frame.place(x=450, y=80)

        tk.Label(self.frame, text="Phonetic Converter", bg='white', fg='black', 
                 font=font1).place(x=70, y=10)

        tk.Label(self.frame, text="Enter text:", bg='white', font=font2).place(x=27, y=100)
        self.text_box = tk.Text(self.frame, width=32, height=5, wrap=tk.WORD, 
                                fg='black', borderwidth=2, relief="solid", bg='white', font=font2)
        self.text_box.place(x=30, y=130)

        tk.Label(self.frame, text="Result:", bg='white', font=font2).place(x=27, y=240)
        self.result_box = tk.Text(self.frame, width=32, height=5, wrap=tk.WORD, 
                                  fg='black', bg='white', borderwidth=2, relief="solid" ,font=font2) 
        self.result_box.place(x=30, y=270)
        self.result_box.config(state=tk.DISABLED)

        tk.Button(self.frame, text="Convert to Phonetic", font=font3, border=0, bg='#000000', fg='white', command=self.text_to_phonetic).place(x=30, y=380)
        tk.Button(self.frame, text="Clear", bg='#000000', font=font3, border=0, fg='white', command=self.clear_fields).place(x=178, y=380)
        tk.Button(self.frame, text="Back to Tools", bg='#000000', font=font3, border=0, fg='white', command=self.back_to_tools).place(x=160, y=430)

    def text_to_phonetic(self):
        text = self.text_box.get("1.0", "end-1c").strip().upper()
        result = ' '.join(self.PHONETIC_ALPHABET.get(char, '') for char in text)
        self.display_result(result)

    def display_result(self, result):
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, result)
        self.result_box.config(state=tk.DISABLED)

    def clear_fields(self):
        self.text_box.delete("1.0", tk.END)
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.config(state=tk.DISABLED)

    def back_to_tools(self):
        self.frame.destroy()
        ToolsPage(self.master, username=self.username)

class SubstitutionCipher:
    def __init__(self, master, username):
        self.master = master
        self.master.title('Substitution Cipher')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)  # Allow resizing
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.master, width=425, height=500, bg="white")
        self.frame.place(x=450, y=80)

        self.heading = Label(self.frame, text='Substitution Cipher', fg='#000000', bg='white', font=font1)
        self.heading.place(x=75, y=20)

        Label(self.frame, text="Enter the text:", bg='white', font=font2).place(x=27, y=80)
        self.text_frame = Frame(self.frame, width=180, height=90, bg='black')
        self.text_frame.place(x=30, y=110)
        self.text_box = Text(self.text_frame, width=32, height=4, wrap=WORD, fg='black', borderwidth=2, relief="solid", bg="white", font=font2)
        self.paste_button = Button(self.frame, text="Paste", bg='white', fg='blue', cursor='hand2', border=0, command=self.paste_from_clipboard)
        self.paste_button.place(x=348, y=170)
        self.text_box.pack()

        Label(self.frame, text="Enter the shift value:", bg='white', font=font2).place(x=27, y=200) 
        self.shift_frame = Frame(self.frame, width=180, height=30, bg='black')
        self.shift_frame.place(x=30, y=230)
        self.shift_box = Text(self.shift_frame, width=10, height=1, wrap=WORD, fg='black', borderwidth=2, relief="solid", bg="white", font=font2)
        self.shift_box.pack()

        Button(self.frame, width=14, pady=7, text='Encrypt', bg='#000000', fg='white', cursor='hand2', border=0, command=self.encrypt_text).place(x=30, y=270)
        Button(self.frame, width=14, pady=7, text='Clear', bg='#000000', fg='white', cursor='hand2', border=0, command=self.reset_fields).place(x=160, y=270)
        Button(self.frame, width=14, pady=7, text='Decrypt', bg='#000000', fg='white', cursor='hand2', border=0, command=self.decrypt_text).place(x=290, y=270)
        Button(self.frame, width=14, pady=7, text='Back', bg='#000000', fg='white', cursor='hand2', border=0, command=self.back_to_tools).place(x=160, y=445)

        Label(self.frame, text="Result:", bg='white', font=font2).place(x=27, y=320)
        self.result_frame = Frame(self.frame, width=180, height=90, bg='black')
        self.result_frame.place(x=30, y=350)
        self.result_box = Text(self.result_frame, width=32, height=4, wrap=WORD, fg='black', borderwidth=2, relief="solid", bg="white", font=font2)
        self.copy_button = Button(self.frame, text="Copy", bg='white', fg='blue', cursor='hand2', border=0, command=self.copy_to_clipboard)
        self.copy_button.place(x=348, y=408) 
        self.result_box.pack()
        self.result_box.config(state=DISABLED)  # Make the result box read-only

    def paste_from_clipboard(self):
            clipboard_text = pyperclip.paste()
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, clipboard_text)

    def copy_to_clipboard(self):
        # Copy text from the "Result:" text box to the clipboard.
        result_text = self.result_box.get("1.0", END)
        self.master.clipboard_clear()
        self.master.clipboard_append(result_text)
        self.master.update()  # Update the clipboard content

        if result_text.strip():  # Check if there is text to copy
            pyperclip.copy(result_text)
            messagebox.showinfo("Copy Successful", "Text copied to clipboard.")
        else:
            messagebox.showwarning("Copy Failed", "No text to copy.")

    def back_to_tools(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        ToolsPage(self.master, username=self.username)

    def reset_fields(self):
        #Reset the text fields for "Enter the text:" and "Results:".
        self.text_box.delete("1.0", END)
        self.shift_box.delete("1.0", END)
        self.result_box.config(state=NORMAL)
        self.result_box.delete("1.0", END)
        self.result_box.config(state=DISABLED)

    def reset_shift_field(self):
        self.shift_box.config(state=NORMAL)
        self.shift_box.delete(1.0, END)

    def encrypt_text(self):
        plaintext = self.text_box.get("1.0", "end-1c")  # Get the text from the text box
        
        if not plaintext:
            messagebox.showwarning("Encrypt Failed", "Please enter text to encrypt.")
            self.reset_shift_field()
            return

        shift = self.get_shift_value()

        if plaintext and shift is not None:
            encrypted_text = self.sub_encrypt(plaintext, shift)
            self.result_box.config(state=NORMAL)  # Enable editing temporarily
            self.result_box.delete(1.0, END)
            self.result_box.insert(END, encrypted_text)
            self.result_box.config(state=DISABLED)  # Make the result box read-only

    def decrypt_text(self):
        ciphertext = self.text_box.get("1.0", "end-1c")  # Get the text from the text box
        
        if not ciphertext:
            messagebox.showwarning("Decrypt Failed", "Please enter text to decrypt.")
            self.reset_shift_field()
            return
        
        shift = self.get_shift_value()

        if ciphertext and shift is not None:
            decrypted_text = self.sub_decrypt(ciphertext, shift)
            self.result_box.config(state=NORMAL)  # Enable editing temporarily
            self.result_box.delete(1.0, END)
            self.result_box.insert(END, decrypted_text)
            self.result_box.config(state=DISABLED)  # Make the result box read-only

    def get_shift_value(self):
        try:
            shift = int(self.shift_box.get("1.0", "end-1c"))  # Get the text from the text box
            return shift
        except ValueError:
            messagebox.showerror("Error", "Invalid shift value. Please enter a valid integer.")
            self.reset_shift_field()

    def sub_encrypt(self, plaintext, shift):
        encrypted_text = ''.join(self.shift_char(char, shift) for char in plaintext)
        return encrypted_text

    def sub_decrypt(self, ciphertext, shift):
        decrypted_text = ''.join(self.shift_char(char, -shift) for char in ciphertext)
        return decrypted_text

    def shift_char(self, char, shift):
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            return chr((ord(char) - start + shift) % 26 + start)
        else:
            return char

class PingToGetIP:
    def __init__(self, master, username):
        self.master = master
        self.master.title('Ping to Get IP')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#fff")
        self.master.resizable(True, True)  # Allow resizing
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.master, width=425, height=500, bg="#000000")
        self.frame.place(x=450, y=80)

        self.heading = tk.Label(self.frame, text='Ping to Get IP', fg='#fff', bg='black', font=font1)
        self.heading.place(x=120, y=20)

        tk.Label(self.frame, text="Enter the Web Domain:", bg='black', fg='white', font=font2).place(x=27, y=80)
        self.domain_entry = tk.Entry(self.frame, width=33, borderwidth=2, relief="solid", fg='black', bg='white', font=font2)
        self.domain_entry.place(x=30, y=110)

        tk.Button(self.frame, width=14, pady=7, text='Get IP', bg='#fff', fg='black', 
                  cursor='hand2', font=font3, border=0, command=self.get_ip).place(x=160, y=140)

        tk.Label(self.frame, text="Results:", bg='black', fg='white', font=font2).place(x=27, y=200)
        self.result_frame = tk.Frame(self.frame, width=280, height=150, bg='#000000')
        self.result_frame.place(x=30, y=230)
        self.result_box = tk.Text(self.result_frame, width=33, height=10, wrap=tk.WORD, fg='#000000', 
                                  borderwidth=2, relief="solid", bg="white", font=font2)
        self.result_box.pack()
        self.result_box.config(state=tk.DISABLED)

        tk.Button(self.frame, width=14, pady=7, text='Back', bg='#fff', fg='#000000', 
                  cursor='hand2', font=font3, border=0, command=self.back_to_tools).place(x=160, y=440) 

    def get_ip(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Error", "Please enter a valid web domain.")
            return

        try:
            ip_address = socket.gethostbyname(domain)
            result_text = f"The IP address of {domain} is:\n{ip_address}"
        except socket.gaierror:
            result_text = f"Failed to resolve the IP address for {domain}."

        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result_text)
        self.result_box.config(state=tk.DISABLED)

    def back_to_tools(self):
        self.clean_up()
        ToolsPage(self.master, username=self.username)

    def clean_up(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()


class PortScan:
    def __init__(self, master, username):
        self.master = master
        self.master.title('Port Scan')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#fff")
        self.master.resizable(True, True)  # Allow resizing
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.master, width=425, height=500, bg="#000000")
        self.frame.place(x=450, y=80)

        self.heading = Label(self.frame, text='Port Scanner', fg='#fff', bg='black', font=font1)
        self.heading.place(x=120, y=20)

        Label(self.frame, text="Enter the IP Address:", bg='black', fg= 'white', font=font2).place(x=27, y=80)
        self.ip_entry = Entry(self.frame, width=33, borderwidth=2, relief="solid", fg='black', bg='white', font=font2)
        self.ip_entry.place(x=30, y=110)

        Button(self.frame, width=14, pady=7, text='Scan Ports', bg='#fff', fg='black', 
               cursor='hand2', font=font3, border=0, command=self.scan_ports).place(x=160, y=140)

        Label(self.frame, text="Results:", bg='black',fg='white', font=font2).place(x=27, y=200)
        self.result_frame = Frame(self.frame, width=280, height=150, bg='#000000')
        self.result_frame.place(x=30, y=230)
        self.result_box = Text(self.result_frame, width=33, height=10, wrap=WORD, fg='#000000', 
                               borderwidth=2, relief="solid", bg="white", font=font2)
        self.result_box.pack()
        self.result_box.config(state=DISABLED)

        Button(self.frame, width=14, pady=7, text='Back', bg='#fff', fg='#000000', 
               cursor='hand2', font=font3, border=0, command=self.back_to_tools).place(x=160, y=440) 

    def scan_ports(self):
        ip_address = self.ip_entry.get().strip()
        if not ip_address:
            messagebox.showerror("Error", "Please enter a valid IP address.")
            return

        self.result_box.config(state=NORMAL)
        self.result_box.delete(1.0, END)

        # Menggunakan nmap untuk memindai port
        nm = nmap.PortScanner()
        try:
            nm.scan(ip_address, '1-1024')  # Memindai port dari 1 hingga 1024
            open_ports = [port for port in nm[ip_address]['tcp'] if nm[ip_address]['tcp'][port]['state'] == 'open']
            
            if open_ports:
                result_text = f"Open ports on {ip_address}:\n" + "\n".join(map(str, open_ports))
            else:
                result_text = f"No open ports found on {ip_address}."
        except Exception as e:
            result_text = f"Error scanning ports: {str(e)}"

        self.result_box.insert(END, result_text)
        self.result_box.config(state=DISABLED)

    def back_to_tools(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        ToolsPage(self.master, username=self.username)

class VulnerabilityCheck:
    def __init__(self, master, username):
        self.master = master
        self.master.title('Vulnerability scan')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#fff")
        self.master.resizable(True, True)  # Allow resizing
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.master, width=450, height=550, bg="#000000")  # Perbesar ukuran frame
        self.frame.place(x=450, y=80)

        self.heading = Label(self.frame, text='Vulnerability Check', fg='#fff', bg='black', font=font1)
        self.heading.place(x=80, y=20)

        Label(self.frame, text="Enter the file/directory path:", bg='black', fg='white', font=font2).place(x=27, y=80)
        self.ip_entry = Entry(self.frame, width=35, borderwidth=2, relief="solid", fg='black', bg='white', font=font2)
        self.ip_entry.place(x=30, y=110)

        Button(self.frame, width=18, pady=7, text='Check Vulnerabilities', bg='#fff', fg='black', 
               cursor='hand2', font=font3, border=0, command=self.check_vulnerabilities).place(x=160, y=140)

        Label(self.frame, text="Results:", bg='black', fg='white', font=font2).place(x=27, y=200)

        # Frame untuk menampung Text dan Scrollbar, diperbesar sedikit
        self.result_frame = Frame(self.frame, width=320, height=180, bg='#000000')  # Perbesar ukuran frame
        self.result_frame.place(x=30, y=230)

        # Scrollbar untuk Text Box
        self.scrollbar = Scrollbar(self.result_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Memperbesar ukuran Text widget
        self.result_box = Text(self.result_frame, width=35, height=12, wrap=WORD, fg='#000000', 
                               borderwidth=2, relief="solid", bg="white", font=font2, yscrollcommand=self.scrollbar.set)
        self.result_box.pack()
        self.result_box.config(state=DISABLED)

        # Menghubungkan scrollbar dengan Text widget
        self.scrollbar.config(command=self.result_box.yview)

        Button(self.frame, width=14, pady=7, text='Back', bg='#fff', fg='#000000', 
               cursor='hand2', font=font3, border=0, command=self.back_to_tools).place(x=175, y=480)

    def check_vulnerabilities(self):
        file_path = self.ip_entry.get().strip()
        if not file_path:
            messagebox.showerror("Error", "Please enter a valid file or directory path.")
            return

        self.result_box.config(state=NORMAL)
        self.result_box.delete(1.0, END)

        # Menjalankan Bandit sebagai subprocess dan menangkap output
        command = f"bandit -r {file_path}"
        try:
            # Menjalankan Bandit sebagai subprocess dan menangkap output
            result = subprocess.run(command, shell=True, text=True, capture_output=True)

            # Memasukkan hasil output Bandit ke dalam result_box
            self.result_box.insert(END, result.stdout)
            self.result_box.insert(END, result.stderr)  # Jika ada error
            self.result_box.config(state=DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Error checking vulnerabilities: {str(e)}")
            self.result_box.config(state=DISABLED)

    def back_to_tools(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        ToolsPage(self.master, username=self.username)

class AboutUsPage:
    def __init__(self, master, username):
        self.master = master
        self.master.title('About Us')
        self.master.attributes('-fullscreen', False)  # Allow maximizing
        self.master.configure(bg="#000000")
        self.master.resizable(True, True)  # Allow resizing
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.master, width=425, height=500, bg="white")
        self.frame.place(x=450, y=80)

        self.heading = Label(self.frame, text='Project Based Learning', bg='white', font=font5)
        self.heading.place(x=115, y=40)
        self.heading = Label(self.frame, text='Kelompok 10 RKS 1-A Pagi', bg='white', font=font6)
        self.heading.place(x=70, y=75)
        self.heading = Label(self.frame, text='Muhammad Rizqy Nur Faiz', bg='white', font=font2)
        self.heading.place(x=120, y=165) 
        self.heading = Label(self.frame, text= (4332401025), font=font3)
        self.heading.place(x=167, y=190)
        self.heading = Label(self.frame, text='Devi Natalya', bg='white', font=font2)
        self.heading.place(x=159, y=210)
        self.heading = Label(self.frame, text= (4332401002), font=font3)
        self.heading.place(x=167, y=234)
        self.heading = Label(self.frame, text='Gina Thasafiya', bg='white', font=font2)
        self.heading.place(x=155, y=255)
        self.heading = Label(self.frame, text= (4332401003), font=font3)
        self.heading.place(x=167, y=280)
        self.heading = Label(self.frame, text='Nursyafika Wahyuni', bg='white', font=font2)
        self.heading.place(x=140, y=303)
        self.heading = Label(self.frame, text= (4332401007), font=font3)
        self.heading.place(x=167, y=330)

        
        Button (self.frame, width=14, pady=5, text='Back', bg='#000000', fg='white', font=font3, cursor='hand2', border=0, command=self.back_to_home).place(x=148, y=380)
      
    def back_to_home(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        HomePage(self.master, username=self.username)

if __name__ == "__main__":
    try:
        conn, cursor = initialize_connection()
        if conn and cursor:  
            root = tk.Tk()
            video_path ="vidio.mp4"
            initialize_video(video_path)  
            app = LoginPage(root)
            root.mainloop()
            if cap:  
                cap.release()
            cv2.destroyAllWindows()
        else:
            print("Koneksi database gagal!")
    except Exception as e:
        print(f"Unexpected error: {e}")
        messagebox.showerror("Error", "An unexpected error occurred. Please check the logs.")
    finally:
        if conn:
            conn.close()
