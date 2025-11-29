# DIFFER: 4AufqXeUNU63Ww9nKwKb8RhqK4ghSgX8X4oSBfHvV2NEZNx7qqkb14Q3CrnYvABqD6MT1g17mQZqsF32stvcD6QzDWZbqoQ
# old: 539f4d7e88075673ae1430d3d326a373b3c06b5729272c073ac5593c25e1cb99
# new: 539f4d7e88075673ae1430d3d326a373b3c16b5729272c073ac5593c25e1cb99
test1 = "539f4d7e88075673ae1430d3d326a373b3c06b5729272c073ac5593c25e1cb99"
test2 = "539f4d7e88075673ae1430d3d326a373b3c16b5729272c073ac5593c25e1cb99"
# DIFFER: 4ARYK2yekQZG6PUCLeNUP1E2oPZoJQWgHcWRzhGHAjwuii1JtNDk2PcX3x7Yft1jFFK7t1QuS87BSGu2JDVMoobv1iTtg9Y
# old: 8d9c541dffbb7696db8538a946d4feef57fa3d60fb80bb672ba910603938082f
# new: 8d9c541dffbb7696db9538a946d4feef57fa3d60fb80bb672ba910603938082f
test1 = "8d9c541dffbb7696db8538a946d4feef57fa3d60fb80bb672ba910603938082f"
test2 = "8d9c541dffbb7696db9538a946d4feef57fa3d60fb80bb672ba910603938082f"
#pip install monero
from monero.seed import Seed
seed1 = Seed(test1)
print('seed1.public_address():',seed1.public_address())
seed2 = Seed(test2)
print('seed2.public_address():',seed2.public_address())
