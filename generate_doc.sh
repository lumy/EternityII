#!/bin/bash
set -ex

doc2md.py -a --no-toc main.py > doc/main.md
doc2md.py -a --no-toc algo_benchmark.py > doc/algo_benchmark.md
doc2md.py -a --no-toc config.py > doc/config.md
doc2md.py -a --no-toc eternity.py > doc/eternity.md
doc2md.py -a --no-toc eval.py > doc/eval.md
doc2md.py -a --no-toc graphs.py > doc/graphs.md
doc2md.py -a --no-toc ind.py > doc/ind.md
doc2md.py -a --no-toc main.py > doc/main.md
doc2md.py -a --no-toc puzzle.py > doc/puzzle.md
doc2md.py -a --no-toc render.py > doc/render.md
doc2md.py -a --no-toc stats.py > doc/stats.md
