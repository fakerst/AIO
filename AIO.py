import subprocess
import joblib
import time
from utils.utils_else import *
from utils.get18filefeatures import *
from utils.get57features import *
from utils.searching import *


class AIO:
    def __init__(self, cmd):
        self.cmd = cmd
        self.cmd_check = replace_spaces_with_underscores(cmd) + ".txt"
        self.cmd_checkt = replace_spaces_with_underscores(cmd) + ".txtt"
        self.cmd_generate = replace_spaces_with_underscores(cmd) + ".darshan"
        self.darshan_logpath = get_cwd() + "/darshan_logpath/"
        self.darshan_anspath = get_cwd() + "/darshan_anspath/"
        self.cModel = joblib.load('Models/model.pkl')
        self.slModel = joblib.load('Models/slModel.pkl')
        self.sgModel = joblib.load('Models/slModel.pkl')
        self.df = None
        self.dfs = None
        self.result_layer = None
        self.tmpfs_path = "/dev/shm/"
        self.runtime = 0
        self.runtime_AIO = 0
        self.speedup = 0

    def run(self):
        self.retrieval_and_collect()
        self.extract_and_predict()
        self.execute()
        self.result()

    def retrieval_and_collect(self):
        if not self.check():
            self.run_with_darshan()
        else:
            self.df = get_app_file(self.darshan_anspath + self.cmd_check)
            print(self.df.index)
            self.dfs = extracting_darshan57(self.darshan_anspath + self.cmd_checkt)

    def extract_and_predict(self):
        # if df is None:
        #    self.retrieval_and_collect()
        result_dict = {}
        # tmpfs
        if (self.df['POSIX_BYTES_READ_LOG10'] == -1).all() and (self.df['File_Per_Proc'] == 1).all():
            fs = [0] * len(self.df)
            result_dict = {k: v for k, v in zip(self.df.index, [self.convert_storage_type(num) for num in fs])}
        else:
            X = self.df[features18_]
            fs = self.cModel.predict(X)
            result_dict = {k: v for k, v in zip(self.df.index, [self.convert_storage_type(num) for num in fs])}
        self.result_layer = result_dict
        print(result_dict)
        self.runtime = (self.df['POSIX_F_READ_TIME'].sum() + self.df['POSIX_F_WRITE_TIME'].sum() + self.df[
            'POSIX_F_META_TIME'].sum()) / self.df['NPROCS'][0]

    def execute(self):
        # for key, value in self.result.items():
        #    print(f"{key}: {value}")

        # tmpfs
        if all(value == "tmpfs" for value in self.result_layer.values()):
            self.execute_tmpfs()
        # GekkoFS
        elif any(value == "GekkoFS" for value in self.result_layer.values()):
            self.execute_GekkoFS()
        elif all(value == "Lustre" for value in self.result_layer.values()):
            self.execute_Lustre()


    def result(self):
        if self.runtime_AIO != 0:
            self.speedup = self.runtime / self.runtime_AIO
            #print(self.runtime)
            #print(self.runtime_AIO)
            print("AIO提升的加速比为：", self.speedup)

    def check(self):
        return search_file(self.darshan_anspath, self.cmd_check)

    def run_with_darshan(self):
        self.darshan_init()
        subprocess.run(self.cmd, shell=True, capture_output=False, text=True)
        self.darshan_parser()
        self.df = get_app_file(self.darshan_anspath + self.cmd_check)
        self.dfs = extracting_darshan57(self.darshan_anspath + self.cmd_checkt)
        self.darshan_terminate()

    def darshan_init(self):
        os.environ["LD_PRELOAD"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-runtime/lib/.libs/libdarshan.so"
        os.environ["DARSHAN_LOGPATH"] = self.darshan_logpath
        os.environ["DARSHAN_LOGFILE"] = self.darshan_logpath + self.cmd_generate

    def darshan_parser(self):
        os.environ["PATH"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-prefix/bin/" +":"+ os.environ["PATH"]
        os.environ["LD_LIBRARY_PATH"] = "/thfs3/home/wuhuijun/darshan-3.4.4-mpich/darshan-prefix/lib" +":"+ os.environ["LD_LIBRARY_PATH"]
        command = "darshan-parser " + self.darshan_logpath + self.cmd_generate + " > " + self.darshan_anspath + self.cmd_check
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = "darshan-parser --total --perf --file " + self.darshan_logpath + self.cmd_generate + " > " + self.darshan_anspath + self.cmd_checkt
        subprocess.run(command, shell=True, capture_output=True, text=True)

    def darshan_terminate(self):
        os.environ["LD_PRELOAD"] = ""

    def convert_storage_type(self, number):
        storage_map = {
            0: "tmpfs",
            1: "Lustre",
            2: "GekkoFS"
        }
        return storage_map.get(number, "unknown")

    def execute_tmpfs(self):
        print("选用的加速层为tmpfs")
        dst = get_last_slash_prefix(get_common_prefix(self.result_layer))
        src = self.tmpfs_path
        commands = [
            "sudo mount --bind " + src + " " + dst,
            self.cmd,
            "sudo umount " + dst
        ]
        start_time = time.time()
        subprocess.run(' && '.join(commands), shell=True, capture_output=False, text=True)
        self.runtime_AIO = time.time() - start_time



    def execute_Lustre(self):
        print("execute lustre")
        best_configlist = self.search_lustre(self.objective_lustre)
        os.environ["LD_PRELOAD"] = "/thfs3/home/wuhuijun/wx/AIO/tuning/mpiio.so"
        self.set_romio(best_configlist[:6])
        self.set_lustre_stripe("asdf",best_configlist[:6])
        start_time = time.time()
        subprocess.run(self.cmd, shell=True, capture_output=False, text=True)
        self.runtime_AIO = time.time() - start_time

    def set_romio(self, romio):
        hint = os.path.join("/thfs3/home/wuhuijun/wx/AIO/tuning/", "hint.txt")
        with open(hint, 'w') as f:
            f.write(str(romio[0]))
            f.write('\n')
            f.write(str(romio[1]))
            f.write('\n')
            f.write(str(romio[2]))
            f.write('\n')
            f.write(str(romio[3]))
            f.write('\n')
            f.write(str(romio[4]))
            f.write('\n')
            f.write(str(romio[5]))
        f.close()

    def set_lustre_stripe(self, path, cs):
        this_stripe_size = cs[0] * 1024 * 1024
        this_stripe_count = cs[1]
        command = "lfs setstripe -S %s -c %s %s" % (this_stripe_size, this_stripe_count, path)
        #subprocess.run(command, shell=True, capture_output=True, text=True)

    def objective_lustre(self,individual):
        dfconfig = pd.DataFrame([individual], columns = romio_features + lustre_feature)
        df = pd.concat([self.dfs, dfconfig], axis=1)
        X = df[log_features + perc_features + romio_features + lustre_feature]
        throught = self.slModel.predict(X)
        print(individual,throught)
        return throught

    def search_lustre(self,objective_function):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("cb_read", random.randint, 0, 2)
        toolbox.register("cb_write", random.randint, 0, 2)
        toolbox.register("ds_read", random.randint, 0, 2)
        toolbox.register("ds_write", random.randint, 0, 2)
        toolbox.register("cb_node", random.randint, 1, 64)
        toolbox.register("cb_config_list", random.randint, 1, 8)
        toolbox.register("stripe_size", random.randint, 1, 64)
        toolbox.register("stripe_count", random.randint, 1, 8)


        toolbox.register("individual", tools.initCycle, creator.Individual,
                        (toolbox.cb_read, toolbox.cb_write, toolbox.ds_read, toolbox.ds_write, toolbox.cb_node, toolbox.cb_config_list,toolbox.stripe_size, toolbox.stripe_count), n=1)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def fix_individual(individual):
            individual[0] = max(0, min(2, int(round(individual[0]))))
            individual[1] = max(0, min(2, int(round(individual[1]))))
            individual[2] = max(0, min(2, int(round(individual[2]))))
            individual[3] = max(0, min(2, int(round(individual[0]))))
            individual[4] = max(1, min(64, int(round(individual[1]))))
            individual[5] = max(1, min(8, int(round(individual[2]))))
            individual[6] = max(1, min(64, int(round(individual[0]))))
            individual[7] = max(1, min(8, int(round(individual[1]))))
            return individual

        toolbox.register("evaluate", objective_function)
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)

        population = toolbox.population(n=50)
        ngen = 2
        cxpb = 0.5
        mutpb = 0.2

        for gen in range(ngen):
            offspring = toolbox.select(population, len(population))
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cxpb:
                    toolbox.mate(child1, child2)
                    fix_individual(child1)
                    fix_individual(child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < mutpb:
                    toolbox.mutate(mutant)
                    fix_individual(mutant)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            population[:] = offspring

            best_individual = tools.selBest(population, 1)[0]
            print(f"Generation {gen + 1}: Best individual = {best_individual}, Best fitness = {best_individual.fitness.values[0]}")

        best_individual = tools.selBest(population, 1)[0]
        print(f"Best individual is: {best_individual}")
        print(f"Best fitness is: {best_individual.fitness.values[0]}")
        return best_individual

    def execute_GekkoFS(self):
        print("execute gekkofs")
        pass

    def __del__(self):
        # kill_proot()
        pass
