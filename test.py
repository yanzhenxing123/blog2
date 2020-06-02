
def combinationSum(candidates,  target):
    candidates.sort()
    length = len(candidates)
    if length <= 0:
        return
    result = []
    temp_result = []
    def auxiliary(index, temp_result, target):
        if target == 0:
            result.append(temp_result)
            return
        if index == length or target < candidates[index]:
            return
        auxiliary(index, temp_result + [candidates[index]], target - candidates[index])
        auxiliary(index + 1, temp_result, target)
    auxiliary(0, temp_result, target)
    return result


if __name__ == '__main__':
    res  = combinationSum([2,3,6,7], 7)
    print(res)


