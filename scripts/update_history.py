from pathlib import Path
import re

p = Path("questions.js")
text = p.read_text(encoding="utf-8")

history = '''  {
    "subject": "Storia",
    "q": "Quale civiltà costruì il Colosseo?",
    "options": ["Egizi", "Romani", "Greci", "Fenici"],
    "correct": 1,
    "explain": "Il Colosseo fu costruito nell'antica Roma durante l'età imperiale."
  },
  {
    "subject": "Storia",
    "q": "Quale popolo costruì le piramidi di Giza?",
    "options": ["Romani", "Egizi", "Etruschi", "Vichinghi"],
    "correct": 1,
    "explain": "Le piramidi di Giza furono costruite nell'antico Egitto come monumenti funerari per i faraoni."
  },
  {
    "subject": "Storia",
    "q": "Chi è tradizionalmente considerato l’autore dell’Iliade e dell’Odissea?",
    "options": ["Omero", "Virgilio", "Dante", "Socrate"],
    "correct": 0,
    "explain": "La tradizione attribuisce a Omero l'Iliade e l'Odissea, due grandi poemi dell'antica Grecia."
  },
  {
    "subject": "Storia",
    "q": "In quale periodo storico visse Leonardo da Vinci?",
    "options": ["Preistoria", "Medioevo", "Rinascimento", "Età contemporanea"],
    "correct": 2,
    "explain": "Leonardo da Vinci visse tra il Quattrocento e il Cinquecento ed è uno dei protagonisti del Rinascimento."
  },
  {
    "subject": "Storia",
    "q": "Quale invenzione di Johannes Gutenberg contribuì alla diffusione dei libri in Europa?",
    "options": ["La bussola", "La stampa a caratteri mobili", "Il telescopio", "La macchina a vapore"],
    "correct": 1,
    "explain": "La stampa a caratteri mobili rese possibile produrre libri più rapidamente e favorì la diffusione della cultura scritta."
  },
  {
    "subject": "Storia",
    "q": "Cristoforo Colombo raggiunse il continente americano nel…",
    "options": ["1292", "1492", "1692", "1792"],
    "correct": 1,
    "explain": "Cristoforo Colombo raggiunse le Americhe nel 1492 durante il viaggio finanziato dalla Corona spagnola."
  },
  {
    "subject": "Storia",
    "q": "Come si chiamavano le grandi costruzioni fortificate tipiche del Medioevo?",
    "options": ["Acquedotti", "Castelli", "Piramidi", "Anfiteatri"],
    "correct": 1,
    "explain": "I castelli erano strutture fortificate molto diffuse nel Medioevo e avevano funzioni difensive e residenziali."
  },
  {
    "subject": "Storia",
    "q": "Quale antica civiltà è associata alla nascita dei Giochi Olimpici?",
    "options": ["Greci", "Egizi", "Romani", "Maya"],
    "correct": 0,
    "explain": "I Giochi Olimpici antichi nacquero in Grecia e si svolgevano a Olimpia."
  },
'''

pattern = re.compile(r'  \{\n    "subject": "Storia".*?(?=  \{\n    "subject": "Geografia")', re.S)
updated, count = pattern.subn(history, text, count=1)
if count != 1:
    raise SystemExit("History question block not found")

p.write_text(updated, encoding="utf-8")
