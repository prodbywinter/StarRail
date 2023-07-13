# importing packages
from CharacterProfiles import *
from Statics import *
import numpy as np
import itertools as it
from time import perf_counter


# returns iterable power set of an iterable
def powerset(iterable):
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s) + 1))


# converts superimpose level to scalar
def SItoScalar(level, multiplier):
    if level in np.arange(1, 6):
        scalar = 1 - 0.25 * (level - 1) + multiplier * 0.25 * (level - 1)
        return scalar
    return 1


# update energy gains from basic, skill, and ult
def updateEnergy(options, char):
    skillAttacks, ultAttacks = char.attacksWith
    ER = (1 +
          int(1 in options) * ENERGY_ROPE_5S + int(2 in options) * VONWACQ +
          int(3 in options) * POST_OP * SItoScalar(postOpSuperimpose, 2) +
          int(5 in options) * ASTA_E4 +
          int(6 in options) * ENERGY_ROPE_4S)
    basic = (char.basicEnergy +
             int(8 in options) * BEFORE_TUTORIAL +
             int(9 in options) * MESHING_COGS) * ER
    skill = (char.skillEnergy +
             int(4 in options) * int(SHARED_FEELING * SItoScalar(sharedFeelingSuperimpose, 2)) +
             skillAttacks * (int(8 in options) * BEFORE_TUTORIAL +
                             int(9 in options) * MESHING_COGS)) * ER
    ult = (char.ultEnergy +
           int(7 in options) * THIEF +
           ultAttacks * (int(8 in options) * BEFORE_TUTORIAL +
                         int(9 in options) * MESHING_COGS)) * ER
    return basic, skill, ult


# finds lowest number of skill casts to reach max energy
def cheapestCombo(basic, skill, ult, rotationTurns, maxEnergy):
    skillCasts = 0
    totalEnergy = ult
    while skillCasts < rotationTurns and totalEnergy + skillCasts * skill + (rotationTurns - skillCasts) * basic \
            < maxEnergy - 0.2:  # game rounds up when within 0.2 of max energy
        skillCasts += 1
    return skillCasts, totalEnergy + skillCasts * skill + (rotationTurns - skillCasts) * basic


# culls subsets that are either parents of 1) illegal subsets or 2) smaller subsets
def cullIllegalResults(results):
    culledResults = []
    smallSubsets = []
    smallSubsets += ILLEGAL_OPTION_COMBOS
    for optionsSubset, skillCasts, comboEnergy in results:
        isSmall = 1
        for smallSubset in smallSubsets:
            if set(smallSubset) <= set(optionsSubset):
                isSmall = 0
        if isSmall:
            if len(optionsSubset) > 0:
                smallSubsets.append(optionsSubset)
            culledResults.append([optionsSubset, skillCasts, comboEnergy])
    return np.asarray(culledResults, dtype=object)


# rewrites option list from numbers to names
def readableOptions(options):
    if len(options) == 0:
        return 'none'
    readable = ''
    for option in options:
        readable += OPTION_DICT[option] + ', '
    readable = readable[:-2]
    return readable


# get un-culled results given a character and turns per rotation
def rawResults(char, rotationTurns):
    maxEnergy = char.maxEnergy
    results = []
    for optionsSubset in powerset(char.options):
        basic, skill, ult = updateEnergy(optionsSubset, char)
        skillCasts, comboEnergy = cheapestCombo(basic, skill, ult, rotationTurns, maxEnergy)
        if comboEnergy >= maxEnergy - 0.2:
            results.append([optionsSubset, skillCasts, comboEnergy])
    return results


# cull and print results given results, character, and turns per rotation
def cullAndPrint(results, char, rotationTurns):
    results = np.asarray(results, dtype=object)
    print(f'{char.name}: {char.maxEnergy} ENERGY IN {rotationTurns} TURNS')
    if len(results) == 0:
        print('No results found!')
    else:
        for i in range(rotationTurns + 1):
            currentResults = results[np.where(results[:, 1] == rotationTurns - i)]
            currentResults = cullIllegalResults(currentResults)
            if len(currentResults) > 0:
                print(
                    f' - {rotationTurns - i} SKILL {i} BASIC ({"%.2f" % (2 * i / rotationTurns - 1)} SPT)')
                for optionsSubset, skillCasts, comboEnergy in currentResults:
                    print(f'{readableOptions(optionsSubset)}: {"%.2f" % comboEnergy} energy')
    return


if __name__ == '__main__':
    # start timer
    t0 = perf_counter()

    # parameters
    char = Natasha
    rotationTurns = 4
    postOpSuperimpose = 1
    sharedFeelingSuperimpose = 3

    # get un-culled results
    results = rawResults(char, rotationTurns)

    # cull and print results
    cullAndPrint(results, char, rotationTurns)

    # timing code
    t1 = perf_counter()
    print()
    print(f'Got results in {"%.5f" % (t1 - t0)} s')
