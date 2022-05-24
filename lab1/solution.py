import sys;
import getopt;
import heapq;


class Node:

    def __init__(self,state,depth,parent,astar=False):

        self.state = state;
        self.depth = depth;
        self.parent = parent;
        self.astar = astar;

    def getState(self):

        return self.state;

    def getParent(self):

        return self.parent;

    def getDepth(self):

        return self.depth;

    def __str__(self):

        if(self.getParent() is not None):
            return f'State:{self.getState()} Depth:{self.getDepth()} Parent: ({self.getParent().getState()})';

        else:

            return f'State:{self.getState()} Depth:{self.getDepth()} Parent: (None)';

    # def __cmp__(self, other):
    #
    #     return cmp(self.getDepth(),other.getDepth());

    def __lt__(self, other):

        if(not self.astar):
            return (self.getDepth(),self.getState())<(other.getDepth(),other.getState());

        else:

            return(self.getDepth()+heuristic(self.getState()),self.getState()) < (other.getDepth()+heuristic(other.getState()),other.getState());

class Search():

    def __init__(self):

        self.states_visited = 0;
        self.totalCost = 0;
        self.path_recreation = [];
        self.path_found = False;


    def bfs(self, s0, succ, goal):

        open = [];
        set_open = set();
        visited = set();
        self.clear();

        open.append(initialize(s0));
        set_open.add(initialize(s0).getState())

        while len(open) != 0:

            self.states_visited +=1;
            n = open.pop(0);
            set_open.remove(n.getState());
            visited.add(n.getState());

            if (goal(n.getState())):

                self.totalCost = n.getDepth();
                self.path(n);
                self.path_found = True;
                return n;

            for m in expand(n, succ):

                if(m.getState() not in visited and m.getState() not in set_open):

                    open.append(m);
                    set_open.add(m.getState());


        return False;


    def ucs(self, s0, succ, goal):

        open = [];
        open_set = dict();
        visited = set();
        self.clear();

        heapq.heappush(open,initialize(s0));
        open_set.update({initialize(s0).getState():initialize(s0)});

        while len(open)!=0:

            self.states_visited +=1;

            n = heapq.heappop(open);
            del open_set[n.getState()]
            visited.add(n.getState());

            if (goal(n.getState())):

                self.totalCost = n.getDepth();
                self.path(n);
                self.path_found = True;
                return n;

            for m in expand(n, succ):

                if(m.getState() not in visited):

                    if(m.getState() in open_set.keys()):

                        help_node = open_set[m.getState()];

                        if(help_node.getDepth() > m.getDepth()):

                            heapq.heappush(open,m)
                            open_set.update({m.getState():m});
                            open.remove(help_node);

                    else:

                        heapq.heappush(open,m);
                        open_set.update({m.getState():m});

        return False;

    def aStarSearch(self,s0,succ,goal,h):

        open = [];
        self.clear();
        closed = dict();
        open_set = dict();

        heapq.heappush(open,initialize(s0));
        open_set.update({initialize(s0).getState():initialize(s0)})

        while len(open)!=0:

            self.states_visited+=1;

            #print(self.states_visited);
            n = heapq.heappop(open);
            del open_set[n.getState()]
            closed.update({n.getState():n})

            if(goal(n.getState())):

                self.totalCost = n.getDepth();
                self.path(n);
                self.path_found = True;
                return n;

            #states_closed = [state.getState() for state in (closed+open)];

            for m in expand(n,succ,True):

                if (m.getState() in open_set.keys() or m.getState() in closed.keys()):

                    if(m.getState() in open_set.keys()):

                        help_node = open_set.get(m.getState());
                    else:

                        help_node = closed.get(m.getState());

                    if(help_node.getDepth() <= m.getDepth()):

                        continue;


                    else:

                        if(help_node.getState() in closed.keys()):

                            del closed[help_node.getState()];

                        if(help_node.getState() in open_set.keys()):

                            open.remove(help_node);
                            del open_set[help_node.getState()];

                heapq.heappush(open,m);
                open_set.update({m.getState():m})


    def path(self,n):

        p = n.getParent();
        self.path_recreation.append(n);

        if (p is None):

            return;

        return self.path(p);


    def getPathRecreation(self):

        return self.path_recreation;

    def getStatesVisited(self):

        return self.states_visited

    def getTotalCost(self):

        return self.totalCost;

    def clear(self):

        self.states_visited = 0;
        self.totalCost = 0;
        self.path_recreation = [];
        self.path_found = False;

    def __str__(self):

        if(self.path_found):

            string = "[FOUND_SOLUTION]: yes"+"\n"+"[STATES_VISITED]: "+str(self.getStatesVisited())+"\n"+"[PATH_LENGTH]: "+str(len(self.getPathRecreation()))+"\n"+"[TOTAL_COST]: "+str(float(self.totalCost))+"\n"+"[PATH]: "
            for s in reversed(self.getPathRecreation()):

                string = string + s.getState();
                string = string + " => ";

            string = string[:-4];
        else:

            string = "[FOUND_SOLUTION]: no";


        return string;


def expand(node,succ,astar=False):

    expands = [];
    nodes = succ(node.getState());

    for n in nodes:

        new_node = Node(n,nodes[n]+node.getDepth(),node,astar);
        expands.append(new_node);


    expands = sorted(expands, key=lambda x: x.getState().lower(), reverse=False);

    return expands;

def initialize(state):

    return Node(state,0,None);


def succ(state):

    return transitions[state];

def goal(state):

    return state in goal_states;

def heuristic(state):

    return heuristics[state];

def check_consistency(data,h):

    consistent = True;
    for parent in data:

        expands = succ(parent); #get the expands of parent node

        for state in sorted(expands.keys(), key=lambda x:x.lower()):

            if(h(parent)> h(state) + expands[state]):

                consistent = False;
                print( f'[CONDITION]: [ERR] h({parent}) <= h({state}) + c: {float(h(parent))} <= {float(h(state))} + {float(expands[state])}');

            else:

                print( f'[CONDITION]: [OK] h({parent}) <= h({state}) + c: {float(h(parent))} <= {float(h(state))} + {float(expands[state])}')

    if(consistent):

        print("[CONCLUSION]: Heuristic is consistent.");

    else:

        print("[CONCLUSION]: Heuristic is not consistent.");

def check_optimality(data,h):

    real_costs = dict();
    optimal = True;

    for parent in data:

        search = Search();
        real_cost = search.ucs(parent,succ,goal);

        if(real_cost):
            

            real_costs.update({parent:real_cost.getDepth()});


    for state in real_costs:

        if (h(state)>real_costs[state]):

            optimal = False;
            print( f'[CONDITION]: [ERR] h({state}) <= h*: {float(h(state))} <= {float(real_costs[state])}');

        else:

            print(f'[CONDITION]: [OK] h({state}) <= h*: {float(h(state))} <= {float(real_costs[state])}');

    if(optimal):

        print("[CONCLUSION]: Heuristic is optimistic.");

    else:

        print('[CONCLUSION]: Heuristic is not optimistic.');

    return real_costs;


#RESULTS
search = Search();


# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]
short_options = "a:s:h:oc";
long_options = ["alg=", "ss=","h=","check-optimistic","check-consistent"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    #print(arguments,values)

except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

algorithm = None;
for current_argument, current_value in arguments:

    if current_argument in ("-a", "--alg"):

        algorithm = current_value;

    elif current_argument in ("-s", "--ss"):

        transitions_file = current_value;

    elif current_argument in ("-h", "--h"):

        heuristics_file = current_value;

    elif current_argument in ("-o","--check-optimistic"):

        flag = "optimistics";

    elif current_argument in ("-c","--check-consistent"):

        flag = "consistent";

if(algorithm!=None):


    transitions = dict();
    heuristics = dict();

    # START

    # Getting transitions
    f = open(transitions_file, "r", encoding="utf8");

    content = f.readlines();
    content = [x.strip() for x in content];
    content = [x for x in content if not x.startswith("#")];

    initial_state = content.pop(0);
    goal_states = content.pop(0).strip().split(" ");

    for s in content:

        pair = s.split(":");
        help = pair[1].strip().split(" ");
        hdict = dict();

        for k in help:

            if (k != ""):
                hdict.update({k.split(",")[0]: int(k.split(",")[1])});

        transitions.update({pair[0]: hdict});

    f.close();

    if(algorithm=="astar"):

        # Getting heuristic
        f = open(heuristics_file, "r", encoding="utf-8");

        content = f.readlines();
        content = [x.strip() for x in content];
        content = [x for x in content if not x.startswith("#")];

        for s in content:
            pair = s.strip().split(":");
            heuristics.update({pair[0]: int(pair[1])});

        f.close();

        search.aStarSearch(initial_state,succ,goal,heuristic);
        print(f"# A-STAR {heuristics_file}");
        print(search);

    elif(algorithm=="ucs"):

        search.ucs(initial_state,succ,goal)
        print(f"# UCS");
        print(search);

    elif(algorithm=="bfs"):

        search.bfs(initial_state,succ,goal)
        print(f"# BFS");
        print(search);

else:

# Here the data for transitions and heuristics will be stored from file
    transitions = dict();
    heuristics = dict();

    # START

    # Getting transitions
    f = open(transitions_file, "r", encoding="utf8");

    content = f.readlines();
    content = [x.strip() for x in content];
    content = [x for x in content if not x.startswith("#")];

    initial_state = content.pop(0);
    goal_states = content.pop(0).strip().split(" ");

    for s in content:

        pair = s.split(":");
        help = pair[1].strip().split(" ");
        hdict = dict();

        for k in help:

            if (k != ""):
                hdict.update({k.split(",")[0]: int(k.split(",")[1])});

        transitions.update({pair[0]: hdict});

    f.close();

    # Getting heuristic
    f = open(heuristics_file, "r", encoding="utf-8");

    content = f.readlines();
    content = [x.strip() for x in content];
    content = [x for x in content if not x.startswith("#")];

    for s in content:
        pair = s.strip().split(":");
        heuristics.update({pair[0]: int(pair[1])});

    f.close();

    if(flag=="optimistics"):

        print(f"# HEURISTIC-OPTIMISTIC {heuristics_file}")
        check_optimality(sorted(transitions.keys(), key=lambda x:x.lower()),heuristic);

    elif(flag=="consistent"):

        print(f"# HEURISTIC-CONSISTENT {heuristics_file}")
        check_consistency(sorted(transitions.keys(), key=lambda x:x.lower()),heuristic);
