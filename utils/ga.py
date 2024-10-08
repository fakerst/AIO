import random
from deap import base, creator, tools, algorithms

# 定义评估函数
def objective_function(individual):
    x, y, z = individual
    return -(x**2 + y**2 + z**2) + 10,  # 返回目标值

def search_lustre(objective_function):
    # 创建一个 fitness_max 类来表示最大化问题
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # 注册不同变量的生成函数（取整数值）
    toolbox = base.Toolbox()
    toolbox.register("attr_x", random.randint, -5, 15)  # x 的取值范围 [-5, 5] 整数
    toolbox.register("attr_y", random.randint, 0, 5)  # y 的取值范围 [0, 10] 整数
    toolbox.register("attr_z", random.randint, -2, 0)  # z 的取值范围 [-20, 0] 整数

    # 注册个体创建函数，分别为每个变量调用不同的生成器
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     (toolbox.attr_x, toolbox.attr_y, toolbox.attr_z), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # 修正函数：将个体中的所有变量限制在合法范围内
    def fix_individual(individual):
        individual[0] = max(-5, min(5, int(round(individual[0]))))  # 修正 x 的范围
        individual[1] = max(0, min(10, int(round(individual[1]))))  # 修正 y 的范围
        individual[2] = max(-20, min(0, int(round(individual[2]))))  # 修正 z 的范围
        return individual

    # 注册评估函数、选择、交叉和变异操作
    toolbox.register("evaluate", objective_function)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)  # 交叉操作
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)  # 变异操作
    toolbox.register("select", tools.selTournament, tournsize=3)

    # 遗传算法的参数
    population = toolbox.population(n=200)  # 初始种群的大小
    ngen = 50  # 迭代次数
    cxpb = 0.5  # 交叉概率
    mutpb = 0.2  # 变异概率

    # 使用内置的算法进行优化
    for gen in range(ngen):
        # 选择下一代的个体
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # 应用交叉操作
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                fix_individual(child1)  # 修正 child1
                fix_individual(child2)  # 修正 child2
                del child1.fitness.values
                del child2.fitness.values

        # 应用变异操作
        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                fix_individual(mutant)  # 修正 mutant
                del mutant.fitness.values

        # 评估新的个体
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # 替换种群
        population[:] = offspring

    # 获取结果：找到的最优解
    best_individual = tools.selBest(population, 1)[0]
    print(f"Best individual is: {best_individual}")
    print(f"Best fitness is: {best_individual.fitness.values[0]}")

search_lustre(objective_function)


