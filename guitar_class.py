"""
Provides the principal characteristics of a physical guitar
and an appropriate interpretation of them where necessary.
"""

import regex


class Guitar:
    """
    Class providing the principal characteristics of a physical guitar
    and an appropriate interpretation of them where necessary.
    """

    # Pattern to catch notes of Western chromatic scale in letter notation.
    _pattern = regex.compile(r"^([A-G](?:#?|b?)(?:\s?|,\s?)){2,}$")

    notes = {
        0: ["C"],
        1: ["C#", "Db"],
        2: ["D"],
        3: ["D#", "Eb"],
        4: ["E"],
        5: ["F"],
        6: ["F#", "Gb"],
        7: ["G"],
        8: ["G#", "Ab"],
        9: ["A"],
        10: ["A#", "Bb"],
        11: ["B"],
        12: ["C"],
        13: ["C#", "Db"],
        14: ["D"],
        15: ["D#", "Eb"],
        16: ["E"],
        17: ["F"],
        18: ["F#", "Gb"],
        19: ["G"],
        20: ["G#", "Ab"],
        21: ["A"],
        22: ["A#", "Bb"],
        23: ["B"],
        24: ["C"],
        25: ["C#", "Db"],
        26: ["D"],
        27: ["D#", "Eb"],
        28: ["E"],
        29: ["F"],
        30: ["F#", "Gb"],
        31: ["G"],
        32: ["G#", "Ab"],
        33: ["A"],
        34: ["A#", "Bb"],
        35: ["B"],
        36: ["C"],
    }

    def __init__(self, tuning: str = "EADGBE", frets: int = 21):
        self.frets = frets
        self.tuning = tuning

    def __str__(self):
        """Simple representation of instrument's main attributes."""
        tuning_str = " | ".join(self._tuning)
        return f"Tuning: {tuning_str}\nStrings: {self._strings}\nFrets: {self._frets}"

    @property
    def frets(self):
        """Instrument's maximum number of frets"""
        return self._frets

    @frets.setter
    def frets(self, frets: int):
        if isinstance(frets, int) and frets > 4:
            self._frets = frets
        else:
            raise ValueError("Inappropriate value for frets")

    @property
    def tuning(self):
        """
        Representation of tuning notes as a str.
        """
        return " | ".join(self._tuning)

    @tuning.setter
    def tuning(self, tuning: str):
        """Will recognise any combination of valid notes and
        provide number of strings based on number of notes.
        Alternate tunings aren't catered for yet."""
        if _matches := self._pattern.match(tuning.strip()):
            self._tuning = _matches.allcaptures()[1]
            self._tuning_notes_idx = self._match_notes(self._tuning, self.notes)
            self._strings = len(self._tuning)
            if tuning not in [
                "EADGBE",
                "EbAbDbGbBbEb",
                "D#G#C#F#A#D#",
                "DGCFAD",
                "DbGbBEAbDb",
                "C#F#BEG#C#",
                "CFBbEbGC",
                "BEADF#B",
                "BbEbAbDbFBb",
                "A#D#G#C#FA#",
                "ADGCEA",
                "AbDbGbBEbAb",
                "G#C#F#BD#G#",
                "GCFBbDG",
                "GbBEADbGb",
                "F#BEAC#F#",
                "FBbEbAbCF",
                "FA#D#G#CF",
            ]:
                raise ValueError(
                    "Alternate tunings (or instruments with more or less than 6 strings) not yet implemented. Only transpositions of standard tuning possible."
                )
        else:
            raise ValueError("Inappropriate value for tuning")

    @property
    def tuning_notes_idx(self):
        """
        List of indices for the notes in the instrument's tuning.
        Useful for other functions, etc.
        """
        return self._tuning_notes_idx

    @tuning_notes_idx.setter
    def tuning_notes_idx(self, value):
        raise TypeError("Don't do this.")

    def _match_notes(self, tuning, notes):
        """
        Acquires the indices (chromatically from 0 to 11, i.e. C to B)
        of notes in tuning property for tuning_notes_idx.
        """
        note_pos = []
        for value in tuning:
            for pos, note_list in notes.items():
                if value in note_list:
                    note_pos.append(pos)
                    break
        return note_pos

    def notes_from_fret(self, fret: int = 0, shflat: str = "#") -> list:
        """
        Provides notes at given fret on each string based on Guitar's tuning.
        """
        if fret > self.frets - 4:
            raise ValueError("Don't fret, but you'll run out of frets.")
        if not isinstance(fret, int) or fret < 0:
            raise ValueError("Inappropriate value for fret.")
        fretted_notes_i = [
            (open_string + fret - 1) % 12 + 1 for open_string in self._tuning_notes_idx
        ]

        fretted_notes_s = []

        for note_i in fretted_notes_i:
            for pos, note_list in self.notes.items():
                if note_i == pos:
                    if len(note_list) == 2 and shflat == "#":
                        fretted_notes_s.append(note_list[0])
                    elif len(note_list) == 2 and shflat == "b":
                        fretted_notes_s.append(note_list[1])
                    else:
                        fretted_notes_s.append(note_list[0])
        return fretted_notes_s
