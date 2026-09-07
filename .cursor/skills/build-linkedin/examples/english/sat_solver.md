There is now an eye-opening "Sweeter Lesson" to complement Sutton's Bitter Lesson: 476× algorithmic speedup beats 3.9× hardware in one decade. Same benchmarks, on a fixed machine.
 
Algorithmic progress in SAT solvers unlocked problems that were previously unreachable, even with scaling! 11% of benchmark problems reachable in 2002 vs 72% of the problems reachable in 2022 on the same machine.

Moshe Vardi points to SAT, the Boolean Satisfiability Problem, the poster child of the most famous category of hard problems in computer science. Vardi cites Seshia's figure: almost 1000x in the century's first decade, on fixed hardware.

The SAT Museum reran every competition winner on one machine. 476x on that decade's benchmarks - same order of magnitude, and outpacing real CPU gains by ~122x.

The foundation was laid in 1996, when Marques-Silva and Sakallah combined the search for a solution with the search for a proof that none exists - Conflict-Driven Clause Learning. Everything after is refinement inside that idea.

Interestingly, the biggest jump of the decade was thanks to preprocessing! (SatELite, 2005).

From 2009 to 2020:
- learning what to forget (Glucose)
- separate restart policies for SAT and UNSAT (MapleSAT), and
- local search + target phases + rephasing (CaDiCaL/Kissat)

Solvers also learned to improve clause representation during processing ("inprocessing", PrecoSAT / Lingeling).

2020-now: started throwing compute at the problem too. Learning how to distribute SAT solving across thousands of cores while intelligently sharing the most promising learned clauses without causing a data bottleneck.

The lesson is that algorithmic improvements can matter even more than scaling and compute. Some amount of hand-crafting is needed and will always be needed to efficiently solve new domains.

What other domains have algorithms still outrunning scaling?