# Fix weird VMF files that hammer doesn't want to open
# Only works on a file like what was posted on https://tf2maps.net/threads/converting-old-maps-to-modern-hammer.35474/#post-435924
# Made by Coding Etham

import os

def print_index_array(arr):
    for n, i in enumerate(arr):
        print(n, i)

side = 'side\n{{\n"id" "{}"\n"plane" "({} {} {}) ({} {} {}) ({} {} {})"\n"material" "{}"\n"uaxis" "[{} {} {} {}] {}"\n"vaxis" "[{} {} {} {}] {}"\n"rotation" "0"\n"lightmapscale" "16"\n"smoothing_groups" "{}"\n}}'

def format_side(old):
    u = old.split(' ')
    new = side.format(0, u[1], u[2], u[3], u[6], u[7], u[8], u[11], u[12], u[13], u[15], u[17], u[18], u[19], u[20], u[29], u[23], u[24], u[25], u[26], u[30], u[28])
    return new.split('\n')

def calculate_indents(il, arr):
    for n in range(len(arr)):
        il -= arr[n].count('}')
        if il < 0:il = 0
        arr[n] = '\t'*il + arr[n]
        il += arr[n].count('{')
    return il, arr

def what_am_i(line, prev, count):
    new = 'idk'
    if 'classname' in line:
        if 'worldspawn' in line:
            new = 'world'
        else:
            new = 'entity'
    elif '[' in line:
        new = 'side'
    
    if (prev == 'world' or prev == 'entity') and line != '{':
        new = prev
    
    if line == '}' and prev == 'entity':
        new = 'idk'
    
    if prev == new:
        count += 1
    else:
        count = 0
    
    return new, count

def update_vmf(arr):
    out = []
    i_am_a = 'idk'
    i_am_c = 0
    logtype = ['idk', 'idk', 'idk']
    for i in arr:
        i_am_a, i_am_c = what_am_i(i, i_am_a, i_am_c)
        if i_am_c == 0:
            if i_am_a == 'idk':
                if not 'mapversion' in out[-1]:
                    out.append('}')
                if logtype[-4] == 'entity' and logtype[-2] == 'side':
                    out.append('}')
            elif i_am_a == 'entity':
                if logtype[-2] == 'side':
                    out += ['}']
                out += ['entity', '{', i]
            elif i_am_a == 'world':
                out += ['world', '{', i]
            elif i_am_a == 'side':
                if logtype[-2] == 'entity':
                    out.pop(-1)
                out += ['solid', '{']
            logtype.append(i_am_a)
        elif i_am_a == 'world':
            out.append(i)
        elif i_am_a == 'entity':
            out.append(i)
        if i_am_a == 'side':
            out += format_side(i)
        #out.append(i_am_a + ' ' + str(i_am_c))
    return out
    

print('Outdated VMF Fixer, only works on maps with lines like', '\n( -256 128 -48 ) ( 192 128 -48 ) ( 192 -256 -48 ) DEV/REFLECTIVITY_50B...', '\nEnter filename.vmf e.g. ctf_2fort.vmf')
i = 'please_enter_vmf_filename.vmf'
while not os.path.isfile(i):
    i = input('Map Name: ')

print('Ok! Found map file.')
filein = open(i, 'r').read().split('\n')
print('Read map file.')
uv = update_vmf(filein)
print('Saving updated vmf to recovered_map.vmf')
with open('recovered_map.vmf', 'w') as f:
    il, ci = calculate_indents(0, uv)
    f.write('\n'.join(ci))
input('Done')
