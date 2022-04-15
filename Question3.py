"""问题3：线性规划求解最短路径"""
import gurobipy as grb

m = grb.Model()

# 定义变量

vars = m.addVars(7, 7, name="x", lb=0, vtype=grb.GRB.BINARY)

"""添加约束"""
# 出边和等于入边和（非起点、终点）
m.addConstrs(vars.sum(i, "*") == vars.sum("*", i) for i in range(1, 6))
# 出边和《=1,入边和《=1
m.addConstrs((vars.sum(i, "*") <= 1 for i in range(7)), name="out")
m.addConstrs((vars.sum("*", i) <= 1 for i in range(7)), name="in")

# 起点出边和为1，入边和为0的约束
m.addConstr(vars.sum(0, "*") == 1, name="start_out")
m.addConstr(vars.sum("*", 0) == 0, name="start_in")

# 终点出边和为0，入边和为1的约束
m.addConstr(vars.sum(6, "*") == 0, name="end_out")
m.addConstr(vars.sum("*", 6) == 1, name="end_in")

# 添加目标函数
# 构建系数矩阵
cl_initial = []

for i in range(7):
    for j in range(7):
        cl_initial.append((i, j))
coeff = grb.tupledict(cl_initial)

# 初始化系数矩阵，使得不存在有向图的两点之间距离很大
for i in cl_initial:
    coeff[i] = 99999

cl = [(0, 1), (0, 2), (0, 3),
      (1, 2), (1, 4),
      (2, 1), (2, 4),
      (3, 5),
      (4, 1), (4, 2), (4, 5), (4, 6),
      (5, 4), (5, 6)]

# 输入对应的两点之间的路径距离
c = [7, 9, 18,
     3, 5,
     3, 4,
     3,
     5, 4, 2, 6,
     2, 3]
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
