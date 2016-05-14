import pprint

def longest_suffix_prefix_match(str1, str2):
	# returns the length of the longest suffix in str1 that is a prefix in str2
	max = 0
	for i in xrange(len(str1)):
		for j in xrange(len(str2), 0, -1):
			if str1[i:] == str2[:j] and len(str1[i:]) > max:
				max = len(str1[i:])
	return max

class State_Machine:
	def __init__(self, sequence):
		# this constructor builds the entire state machine from the sequence and genome

		self.sequence = sequence

		self.states = range(len(sequence)+1) # integer from 0 to n where n is the length of the search sequence
		self.transitions = [] # list of 3-long lists of (start state, read character, end state)

		for i in xrange(len(self.sequence)):

			# this adds the naive transitions, like the ones described in this line from the spec:
			# STATE_1 --C--> STATE_2 --A--> STATE_3 --T--> END
			self.transitions.append([i, self.sequence[i], i+1])

			# this ensures you go back to the beginning if you read a character that isn't in your string
			for char in ['A', 'C', 'T', 'G']:
				if char not in self.sequence:
					self.transitions.append([i, char, 0])

		# this implements the suffix matching part of the algorithm (this is difficult and I'm not 100% sure it's correct)
		for state in self.states:
			for char in ['A', 'C', 'T', 'G']:
				read_so_far = self.sequence[:state] + char
				shift = longest_suffix_prefix_match(read_so_far, self.sequence)
				self.transitions.append([state, char, shift])

		#pprint.pprint(self.transitions)

	def traverse(self, genome):
		# starts from state 0, follows the sequence. if it ever reaches the last state,
		# then clearly the DFA accepts the sequence, which means the sequence does exist in the genome.
		# otherwise, return false.
		state = self.states[0]

		for char in genome:
			transitioned_yet = False
			#print 'reading {}'.format(char)
			for transition in self.transitions:
				if not transitioned_yet and transition[0] == state and transition[1] == char:
					state = transition[2]
					#print 'moving to state' + str(state)
					transitioned_yet = True
			if state == self.states[len(self.sequence)]:
				return True

		return False

def gene_in_genome(genome, sequence):
	state_machine = State_Machine(sequence)
	print state_machine.traverse(genome)

# tests

gene_in_genome('AGCGACTGACTG', 'ACT') # expect True
gene_in_genome('AAAAA', 'A') # expect True
gene_in_genome('AGCG', 'ACG') # expect False
gene_in_genome('AGGGA', 'GG') # expect True
gene_in_genome('AAGGCTTAGCTAATTAAAA', 'AGCT') # expect True
gene_in_genome('AAGGCTTAATCTAAAA', 'AGCT') # expect False
gene_in_genome('AAGGCTTAATCTAAAA', 'AGT') # expect False
gene_in_genome('AAGGCTTAATCTAAAA', 'CTTAA') # expect True
