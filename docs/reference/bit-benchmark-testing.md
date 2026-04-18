Benchmarks

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: gemma-4-31b-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128         18902.7       92.62    54.2 tok/s    10.9 tok/s      30.665    37.6 tok/s    17.79 GB
pp4096/tg128         79347.0      103.16    51.6 tok/s     9.8 tok/s      92.449    45.7 tok/s    19.30 GB
pp8192/tg128        172109.6      136.46    47.6 tok/s     7.4 tok/s     189.440    43.9 tok/s    19.61 GB
pp16384/tg128       341264.8      227.67    48.0 tok/s     4.4 tok/s     370.179    44.6 tok/s    20.45 GB
pp32768/tg128       805753.8      312.80    40.7 tok/s     3.2 tok/s     845.480    38.9 tok/s    22.79 GB
pp65536/tg128      3103968.9     1240.68    21.1 tok/s     0.8 tok/s    3261.536    20.1 tok/s    27.57 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          10.9 tok/s     1.00x    54.2 tok/s    54.2 tok/s     18902.7      30.665
2x           2.6 tok/s     0.24x    15.9 tok/s     8.0 tok/s    128345.9     226.232
4x           4.0 tok/s     0.37x    36.5 tok/s     9.1 tok/s     83401.3     241.672

 ===
 
 gemma-4-26b-it-bf16:
 
 "Model 'gemma-4-26b-a4b-it-bf16' (50.47GB) exceeds max-model-memory (50.40GB)"
 
- Model has been deleted from drive
 
 ===
 
 oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: Qwen3.5-35B-A3B-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128          4866.8       27.63   210.4 tok/s    36.5 tok/s       8.375   137.5 tok/s    19.25 GB
pp4096/tg128         16352.3       29.72   250.5 tok/s    33.9 tok/s      20.127   209.9 tok/s    20.03 GB
pp8192/tg128         33991.4       34.00   241.0 tok/s    29.6 tok/s      38.310   217.2 tok/s    20.38 GB
pp16384/tg128        80526.5       42.55   203.5 tok/s    23.7 tok/s      85.931   192.2 tok/s    21.00 GB
pp32768/tg128       206183.3       62.60   158.9 tok/s    16.1 tok/s     214.133   153.6 tok/s    22.34 GB
pp65536/tg128       483950.9      102.14   135.4 tok/s     9.9 tok/s     496.922   132.1 tok/s    25.02 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          36.5 tok/s     1.00x   210.4 tok/s   210.4 tok/s      4866.8       8.375
2x          33.2 tok/s     0.91x   149.8 tok/s    74.9 tok/s     13451.6      21.394
4x          40.5 tok/s     1.11x   152.8 tok/s    38.2 tok/s     26127.6      39.454

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: DeepSeek-R1-Distill-Qwen-32B-MLX-4Bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128         21598.4       84.33    47.5 tok/s    12.0 tok/s      32.308    35.7 tok/s    17.89 GB
pp4096/tg128         54762.9      101.31    74.8 tok/s     9.9 tok/s      67.629    62.5 tok/s    19.03 GB
pp8192/tg128        127907.7      119.99    64.1 tok/s     8.4 tok/s     143.147    58.1 tok/s    19.92 GB
pp16384/tg128       349728.2      163.98    46.9 tok/s     6.1 tok/s     370.554    44.6 tok/s    21.89 GB
pp32768/tg128       802248.2      261.10    40.8 tok/s     3.9 tok/s     835.408    39.4 tok/s    25.93 GB
pp65536/tg128      1980231.7      369.36    33.1 tok/s     2.7 tok/s    2027.140    32.4 tok/s    34.04 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          12.0 tok/s     1.00x    47.5 tok/s    47.5 tok/s     21598.4      32.308
2x           9.1 tok/s     0.76x    49.5 tok/s    24.8 tok/s     41122.7      69.478
4x           9.7 tok/s     0.81x    91.5 tok/s    22.9 tok/s     33284.0      97.789

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: Mistral-Small-3.2-24B-Instruct-2506-MLX-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128         19738.5       86.03    51.9 tok/s    11.7 tok/s      30.664    37.6 tok/s    13.14 GB
pp4096/tg128         76398.4       99.76    53.6 tok/s    10.1 tok/s      89.067    47.4 tok/s    13.92 GB
pp8192/tg128        155942.5      107.11    52.5 tok/s     9.4 tok/s     169.546    49.1 tok/s    14.57 GB
pp16384/tg128       281552.9      104.11    58.2 tok/s     9.7 tok/s     294.775    56.0 tok/s    15.69 GB
pp32768/tg128       573946.1      141.24    57.1 tok/s     7.1 tok/s     591.884    55.6 tok/s    18.25 GB
pp65536/tg128      1349190.3      192.96    48.6 tok/s     5.2 tok/s    1373.696    47.8 tok/s    23.31 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          11.7 tok/s     1.00x    51.9 tok/s    51.9 tok/s     19738.5      30.664
2x          15.4 tok/s     1.32x    64.1 tok/s    32.0 tok/s     31790.4      48.523
4x          16.1 tok/s     1.38x   125.0 tok/s    31.3 tok/s     24391.1      64.496

===

