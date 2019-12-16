import random
import csv

print("Enter population size for team selection: ", end=" ")
POPULATION_SIZE = int(input())
file = open("dt.csv")
data = csv.reader(file)
bat = dict()
bow = dict()
al = dict()
wc = dict()
player = dict()
for row in data:
        temp = []
        for col in row:
          temp. append(col)
        player[row[0]] = temp
        if(row[-1] == "BAT"):
          bat[row[0]] = temp
        elif(row[-1] == "BOW"):
          bow[row[0]] = temp
        elif(row[-1] == "ALL"):
          al[row[0]] = temp
        elif(row[-1] == "WC"):
          wc[row[0]] = temp			


class Individual(object):
	def __init__(self, chromosome):
		self.chromosome = chromosome
		self.fitness = self.cal_fitness()

	@classmethod
	def mutated_genes(self):
		ls = []
		while(len(ls)!=4):
        		t = random.choice(list(bat.keys()))
        		if(t not in ls):
                		ls.append(t)
		while(len(ls)!=8):
		        t = random.choice(list(bow.keys()))
		        if(t not in ls):
		                ls.append(t)
		while(len(ls)!=10):
		        t = random.choice(list(al.keys()))
		        if(t not in ls):
		                ls.append(t)
		while(len(ls)!=11):
		        t = random.choice(list(wc.keys()))
		        if(t not in ls):
		                ls.append(t)
		return ls	                

	@classmethod
	def create_gnome(self):
		return self.mutated_genes()
 
	def fit(self,item):
	        ft  = list(player.get(self.chromosome[item]))
	        gl = int(ft[4])
	        gp = int(ft[2])
	        gw = int(ft[5])
	        return((1-(gl/gp)+gw)/(1+gw))	

	def cal_fitness(self):
		fitness = 0
		for i in range(11):
			fitness = fitness + self.fit(i)
		return fitness / 11 		

	def mate(self, parent2):
		child_chromosome = []
		for i in range(11):
			if(i < 6):
				child_chromosome.append(self.chromosome[i])
			else:
				child_chromosome.append(parent2.chromosome[i])	
			
		return Individual(child_chromosome)	
				

def main():
	global POPULATION_SIZE

	found = False

	generation = 1

	population = []

	for _ in range(POPULATION_SIZE):
		gnome = Individual.create_gnome()
		population.append(Individual(gnome))

	for i in population:
		 print(i.chromosome," ", i.fitness)	

	flag = 0
	tempfitness = 0
	while not found:
		population = sorted(population, key = lambda x: x.fitness, reverse = True)
		if (population[0].fitness == tempfitness):
			flag = flag + 1
		else:
			tempfitness = population[0].fitness
			flag = 0

		if(flag == 10):
			found = True
			break	
		
		new_generation = []

		s = int((10 * POPULATION_SIZE) / 100)

		new_generation.extend(population[:s])

		s = int((90 * POPULATION_SIZE) / 100)

		for _ in range(s):
			parent1 = random.choice(population[:50])
			parent2 = random.choice(population[:50])
			child1 = parent1.mate(parent2)
			child2 = parent2.mate(parent1)
			new_generation.append(child1)
			new_generation.append(child2)

		for gene in  new_generation:
			fl = 0
			for i in gene.chromosome:
				if(gene.chromosome.count(i)>1):
					fl = 1
			if(fl == 0):		
				population.append(gene)		


		print("Generation:", generation,"\tGene:",population[0].chromosome,"\tFitness:", population[0].fitness)

		generation = generation + 1

	print("Generation:", generation,"\tGene:",population[0].chromosome,"\tFitness:", population[0].fitness)
	print()
	print("FINAL PROPOSED TEAM")
	print()
	print("Player ID\tPlayer Name\tSpeciality")
	for i in range(11):
		row = player.get(population[0].chromosome[i])
		print(row[0], "\t\t",row[1],"\t\t", row[-1])
	

if __name__ == "__main__":
	main()		
