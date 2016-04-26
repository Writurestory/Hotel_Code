import os

def send_to_print(txt):
    printer = os.popen('POS-58', 'w')
    for t in txt:
        printer.write('%s\n' %t)
    printer.close()

if __name__ == '__main__':
    send_to_print(['sssssss','bbbbbb'])
