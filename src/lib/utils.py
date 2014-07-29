# coding=utf-8
__author__ = 'xeye'


def iterate_stream(stream):
    """Char by char iteration ignoring newlines"""
    for line in stream:
        for char in line:
            yield char


if __name__ == '__main__':
    pass