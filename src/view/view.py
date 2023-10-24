from .cli_input import cli_main
from .terminal_output.display import notification
from .terminal_output.employees import ask_credentials, display_employees, display_employee


class View:
    def notification(self, status, message):
        notification(status, message)

    def ask_credentials(self):
        return ask_credentials()

    def read_user_input(self):
        return cli_main()

    def display_employees(self, data):
        display_employees(data)

    def display_employee(self, employee):
        display_employee(employee)

    def __init__(self):
        pass
