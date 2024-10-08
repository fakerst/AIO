import random
from deap import base, creator, tools, algorithms
import joblib

# 定义评估函数
def objective_lustre(individual):
    slModel = joblib.load('Models/slModel.pkl')
    X = self.dfs[log_features + perc_features + romio_features + lustre_feature]
    throught = self.slModel.predict(X)
    return through

def search_lustre(objective_function):
    # 创建一个 fitness_max 类来表示最大化问题
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # 注册不同变量的生成函数（取整数值）
    toolbox = base.Toolbox()
    toolbox.register("cb_read", random.randint, 0, 2)  # x 的取值范围 [-5, 5] 整数
    toolbox.register("cb_write", random.randint, 0, 2)  # y 的取值范围 [0, 10] 整数
    toolbox.register("ds_read", random.randint, 0, 2)  # z 的取值范围 [-20, 0] 整数
    toolbox.register("ds_write", random.randint, 0, 2)  # x 的取值范围 [-5, 5] 整数
    toolbox.register("cb_node", random.randint, 1, 64)  # y 的取值范围 [0, 10] 整数
    toolbox.register("cb_config_list", random.randint, 1, 8)  # z 的取值范围 [-20, 0] 整数
    toolbox.register("stripe_size", random.randint, 1, 64)  # y 的取值范围 [0, 10] 整数
    toolbox.register("stripe_count", random.randint, 1, 8)  # z 的取值范围 [-20, 0] 整数

    # 注册个体创建函数，分别为每个变量调用不同的生成器
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     (toolbox.cb_read, toolbox.cb_write, toolbox.ds_read, toolbox.ds_write, toolbox.cb_node, toolbox.cb_config_list,toolbox.stripe_size, toolbox.stripe_count), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # 修正函数：将个体中的所有变量限制在合法范围内
    def fix_individual(individual):
        individual[0] = max(0, min(2, int(round(individual[0]))))  # 修正 x 的范围
        individual[1] = max(0, min(2, int(round(individual[1]))))  # 修正 y 的范围
        individual[2] = max(0, min(2, int(round(individual[2]))))  # 修正 z 的范围
        individual[3] = max(0, min(2, int(round(individual[0]))))  # 修正 x 的范围
        individual[4] = max(1, min(64, int(round(individual[1]))))  # 修正 y 的范围
        individual[5] = max(1, min(8, int(round(individual[2]))))  # 修正 z 的范围
        individual[6] = max(1, min(64, int(round(individual[0]))))  # 修正 x 的范围
        individual[7] = max(1, min(8, int(round(individual[1]))))  # 修正 y 的范围
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

        # 每轮输出最佳个体及其 fitness
        best_individual = tools.selBest(population, 1)[0]
        print(f"Generation {gen + 1}: Best individual = {best_individual}, Best fitness = {best_individual.fitness.values[0]}")

    # 获取结果：找到的最优解
    best_individual = tools.selBest(population, 1)[0]
    print(f"Best individual is: {best_individual}")
    print(f"Best fitness is: {best_individual.fitness.values[0]}")

#search_lustre(objective_function)


