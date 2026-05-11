import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox
import winsound, json
from logger import appdata, config, dis, record, langs, exps, ic
import logging as logg

box=None
log=logg.getLogger("APP")

appdata.mkdir(parents=True, exist_ok=True)
if not record.exists():
    record.write_text(json.dumps({"language":"en"}, indent=4), encoding="utf-8")

with open(record, "r", encoding="utf-8") as d:
    inf=json.load(d)
with open(langs, "r", encoding="utf-8") as b:
    language=json.load(b)["gui"]
lan=language[inf["language"]]

def line(row, column, span=1, pad=(0, 0)):
    new_line=ttk.Separator(
        okno, orient="horizontal"
    ).grid(row=row, column=column, sticky="ew", columnspan=span, pady=pad)
    return new_line

def alert():
    if z_fix.get():
        if z_settings.get()=="standard":
            say=lan["fix_say_standard"]
        elif z_settings.get()=="custom":
            say=lan["fix_say_custom"]
        log.debug(lan["fix_warning"])
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        answer=messagebox.askyesno(
            lan["fix_say_title"], say, icon="warning"
        )
        if not answer:
            z_fix.set(value=False)

def change():
    if z_settings.get()=="custom":
        log.debug(lan["mode_custom"])
        create.configure(state="normal")
        kategorie.configure(state="disabled")
        podkategorie.configure(state="disabled")
        z_kategorie.set("True")
        z_podkategorie.set("True")
        show.configure(state="disabled")
        disable.configure(state="disabled")
    elif z_settings.get()=="standard":
        log.debug(lan["mode_standard"])
        create.configure(state="disabled")
        kategorie.configure(state="normal")
        podkategorie.configure(state="normal")
        show.configure(state="normal")
        disable.configure(state="normal")

def show_standard():
    with open(exps, "r", encoding="utf-8") as f:
        content=json.load(f)
        log.debug(lan["loading"])
        if z_language.get()=="en":
            content=content["en"]
        else:
            content=content["pl"]

    log.debug(lan["preview_root"])
    preview=tk.Toplevel()
    preview.title(lan["preview_title"])
    preview.resizable(False, False)
    preview.iconbitmap(ic)

    log.debug(lan["preview_items"])
    tekst=tk.Text(
        preview, width=150, height=40
    )
    tekst.insert("1.0", json.dumps(content, indent=4, ensure_ascii=False))
    tekst.config(state="disabled")
    tekst.pack()
    tk.Button(preview, text=lan["close"], command=preview.destroy).pack()

    preview.grab_set()
    preview.wait_window()

def build(dili):
    def validate(data):
        if dili=="dict":
            if not isinstance(data, dict):
                log.warning(lan["warning_structure"])
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                messagebox.showerror(
                    lan["invalid_structure"],
                    lan["invalid_structure_say"], parent=editor
                )
                return False
            for key, value in data.items():
                if not isinstance(key, str):
                    log.warning(lan["warning_dict_key"])
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    messagebox.showerror(
                        lan["invalid_key"],
                        lan["invalid_key_say"].format(key=key), parent=editor
                    )
                    return False
                if isinstance(value, list):
                    for item in value:
                        if not isinstance(item, str):
                            log.warning(lan["warning_dict_list_key"])
                            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                            messagebox.showerror(
                                lan["invalid_item"],
                                lan["invalid_item_say"].format(key=key, item=item), parent=editor
                            )
                            return False
                elif isinstance(value, dict):
                    log.debug(lan["next"])
                    if not validate(value, f"{key}"):
                        return False
                else:
                    log.warning(lan["warning_structure"])
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    messagebox.showerror(
                        lan["invalid_value"],
                        lan["invalid_value_say"].format(key=key), parent=editor
                    )
                    return False
            log.debug(lan["no_error"])
            return True
        
        else:
            if not isinstance(data, list):
                log.warning(lan["warning_list_structure"])
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                messagebox.showerror(
                    lan["invalid_structure"],
                    lan["invalid_list_structure"], parent=lister
                )
                return False
            for index in data:
                if not isinstance(index, str):
                    log.warning(lan["warning_plik"])
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    messagebox.showerror(
                        lan["invalid_value"],
                        lan["invalid_index"].format(index=index), parent=lister
                    )
                    return False
                parts=index.split(".")
                if len(parts) <2:
                    log.warning(lan["warning_len"])
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    messagebox.showerror(
                        lan["invalid_format"],
                        lan["invalid_format_say"].format(index=index), parent=lister
                    )
                    return False
                if any(p=="" for p in parts):
                    log.warning(len["warning_plik_dot"])
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    messagebox.showerror(
                        lan["invalid_format"],
                        lan["invalid_index_format"].format(index=index), parent=lister
                    )
                    return False
            log.debug(lan["no_error"])
            return True
    def check(text):
        try:
            data=json.loads(text)
            log.debug(lan["load"])
        except json.JSONDecodeError as error:
            log.error(lan["error"].format(error=error))
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            messagebox.showerror(
                lan["json_error"],
                lan["json_error_say"].format(msg=error.msg, lineno=error.lineno, colno=error.colno), parent=editor if dili=="dict" else lister
            )
            return None
        
        if not validate(data):
            log.debug(lan["notvalidate"])
            return None
        
        return data

    def save():
        data=check(tekst.get("1.0", "end").strip())
        
        if not data==None:
            if dili=="dict":
                config.write_text(json.dumps(data, indent=4), encoding="utf-8")
                log.debug(lan["write"].format(plik=config.name))
            else:
                dis.write_text(json.dumps(data, indent=4), encoding="utf-8")
                log.debug(lan["write"].format(plik=config.name))

            messagebox.showinfo(
                lan["saved"], lan["saved_say"], parent=editor if dili=="dict" else lister
            )
            editor.destroy() if dili=="dict" else lister.destroy()

    def tab(event):
        tekst.insert("insert", " "*4)
        return "break"
    
    def on_close():
        if (dili=="dict" and not tekst.get("1.0", "end").strip()==config.read_text()) or (dili=="list" and not tekst.get("1.0", "end").strip()==dis.read_text()):
            log.debug(lan["on_close"])
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            answer=messagebox.askyesnocancel(
                lan["unsaved"], 
                lan["unsaved_say"], 
                parent=editor if dili=="dict" else lister
            )
            if answer==True:
                save()
            elif answer==False:
                editor.destroy() if dili=="dict" else lister.destroy()
        else:
            editor.destroy() if dili=="dict" else lister.destroy()

    if dili=="dict":
        appdata.mkdir(parents=True, exist_ok=True)
        if not config.exists():
            config.write_text(json.dumps({}, indent=4), encoding="utf-8")

        log.debug(lan["open"].format(plik=config.name))
        editor=tk.Toplevel()
        editor.title(config.name)
        editor.resizable(False, False)
        editor.iconbitmap(ic)

        tekst=tk.Text(
            editor, width=150, height=40
        )
        tekst.insert("1.0", config.read_text(encoding="utf-8"))
        tekst.pack()

        tk.Button(editor, text=lan["save"], command=save).pack()

        tekst.bind("<Tab>", tab)
        editor.protocol("WM_DELETE_WINDOW", on_close)

        editor.grab_set()
        editor.wait_window()
    else:
        appdata.mkdir(parents=True, exist_ok=True)
        if not dis.exists():
            dis.write_text(json.dumps([], indent=4), encoding="utf-8")

        log.debug(lan["open"].format(plik=dis.name))
        lister=tk.Toplevel()
        lister.title(dis.name)
        lister.resizable(False, False)
        lister.iconbitmap(ic)

        tekst=tk.Text(
            lister, width=150, height=40
        )
        tekst.insert("1.0", dis.read_text(encoding="utf-8"))
        tekst.pack()
        tk.Button(lister, text=lan["save"], command=save).pack()

        tekst.bind("<Tab>", tab)
        lister.protocol("WM_DELETE_WINDOW", on_close)

def on_submit():
    if box:
        log.debug(lan["using"])
        box(
            z_settings.get(),
            z_kategorie.get(),
            z_podkategorie.get(),
            z_fix.get(),
            z_language.get()
        )
        write={"language":z_language.get()}
        with open(record, "w", encoding="utf-8") as p:
            json.dump(write, p, indent=4)
        log.info(lan["end"])
        okno.destroy()

def on_exit():
    write={"language":z_language.get()}
    with open(record, "w", encoding="utf-8") as p:
        json.dump(write, p, indent=4)
    log.info(lan["end"])
    okno.destroy()

#tworzenie okna#
def start(callback):
    global okno, create, kategorie, podkategorie, show, disable, box, z_fix, z_kategorie, z_podkategorie, z_settings, z_language

    def translate():
        global lan
        log.debug(lan["translate"])

        lan=language[z_language.get()]
        language_label.config(text=lan["language"])
        settings_label.config(text=lan["settings"])
        standard.config(text=lan["standard"])
        custom.config(text=lan["custom"])
        kategorie.config(text=lan["categories"])
        podkategorie.config(text=lan["subcategories"])
        show.config(text=lan["show"])
        disable.config(text=lan["disable"])
        create.config(text=lan["create"])
        fix.config(text=lan["fix"])
        submit.config(text=lan["submit"])
        okno.update()

    box=callback

    log.debug(lan["main"])
    okno=tk.Tk()
    okno.title("MFP sorter")
    okno.columnconfigure(0, minsize=10)
    okno.columnconfigure(5, minsize=80)
    okno.iconbitmap(ic)
    okno.resizable(False, False)

    #czcionka#
    default=font.nametofont("TkDefaultFont")
    default.configure(size=11, family="Arial")

    #zmienne#
    z_language=tk.StringVar(value=inf["language"])
    z_kategorie=tk.BooleanVar(value=True)
    z_podkategorie=tk.BooleanVar(value=True)
    z_fix=tk.BooleanVar(value=False)
    z_settings=tk.StringVar(value="standard")

    #Tworzenie#
        #język#
    language_label=tk.Label(
        okno, text=lan["language"], font=font.Font(weight="bold", size=12)
    )
    eng=tk.Radiobutton(
        okno, text="English", variable=z_language, value="en", command=translate
    )
    pl=tk.Radiobutton(
        okno, text="Polski" ,variable=z_language, value="pl", command=translate
    )
        #ustawienia#
    settings_label=tk.Label(
        okno, text=lan["settings"], font=font.Font(weight="bold", size=12)
    )
    standard=tk.Radiobutton(
        okno, text=lan["standard"], variable=z_settings, value="standard", command=change
    )
    custom=tk.Radiobutton(
        okno, text=lan["custom"], variable=z_settings, value="custom", command=change
    )
        ###
    kategorie=tk.Checkbutton(
        okno, text=lan["categories"], variable=z_kategorie
    )
    podkategorie=tk.Checkbutton(
        okno, text=lan["subcategories"], variable=z_podkategorie
    )
    show=tk.Button(
        okno, text=lan["show"], command=show_standard
    )
    fix=tk.Checkbutton(
        okno, text=lan["fix"], variable=z_fix, command=alert
    )
        #potwierdzenie#
    submit=tk.Button(
        okno, text=lan["submit"], command=on_submit
    )
    hline=ttk.Separator(
        okno, orient="vertical"
    )
    create=tk.Button(
        okno, text=lan["create"], state="disabled", command=lambda: build("dict")
    )
    disable=tk.Button(
        okno, text=lan["disable"], command=lambda: build("list")
    )

    #rysowanie#
    log.debug(lan["drawing"])
        #języki#
    line(0, 0, pad=(10, 10))
    language_label.grid(row=0, column=1)
    line(0, 2, 5, (10, 10))
    eng.grid(row=1, column=1)
    pl.grid(row=1, column=2)
        #ustawienia#
    line(2, 0)
    settings_label.grid(row=2, column=1)
    line(2, 2, 5)
    standard.grid(row=3, column=1)
    kategorie.grid(row=4, column=1)
    podkategorie.grid(row=4, column=2)
    show.grid(row=5, column=1, columnspan=2, pady=(0, 5))
    disable.grid(row=6, column=1, columnspan=2, pady=(0, 10))
    fix.grid(row=7, column=1, columnspan=5)
    hline.grid(row=3, column=3, rowspan=4, sticky="ns")
    custom.grid(row=3, column=4)
    create.grid(row=4, column=4, columnspan=2, pady=(0, 5), rowspan=3)
        #potwierdzenie#
    line(8, 0, 7, (10, 0))
    submit.grid(row=9, column=0, columnspan=6)

    okno.protocol("WM_DELETE_WINDOW", on_exit)

    okno.mainloop()