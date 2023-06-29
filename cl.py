# this simple script generates msvc styled compiler options with use of unix cc style compiler options
# it's directly prints the output, without any executions; but you can pass the output to the cl.exe.
#
# an example:
#  * '-std=c++20 example.cpp -o example.exe' as args, generates: '/nologo /EHsc /std:c++20 /Zc:__cplusplus /Tpexample.cpp /Feexample.exe'
#
# MIT License
#
# Copyright (c) 2023 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
#

from sys import argv

cl_args = ['/nologo', '/EHsc']
cl_link_args = ['/link']
index = 0

for arg in argv:
    if arg[0] == '-':
        match arg:
            case '-ansi':
                cl_args.append('/Za')
            case '-c':
                cl_args.append('/c')
            case '-O0':
                cl_args.append('/Ot')
            case '-O2':
                cl_args.append('/O2')
            case '-mavx':
                cl_args.append('/arch:AVX')
            case '-mavx2':
                cl_args.append('/arch:AVX2')
            case '-mavx512f' \
                 | '-mavx512pf' \
                 | '-mavx512er' \
                 | '-mavx512cd' \
                 | '-mavx512vl' \
                 | '-mavx512bw' \
                 | '-mavx512dq' \
                 | '-mavx512ifma' \
                 | '-mavx512vbmi':
                cl_args.append('/arch:AVX512')
            case '-msse2':
                cl_args.append('/arch:SSE2')
            case '-msse':
                cl_args.append('/arch:SSE')
            case '-m32':
                cl_args.append('/arch:IA32')
            case '-C':
                cl_args.append('/C')
            case '-E':
                cl_args.append('/EP')
            case '-L':
                if index + 1 < len(argv):
                    next_arg = argv[index + 1]
                    index += 1
                    cl_link_args.append(f'/LIBPATH:{next_arg}')
                    continue
            case '-o':
                if index + 1 < len(argv):
                    next_arg = argv[index + 1]
                    index += 1
                    if '.o' in next_arg or '.obj' in next_arg:
                        cl_args.append(f'/Fo{next_arg}')
                    else:
                        cl_args.append(f'/Fe{next_arg}')
                    continue
            case '-isystem':
                if index + 1 < len(argv):
                    next_arg = argv[index + 1]
                    index += 1
                    cl_args.append(f'/I{next_arg}')
                    continue
            case '-I':
                if index + 1 < len(argv):
                    next_arg = argv[index + 1]
                    index += 1
                    cl_args.append(f'/I{next_arg}')
                    continue
            case '-fexcess-precision=fast':
                cl_args.append('/fp:fast')
            case '-fexcess-precision=standard':
                cl_args.append('/fp:strict')
            case '-fsanitize=address':
                cl_args.append('/fsanitize=address')
            case '-fsanitize-coverage=trace-cmp':
                cl_args.append('/fsanitize-coverage=trace-cmp')
            case '-fstack-check':
                cl_args.append('/Ge')
            case '-fexceptions':
                cl_args.append('/GX')
            case '-funsigned-char':
                cl_args.append('/J')
            case '-Wunknown-warning':
                cl_args.append('/options:strict')
            case '-nostdinc' \
                 | '-nostdinc++':
                cl_args.append('/X')
            case _:
                if len(arg) > 2:
                    if arg[:2] == '-l':
                        cl_args.append(f'{arg[2:]}.lib')
                    elif arg[:2] == '-I':
                        # don't forget to replace slash
                        # with backslash (or vice versa) for specifying paths
                        cl_args.append(f'/I{arg[2:]}')
                    elif len(arg) > 5 and arg[:5] == '-std=':
                        cl_args.append(f'/std:{arg[5:]}')

                        if '-std=c++' in arg:
                            cl_args.append('/Zc:__cplusplus')
                    elif arg[:2] == '-D':
                        cl_args.append(f'/D{arg[2:]}')
                    elif arg[:2] == '-L':
                        cl_link_args.append(f'/LIBPATH:{arg[2:]}')
    elif arg[0] == '/':
        cl_args.append(arg)
    elif len(arg) > 3 and (arg[-3:] == '.cc' or
                           (len(arg) > 4 and arg[-4:] == '.cpp') or
                           (len(arg) > 4 and arg[-4:] == '.cxx')):
        cl_args.append(f'/Tp{arg}')

    index += 1

if not len(cl_link_args) == 1:
    for x in cl_link_args:
        cl_args.append(x)

for x in cl_args:
    print(x, end=' ')
