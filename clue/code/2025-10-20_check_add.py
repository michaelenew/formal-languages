from __future__ import annotations

class SetNum:
    def __init__(self, components: frozenset[SetNum]):
        if type(components) != frozenset:
            raise ValueError(f'Bad type trying to build SetNum {type(components)}')
        if any(type(contained) != SetNum for contained in components):
            raise ValueError(f'Bad contained type trying to build SetNum {set(map(type, components))}')
        self.components = components

    @classmethod
    def from_int(cls, num: int) -> SetNum:
        binary = bin(num)
        iter_through = binary[::-1][:-2]
        component = 0
        all_components = set()
        for exists in iter_through:
            if exists == '1':
                all_components.add(SetNum.from_int(component))
            component = component + 1
        return SetNum(frozenset(all_components))
    
    def to_int(self) -> int:
        return sum(
            2 ** component.to_int()
            for component in self.components
        )
    
    def x2(self, max_place: int = 100) -> SetNum:
        return SetNum(frozenset({
            SetNum.from_int(inted + 1)
            for component in self.components
            for inted in [component.to_int()]
            if max_place is None or inted < max_place
        }))

    def bang(self, places: int = 100) -> SetNum:
        curr_total = self
        curr_self_xn = self
        for _ in range(places):
            curr_self_xn = curr_self_xn.x2(places)
            curr_total = curr_total ^ curr_self_xn
        return curr_total
    
    def bang_inv(self) -> SetNum:
        return self ^ self.x2()
    
    def __and__(self, other: SetNum) -> SetNum:
        return SetNum(self.components.intersection(other.components))
    
    def __xor__(self, other: SetNum) -> SetNum:
        return SetNum(
            self.components.union(other.components)
            - self.components.intersection(other.components)
        )

    def __hash__(self) -> int:
        return hash(frozenset({
            hash(component)
            for component in self.components
        }))
    
    def __eq__(self, other: SetNum) -> bool:
        return self.to_int() == other.to_int()
    

    def __add__(self, other: SetNum) -> SetNum:
        self_and_other_2 = (self & other).x2()
        self_and_other_4 = self_and_other_2.x2()
        self_term = (self.x2() & self_and_other_4)
        other_term = (other.x2() & self_and_other_4)

        mbin = lambda s : bin(s.to_int())[::-1][:-2]
        bang_bin = lambda s : mbin(s.bang())
        print()
        print()
        print()
        print(mbin(self))
        print(mbin(other))
        print()
        print(mbin(self_and_other_2))
        print(bang_bin(self_and_other_2))
        print(mbin(self_and_other_4))
        print(bang_bin(self_and_other_4))
        print(mbin(self_term))
        print(bang_bin(self_term))
        print(mbin(other_term))
        print(bang_bin(other_term)) #

        return self ^ other ^ (
            self_and_other_2
            ^ self_and_other_4
            ^ self_term
            ^ other_term
        ).bang()
    

    # def __add__(self, other: SetNum) -> SetNum:
    #     self_and_other_2 = (self & other).x2()
    #     self_and_other_4 = self_and_other_2.x2()
    #     return self ^ other ^ (
    #         self_and_other_2
    #         ^ self_and_other_4
    #         ^ ((self.x2() ^ other.x2()) & self_and_other_4)
    #     ).bang()
    
    def __str__(self) -> str:
        return f'SetNum({self.to_int()})'



# from_int is working
# print(set(map(str, SetNum.from_int(31).components)))


# x2 is working
# for i in range(100):
#     print(i, i * 2, SetNum.from_int(i).x2().to_int())


# ^ is working
# for i in range(10):
#     for j in range(10):
#         num_i = SetNum.from_int(i)
#         num_j = SetNum.from_int(j)
#         actual_components = sorted(map(str, (num_i ^ num_j).components))
#         num_i_components = set(map(str, num_i.components))
#         num_j_components = set(map(str, num_j.components))
#         expected_components = sorted(num_i_components.union(num_j_components) - num_j_components.intersection(num_i_components))
#         if expected_components != actual_components:
#             print(i, j, expected_components, actual_components)


# & is working
# for i in range(10):
#     for j in range(10):
#         num_i = SetNum.from_int(i)
#         num_j = SetNum.from_int(j)
#         actual_components = sorted(map(str, (num_i & num_j).components))
#         num_i_components = set(map(str, num_i.components))
#         num_j_components = set(map(str, num_j.components))
#         expected_components = sorted(num_j_components.intersection(num_i_components))
#         if expected_components != actual_components:
#             print(i, j, expected_components, actual_components)


# bang and bang_inv are working
mbin = lambda s : bin(s.to_int())[::-1][:-2]
for i in range(100):
    if SetNum.from_int(i) != SetNum.from_int(i).bang().bang_inv() or SetNum.from_int(i).bang_inv().bang() != SetNum.from_int(i):

        print()
        print()
        print()
        print(mbin(SetNum.from_int(i)))
        print(mbin(SetNum.from_int(i).bang().bang_inv()))
        print(mbin(SetNum.from_int(i).bang_inv().bang()))
        print()
        print(mbin(SetNum.from_int(i)))
        print(mbin(SetNum.from_int(i).bang()))



# # Verifying addition:
# for i in range(10):
#     for j in range(10):
#         num_i = SetNum.from_int(i)
#         num_j = SetNum.from_int(j)
#         first = '{} + {} = {}'.format(i, j, i+j)
#         second = '{} + {} = {}'.format(num_i.to_int(), num_j.to_int(), (num_i + num_j).to_int())

#         if first != second:
#             print(first, '|', second)
#             print(sorted(map(str, num_i.components))[::-1], sorted(map(str, num_j.components))[::-1])
#             print()



