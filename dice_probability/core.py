'''
I am using occurences rather than probabilities for the majority of the calculations. This makes it a lot easier
to combine multiple dice rolls together.

When I have my final number of occurences, I can then use die_probs() in order to turn the
occurences into probabilities which can then be used to do stuff like calculating damage


'''

import math

def create_die(sides):
    """Create a die with the specified number of sides."""
    return {i: 1 for i in range(1, sides + 1)}

# Pre-defined dice
d4 = create_die(4)
d6 = create_die(6)
d8 = create_die(8)
d10 = create_die(10)
d12 = create_die(12)
d20 = create_die(20)

def die_probs(die):
     ''' Takes the number of occurences on a die roll or a set of die rolls,
     and turns those into probabilities in the form of a probability mass function (pmf)
     This also works with lists containing dictionaries. In that case, the output is also
     A list containing the same number of dictionaries
     '''

     #if the dieroll or set of dierolls is given as a single dictionary, use this code
     if isinstance(die,dict):
          pmf = {roll: occ/(sum(die.values())) for roll, occ in die.items()}

     #if the dieroll is given as a list containings a few separate dictionaries
     #(as is the case when working with crits) instead use this code
     #We need to sum the occurences of all the dictionaries in the list to get
     #to the total number of occurences, instead of summing them individually per dictionary
     if isinstance(die,list):
          die_total = 0
          for die_dict in die:
               die_total += sum(die_dict.values())

          pmf = [{roll: occ / die_total for roll, occ in sub_die.items()}for sub_die in die]

     return (pmf)

def many_dice (*dice, with_crit = False):

     ''' Calculates the number of occurences of each outcome as
     the result of taking the sum of rolling multiple dice. This function
     always returns a list containing a dictionary. If with_crit is set to true, it instead
     returns a list with three dictionaries. One with the regular rolls, one with the crit fails
     and one with the crit hits. The crits are based on the first die in the input.
     '''

     if isinstance (dice[0],tuple):
               dice = dice[0]

     if not with_crit:
     #This code ensures that if a tuple is entered as variable, we don't convert the nested tuple
     #Into a regular tuple. The nested tuple happened when calling many_dice through other functions
          
              
          outcome = {}

          #we add the dice to the outcome one by one
          for die in dice:
             
             if outcome:
                 temp_outcome = {}
                 
                 for die_roll, die_occ in die.items():

                     #each new roll is determined by the sum of a roll we already had stored and the current
                     #die roll. The number of occurences is the product of our stored occurence and the
                     #current die rolls occurences. Several combinations can contribute to the same new roll
                     for outcome_roll, outcome_occ in outcome.items():
                         new_roll = die_roll + outcome_roll
                         new_occ = outcome_occ * die_occ

                         if new_roll in temp_outcome:
                             temp_outcome[new_roll] += new_occ

                         else:
                             temp_outcome[new_roll] = new_occ
                             
                 outcome = temp_outcome
                 
             else:
                 outcome = die
             
          return ([outcome])


     if with_crit:

 
          outcomes = [{},{},{}]
          
          #we add the dice to the outcome one by one

         
          for die in dice:
                       
               if outcomes[0]:
                    temp_outcomes = [{},{},{}]
                      
                    for die_roll, die_occ in die.items():
                         for i, outcome in enumerate(outcomes):
                              #print(outcome)
                              
                              #each new roll is determined by the sum of a roll we already had stored and the current
                              #die roll. The number of occurences is the product of our stored occurence and the
                              #current die rolls occurences. Several combinations can contribute to the same new roll
                              
                              for outcome_roll, outcome_occ in outcome.items():
                                   #print(outcome_roll)
                                   new_roll = die_roll + outcome_roll
                                   #print(new_roll)
                                   new_occ = outcome_occ * die_occ
                                   #print('is', new_roll, 'in: ', temp_outcomes[0], '?')
                              
                                   if new_roll in temp_outcomes[i]:
                                       temp_outcomes[i][new_roll] += new_occ
                                       #print(temp_outcomes[0][new_roll])

                                   else:
                                       temp_outcomes[i][new_roll] = new_occ
                                       #print(temp_outcomes[0])
                                  
                    outcomes = temp_outcomes
                                     
               else:
                 outcomes[0] = dict(list(die.items())[1:-1])
                 outcomes[1] = dict(list(die.items())[:1])
                 outcomes[2] = dict(list(die.items())[-1:])
                 
##          #testcode to make sure that when you combine all the crit values,
##          #you get back to the same result as the non-crit values
##          combined = {}
##          for outcome in outcomes:
##               if combined:
##                    for roll, occ in outcome.items():
##                         if roll in combined:
##                              combined[roll] += occ
##                         else:
##                              combined[roll] = occ
##               else:
##                    combined = outcome
##
##          combined_sorted = {key: val for key, val in sorted(combined.items())}     
##          print (combined_sorted)
             
          return (outcomes)


def Adv (die = d20, n = 2) :
    '''
    Calculates the number of occurences of each possible outcome when rolling a number of
    dice and keeping the highest value
    Takes an argument die for die size, and an argument n for number of dice
    '''
    #Calculate the probabilities of the complementary cumulative distribution function (com cdf).
    #I then turn this into the probability mass function (pmf)
    #There might be other ways but I just know the mathematical formula for this
    #one which means I don't need to use nested loops
    com_cdf = {roll: (roll / len(die)) ** n for roll in die} 
    pmf = {}
    
    for roll, prob in com_cdf.items():
        if roll == 1:
            pmf[roll] = prob
        else:
            pmf[roll] = prob - com_cdf[roll - 1]

    #turn the calculated probabilities into occurences, since occurences make it much easier
    #to do further calculations with dice rolls
    occs = {key: int(round(value * len(die)**n)) for key, value in pmf.items()}
    return (occs)

def disAdv(die = d20, n = 2):
    '''
    Calculates the number of occurences of each possible outcome when rolling a number of
    dice and keeping the lowest value.
    Takes an argument die for die size, and an argument n for number of dice.
    This function works by simply inverting the Adv() function
    '''
    occs = {len(die) + 1 - key: value for key, value in Adv(die, n).items()}
    
    sorted_occs = {key: val for key, val in sorted(occs.items())} 
    
    return (sorted_occs)    
    

def check (*dice, mod = 0, with_crit = True):
     '''
     Adds a modifier to the rolls, resulting in a pmf for a full on ability/attack/spell check
     '''
     #This code ensures that if a tuple is entered as variable, we don't convert the nested tuple
     #Into a regular tuple. The nested tuple happened when calling check through other functions
     if isinstance (dice[0],tuple):
          dice = dice[0]
         
     
     dice_occs = many_dice(dice, with_crit = with_crit)
     unmod_pmf = die_probs(dice_occs)
     #print(unmod_pmf)
     pmf = [{},{},{}]
     for i, sub_pmf in enumerate(unmod_pmf):
          pmf[i] = {key+ mod : value  for key, value in sub_pmf.items()}
     

##     if with_crit :
##          pmf = (pmf_hit,pmf_crit_hit,pmf_fumble)
##     else:
##          pmf

     return (pmf)


def damage_per_outcome(
     base_damage = 1,
     bonus_damage = 0,
     crit = False,
     fumble = False,
     impact = False, #1 on heavy
     rolls = list(range(1,21)),
     defense = 10,
     dr = 0, #bypassed by heavy or critical
     bonus_reduction = 0,
     type_multiplier = 1,
     type_adder = 0,
     gwf = False, #2 on brutal or critical
     brutal_strikes = False #1 on brutal
     ):

    dict_keys = list(rolls)

    damage_on_roll = {}

    #A fumble always results in no damage
    if fumble:
         damage_on_roll = {key:0 for key in dict_keys}

         return damage_on_roll
     
    impact_dmg = 0
    gwf_dmg = 0
    brutal_strikes_dmg = 0
    
    for key in dict_keys:
        if key < defense and crit == False:
            damage_on_roll[key] = 0
        else:
            impact_dmg = 0
            gwf_dmg = 0 #
            brutal_strikes_dmg = 0
            crit_dmg = 0
            dr_reduction = dr

            if crit:
                 dr_reduction = 0
                 crit_dmg = 2
                 if gwf: gwf_dmg = 2
            
            by_fives_damage = max(math.floor((key - defense) / 5),0)
            if by_fives_damage >= 1:
                if impact : impact_dmg = 1
                    
                dr_reduction = 0
            if by_fives_damage >= 2:
                if gwf: gwf_dmg = 2
                    
                if brutal_strikes: brutal_strikes_dmg = 2
   
            damage = base_damage + bonus_damage + crit_dmg + impact_dmg + gwf_dmg + brutal_strikes_dmg + by_fives_damage 
            reduction = dr_reduction + bonus_reduction

            pre_total = max (damage - reduction, 0)

            total = math.ceil((pre_total + type_adder) * type_multiplier)
            
            damage_on_roll[key] = total
        

    return (damage_on_roll)



def attack_outcomes (*dice,
                     mod = 0,
                     defense = 10,
                     base_damage = 1,
                     bonus_damage = 0,
                     impact = False,
                     dr = 0, 
                     bonus_reduction = 0,
                     type_multiplier = 1,
                     type_adder = 0,
                     gwf = False, #2 on brutal or critical
                     brutal_strikes = False #1 on brutal
                     ):

     if isinstance (dice[0],tuple):
          dice = dice[0]
     
     normals, fumbles ,crits = check(dice, mod = mod, with_crit = True)

     

     damage_on_roll_normal = damage_per_outcome(crit = False,
                                                fumble = False,
                                                rolls = normals,
                                                defense = defense,
                                                base_damage = base_damage,
                                                bonus_damage = bonus_damage,
                                                impact = impact,
                                                dr = dr, 
                                                bonus_reduction = bonus_reduction,
                                                type_multiplier = type_multiplier,
                                                type_adder = type_adder,
                                                gwf = gwf, 
                                                brutal_strikes = brutal_strikes 
                                                )
     
     damage_on_roll_fumble = damage_per_outcome(crit = False,
                                                fumble = True,
                                                rolls = fumbles,
                                                defense = defense,
                                                base_damage = base_damage,
                                                bonus_damage = bonus_damage,
                                                impact = impact,
                                                dr = dr, 
                                                bonus_reduction = bonus_reduction,
                                                type_multiplier = type_multiplier,
                                                type_adder = type_adder,
                                                gwf = gwf, 
                                                brutal_strikes = brutal_strikes 
                                              )

     damage_on_roll_crit = damage_per_outcome(crit = True,
                                              fumble = False,
                                              rolls = crits,
                                              defense = defense,
                                              base_damage = base_damage,
                                              bonus_damage = bonus_damage,
                                              impact = impact,
                                              dr = dr, 
                                              bonus_reduction = bonus_reduction,
                                              type_multiplier = type_multiplier,
                                              type_adder = type_adder,
                                              gwf = gwf, 
                                              brutal_strikes = brutal_strikes 
                                              )

     
     
     damage_pmf = {damage:0 for damage in list(damage_on_roll_normal.values()) +
                   list(damage_on_roll_crit.values()) + list(damage_on_roll_fumble.values())
                   }
     for dmg_key, dmg_value in damage_on_roll_normal.items():
          for hit_key, hit_value in normals.items():
               if dmg_key == hit_key:
                    damage_pmf[dmg_value] += hit_value
     for dmg_key, dmg_value in damage_on_roll_crit.items():
          for hit_key, hit_value in crits.items():
               if dmg_key == hit_key:
                    damage_pmf[dmg_value] += hit_value
     for dmg_key, dmg_value in damage_on_roll_fumble.items():
          for hit_key, hit_value in fumbles.items():
               if dmg_key == hit_key:
                    damage_pmf[dmg_value] += hit_value
          

     #damage_on_roll_normal = damage_per_outcome(crit = True,to_hit = crits)

     damage_pmf = {key: round(value, 4) for key, value in damage_pmf.items()}
         
     return (damage_pmf)
    

def average_atk_damage (damage_pmf):

     
     average_damage = sum([key * value for key, value in damage_pmf.items()])

     return (round(average_damage,2))