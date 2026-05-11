from pathlib import Path
import json
import shutil as shl
import logging as logg
from logger import main, config, dis, sorter, langs, exps

log=logg.getLogger("APP")
with open(langs, "r", encoding="utf-8") as o:
    language=json.load(o)["sort"]

def sort(sett, kat, podkat, lang):
    lan=language[lang]
    files = list(main.iterdir())
    def check(suf, exp, folders=None):
        if folders is None:
            folders=[]
        if isinstance(exp, list):
            if suf in exp:
                log.info(lan["found"].format(suf=suf, exp=exp))
                return folders
            return None
        elif isinstance(exp, dict):
            for name, value in exp.items():
                result=check(suf, value, folders + [name])
                if result is not None:
                    return result
        return None

    with open(exps if sett=="standard" else config, "r", encoding="utf-8") as f:
        expands=json.load(f)
        if sett=="standard":
            expands=expands[lang]
            log.debug(lan["standard"])
        else:
            log.debug(lan["exp"].format(config=config))
    with open(dis, "r", encoding="utf-8") as d:
        without=json.load(d)
        log.debug(lan["dis"].format(dis=dis))

    if lang=="pl":
        withoutpodkat=["Pokaz", "Edycja", "Szablony", "Dokumenty tekstowe", "Arkusze", "Dane tabelaryczne", "Pomocnicze", "Grafika", "Grafika wektorowa", "Surowe", "Specjalistyczne", "Stratne", "Bezstratne", "Nieskompresowane", "inne", "Uniwersalne", "Archiwalne", "HTML", "CSS", "JavaScript", "TypeScript", "PHP", "Frameworki", "Python", "Java", "C++", "C", "C#", "Rust", "Go", "Swift", "Kotlin", "Ruby", "Shell/Bash", "PowerShell", "Windows Batch", "Lua", "Perl"]
        withkat=["Obrazy", "Muzyka", "Wideo", "Kompresje"]
    else:
        withoutpodkat=["Shows", "Edits", "Templates", "Text documents", "Sheets", "Tabular data", "Auxiliary", "Graphics", "Vector graphics", "Raw", "Specialized", "Lossy", "Lossless", "Uncompressed", "Other", "Universal", "Archival", "HTML", "CSS", "JavaScript", "TypeScript", "PHP", "Frameworki", "Python", "Java", "C++", "C", "C#", "Rust", "Go", "Swift", "Kotlin", "Ruby", "Shell/Bash", "PowerShell", "Windows Batch", "Lua", "Perl"]
        withkat=["Pictures", "Music", "Video", "Compressions"]

    counter=0
    exists_counter=0
    not_found_counter=0
    path=main

    for plik in files:
        log.debug(lan["checking"].format(plik=plik.name))
        if plik==sorter or plik.is_dir() or plik.name=="dev.log" or plik.name=="user.log" or plik.name in without:
            log.info(lan["skip"])
            continue
        
        lista=check(plik.suffix.lower(), expands)

        if lista is None:
            log.info(lan["notfound"])
            not_found_counter+=1
            continue
        else:
            log.info(lan["foundend"].format(plik=plik.name, lista=lista))

        if not kat and not lista[0] in withkat:
            log.debug(lan["kat"].format(kat=lista[0]))
            lista.remove(lista[0])
        if not podkat and lista[-1] in withoutpodkat:
            log.debug(lan["subkat"].format(subkat=lista[-1]))
            lista.remove(lista[-1])
            
        target_path=path

        for fold in lista:
            target_path = target_path / fold
        
        target_path.mkdir(parents=True, exist_ok=True)
        log.debug(lan["preparing"].format(target=target_path))
        target=target_path / plik.name

        if target.exists():
            log.info(lan["exists"].format(plik=plik.name, folder=target_path))
            exists_counter+=1
            continue
        
        log.info(lan["final"].format(plik=plik, target=target))
        shl.move(str(plik), str(target))
        counter+=1

def fix(sett, lang):
    lan=language[lang]
    files = list(main.iterdir())
    with open(exps if sett=="standard" else config) as f:
        template=json.load(f)
        if sett=="standard":
            template=template[lang]

    for plik in files:
        if plik.is_dir() and plik.name in template:
            log.debug(lan["fixing"].format(plik=plik.name))
            for subplik in plik.rglob("*"):
                if subplik.is_file():
                    log.info(lan["getting"].format(plik=subplik, folder=plik))
                    shl.move(str(subplik), str(main/subplik.name))
            log.debug(lan["deleting"].format(plik=plik.name))
            shl.rmtree(plik)