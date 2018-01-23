with open('beep-1.0.txt') as inf:
  pronciations = {}
  for line in inf:
    if not line.startswith('#'):
      word, pronciation = line.strip().split(None, 1)
      pronciations[pronciation] = word

def read_clusters(fname):
  clusters = []
  with open(fname) as inf:
    for line in inf:
      count, cluster = line.strip().split(' ', 1)
      if cluster == '(null)':
        cluster = ''    
      clusters.append((
        () if cluster == '(null)'else tuple(cluster.split()),
        int(count)))
  return clusters

onsets = read_clusters('onsets.txt')
nucleii = read_clusters('nucleii.txt')
codas = read_clusters('codas.txt')

absent = []
present = []
for onset, onset_count in onsets:
  for nucleus, nucleus_count in nucleii:
    for coda, coda_count in codas:
      vague_likelihood = onset_count * nucleus_count * coda_count
      syllable = ' '.join(onset + nucleus + coda)

      l = present if syllable in pronciations else absent
      l.append((-vague_likelihood, len(syllable), syllable,
                '%s   %s %s\n' % (
                  str(vague_likelihood).rjust(10),
                  syllable.ljust(20),
                  pronciations.get(syllable, ''))))

with open('absent.txt', 'w') as outf:
  for _, _, _, x in sorted(absent):
    outf.write(x)      
      
with open('present.txt', 'w') as outf:
  for _, _, _, x in sorted(present):
    outf.write(x)
      
      
      
