from tkinter import *
from tkinter import messagebox
from string import ascii_letters as letters, digits

correct_symbols = letters + digits


def exit_the_program():
    if messagebox.askquestion('Вийти з програми?', 'Ви дійсно бажаєте вийти?') == 'yes':
        exit()


class WindowBlank:
    def __init__(self, window, title, entry_col, button0_text, button0_command, pos='+0'):
        self.root = window
        self.root.resizable(width=False, height=False)
        self.root.geometry(f'600x280{pos}+{self.root.winfo_screenheight() // 2 - 140}')
        self.root.title(title)

        self.root['bg'] = '#ccc'
        self.login_label = Label(self.root, text='Логін', font='Consolas 25', fg='#000000', bg='#ccc')
        self.login_entry = Entry(self.root, font='Consolas 20', fg='#00000A', bg=entry_col, relief='solid',
                                 justify='center', selectbackground='#B5FFFE', selectforeground='#5A3000')

        self.password_label = Label(self.root, text='Пароль', font='Consolas 25', fg='#000000', bg='#ccc')
        self.password_entry = Entry(self.root, font='Consolas 20', fg='#00000A', bg=entry_col, relief='solid',
                                    justify='center',
                                    show='*', selectbackground='#B5FFFE', selectforeground='#5A3000')
        self.button0 = Button(self.root, text=button0_text, font='Consolas 15', fg='#2e2525', bg='#B3FF04',
                              relief='solid', justify='center', command=button0_command)

        self.exit_button = Button(self.root, text='Вийти з програми', font='Consolas 15', fg='#090809', bg='#FFA79D',
                                  relief='solid', justify='center', command=exit_the_program)

        self.login_label.pack()
        self.login_entry.pack(padx=self.root.winfo_screenwidth() * 0.01, fill='x')

        self.password_label.pack()
        self.password_entry.pack(padx=self.root.winfo_screenwidth() * 0.01, fill='x')

        self.button0.pack(side=TOP, pady=10)
        self.exit_button.pack(side=BOTTOM, pady=10)


class Register(WindowBlank):
    data = {}

    def __init__(self, _login):
        super().__init__(Toplevel(_login), 'Реєстрація', '#61daff', 'Зареєструватися', self.register, '-345')

    @staticmethod
    def check(string: str, minlen: int = -1) -> tuple[bool, bool, bool]:
        symbols_is_correct = True
        for symbol in string:
            if symbol not in correct_symbols:
                symbols_is_correct = False
                break
        if minlen is None or len(string) >= minlen:
            len_is_correct = True
        else:
            len_is_correct = False
        is_correct = symbols_is_correct and len_is_correct
        return is_correct, symbols_is_correct, len_is_correct

    def register(self):
        login_check_result = self.check(self.login_entry.get(), 1)
        password_check_result = self.check(self.password_entry.get(), 8)

        if login_check_result[0] and password_check_result[0]:
            Register.data.update({self.login_entry.get(): self.password_entry.get()})
            self.root.title(f'Кількість користувачів: {len(Register.data)}')
            self.login_entry.configure(bg='#B3FF04')
            self.password_entry.configure(bg='#B3FF04')
            return messagebox.showinfo('Вітаємо', 'Ви успішно зареєструвалися!')
        else:
            self.login_entry.configure(bg='#61daff')
            self.password_entry.configure(bg='#61daff')
            error_massage = ''
            error_counter = 0
            if not login_check_result[2]:
                error_massage += 'Логін повинен містити хоча б один символ\n'
                error_counter += 1
                self.login_entry.configure(bg='#FFB297')
            elif not login_check_result[1]:
                error_massage += f'Логін має містити тільки такі символи: {" ".join(list(correct_symbols))}\n'
                error_counter += 1
                self.login_entry.configure(bg='#FFB297')
            if not password_check_result[2]:
                error_massage += 'Пароль має містити мінімум вісім символів\n'
                error_counter += 1
                self.password_entry.configure(bg='#FFB297')
            if not password_check_result[1]:
                error_massage += f'Пароль має містити тільки такі символи: {" ".join(list(correct_symbols))}\n'
                error_counter += 1
                self.password_entry.configure(bg='#FFB297')
            error_caption = f'Errors: {error_counter}'
            return messagebox.showerror(error_caption, error_massage)


class Login(WindowBlank):
    def __init__(self):
        self.current_user = None
        super().__init__(Tk(), 'Вхід', '#F9B93A', 'Увійти', self.login, '+345')
        self.delete_button = Button(self.root, text='Delete\nthis\naccount', font='Consolas 15',
                                    bg='#ffffff', fg='#888888', disabledforeground='#888888',
                                    relief='solid', justify='center',
                                    command=self.delete_current_account, state='disabled', default='active')
        self.delete_button.pack(side='left', before=self.login_label, fill='y')

    @staticmethod
    def check(user_login, password):
        return user_login in Register.data.keys(), password in Register.data.values()

    def delete_current_account(self):
        if messagebox.askquestion('Видалити цей аккаунт?', 'Ви справді хочете видалити цей аккаунт?') == 'yes':
            self.delete_button.configure(state='disabled', bg='#ffffff', fg='#888888')
            Register.data.pop(self.current_user)
            self.current_user = None
            self.root.title('Вхід')
            if len(Register.data) > 0:
                register.root.title(f'Кількість користувачів: {len(Register.data)}')
                return
            register.root.title('Реєстрація')

    def login(self):
        check_result = self.check(self.login_entry.get(), self.password_entry.get())

        self.login_entry.configure(bg='#F9B93A')
        self.password_entry.configure(bg='#F9B93A')
        if check_result[0]:
            if check_result[1]:
                self.delete_button.configure(state='normal', bg='#C90101', fg='#ffffff')
                self.current_user = self.login_entry.get()
                self.root.title(self.current_user)
                self.login_entry.configure(bg='#B3FF04')
                self.password_entry.configure(bg='#B3FF04')
                return messagebox.showinfo('Вітаємо', 'Ви успішно увійшли!')
            else:
                self.password_entry.configure(bg='#FF1900')
                return messagebox.showerror('Неправильний пароль', 'Ви ввели неправильний пароль\nСпробуйте ще раз!')
        else:
            self.login_entry.configure(bg='#FF1900')
            return messagebox.showerror('Неправильний логін', 'Ви ввели неправильний логін\nСпробуйте ще раз!')


login = Login()
register = Register(login.root)

login.root.mainloop()
