import sys
from collections import defaultdict

VOWELS = 'aa ae ah ao aw ax ay ea eh er ey ia ih iy oh ow oy ua uh uw'.split()
CONSONANTS = 'p b t d f v th dh s z sh zh ch jh k ng g m n l r w y hh'.split()

onsets = defaultdict(list)  # onset -> list of example words
nucleii = defaultdict(list)  # nucleus -> list of example words
codas = defaultdict(list)  # coda -> list of example words

syllable_examples = {}  # syllable -> word

with open('syllables.txt') as inf:
  for line in inf:
    syllable, example_word = line[:16], line[16:].strip()
    syllable = syllable.split()
    assert all(x.islower() for x in syllable)
    for x in syllable:
      if x not in VOWELS + CONSONANTS:
        raise Exception('bad phoneme %r in %r' % (x, line))
    assert all(not x.islower() for x in example_word)

    syllable_examples[tuple(syllable)] = example_word
    
    onset = []
    nucleus = []
    coda = []

    for phoneme in syllable:
      if phoneme in VOWELS:
        assert not nucleus
        nucleus.append(phoneme)
      else:
        if not nucleus:
          onset.append(phoneme)
        else:
          coda.append(phoneme)

    onsets[tuple(onset)].append((example_word, syllable))
    nucleii[tuple(nucleus)].append((example_word, syllable))
    codas[tuple(coda)].append((example_word, syllable))
    
  if False:
    for category, category_dict in [
        ("Onsets", onsets),
        ("Nucleii", nucleii),
        ("Codas", codas)]:
      print('%s: %s' % (category, len(category_dict)))
      counted = [(-len(examples), cluster, examples)
                 for cluster, examples
                 in category_dict.items()]
      
      for _, cluster, examples in sorted(counted):
        example, example_syllable = examples[0]
        if True:
          print('%s   %s %s (%s)' % (
            str(len(examples)).rjust(4),
            ' '.join(cluster).ljust(8),
            example.ljust(18),
            ' '.join(example_syllable)))
        else:
          print ('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            len(examples), ' '.join(cluster), example, ' '.join(example_syllable)))
        print('')

  if True:
    for example, example_syllable in sorted(codas[tuple(sys.argv[1:])]):
      print('%s %s' % (example.ljust(20), ' '.join(example_syllable)))

      
