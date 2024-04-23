import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime, timedelta
import csv
import winsound
import threading


class Event:
    def __init__(self, deadline, title, description):
        self.deadline = deadline
        self.title = title
        self.description = description

    def check_deadline(self):
        if datetime.now() >= self.deadline:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            messagebox.showinfo("Deadline Alert!", f'Deadline for {self.title}!'
                                                   f'\n{self.description}')
            return True
        return False



