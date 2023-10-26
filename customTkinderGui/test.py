import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter App")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # create main entry
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # create button next to entry
        self.main_button_1 = customtkinter.CTkButton(self, text="Button1")
        self.main_button_1.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Tab 1")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")

        # create bottom buttons
        self.button_2 = customtkinter.CTkButton(self, text="Button 2")
        self.button_2.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.button_3 = customtkinter.CTkButton(self, text="Button 3")
        self.button_3.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
