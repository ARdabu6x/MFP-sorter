import logging as logg
from pathlib import Path
import os, sys

if getattr(sys, 'frozen', False):
    sorter=Path(sys.executable)
    main=sorter.parent
    base=Path(sys._MEIPASS)
else:
    main=Path(__file__).parent.parent
    sorter=Path(__file__).parent
    base=sorter

langs=base/"languages.json"
exps=base/"expands.json"
ic=base/"icon.ico"
appdata=Path(os.getenv("APPDATA"))/"MFP sorter"
config=appdata/"custom.json"
dis=appdata/"disable.json"
record=appdata/"record.json"

log=logg.getLogger("APP")
log.setLevel(logg.DEBUG)

user=logg.FileHandler(main/"user.log", "w", encoding="utf-8")
user.setLevel(logg.INFO)
user.setFormatter(logg.Formatter("%(asctime)s - %(message)s"))

dev=logg.FileHandler(main/"dev.log", "w", encoding="utf-8")
dev.setLevel(logg.DEBUG)
dev.setFormatter(logg.Formatter("%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"))

log.addHandler(user)
log.addHandler(dev)