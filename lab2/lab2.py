import itertools;
import sys;

intex = 0;
dict_of_index = dict();
dict_index = 1;

def valid(c1):

    valid = False;
    negate_c1 = negate(c1);

    for x in c1:

        if x in negate_c1:

            valid = True;
            break;

    return valid;


def negate(clause):

    negate_clause= set();

    for x in clause:

        if x.startswith("~"):

            negate_clause.add(x[1:]);

        else:

            negate_clause.add("~"+x);

    return negate_clause;

def negate_single(literal):


    if literal.startswith("~"):

        negated_literal = literal[1:];

    else:

        negated_literal = "~"+literal;

    return negated_literal;


def plResolve(c1,c2):

    negate_c2 = negate(c2);
    resolvent = {};
    can_resolve  = False;

    for x in c1:

        if x in negate_c2:

            can_resolve = True;
            break;

    if(can_resolve):

        c1.remove(x);
        c2.remove(negate_single(x));

        resolvent = c1.union(c2);

        if(len(resolvent)==0):

            resolvent.add("NIL");

    return resolvent;

def selectClauses(clauses,SoS):


    return itertools.product(clauses,SoS);

def eraseMethod(c):

    global intex;
    p = c.copy();

    for x in c:

        for y in c:

            if x.issubset(y) and x!=y and y in p:

                p.remove(y);

    for i in p:

        if valid(i):

            p.remove(i);

    return p;

def parentSet(x,check_set):

    is_parent_set = False;
    for i in check_set:

        if x!=i and x.issuperset(i):

            is_parent_set = True;
            break;

    return is_parent_set;

def plResolution(clauses,new):

    global intex;
    global dict_index;
    #print(clauses)
    clauses.extend(new);
    intex = len(clauses);

    while(True):

        clauses = eraseMethod(clauses);
        new = eraseMethod(new)
        for c1,c2 in selectClauses(clauses,new):

            resolvents = plResolve(c1.copy(),c2.copy());

            if("NIL" in resolvents):

                resolvents_string = " v ".join(resolvents);
                dict_of_index.update({tuple(list(resolvents)): dict_index});
                print(f"{dict_index}. {resolvents_string} ({dict_of_index[tuple(list(c1))]},{dict_of_index[tuple(list(c2))]})")
                dict_index += 1;
                return True;

            else:

                if (resolvents not in new and len(resolvents)!=0 ):


                    dict_of_index.update({tuple(list(resolvents)): dict_index})

                    resolvents_string = " v ".join(resolvents);
                    print(f"{dict_index}. {resolvents_string} ({dict_of_index[tuple(list(c1))]},{dict_of_index[tuple(list(c2))]})")
                    dict_index += 1;
                    new.append(resolvents);

        subset = True;

        for x in new:

            if x not in clauses and len(x)!=0:

                clauses.append(x);
                subset = False;

        if subset:

            return False;

argument = sys.argv[1];

if(argument=="resolution"):

    file = sys.argv[2];

    f = open(file, "r");
    content = f.readlines();
    content = [x.strip() for x in content];
    content = [x.lower() for x in content if not x.startswith("#")];
    statement = content[-1];
    goal = [negate({x}) for x in content[-1].split(" v ")];

    content = content[:-1];
    content = [set(x.split(" v ")) for x in content];


    for x in content:

        x_string = " v ".join(x);
        print (f"{dict_index}. {x_string}");
        dict_of_index.update({tuple(list(x)):dict_index});
        dict_index+=1;


    for x in goal:

        x_string = " v ".join(x);
        print (f"{dict_index}. {x_string}");
        dict_of_index.update({tuple(list(x)):dict_index});
        dict_index+=1;

    print("===============");

    if(plResolution(content.copy(),goal.copy())):

        print("===============");
        print(f"[CONCLUSION]: {statement} is true");

    else:
        print("===============");
        print(f"[CONCLUSION]: {statement} is unknown");

elif (argument=="cooking"):

    file = sys.argv[2];
    input_file_name = sys.argv[3];

    f = open(file, "r");
    content = f.readlines();
    content = [x.strip() for x in content];
    content = [x.lower() for x in content if not x.startswith("#")];
    goal = [negate({x}) for x in content[-1].split(" v ")];

    content = [set(x.split(" v ")) for x in content];

    input_file = open(input_file_name,"r");
    inputs = input_file.readlines();
    inputs = [x.strip() for x in inputs];
    inputs = [x.lower() for x in inputs if not x.startswith("#")];

    for i in inputs:

        dict_index = 1;

        if(i[-1]=="?"):

            print(f"Users command: {i}");
            statement = i[:-2].split(" v ");
            statement = [negate({x}) for x in statement]

            for x in content:

                x_string = " v ".join(x);
                print(f"{dict_index}. {x_string}");
                dict_of_index.update({tuple(list(x)): dict_index})
                dict_index += 1;

            for x in statement:

                x_string = " v ".join(x);
                print(f"{dict_index}. {x_string}");
                dict_of_index.update({tuple(list(x)):dict_index})
                dict_index+=1;

            # print(statement)
            print("===============")
            # print(content)
            # print(statement)
            if(plResolution(content.copy(),statement.copy())):

                print("===============")
                print(f"[CONCLUSION]: {i[:-2]} is true");

            else:
                print("===============")
                print(f"[CONCLUSION]: {i[:-2]} is unknown");

            print("");

        if(i[-1]=="-"):

            content.remove(set(i[:-2].split(" v ")))

        if(i[-1]=="+"):

            content.append(set(i[:-2].split(" v ")))
