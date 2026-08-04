from models.Statement import Statement, Symbol

a = Symbol('A', True)
b = Symbol('B', True)

a_xor_b_meta = (a ^ b).meta()
a_union_b_meta = (a | b).meta()

true = Statement()

true |= a & b # a and b are disparate

# ### 2025-03-22 Work
# # Every ordinary symbol is disparate from the meta symbols
# true |= a & a_xor_b_meta
# true |= a & a_union_b_meta
# true |= b & a_xor_b_meta
# true |= b & a_union_b_meta

# print('true:', str(true), '\n')

# # You and I know that a_xor_b_meta == a_union_b_meta. Does the statement?
# metas_equal = a_xor_b_meta ^ a_union_b_meta
# print('metas equal:', metas_equal, '\n')
# print('missing:', str(metas_equal ^ (metas_equal & true)), '\n')


### 2025-03-28 work
true |= (a | b) & (a_xor_b_meta | a_union_b_meta)
metas_equal = a_xor_b_meta ^ a_union_b_meta
missing = metas_equal ^ (metas_equal & true)
print('missing:', str(missing), '\n')

true_and_missing = missing | true
print('with missing:', metas_equal ^ (true_and_missing & metas_equal), '\n')

# true = true.with_symbol(a).with_symbol(b).with_symbol(a_xor_b_meta).with_symbol(a_union_b_meta)
# print('missing after symbols:', str(metas_equal ^ (metas_equal & true)))

true = Statement.empty()
proof = ((a | b) & (a_xor_b_meta | a_union_b_meta)) | (((a | b) ^ Statement.full()) & (a_xor_b_meta ^ a_union_b_meta))
true |= proof
metas_equal = a_xor_b_meta ^ a_union_b_meta
# (A ^ B ^ A&B ^ U) & ({A ^ B} ^ {A ^ A&B ^ B})
print('metas equal:', metas_equal, '\n')
print('proof:', proof, '\n')
print('proof shows a ^ b:', (a ^ b) ^ (true & (a ^ b)), '\n')
print('proof shows metas are equal:', metas_equal ^ (metas_equal & true), '\n')
print('proof shows a_union_b_meta is empty:', a_xor_b_meta ^ (a_xor_b_meta & true), '\n')
print('proof shows a_xor_b_meta is empty:', a_xor_b_meta ^ (a_xor_b_meta & true), '\n')


# ### 2025-03-31 work
# a_equal_b = (a ^ b) | (
#     true
#     .with_symbol(a)
#     .with_symbol(b)
#     .with_symbol(a_xor_b_meta)
#     .with_symbol(a_union_b_meta)
# )

# print('missing:', str(metas_equal ^ (metas_equal & a_equal_b)), '\n')

### 2025-04-03 work
true = Statement.empty()
