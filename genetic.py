﻿from operator import attrgetter
import random


def crossover(parent, parent2, get_fitness, customCrossover):
    childGenes = parent.Genes[:]
    if customCrossover is not None:
        customCrossover(childGenes, parent2.Genes[:])
    else:
        destIndex = random.randint(0, len(parent.Genes) - 1)
        srcIndex = destIndex if len(parent2.Genes) > destIndex else random.randint(0, len(parent2.Genes) - 1)
        childGenes[destIndex] = parent2.Genes[srcIndex]
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness, "crossover")


def mutate(parent, geneSet, get_fitness, createGene, customMutate):
    childGenes = parent.Genes[:]
    if customMutate is not None:
        customMutate(childGenes)
    else:
        index = random.randint(0, len(parent.Genes) - 1)
        if geneSet is not None:
            geneIndex = random.randint(0, len(geneSet) - 1)
            childGenes[index] = geneSet[geneIndex]
        else:
            childGenes[index] = createGene(index, len(childGenes))

    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness, "mutate")


def generateParent(minLength, maxLength, geneSet, get_fitness, createGene):
    childGenes = []
    length = random.randint(minLength, maxLength)
    if geneSet is not None:
        for i in range(0, length):
            geneIndex = random.randint(0, len(geneSet) - 1)
            childGenes.append(geneSet[geneIndex])
    else:
        for i in range(0, length):
            childGenes.append(createGene(i, length))
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness, "random")


def getBest(get_fitness, display, minLen, optimalFitness,
            geneSet=None, createGene=None, maxLen=None,
            customMutate=None, customCrossover=None):
    random.seed()
    if geneSet is None and createGene is None:
        raise ValueError('must specify geneSet or createGene')
    if geneSet is not None and createGene is not None:
        raise ValueError('cannot specify both geneSet and createGene')
    if maxLen is None:
        maxLen = minLen
    bestParent = generateParent(minLen, maxLen, geneSet, get_fitness, createGene)
    display(bestParent)

    options = {
        0: lambda p: mutate(p, geneSet, get_fitness, createGene, customMutate),
        1: lambda p: crossover(p, bestParent, get_fitness, customCrossover)
    }

    while bestParent.Fitness < optimalFitness:
        parent = generateParent(minLen, maxLen, geneSet, get_fitness, createGene)
        attemptsSinceLastImprovement = 0
        while attemptsSinceLastImprovement < 128:
            child = options[random.randint(0, len(options) - 1)](parent)
            if child.Fitness > parent.Fitness:
                parent = child
                attemptsSinceLastImprovement = 0
            attemptsSinceLastImprovement += 1

        if bestParent.Fitness < parent.Fitness:
            bestParent, parent = parent, bestParent
            display(bestParent)

    return bestParent


class Individual:
    Genes = None
    Fitness = None
    Strategy = None

    def __init__(self, genes, fitness, strategy):
        self.Genes = genes
        self.Fitness = fitness
        self.Strategy = strategy
