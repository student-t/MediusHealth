#
# Native implementation for Apriori Algorithm
#
# This script assumes the input TSV file come from clean.py.
# 
# Run with python3 apriori.py data.tsv 10 where 10 is the support threshold
#

import sys
from queue import Queue

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(('\nRun with python3 apriori.py data.tsv 10 where 10 is the support threshold'))
    else:
        # Support threshold (no type checking assuming it's an integer)
        thre = int(sys.argv[2])

        def readTSV(name):
            r = open(name, 'r')
            for line in r:
                strs = line.split('\t')
                assert(len(strs) == 2)
                yield (strs[0], strs[1].strip())

        #
        # Native implementation for candidate generation (simply join the items)
        #

        def candidate(items, k1):
            return (([i + ' ' + j for i in items for j in k1]))

        #
        # Native implementation for counting input items and return a dictionary with the counts
        #

        def count(items, trans):
            x = {i:0 for i in items}
    
            for tran in trans:
                for item in items:
                    x[item] += tran.count(item)
            return x
    
        items = set()

        # Transactions (e.g. medical records)
        trans = []

        for (x, y) in readTSV(sys.argv[1]):
            trans.append(y)
    
            # Our cleanup script guarantees no English stopwords, no tabs etc. We just need to break the text by space to get individual words.
            items.update(y.split(' '))

        # Data structure for breadth-first search
        q = Queue()

        for item in items:
            q.put(item)

        # Start off with k=2 (individual words at k=1 computed in the loop above)
        k = 2

        fItems = {}
        fFreqs = {}

        #
        # Apply breadth-first search with pruning
        #

        while not q.empty():
            items = set()
    
            # Get all items from the queue, more effiicient for frequency counting
            while not q.empty():
                items.add(q.get())

            # Count all items at k
            freq = count(items, trans) 

            # Prunce away all items that are smaller than the support threshold. We can do this because of apriori property.
            items = [i for i in items if freq[i] >= thre]

            if len(items) > 0:
                fItems[k-1] = items
                fFreqs[k-1] = freq
        
                # Compute candidate sets at k
                for j in candidate(items, fItems[1]):
                    q.put(j)
            
                k += 1

        for i in fItems:
            for j in fItems[i]:
                print(str(j) + '\t' + str(fFreqs[i][j]))
