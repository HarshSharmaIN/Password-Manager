from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    random_letters = [choice(letters) for _ in range(randint(8, 10))]
    random_chars = [choice(symbols) for _ in range(randint(2, 4))]
    random_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = random_letters + random_chars + random_numbers
    shuffle(password_list)
    password = ''.join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title='Password Manager', message='Password Copied to Clipboard')

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website_name = website_input.get().title()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website_name: {
            'email': email,
            'password': password
        }
    }

    if len(website_name) == 0 or len(password) == 0:
        messagebox.showwarning(title='Empty Field', message="Website Name or Password can't be empty!")
    else:
        confirmation = messagebox.askokcancel(title=f'{website_name}', message=f'The entered details are:-\nEmail: {email}\nPassword: {password}\nIs it okay to save?')

        if confirmation:
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_password():
    website_name = website_input.get().title()
    if len(website_name) == 0:
        messagebox.showwarning(title='Empty Field', message="Website Name can't be empty!")
    else:
        try:
            with open('data.json') as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror(title='error', message='No datafile found')
        else:
            if website_name in data:
                email = data[website_name]['email']
                password = data[website_name]['password']
                messagebox.showinfo(title=f'{website_name}', message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showwarning(title=f'{website_name}', message='No details for the website exists.')

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

website_label = Label(text='Website:')
website_label.grid(row=1, column=0, sticky='w')

website_input = Entry(width=33)
website_input.grid(row=1, column=1, sticky='e')
website_input.focus()

search_button = Button(text='Search', command=search_password)
search_button.grid(row=1, column=2, sticky='w', ipadx=7)

email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0, sticky='w')

email_input = Entry(width=43)
email_input.grid(row=2, column=1, columnspan=2, sticky='e')
email_input.insert(0, 'harshsharma@email.com')

password_label = Label(text='Password:')
password_label.grid(row=3, column=0, sticky='w')

password_input = Entry(width=33)
password_input.grid(row=3, column=1, sticky='e')

generate_password_button = Button(text='Generate', command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text='Add', width=36, command=save_data)
add_button.grid(row=4, column=1, pady=20)

window.mainloop()
