# ALGORITHMIC SCALE GENERATOR
#### [Brief video demo (for CS50P)](https://youtu.be/NX96r-2rky8)
#### Description:

A module designed to algorithmically assemble asymmetrical, non-(overly)chromatic musical scales, providing output in a simplified form of tablature and (for players of non-guitar-adjacent instruments) as a list of the scale's constituent notes in letter notation.

## **Technical overview and usage**
The module provides a new scale every time the program is run, without any user input.
Furthermore, it accepts four optional command-line arguments that allow the user to both fully customise the primary attributes of the scales and set, where appropriate[^1], whether notes in letter notation are displayed as sharps or flats.
Further details regarding the command-line interface and the values expected can be viewed in the module's `-h, --help`:

![A screenshot of the module's command-line help, which details the possible command-line arguments and appropriate values for them](https://i.imgur.com/QO00DqN.png)

The module relies on a `Guitar` class that contains, or sets and contains, values necessary for the proper functioning of the module, such as:
- The tuning of the virtual guitar and the indices of the notes in the tuning. This currently has limited customisability; only 1:1 transpositions of standard tuning work for now.
- Its number of frets (customisable). This is the main factor limiting the maximum fret a scale can start on.
- A dictionary of lists with the `key: [value]` pairs being, respectively, an index and a note value in letter notation (or note value equivalencies in cases of sharps/flats).

> *A necessary note on terminology*[^2]: **Skeleton** *is used to refer both to the scale assembled by the program and the "skeleton" (i.e. pattern) used to produce it.* **String grouping** *refers to what we might be inclined to think of as a Skeleton's "depth" and acts as a binding rule fundamental to how a Skeleton is constructed. For example, a Skeleton with a string grouping of 2 must be played over two strings (i.e. strings 1 and 2) and then repeated without alteration on the next available groups of 2 strings (i.e. on strings 3 and 4 and finally on strings 5 and 6).*

Simplified overview of the `main()` function's execution:
- `optional_arguments()[0:3]` returns the optional command-line arguments for the Skeleton's starting fret, length, and string grouping. If no arguments are provided, they receive default values that trigger their random, algorithmic assignment in the following function.
- `form_skeleton()` is, in short, responsible for curating the values that will make up the list of unique integers that serve as the foundational pattern for the Skeleton. It returns the aforementioned list (`skeleton`) and the now final values for `string_grouping` and `start_fret`.
- The above return values are then passed into `skeleton_to_fretboard()`, interpreted, and formatted as pseudo-tablature. `skeleton_to_fretboard()` then returns:
    - `tab_print`,
    - `cipher`,
    - `starting_notes`,
    - `start_fret`,
    - `string_grouping`,
    - and `skeleton`.
- Of the above return values, `cipher`, `starting_notes`, `string_grouping`, `start_fret`, and `optional_arguments()[3]` (our sharps [#] or flats [b] command-line option) are then passed to `get_skel_notes()`, which returns a list of all the notes, in letter notation, contained in the Skeleton after its complete analysis and assembly.
- We then print the graphical, pseudo-tablature representation of the Skeleton and the notes therein contained. The string grouping and starting fret, which are self-evident when viewing the tablature, can be "commented" back "in" within `main()`, should one so desire.

#### Example output:
```
e | 4
b | 0--2
g | 0--2
D | 4
A | 0--2
E | 0--2

Skeleton:
0, 2, 5, 7, 14
Notes:
E, F#, A, B, F#, G, A, B, C#, G#
```

### Independently callable functions:

`unearth_skeleton()`, `skeleton_to_fretboard()`, and `get_skel_notes()` have been designed to work independently, allowing us to satisfy more niche needs. That being said, certain limitations must be taken into account.

**Example usage and comments:**

```
>>> from project import unearth_skeleton
>>> unearth_skeleton(5, 12)
```
`unearth_skeleton()`, which is usually only used internally within `form_skeleton()`, takes two arguments, `length` and `ceiling`, and in this case allows us to generate a completely random list of `5` *unique* integers  up to the maximum interval, or "`ceiling`", of `12` (note that we're expressing intervals in semitones: 12 = an octave).

The output should look a little something like this:
```
[0, 1, 7, 10, 12]
```
The applicability of this unprocessed Skeleton all on its lonesome depends on you. Let's say, for the sake of example, that you particularly like the cut of its jib. You could then pass it to the `skeleton_to_fretboard()` function, pass that to `print()`, and hopefully get a readable tab output. Let's omit looking at a string grouping of 1 and go straight to the more interesting 2. No offence, 1[^3].
```
>>> from project import skeleton_to_fretboard
>>> print(skeleton_to_fretboard([0, 1, 7, 10, 12], string_grouping=2, start_fret=0)[0])
```

- Given that we're using the function out of context, we must provide the required arguments for the `skeleton`, `string_grouping`, and `start_fret` parameters ourselves.
- We know from the docstring for `skeleton_to_fretboard()` that it returns a tuple containing several items; we only need the first of them, `tab_print`, which is accessed at index `[0]`.

Here is our output, currently for guitarists only:
```
e | 2--5--7
b | 0--1
g | 2--5--7
D | 0--1
A | 2--5--7
E | 0--1
```
Interesting but not particularly playable. Again, let's bear in mind that **the curation algorithm is being bypassed**, so something as awkward as this would actually never be returned by the program. That being said, let's see what happens if we try a string grouping of 3:

```
>>> print(skeleton_to_fretboard([0, 1, 7, 10, 12], string_grouping=3, start_fret=0)[0])
```
And the output:

```
e | 0--2
b | 2
g | 0--1
D | 0--2
A | 2
E | 0--1
```

Better. The interpretation algorithm is able to map this out in a way that is much more playable (indeed, this Skeleton is "valid" in the sense that the program would eventually generate it on its own, depending on your luck). But what about the more civilised among us? Those who wouldn't dare sully their reputations with an instrument as base as the vulgar geetar (or perhaps the sophisticates camouflaging as members of the axe-wielding rabble). Fortunately, we've something for everyone. The `skeleton_to_fretboard()` function returns all of the values we need, and some we don't, to pass to `get_skel_notes()`. This means we can print a list of the actual notes contained in the whole Skeleton.
```
>>> from project import get_skel_notes
>>> get_skel_notes(*skeleton_to_fretboard([0, 1, 7, 10, 12], string_grouping=3, start_fret=0)[1:5])
```
Gives us:

```
['E', 'F', 'B', 'D', 'E', 'G', 'G#', 'C#', 'E', 'F#']
```

Nota bene:
- `get_skel_notes()` only wants four of the six arguments returned by `skeleton_to_fretboard()`, and the four we need can be accessed by slicing with `[1:5]`.
- If we want to view sharps as their equivalent flats, we can add the `shflat="b"` argument as follows:
```
>>> get_skel_notes(*skeleton_to_fretboard([0, 1, 7, 10, 12], string_grouping=3, start_fret=0)[1:5], shflat="b")
```

```
['E', 'F', 'B', 'D', 'E', 'G', 'Ab', 'Db', 'E', 'Gb']
```
You may by now have deduced that you could simply whimsically pass your own random list of integers as the first argument (`skeleton`) in `skeleton_to_fretboard()`.
This path can lead to gifts of broadly varying benefits, dependent primarily on the length of the list and the range of the intervals. It circumvents all of the code designed to make (sure) things work. Nevertheless, I felt it important to include the possibility of somewhat wandering astray, without being cruelly stared down by error messages, so I could observe demonstrations of the ways in which the curation and interpretation algorithms may be lacking.

## A deep yet glancing look at two core functions

By far the greatest gauntlet thrown down to my grey matter was figuring out the logic necessary for the curation and interpretation of the Skeletons. The code itself for the following functions should be consulted in case of curiosity. Otherwise, here is a very rudimentary overview of what happens in `form_skeleton()` and `skeleton_to_fretboard()` when running the program:

- `form_skeleton()`, as we know, forms the `skeleton` pattern. It takes three optional arguments, `start_fret`, `length`, and `string_grouping`. Their default arguments result in an appropriately random final value being assigned to each of them. `start_fret` is checked to make sure its value, in comparison to the instrument's number of frets, is permissible, or in case of random assignment, whether the randomly chosen number is permissible.
A similar process takes place for `string_grouping`.
We then make use of a `match` `case` statement to ensure the appropriate checks are carried out based on the value of `string_grouping`:
    - we check and assign `length` (`string_grouping` dictates a minimum and maximum value here),
    - we create the variable `ceiling` (the maximum allowed interval), which is assigned an integer, again according to `string_grouping`,
    - if `string_grouping == 1` we run the `unearth_skeleton()` function, with `length` and `ceiling` as arguments, in a `while` loop to check one specific condition designed to avoid over-chromaticism; here, the `skeleton` doesn't require further checks as the restrictive nature of the values for `string_grouping`, `length`, and `ceiling` essentially does the curating for us,
    - otherwise, `unearth_skeleton()` is placed in a `while` loop and a number of tedious conditions are checked before,
    - we return `skeleton`, `string_grouping`, and `start_fret`.

- `skeleton_to_fretboard()` takes the values of `string_grouping` and `start_fret` and uses them to figure out how the note indices in `skeleton` should be transposed and displayed:
    - first, using the indices of the tuning notes provided by our instance of `Guitar`, the notes at the assigned starting fret on each string are determined,
    - as with `form_skeleton()`, we use a `match` `case` statement to ensure the appropriate checks are carried out based on the value of `string_grouping`,
    - variables providing the indices of the notes determined in the first step, for individual strings and groups of strings (`string_one`, `string_two`, `strings_two_four_six`, etc.), allow us, after checking conditions and doing some simple maths, to append `cipher`, a list of six lists (one for each string), with the frets that correspond to the notes resulting from the application of the `skeleton` to the appropriate strings,
    - the final step is to put the lists within `cipher` in the correct order, which is carried out as part of the formatting of the tablature output, and to create the final, printable variable, `tab_print`.
    - we return `tab_print` and `skeleton` so we can print them, and `cipher`, `starting_notes`, `start_fret`, and `string_grouping` so we can pass them to `get_skel_notes()`.


[^1]: No B# for C here, sorry.


[^2]: An unnecessary note on terminology and methodology: faced with having to give some kind of name to these pseudo-scales, I settled on a somewhat euphemistic use of "Skeleton" (or "Skel") to refer both to the pattern<sup>i</sup> and the scale<sup>ii</sup> resulting from the former's digestion by the algorithm. The algorithm specific to this module yields only what is known as (i.e. what I've called) the *Reprobate Skeleton*; five further "natures" are intended. The rules governing the formulation of the Reprobate Skeleton find their modest technical origins in a method I indulge(d) in for the purposes of attempting to remove the possibility of resorting to subconsciously stocked tropes or "licks" when improvising and practising: inventing new, unfamiliar scales using physical shapes on the fretboard as a point of departure. The simplest technique was to map single-string patterns vertically across the guitar's fretboard (something I'm sure every player of a stringed instrument has done at some point), then, when ambition allowed, a slightly less simple technique involved mapping multi-string patterns onto the next (as yet untouched) group of strings.
    - *i*. A list with a maximum length of 12 containing note indexes in the form of intervals expressed in number of semitones (0 = unison, 1 = minor second, 2 = major second, 12 = octave, etc., see [here](https://en.wikipedia.org/wiki/Interval_(music)#Main_intervals)).
    - *ii*. That is, all of the notes resulting from the application of the Skeleton's intervals (in relation to the 0, a.k.a. unison) to the appropriate string.


[^3]: It's worth taking this opportunity to elucidate one of the fundamental rules governing a Skeleton's construction: intervals greater than a major third (4 semitones) are not permitted on a single string (primarily for obvious ergonomic reasons, additionally because I learned early on that restrictive design choices such as this were inevitable). Therefore — while the use of the `skeleton_to_fretboard()` function out of context allows us to view this particular Skeleton's tab with a string grouping of 1 — within the module itself, the `form_skeleton()`'s curation conditions would not allow this to happen, and, more illustratively, if we sought to generate a Skeleton with a length of 5 and a string grouping of 1 via the optional command-line arguments (`-l 5 -g 1`) we would politely be informed that the appropriate length for a Skeleton with a string grouping of 1 is between 2 and 4.
