import GUI, sort, logging, json
from logger import record, langs

with open(langs, "r", encoding="utf-8") as b:
    language=json.load(b)["main"]
with open(record, "r", encoding="utf-8") as d:
    inf=json.load(d)
lan=language[inf["language"]]
log=logging.getLogger("APP")
log.info(lan["start"])

def program(settings, kategorie, podkategorie, fix, lang):
    lan=language[GUI.z_language.get()]
    if fix:
        log.debug(lan["fix"])
        sort.fix(settings, lang)
    log.debug(lan["sort"])
    sort.sort(settings, kategorie, podkategorie, lang)

log.debug(lan["gui"])
GUI.start(program)