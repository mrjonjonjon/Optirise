def my_log(x):
    ans=0
    while x&1==0:
        x>>=1
        ans+=1
    return ans


print(my_log(1))