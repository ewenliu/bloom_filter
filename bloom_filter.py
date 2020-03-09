# -*- coding: utf-8 -*-#

# 提供二进制向量
from bitarray import bitarray
# 提供hash函数mmh3.hash()
import mmh3


class BloomFilter(set):
    """
    size: 二进制向量长度
    hash_count: hash函数个数

    一般来说，hash函数的个数要满足（hash函数个数=二进制长度*ln2/插入的元素个数）
    """
    def __init__(self, size, hash_count):
        super(BloomFilter, self).__init__()
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.size = size
        self.hash_count = hash_count

    def __len__(self):
        return self.size

    # 使得BloomFilter可迭代
    def __iter__(self):
        return iter(self.bit_array)

    def add(self, item):
        for ii in range(self.hash_count):
            # 假设hash完的值是22，size为20，那么取模结果为2，将二进制向量第2位置为1
            index = mmh3.hash(item, ii) % self.size
            self.bit_array[index] = 1

        return self

    # 可以使用 xx in BloomFilter方式来判断元素是否在过滤器内（有小概率会误判不存在的元素也存在, 但是已存在的元素绝对不会误判为不存在）
    def __contains__(self, item):
        out = True
        for ii in range(self.hash_count):
            index = mmh3.hash(item, ii) % self.size
            if self.bit_array[index] == 0:
                out = False

        return out


def main():
    bloom = BloomFilter(100, 10)
    animals = ['dog', 'cat', 'giraffe', 'fly', 'mosquito', 'horse', 'eagle',
               'bird', 'bison', 'boar', 'butterfly', 'ant', 'anaconda', 'bear',
               'chicken', 'dolphin', 'donkey', 'crow', 'crocodile']
    # 新增过滤规则
    for animal in animals:
        bloom.add(animal)

    # 已经插入的动物应该绝对满足存在
    for animal in animals:
        if animal in bloom:
            print('{}在布隆过滤器中......'.format(animal))
        else:
            print('{}不在布隆过滤器中......'.format(animal))

    print('\n')
    print('这是分割线', '-'*100)
    print('\n')

    # 未插入的动物，发现'sheep'不在过滤规则里，但是确判定为存在，由此可见布隆过滤器有一定的误判几率（宁可误杀不可放走）
    other_animals = ['badger', 'cow', 'pig', 'sheep', 'bee', 'wolf', 'fox',
                     'whale', 'shark', 'fish', 'turkey', 'duck', 'dove',
                     'deer', 'elephant', 'frog', 'falcon', 'goat', 'gorilla',
                     'hawk']
    for other_animal in other_animals:
        if other_animal in bloom:
            print('{}在布隆过滤器中......'.format(other_animal))
        else:
            print('{}不在布隆过滤器中......'.format(other_animal))


if __name__ == '__main__':
    main()
