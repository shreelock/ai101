import sys
import time
COUNT=0
#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

def compute_dis_arr(golomb_arr):
    dist_arr=[]
    lgol = len(golomb_arr)
    for i in xrange(lgol):
        for j in xrange(lgol):
            diff = abs(golomb_arr[i] - golomb_arr[j])
            if diff not in dist_arr:
                dist_arr.append(diff)
    return dist_arr


def check_golomb(newitem, golomb_arr):
    #pint "Checking ", newitem, " for ", golomb_arr
    global COUNT
    COUNT=COUNT+1
    dist_arr=compute_dis_arr(golomb_arr)
    # print "enterin : ", COUNT

    for item in golomb_arr:
        diff = abs(item - newitem)
        if diff in dist_arr:
            return False

    #pint "Check is true for", newitem, golomb_arr
    return True

def run_golomb(order, startidx, length, golomb_arr):
    #pint "\nGolomb Arr :", golomb_arr
    golomb_L = 0
    golomb_M = 0

    if len(golomb_arr) != 0:
        golomb_L = max(golomb_arr) - min(golomb_arr)
        golomb_M = len(golomb_arr)

    if golomb_M==order and golomb_L==length:
        return (True, golomb_arr)

    if golomb_L>length:
        return (False, False)

    for i in range(startidx, length+1):
        #pint "Distance : ", i

        if check_golomb(i, golomb_arr):
            # we are assigning the values to the next variable if only
            # it satisfies the constraints for before variables.
            gol_copy = golomb_arr[:]
            gol_copy.append(i)

            (retval, retarr) = run_golomb(order, i+1, length, gol_copy)
            if retval == True:
                return (True, retarr)

    return (False, False)


def run_golomb_fc(order, startidx, length, golomb_arr):
    #pint "\nGolomb Arr :", golomb_arr
    golomb_L = 0
    golomb_M = 0

    if len(golomb_arr) != 0:
        golomb_L = max(golomb_arr) - min(golomb_arr)
        golomb_M = len(golomb_arr)

    if golomb_M==order and golomb_L==length:
        return (True, golomb_arr)

    if golomb_L>length:
        return (False, False)

    for i in range(startidx, length+1):
        # print "Distance : ", i
        flag = False
        dist_arr_n = compute_dis_arr(golomb_arr)
        for assgn in golomb_arr:
            for dists in dist_arr_n:
                if i == assgn+dists:
                    flag = True
                    break
        if flag == True:
            continue

        if check_golomb(i, golomb_arr):
            gol_copy = golomb_arr[:]
            gol_copy.append(i)

            (retval, retarr) = run_golomb_fc(order, i+1, length, gol_copy)
            if retval == True:
                return (True, retarr)

    return (False, False)


#Your backtracking function implementation
def BT(L, M):
    "*** YOUR CODE HERE ***"
    golomb_arr=list()
    t = time.time()
    (retval, retarr) = run_golomb(M, 0, L, golomb_arr)
    if retval==True:
        goodretarr = retarr
        goodL = L
        # print "solution exists."
        L=M-1
        retval = False
        while (retval == False):
            L=L+1
            global COUNT
            COUNT=0
            print "Golomb ruler does not exist for M=", M, "L=",L, "\n finding more optimal length"
            (retval, retarr) = run_golomb(M, 0, L, golomb_arr)
            if retval == True:
                goodretarr = retarr
                goodL = L

        # print "L : ", L+1
        elapsed = time.time() - t
        print "Elapsed : ", elapsed
        print "count : ", COUNT
        return goodL, goodretarr
    return -1,[]

#Your backtracking+Forward checking function implementation
def FC(L, M):
    golomb_arr=list()
    t = time.time()
    (retval, retarr) = run_golomb_fc(M, 0, L, golomb_arr)
    if retval==True:
        goodretarr = retarr
        goodL = L
        # print "solution exists."
        L=M-1
        retval = False
        while (retval == False):
            L=L+1
            global COUNT
            COUNT=0
            print "Golomb ruler does not exist for M=", M, "L=",L, "\n finding more optimal length"
            (retval, retarr) = run_golomb_fc(M, 0, L, golomb_arr)
            if retval == True:
                goodretarr = retarr
                goodL = L

        # print "L : ", L+1
        elapsed = time.time() - t
        print "Elapsed : ", elapsed
        print "count : ", COUNT
        return goodL, goodretarr
    return -1,[]

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

if __name__ == '__main__':
    L= 17
    M = 2
    print BT(L,M)
    print FC(L,M)