from colorama import init, Fore, Style

# source: Scripts IIC2233

init()

colors = {'normal': (Fore.RESET,),
          'alert': (Fore.YELLOW,),
          'result': (Fore.GREEN,),
          'info': (Fore.CYAN,),
          'danger': (Fore.RED,),
          'progress':(Fore.MAGENTA,),
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

def print_invalid_file(_file: str) -> None:
    _msg = f'Invalid file {_file}\nPlease check file and try again'
    cool_print_decoration(_msg, 'danger')

# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):

    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    cool_print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r', style='progress')

    print('\n') if iteration == total else None