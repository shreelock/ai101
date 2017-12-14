import sys
import random
import copy

def backtracking(level, var_assigned_map, var_domain_map, var_value_map):
    if all_vars_assigned(var_assigned_map):
        print "All assigned", var_value_map
        return

    print "\n\nVariable Assigned Map : ", var_assigned_map
    print "Variable Val Map : ", var_value_map

    unvar = pick_unassigned_var(var_assigned_map)
    print "Selected Unassigned Variable : ", unvar

    for val in var_domain_map[unvar]:
        var_value_map[unvar] = val
        var_assigned_map[unvar] = True
        print "Assigned Variable Val Map : ", var_value_map

        flag = True

        if not all_constraints_satisfied(unvar, var_value_map):
            flag = False

        if constraints_satisfied(var_value_map):
            print "Exiting ... ", var_value_map
            sys.exit(0)


        if flag == True:
            print "Movng to next level"
            backtracking(level+1, copy.deepcopy(var_assigned_map), copy.deepcopy(var_domain_map), copy.deepcopy(var_value_map))








def all_vars_assigned(var_assigned_map):
    for key,val in var_assigned_map.iteritems():
        if val == None:
            return False

    return True

def pick_unassigned_var(var_assigned_map):
    unass_list = list()
    for key, val in var_assigned_map.iteritems():
        if val == None:
            unass_list.append(key)

    return random.choice(unass_list)


def all_constraints_satisfied(var, var_value_map):
    diff_list= list()
    v2 = var_value_map[var]
    print "Comparing ",v2, " , ", var_value_map
    for k1, v1 in var_value_map.iteritems():
        if v1 != None and k1!=var:
            print v1, v2
            diff = abs(v1 - v2)
            if diff in diff_list:
                print "Diff found. returingi"
                return False
            else:
                diff_list.append(diff)
    return True

def constraints_satisfied(var_value_map):
    print "Entering final constraints loop"
    diff_list= list()
    keys = var_value_map.keys()
    for i in xrange(len(keys)):
        if (i+1<len(keys)):
            for j in range(i+1, len(keys)):
                v1=var_value_map[keys[i]]
                v2=var_value_map[keys[j]]
                if v1 != None and v2!=None:
                    print v1, v2
                    diff = abs(v1 - v2)
                    if diff in diff_list:
                        print "Diff found. returingi"
                        return False
                    else:
                        diff_list.append(diff)


    # for k1, v1 in var_value_map.iteritems():
    #     for k2, v2 in var_value_map.iteritems():
    #         print "Comparing ",v2, ",",v1, "," , var_value_map
    #         if v1 != None and v2!=None and k1!=k2:
    #             print v1, v2
    #             diff = abs(v1 - v2)
    #             if diff in diff_list:
    #                 print "Diff found. returingi"
    #                 return False
    #             else:
    #                 diff_list.append(diff)

    print "everything satisfied"
    return True



if __name__ == '__main__':
    L = int(sys.argv[2])
    M = int(sys.argv[1])
    var_assigned_map = dict()
    var_domain_map = dict()
    var_value_map = dict()

    domain_list = range(0, L+1)

    for i in range(1, M+1):
        v = "V"+str(i)
        var_assigned_map[v] = None
        var_domain_map[v] = domain_list
        var_value_map[v] = None

    backtracking(0, var_assigned_map, var_domain_map, var_value_map)