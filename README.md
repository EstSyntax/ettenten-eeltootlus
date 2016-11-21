Eeltöötlusmoodul

Selle süntaksianalüüsi-eelse eeltöötlusmooduli versioon on mõeldud etTenTeni korpuse tekstitüüpide (perioodika, valitsus, religioon, informatiivne, unknown, foorum ja blogi) jaoks. Moodulist on kaks versiooni. Esimene versioon on mõeldud perioodika, valitsuse, religiooni, informatiivse ja tundmatu tekstitüübile (eeltootlus_ettenten, ettenten_patterns), teine versioon on mõeldud foorumi ja blogi tekstitüübile (eeltootlus_ettenten_blg_frm, ettenten_patterns_blg_frm).

Versioonide erinevus tuleneb tekstitüüpide eripärast, st erinevalt esimesest on teises versioonis emotikone tuvastavad mustrid (vt punkt 1), kuid ülejäänud mustrite osas on need identsed. Programmi lähtefailid on ela-kujul, kus iga sõne ja märgend (va doc-päis) on eraldi real. Programmi väljundis paiknevad kõik lõigud eraldi ridadel ning kõik ühte lõiku kuuluvad laused ühel real.

Mooduli eesmärk on parandada etTenTeni korpuses lausestamist ning mitteleksikaalset sisu, mis takistab süntaksianalüsaatori edukat tööd. Lausestusvigadest parandatatakse seda, kus lausemärgendid on üleliigsed, puudulikud või paiknevad vales kohas. Süntaktilise analüüsi vigu põhjustavate vigade korral ühendatakse lause sees paiknevad mitteleksikaalsed elemendid täiendava märgendiga (<+/>). <ignore> ja </ignore> märgendid paigutatakse mitte-lauselise sisu ümber (nt sulgude sees paiknevate lühendite, sõnede, sümbolite ja arvude kombinatsioonid, tekstisisene viitamine jne).

Eeltöötlusmooduli käivitamine blogi ja foorumi tekstitüüpide peal:

Ühe kindla faili töötlemiseks:
python3 eeltootlus_ettenten_blg_frm.py --file sisendkausta_path/fail --output-dir väljundkausta_path

Ühe kindla faili töötlemiseks (lausete loendamisega):
python3 eeltootlus_ettenten_blg_frm.py --file sisendkausta_path/fail --output-dir väljundkausta_path --count-sentences

Terve kausta töötlemine:
python3 eeltootlus_ettenten_blg_frm.py --directory sisendkausta_path --output-dir väljundkausta_path

Terve kausta töötlemine (lausete loendamisega):
python3 eeltootlus_ettenten_blg_frm.py --directory sisendkausta_path --output-dir väljundkausta_path --count-sentences

Skriptis kasutamiseks:
cat sisendkausta_path/fail | python3 eeltootlus_ettenten_blg_frm.py > uus_fail

Skriptis kasutamiseks (lausete loendamisega):
cat sisendkausta_path/fail | python3 eeltootlus_ettenten_blg_frm.py --count-sentences > uus_fail
