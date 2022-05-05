from asyncio.windows_events import NULL
from distutils.log import error
from math import sin, cos, tan, pi

plus_token = {
    'type'      : 'operator',
    'value'    : '+',
    'assoc'     : 'left',
    'precedence' : 1,
    'operands'  : 2,
    'func'      : lambda a : a[1] + a[0]
}

minus_token = {
    'type'      : 'operator',
    'value'    : '-',
    'assoc'     : 'left',
    'precedence' : 1,
    'operands'  : 2,
    'func'      : lambda a : a[1] - a[0]
}

multiply_token = {
    'type'      : 'operator',
    'value'    : '*',
    'assoc'     : 'left',
    'precedence' : 2,
    'operands'  : 2,
    'func'      : lambda a : a[1] * a[0]
}
divide_token = {
    'type'      : 'operator',
    'value'    : '/',
    'assoc'     : 'left',
    'precedence' : 2,
    'operands'  : 2,
    'func'      : lambda a : a[1] / a[0]
}
openbrace_token = {
    'type'      : 'operator',
    'value'    : '(',
    'assoc'     : 'none',
    'precedence' : -1,
    'operands'  : 2,
    'func'      : NULL
}
closebrace_token = {
    'type'      : 'operator',
    'value'    : ')',
    'assoc'     : 'none',
    'precedence' : -1,
    'operands'  : 2,
    'func'      : NULL
}
pow_token = {
    'type'      : 'operator',
    'value'    : '^',
    'assoc'     : 'right',
    'precedence' : 3,
    'operands'  : 2,
    'func'      : lambda a : a[1] ** a[0]
}
sin_token = {
    'type'      : 'function',
    'value'    : 'sin',
    'assoc'     : 'right',
    'precedence' : 4,
    'operands'  : 1,
    'func'      : lambda a : sin(a[0])
}
cos_token = {
    'type'      : 'function',
    'value'    : 'cos',
    'assoc'     : 'right',
    'precedence' : 4,
    'operands'  : 1,
    'func'      : lambda a : cos(a[0])
}
tan_token = {
    'type'      : 'function',
    'value'    : 'tan',
    'assoc'     : 'right',
    'precedence' : 4,
    'operands'  : 1,
    'func'      : lambda a : tan(a[0])
}
pi_token = {
    'type'      : 'function',
    'value'    : 'pi',
    'assoc'     : 'right',
    'precedence' : 4,
    'operands'  : 0,
    'func'      : lambda a : pi
}
round_token = {
    'type'      : 'function',
    'value'    : 'round',
    'assoc'     : 'right',
    'precedence' : 4,
    'operands'  : 1,
    'func'      : lambda a : round(a[0])
}

def cnmt(a):
    return {
        'type'      : 'number',
        'value'     : a
    }

queue = []
opstack = []

def process(token):
    if token['type'] == 'number':
        queue.append(token)
    elif token['type'] == 'function':
        opstack.append(token)
    elif token['type'] == 'operator':
        if token == openbrace_token :
            opstack.append(token)
        elif token == closebrace_token :
            while ((len(opstack) > 0) and (opstack[-1] != openbrace_token)) :
                queue.append(opstack.pop())
            opstack.pop()
            if(len(opstack) > 0):
                if(opstack[-1]['type'] == 'function'):
                    queue.append(opstack.pop())

        else:
            while(((len(opstack) > 0) and (token['precedence'] <= opstack[-1]['precedence'])) and (token['assoc'] == 'left')):
                queue.append(opstack.pop())
            opstack.append(token)
    
    # print('queue: ', end='')
    # for i in range(len(queue)):
    #     print(queue[i]['value'], end=' ')
    # print('\nstack: ', end='')
    # for i in range(len(opstack)):
    #     print(opstack[i]['value'], end=' ')
    # print()

def post_process():
    while len(opstack) > 0:
        if opstack[-1] == openbrace_token:
            error('received \'(\' at post-processing')
        else : queue.append(opstack.pop())

symbols = '+-*/()^'
symbols_token = [
    plus_token,
    minus_token,
    multiply_token,
    divide_token,
    openbrace_token,
    closebrace_token,
    pow_token
]
funcs = [
    'sin',
    'cos',
    'tan',
    'pi',
    'round'
]
funcs_token = [
    sin_token,
    cos_token,
    tan_token,
    pi_token,
    round_token
]

a = str(input())

while(len(a)):
    if a[0] in symbols:
        process(symbols_token[symbols.index(a[0])])
        a = a[1:]
        continue
    elif a[0] in '1234567890':
        cnt = 0
        for i in a:
            if i not in '1234567890.': 
                break
            cnt += 1
        num = a[0:cnt]
        process(cnmt(float(num)))
        a = a[cnt:]
        continue
    elif a[0] in "qwertyuiopasdfghjklzxcvbnm":
        for i in range(len(funcs)):
            if(a.find(funcs[i]) == 0):
                process(funcs_token[i])
                a = a[len(funcs[i]):]
                continue
    else:
        a = a[1:]

post_process()
print('queue after process: ', end='')
for i in range(len(queue)):
    print(queue[i]['value'], end=' ')
print()


for i in range(len(queue)):
    if(queue[i]['type'] == 'operator') or (queue[i]['type'] == 'function'):
        operands = []
        for j in range(queue[i]['operands']):
            for k in range(i, -1, -1):
                if queue[k]['type'] == 'number':
                    operands.append(k)
                    queue[k]['type'] = 'used'
                    break
        operandsval = []
        for j in range(len(operands)):
            operandsval.append(queue[operands[j]]['value'])
        queue[i] = cnmt(queue[i]['func'](operandsval))
        print('queue: ', end='')
        for i in range(len(queue)):
            if queue[i]['type'] == 'used': continue
            print(queue[i]['value'], end=' ')
        print()