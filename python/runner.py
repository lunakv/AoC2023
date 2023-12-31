#!/usr/bin/env python3
import sys
import os
import re
import importlib
import time
import inspect
import pkgutil

import solutions
from utils import parser, timing

this_dir = os.path.dirname(os.path.realpath(__file__))

def pad(day):
    return day if len(day) > 1 else "0" + day

def get_file(day, inp):
    for name in (inp, f'{inp}.txt'):
        try:
            with open(f'{this_dir}/../inputs/{day}/{name}') as f:
                file = f.read()
            return file
        except:
            pass
    return None

def parse_opts():
    opts = {"mode": "basic", "input": "input", "day": "latest"}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-i":
            opts["mode"] = "interactive"
        elif sys.argv[i] == "-t":
            opts["input"] = sys.argv[i+1]
            i += 1
        else:
            opts["day"] = sys.argv[i]
        i += 1
    return opts

def get_solved_days():
    modules = (name for _, name, pkg in pkgutil.iter_modules(solutions.__path__) if not pkg)
    days = []
    for module in modules:
        m = re.fullmatch(r'day(\d\d)', module)
        if m:
            days.append(m.group(1))
    return sorted(days)


def get_days(opts):
    day = opts["day"]
    if opts["mode"] == "interactive":
        print('Select day: ', end='')
        return [input()]
    if day == "latest":
        return get_solved_days()[-1:]
    elif day == "all":
        return get_solved_days()
    else:
        return [day]

def input_args(runner, file, timer):
    args = inspect.getfullargspec(runner).args
    filled_args = {}
    for arg in args:
        if arg == 'timer':
            filled_args[arg] = timer
        else:
            filled_args[arg] = parser.parse(file, arg)
    return filled_args
    return {arg: parser.parse(file, arg) for arg in args}
    

def dispatch(day, kind):
    day = pad(day)
    file = get_file(day, kind)
    module = importlib.import_module(f"solutions.day{day}")
    print(f'==== Day {day} ====')
    if file:
        timer = timing.Timer()
        args = input_args(module.run, file, timer)
        timer.tick()
        module.run(**args)
        timer.tick()
        print('Finished in', timer)
    else:
        print('Input not available for day', day)

def main():
    opts = parse_opts()
    days = get_days(opts)
    for i in range(len(days)):
        dispatch(days[i], opts["input"])
        if i < len(days) - 1:
            print()

if __name__ == "__main__":
    main()
    
