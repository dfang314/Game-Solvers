# you have 2 buckets of size 5 and 3, starting empty
# you have a well of 6 starting energy
# your moves are:
#   transfer energy from one bucket to the other
#   take from well into a bucket (requires filling the bucket)
#   empty bucket back into well
# win by having 4 energy in the big bucket

# moves:
# 0 = fill big
# 1 = transfer big to small
# 2 = dump big
# 3 = fill small
# 4 = transfer small to big
# 5 = dump small

def to_mod_six(num):
    ret = []
    while num >= 6:
        ret.append(num % 6)
        num //= 6
    ret.append(num)
    return ret[::-1]

# print(to_mod_six(81))

def solves(seq):
    big_bucket = 0
    small_bucket = 0
    well = 6
    for move in seq:
        if move == 0:
            if well + big_bucket < 5:
                return
            well = well + big_bucket - 5
            big_bucket = 5
        elif move == 1:
            while big_bucket > 0 and small_bucket < 3:
                big_bucket -= 1
                small_bucket += 1
        elif move == 2:
            well += big_bucket
            big_bucket = 0
        elif move == 3:
            if well + small_bucket < 3:
                return
            well = well + small_bucket - 3
            small_bucket = 3
        elif move == 4:
            while small_bucket > 0 and big_bucket < 5:
                big_bucket += 1
                small_bucket -= 1
        else:
            well += small_bucket
            small_bucket = 0

        if big_bucket == 4:
            print(seq)
            return


for i in range(11000000):
    new_seq = to_mod_six(i)
    solves(new_seq)

    # to_mod_six never generates 0 leading
    # so we make it
    # note that multiple 0 leading is equivalent to 0 such 0
    new_seq = [0] + new_seq
    solves(new_seq)

# prints [3, 4, 3, 4, 2, 4, 3, 4]


