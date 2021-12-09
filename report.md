# Plan 
Therefore, we would like to explore pricing strategies in a simplified version of the power
contracts market. Initially, the project will include the following steps:

1. Fit a Gaussian Process model to historic energy demand data [3]. This will model
the uncertainty in demand at any given time, but should include a kernel that can
account for some variations in demand based on factors such as time of day,
season, and long term changes. As an extension, this model could be improved by
including inputs other than time.
2. Refactor a simplified power contract market as a newsvendor problem using
miniSCOT [5]. We will create a parameterizable strategy (for example, the price and
quantity of energy to sell at a given time) for a single firm in this market, and use the
simulation to model the potential profit of this firm in the simulated market.
3. If possible, we will fit a Gaussian Process emulator to this simulation as well and
use Bayesian Optimization to find an optimal strategy for the firm in this simple
market. In this case, we would be using BO to find a maximum value of the the
function.

Although our model will be oversimplified, it should provide insight into the effect of
different strategies on profit within an uncertain market, and it will demonstrate that
miniSCOT can be used to model a variety of real world problems.