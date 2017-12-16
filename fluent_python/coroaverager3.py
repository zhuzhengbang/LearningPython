from collections import namedtuple

Result = namedtuple('Result','count average')

#the subgenerator
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count+=1
        average = total/count
    return Result(count,average)

#the delegating generator
def grouper(results,key):
    while True:
        results[key] = yield from averager()


#the client code, a.k.a. the caller
def main(data):
    results = {}
    for key,values in data.items():
        group = grouper(results,key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None) #important

    report(results)

def report(results):
    for key,result in sorted(results.items()):
        group,unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count,group,result.average,unit))


data = {

    'girls;kg':
        [40.9,38.5],
    'girls;m':
        [1.6,1.51],
    'boys;kg':
        [39.0,40.8],
    'boys;m':
        [1.38,1.5]

    }

if __name__=='__main__':
    main(data)
    
