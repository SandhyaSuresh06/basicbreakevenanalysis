import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from whatif import Model
from whatif import get_sim_results_df

class SingleProductSPF(Model):
    """Base model

    This model relates profit of a company’s single product to the following inputs. 

    * there's a fixed cost of manufacturing this product each month
    * there's a variable cost per unit,
    * we have a known selling price,
    * demand is calculated based on historical data on selling price and monthly demand,
    * for each unsold item, we can get a partial refund of our unit cost,
    * function relating demand and selling price is D = 0.06S^2-35S+4900.

    Attributes
    ----------
    fixed_cost : float or array-like of float, optional
        fixed cost of manufacturing the product each month (default 5000.00)
    var_cost : float or array-like of float, optional
        variable cost per unit (default 100.00)
    selling_price : float or array-like of float, optional
        Selling price for the product (default 115.00)
    spf_constant : float or array-like of float, optional
        Constant value involved in the calculation of demand (default 4900.00)
    spf_linear : float or array-like of float, optional
        Coefficient of the linear degree of the selling price function (default -35)
    spf_quadratic : float or array-like of float, optional
        Coefficient of the quadratic degree of the selling price function (default 0.06)
    """
    def __init__(self, fixed_cost=5000, var_cost=100, selling_price=115,
                 spf_constant=4900, spf_linear=-35, spf_quadratic= 0.06 ):
        self.fixed_cost = fixed_cost
        self.var_cost = var_cost
        self.selling_price = selling_price
        self.spf_constant = spf_constant
        self.spf_linear = spf_linear
        self.spf_quadratic = spf_quadratic

    def calculate_demand(self):
        """Compute demand"""
        demand = self.spf_quadratic * (self.selling_price ** 2) \
                 + (self.spf_linear * self.selling_price) + self.spf_constant
        return demand
    
    def total_var_cost(self):
        """Compute total variable cost based on demand and variable cost per unit"""
        return self.calculate_demand() * self.var_cost

    def total_revenue(self):
        """Compute total sales revenue based on demand and selling price"""
        return self.calculate_demand() * self.selling_price

    def total_cost(self):
        """Compute total cost based on fixed cost and total variable cost"""
        return self.fixed_cost + self.total_var_cost()

    def profit(self):
        """Compute profit based on revenue and cost"""
        profit = self.total_revenue() - self.total_cost()
        return profit
    
import sys
print('\n'.join(sys.path))

model = SingleProductSPF()
print(model)
print(model.profit())

# Specify input ranges for scenarios (dictionary)
# 1-way table

dt_param_ranges_1 = {'selling_price': np.arange(80, 141, 10)}
print(dt_param_ranges_1)

# Specify desired outputs (list)
outputs = ['profit', 'demand']

# Use data_table function to create 1-way data table
m1_dt1_df = model.data_table(dt_param_ranges_1, outputs)
m1_dt1_df

# Use goal_seek to compute break even demand
break_even_demand = model.goal_seek('profit', 0, 'demand', 0, 1000, 1000)