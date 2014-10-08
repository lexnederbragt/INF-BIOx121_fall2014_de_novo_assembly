stopAfter = unitigger
unitigger = bogart
utgErrorRate = 0.06
utgErrorLimit = 4.5

cnsErrorRate = 0.25
cgwErrorRate = 0.25
ovlErrorRate = 0.06

frgMinLen = 500
ovlMinLen = 40

merSize=14

merylMemory = 16282
merylThreads = 2 # not 8

ovlStoreMemory = 16282

# grid info
useGrid = 0
scriptOnGrid = 0
frgCorrOnGrid = 0
ovlCorrOnGrid = 0

sge = -S /bin/bash -sync y -V -q None
sgeScript = -pe None 15
sgeConsensus = -pe None 1
sgeOverlap = -pe None 1
sgeFragmentCorrection = -pe None 2
sgeOverlapCorrection = -pe None 1

ovlHashBits = 25
ovlHashBlockLength = 982515712
ovlRefBlockSize =  13

ovlThreads = 1
ovlConcurrency = 1 # not 15
batThreads = 2 #new
frgCorrThreads = 2
frgCorrBatchSize = 100000
ovlCorrBatchSize = 100000

sgeName = pacbioReads
