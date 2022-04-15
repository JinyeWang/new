"""问题1-2：指派问题"""
import gurobipy as grb

m = grb.Model()

# 定义变量

vars = m.addVars(3, 3, name="x", lb=0)

"""添加约束"""
# 添加分配约束
m.addConstr(vars.sum(0, "*") == 1)
m.addConstr(vars.sum(1, "*") == 1)
m.addConstr(vars.sum(2, "*") == 1)

# 添加分配数量约束
m.addConstr(vars.sum("*", 0) <= 1)
m.addConstr(vars.sum("*", 1) <= 1)
m.addConstr(vars.sum("*", 2) <= 1)

# 添加目标函数
# 构建系数矩阵
cl = [(0, 0), (0, 1), (0, 2),
      (1, 0), (1, 1), (1, 2),
      (2, 0), (2, 1), (2, 2)]
coeff = grb.tupledict(cl)
# c = [10, 15, 9, 9, 18, 5, 6, 14, 3]
c = [10, 15, 9, 9, 18, 5, 6, 14, 3]
j = 0
for index in cl:
    coeff[index] = c[j]
    j += 1
# 目标函数
m.setObjective(vars.prod(coeff), grb.GRB.MINIMIZE)

# 求解
m.optimize()
print("最优值：", m.objVal)
for v in m.getVars():
    print("决策变量：", v.varname, '=', v.x)
