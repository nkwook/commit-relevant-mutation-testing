pre_score=[0.667, 0.667, 1, 0.7895, 0.4, 0.2963, 0]
post_score=[0.575, 0.667, 0.8667, 0.8861, 0.6316, 0.5, 0.6111]

#calculate correlation between two lists
def correlation(list1, list2):
    if len(list1) != len(list2):
        print("Error: lists are not the same length")
        return
    n = len(list1)
    sum1 = 0
    sum2 = 0
    sum1Sq = 0
    sum2Sq = 0
    pSum = 0
    for i in range(n):
        sum1 += list1[i]
        sum2 += list2[i]
        sum1Sq += list1[i] ** 2
        sum2Sq += list2[i] ** 2
        pSum += list1[i] * list2[i]
    num = pSum - (sum1 * sum2 / n)
    den = ((sum1Sq - sum1 ** 2 / n) * (sum2Sq - sum2 ** 2 / n)) ** 0.5
    if den == 0:
        return 0
    return num / den

print(correlation(pre_score, post_score))