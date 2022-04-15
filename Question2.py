"""问题2：教授上课的指派问题"""
import gurobipy as grb

m = grb.Model()

# 定义变量

vars = m.addVars(4, 4, name="x", lb=0, vtype=grb.GRB.INTEGER)

"""添加约束"""
# 添加每位教授只上一门课的约束
m.addConstrs((vars.sum(i, "*") == 1 for i in range(4)), name="course")

# 添加一门课只由一个老师来上的约束
m.addConstrs((vars.sum("*", j) == 1 for j in range(4)), name="course")

# 添加目标函数
# 构建系数矩阵
cl = [(0, 0), (0, 1), (0, 2), (0, 3),
      (1, 0), (1, 1), (1, 2), (1, 3),
      (2, 0), (2, 1), (2, 2), (2, 3),
      (3, 0), (3, 1), (3, 2), (3, 3)]
coeff = grb.tupledict(cl)

# 教授D不能教授博士生水平的课程,设置对应的评价分数为一个很小的值
c = [2.8, 2.2, 3.3, 3.0,
     3.2, 3.0, 3.6, 3.6,
     3.3, 3.2, 2.5, 3.5,
     3.2, 2.8, 2.5, 0.001]
j = 0
for index in cl:
    coeff[index] = c[j]
    j += 1
# 目标函数
m.setObjective(vars.prod(coeff), grb.GRB.MAXIMIZE)

# 求解
m.optimize()
print("最优值：", m.objVal)
for v in m.getVars():
    print("决策变量：", v.varname, '=', v.x)
