from colorama import init, Fore, Style

# source: Scripts IIC2233

init()

colors = {'normal': (Fore.RESET,),
          'alert': (Fore.YELLOW,),
          'result': (Fore.GREEN,),
          'info': (Fore.CYAN,),
}

def cool_print_decoration(message, style, separator='-'):
    cool_print('\n' + separator * 4 + '\n')
    cool_print(message, style = style)
    cool_print('\n' + separator * 4)

def cool_print(*args, style='normal', **kwargs):
    print(*colors[style], end="")

    print(*args, **kwargs)

    print(*colors['normal'], end="")

    if style == 'alert':
        with open('alerts.log', 'a') as f:
            f.write(repr(args))
            f.write("\n")
