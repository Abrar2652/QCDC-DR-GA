import copy

class port():
    U = 0
    L = 0
    def __init__(self, load, unload, dockyard, unload_seq, max_dock_stack_height):
        self.load = copy.deepcopy(load)
        self.unload = copy.deepcopy(unload)
        self.dockyard = copy.deepcopy(dockyard)
        self.unload_seq = copy.deepcopy(unload_seq)
        self.no_of_dock_stacks = len(dockyard)
        self.no_of_stacks_on_ship = len(unload)
        self.max_dock_stack_height = max_dock_stack_height
        self.result = list()
        
    def calculate_rehandles(self, cont):
        rehandles = 0
        found = False
        i = 0
        while i < self.no_of_dock_stacks:
            cur_stack_height = len(self.dockyard[i])
            for j in range(cur_stack_height):
                if self.dockyard[i][j] == cont:
                    found = True
                    while self.dockyard[i][-1] != cont:
                        rehandles += 1
                        r_con = self.dockyard[i].pop()
                        #shift the container to the neaarest minimum stack
                        if i == 0:
                            it = 1
                            while len(self.dockyard[it]) == self.max_dock_stack_height:
                                it += 1
                            self.dockyard[it].append(r_con)
                        elif i == self.no_of_dock_stacks - 1:
                            it = self.no_of_dock_stacks - 2
                            while len(self.dockyard[it]) == self.max_dock_stack_height:
                                it -= 1
                            self.dockyard[it].append(r_con)
                        else:
                            left = i - 1
                            right = i + 1
                            while True:
                                if len(self.dockyard[left]) < self.max_dock_stack_height:
                                    self.dockyard[left].append(r_con)
                                    break
                                elif len(self.dockyard[right]) < self.max_dock_stack_height:
                                    self.dockyard[right].append(r_con)
                                    break
                                if left == 0 and right == self.no_of_dock_stacks - 1:
                                    self.dockyard.append([])
                                    self.no_of_dock_stacks += 1
                                left = max(0, left - 1)
                                right = min(self.no_of_dock_stacks - 1, right + 1)
                    self.dockyard[i].pop()
                    # print("rehandles: ", rehandles)
                    return rehandles
            i += 1
        if found == False:
            print("Error: Container Not found!!! in dockyard")
        return 0

    def loading_operation(self):
        idx = self.unload_seq[self.L] - 1
        l = len(self.load[idx])
        if l == 0:
            if len(self.unload[self.unload_seq[self.L + 1] - 1]) == 0:
                self.L += 1
                idx = self.unload_seq[self.L] - 1
            else:
                return False, 0

        cont = self.load[idx].pop(0)
        # print("loaded: ", cont)
        self.result.append('L')
        return True, self.calculate_rehandles(cont)

    def unload_first_stack(self):
        for c in range(len(self.unload[self.unload_seq[self.U] - 1])):
            cont = self.unload[self.unload_seq[self.U] - 1].pop()
            if cont == 'F':
                continue
            # print("Unloaded: ", cont)
            self.result.append('U')

def calculate_total_cost(dataset):
    single_cycle = 0
    double_cycle = 0
    total_rehandles = 0
    #unload forst stack
    dataset.unload_first_stack()
    
    #calculating for the rest of the stacks
    while dataset.U < dataset.no_of_stacks_on_ship:
        idx = dataset.unload_seq[dataset.U] - 1
        length = len(dataset.load[dataset.L])
        l_flag = False
        while len(dataset.unload[idx]) > 0:
            u_cont = dataset.unload[idx].pop()
            if u_cont == 'F':
                continue
            # print("ucloaded: ", u_cont)
            dataset.result.append('U')

            flag = dataset.loading_operation()
            total_rehandles += flag[1]
            l_flag = flag[0]
        if l_flag == False:
            flag = dataset.loading_operation()
            total_rehandles += flag[1]
        
        dataset.U += 1
    while len(dataset.load[dataset.unload_seq[-1] - 1]) > 0:
        flag = dataset.loading_operation()
        total_rehandles += flag[1]    
    #calculate single-dual cycles
    i = 0
    while len(dataset.result) > i:
        if dataset.result[i] == 'U' and dataset.result[i + 1] == 'L':
            double_cycle += 1
            i += 1
        else:
            single_cycle += 1
        i += 1
    return single_cycle, double_cycle, total_rehandles