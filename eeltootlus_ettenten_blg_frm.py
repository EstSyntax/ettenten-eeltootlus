#!/usr/bin/python3
# coding: utf8

"""
Eeltöötlusmoodul etTenTeni korpuse blogi ja foorumi tekstitüübi jaoks.

Programmi käivitamiseks:

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

"""

from __future__ import print_function

import argparse
import os
from multiprocessing.dummy import Pool
import re
import sys
from io import StringIO

import ettenten_patterns_blg_frm



class Processor(object):
    def __init__(self, count_sentences):
        """
        Protsessori konstruktor
        count_sentences määrab, kas lauseid protsessimise ajal failis
        loendatakse või mitte
        """
        self.count_sentences = count_sentences
        self._sentence_count = 0
        self._sentence_patt = re.compile(r'<s>(?! <id="\d+">)')
        self._ignore_patt = re.compile(r'(<ignore>.*</ignore>)')

    def _count_sentences(self, line):
        """
        lisab etteantud reas lause alguse sümboli järele selle lause
        järjekorranumbri failis ja tagastab muudetud rea
        """
        if not self.count_sentences:
            return line
        # lisame ükshaaval lausete alguste juurde järjekorranumbri, kuni
        # pole enam ühtegi järjekorranumbrita lause algust
        parts = []
        for part in self._ignore_patt.split(line):
            if not self._ignore_patt.match(part):
                while self._sentence_patt.search(part):
                    self._sentence_count += 1
                    part = self._sentence_patt.sub(r'<s> <id="%d">' % self._sentence_count, part, count=1)
            parts.append(part)
        return "".join(parts)

    def process_line(self, line):
        """ teostab rea töötlemise """
        # asendame kõik etteantud mustri vasted, kui mustrile üldse vaste leidub
        if not re.findall('<doc', line):
            for regexp, replace in ettenten_patterns_blg_frm.PATTERNS:
                if callable(regexp):
                    line = regexp(line)
                elif regexp.findall(line):
                    line = regexp.sub(replace, line)
                    if re.findall(r'<emotikon=[^\s]+(\s\))+/>', line):
                        line = re.sub(r'\)\s\)', '))', line)
                        line = re.sub(r'\)\s\)', '))', line)
        return self._count_sentences(line)

    def process(self, fid=None, fod=None):
        """ faili töötlemine, sisendiks faili tüüpi objektid """
        # kui sisendit või väljundit ette ei anta kasutame
        # vastavalt standardsisendit või standardväljundit
        if fid is None:
            fid = sys.stdin
        if fod is None:
            fod = sys.stdout
        fod.writelines(map(self.process_line, fid))

    def process_file(self, file_path, output_dir_path):
        """ faili töötlemine, sisendiks failiteed """
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir_path, filename)
        output_path = "%s_eel%s" % os.path.splitext(output_path)
        if file_path == output_path:
            print("Skipping file %s, it would be overwritten" % file_path)
            return
        else:
            print("Processing file %s to %s" % (file_path, output_path))
        with open(file_path) as fid, open(output_path, 'w') as fod:
            data = fid.read()
            yhele_reale = re.sub('\n', ' ', data)
            kirjavahemargi_eemaldus = re.sub('(<\|\+/> )|(<\+\|/> )|(<\+/> )', '', yhele_reale)
            dok_eraldamine = re.sub('</doc>', '</doc>\n', kirjavahemargi_eemaldus)
            loigu_eraldamine = re.sub(' <p', '\n<p', dok_eraldamine)
            self.process(StringIO(loigu_eraldamine), fod)
            # self.process(fid, fod)

    @staticmethod
    def process_directory(input_dir, output_dir, count_sentences):
        """
        Kaustas olevate xml failide töötlemine
        Funktsiooni argumentideks on sisend- ja väljundkausta teed
        """

        def process(filepath):
            Processor(count_sentences).process_file(filepath, output_dir)

        # kui väljundkausta ei eksisteeri, siis tee see
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # otsime sisendkaustast üles kõik xml-laiendiga failid
        urls = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if
                f.endswith('.url')]
        Pool().map(process, urls)  # funktsiooni process rakendatakse kõikidele failidele eraldi lõimedena


def main():
    # käsurea parameetrite paikapanemine
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file', type=str, metavar='filepath',
        help='file to be parsed')
    parser.add_argument(
        '--directory', type=str, metavar='dirpath',
        help='parse all files from the directory')
    parser.add_argument(
        '--output-dir', type=str, metavar='outputpath',
        help='directory where parsed files are saved')
    parser.add_argument(
        '--count-sentences', dest='count_sentences', action='store_true',
        help='boolean, whether to count sentence tags in xml or not')
    parser.set_defaults(count_sentences=False)
    args = parser.parse_args()

    error = ""
    if args.file and args.directory:
        error = "Provide file or directory, not both"
    elif args.file and not os.path.exists(args.file):
        error = "File %r does not exists" % args.file
    elif args.directory and not os.path.exists(args.directory):
        error = "Directory %r does not exists" % args.directory
    elif args.file and not args.output_dir:
        error = "Missing output directory for file parsing"
    elif args.directory and not args.output_dir:
        error = "Missing output directory for parsing directory"
    if error:
        sys.stderr.write("%s\n" % error)
        sys.exit(1)

    # try:
    #     import regex
    # except ImportError:
    #     print('Mooduli "regex" importimine ebaõnnestus.')
    #     print('Mooduli "regex" saad paigaldada käsuga `(sudo) pip install regex`')
    #     print('Mooduli dokumentatsioon on leitav siit: https://pypi.python.org/pypi/regex')
    #     sys.exit(1)

    if args.file:  # kui käsurea parameetriks on fail, siis töötle seda faili
        Processor(args.count_sentences).process_file(
            args.file, args.output_dir)
    elif args.directory:  # kui sisendiks on kaust, siis töötle seal kaustas olevaid xml-faile
        Processor.process_directory(
            args.directory, args.output_dir, args.count_sentences)
    else:
        # kui faili/kausta parameetrit ei anta, siis loe sisend standardsisendist
        # ja kirjuta väljund standardväljundisse (nt skriptis kasutamiseks)
        Processor(args.count_sentences).process()


if __name__ == '__main__':
    main()
