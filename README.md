# Agent-based modeling of the spread of antibiotic resistance in a bacterial population, taking into account spatial coordinates, reception of nutrients and antibacterial agents
Fall project in [Bioinformatics Institute](https://bioinf.me/en).

## Aim of the project
To model a system that allows to observe the dynamics of the spread of resistance in a bacterial population based on the specified parameters.  

## Methods
An agent-based approach to modeling is used, which consists in assigning predetermined rules and parameters to each individual component of the system, i.e. a bacterial cell and a particle of nutrient.  

## Requirements
Interpreter: Python >=3.6  
OS: Any (Linux preferably for celluloid package installation)  
CPU:  

Packages:  
numpy 1.19.4  
matplotlib 3.3.3  
celluloid 0.2.0  

## Instructions for running the program
All program code is presented in the `main.py` file and can be run in Pycharm.
The main parameters that can be varied to obtain different results are the initial bacterial count and the nutrient quantity. It is also possible to vary the values of the variables for the maximum life of bacteria, the speed of movement and division of bacterial cells, the probability for a sensitive cell to become resistant, and the probability of accidental loss of the plasmid by a resistant bacterium.  

## Simulation output
The program allows to visualize the dynamics of changes in the number of sensitive and resistant bacteria over time under the pressure of an antibiotic entering the system by plotting graphs that allow to assess the spread of resistance. The program also displays an animation that simulates the real behavior of bacteria and illustrates the process of antibiotic intake and the changes it leads to.  

![Model animation](https://lh3.googleusercontent.com/ypyY4gdis9bb-2UKvKFjKf1TIS8VT105vgd3dt0TGmaMOOClaX3Zn1KbLTtCudOmIpbtKPpbQLiua2b5m0qUZOF7QZH6yuXbPXge_ZqWEXwVD9hb_hNH-0C7LZCoB-J5KOjQL4VHOPpu-jfEF-d2qXUZkIwmUsgniJCdCLOVophM5o9-tjYQq4hEyuS2YM69_Z-yCiQfXespdcTQ6fPerDbTi89xzmkZmF5TeLQDIxJrEOMvJNwjxe4lobo7zZS96bVAHxohp8qNwb2bF33fsYQnXj9To11jPkToaUO3GbAa0iu6w88QLH5b4yzdEashdfWL9eKvMOmrxqL3RJBIYV_zOyB-lAAtcgRgZkoGEM_Vyp-2XUzEAPmKmVw7fUiSI4rnXtXzRForYDZFGo7XXiRDhK8NkHKIuYB1IX-SMBdYmaLic5Gcj7nqSyWsJ3bSV03T7uBYO-a6KlQqwrh-iByu9k8WfiJtP35u5Ua3hZXJpG6QZO3fb7iRoDZ5RJ6_lVb58nq5p8loE6oRiKykTJHjn52343E9TaMndIHshBi0wuZEWOr4XwMzwjgM6XcDQGMuOpxZOyhJMs6P6QZrKec5zt91elMSQANAS-wtP6JKqqv9Xum5H0_9T2QSiRVaWJwHQjUEQ6zkN1b33ZLJshlC5MOFz617r-2CR46r2EguOVfyFRK9kw=w1837-h1048-no?authuser=0)

## References
1. Arepeva, Maria et al. “What should be considered if you decide to build your own mathematical model for predicting the development of bacterial resistance? Recommendations based on a systematic review of the literature.” Frontiers in microbiology vol. 6 352. 29 Apr. 2015, doi:10.3389/fmicb.2015.00352
2. [Celluloid](https://github.com/jwkvam/celluloid) package for animations creating.
