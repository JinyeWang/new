"""问题1-1：转运问题"""
import gurobipy as grb

m = grb.Model()

# 定义变量的下标
tl = [(1, 3), (1, 4),
      (2, 3), (2, 4),
      (3, 5), (3, 6), (3, 7), (3, 8),
      (4, 5), (4, 6), (4, 7), (4, 8)]
# 定义变量

vars = m.addVars(tl, name="x", lb=0, vtype=grb.GRB.INTEGER)

# 添加产量约束
m.addConstr(vars.sum(1, "*") <= 600)
m.addConstr(vars.sum(2, "*") <= 400)
# 流平衡约束
m.addConstr(vars.sum(3, "*") == vars.sum("*", 3))
m.addConstr(vars.sum(4, "*") == vars.sum("*", 4))
# 需求约束
m.addConstr(vars.sum("*", 5) == 200)
m.addConstr(vars.sum("*", 6) == 150)
m.addConstr(vars.sum("*", 7) == 350)
m.addConstr(vars.sum("*", 8) == 300)

# 添加目标函数
# 构建系数矩阵
cl = [(1, 3), (1, 4),
      (2, 3), (2, 4),
      (3, 5), (3, 6), (3, 7), (3, 8),
      (4, 5), (4, 6), (4, 7), (4, 8)]
coeff = grb.tupledict(cl)
c = [2, 3,
     3, 1,
     2, 6, 3, 6,
     4, 4, 6, 5]

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
