import sh

def interface_ip(interface, addr_type='inet'):
    """
    Return the first IP address of the interface that is of the specified type

    By default the type is set to inet (ipv4). If you want the v6 address then
    specify 'inet6' for the type.
    """
    # get the ip addr show output for our interface and split it into pieces
    output = sh.ip.addr("show", interface)
    pieces = output.split()

    # find the index of our type
    inet_idx = pieces.index(addr_type)

    # return the first part of the next piece, split by '/'
    return pieces[inet_idx + 1].split('/')[0]
